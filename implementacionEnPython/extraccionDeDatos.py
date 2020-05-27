import xml.etree.ElementTree as ET
import sqlite3 as sql
from .funciones import funciones, crud


# Apertura y lectura del archivo KML importado de Google Maps
with open("data/cruces.kml", "r") as kFile:
    xmlR = ET.fromstring(kFile.read())
    kFile.close()

# Este es el prefijo del xlmns '{http://www.opengis.net/kml/2.2}'
prf = {'prefix': 'http://www.opengis.net/kml/2.2'}


# cooking kml ---->
folders = xmlR.findall('prefix:Document/prefix:Folder', prf)

# Diccionario de tablas y datos para mapear
# Esto viene de aca <ExtendedData><Data name="Línea"> <value>Belgrano Norte</value></ExtendedData>
# Datos en el tag Data me va a decir en que tabla inserto el valor
tables = ["Linea", "Ramal", "Servicio", "Actualidad", "TipoObra"]
tablesIdsDict = {
    "line_id": "Linea",
    "ramal_id": "Ramal",
    "servicio_id": "Servicio",
    "actualidad_id": "Actualidad",
    "obra_id": "TipoObra"
}

# Creacion y conexion a la base de datos
createDB = True
dropOldDB = False
if createDB:
    crud.createDb()
dbName = f'dbs/data.sqlite'
conn = sql.connect(dbName)
cur = conn.cursor()

count = 0
allData = list()
for f in folders:
    data = dict()
    folderName = f.find('prefix:name', prf).text.strip()
    # print(f'******** Folder Name {folderName}') # <---- BLOCK FOR DEBUGGING ---->
    cur.execute('INSERT OR IGNORE INTO Folder (name) VALUES (?)', (folderName,))
    cur.execute('SELECT id FROM Folder WHERE name = ?', (folderName,))
    folder_id = cur.fetchone()[0]  # Db atribute
    placeList = f.findall('prefix:Placemark', prf)
    for p in placeList:
        count += 1
        if p.find('prefix:name', prf).text:
            placeName = p.find('prefix:name', prf).text.strip()
        else:
            placeName = None
        # print(f'******** Place Name {placeName}') # <---- BLOCK FOR DEBUGGING ---->
        placeDescription = p.find('prefix:description', prf).text.strip()
        extendedData = p.find('prefix:ExtendedData', prf)
        exD = dict()
        exDTablesAtrId = dict()
        if len(extendedData):
            for d in extendedData:
                atributo = d.attrib["name"]
                valor = d[0].text
                # <---- BLOCK FOR DEBUGGING ---->                                
                # print('<---- BLOCK FOR DEBUGGING ---->')
                # print('<---- END BLOCK FOR DEBUGGING ---->')
                # <---- BLOCK FOR DEBUGGING ---->
                if funciones.transform(atributo, True) in tables:
                    atributo = funciones.transform(atributo, True)
                    # print(f'Atributo de tabla {atributo}') # <---- BLOCK FOR DEBUGGING ---->
                    cur.execute(f'INSERT OR IGNORE INTO {atributo} (name) VALUES (?)', (valor,))
                    cur.execute(f'SELECT id FROM {atributo} WHERE name = ?', (valor,))
                    atId = cur.fetchone()[0]
                    exDTablesAtrId.update({atributo: atId})
                    continue
                atributo = funciones.transform(atributo)
                # print(f'Atributo de campo {atributo}') # <---- BLOCK FOR DEBUGGING ---->
                exD.update({atributo: valor})
        lon, lat, z = p.find("prefix:Point", prf)[0].text.strip().split(",")
        cur.execute('''
            INSERT OR IGNORE INTO kmlData ( 
                folder_id, 
                placeName, 
                placeDescription,
                lon,
                lat, 
                line_id, 
                ramal_id,
                servicio_id ,
                actualidad_id,
                nomalt,
                obs,
                prev2019,
                prev2023,
                obra_id,
                estado,
                progresiva,
                anoEstimadoDeObra,
                ultimaActualizacion
            )
            VALUES (?, ?, ?, ? ,? ,? ,? ,? ,?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ''',
                    (
                        folder_id,
                        placeName,
                        placeDescription,
                        lon,
                        lat,
                        exDTablesAtrId[tablesIdsDict["line_id"]],
                        exDTablesAtrId[tablesIdsDict["ramal_id"]],
                        exDTablesAtrId[tablesIdsDict["servicio_id"]],
                        exDTablesAtrId[tablesIdsDict["actualidad_id"]],
                        exD.get("nomAlt", None),
                        exD.get("obs", None),
                        exD.get("prev2019", None),
                        exD.get("prev2023", None),
                        exDTablesAtrId.get(tablesIdsDict["obra_id"], None),
                        exD.get("estado", None),
                        exD.get("progresiva", None),
                        exD.get("anoEstimadoDeObra", None),
                        exD.get("ultimaActualizacion", None)
                    )
                    )
        conn.commit()

registros = cur.execute('SELECT COUNT(id) FROM kmlData').fetchone()[0]
print(f'{count} etiquetas de "placeMark fueron encontradas y contadas.')
print(f'{registros} fueron insertados en la base de datos')

