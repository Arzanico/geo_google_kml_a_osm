FS= require('fs');

kml= FS.readFileSync('cruces.kml','utf-8');
/* el formato es
  <Folder>
      <name>Linea Belgrano norte</name>
      <Placemark>
        <name>Av de Mayo</name>
        <description><![CDATA[L�nea: Belgrano Norte<br>Ramal: Retiro - Villa Rosa<br>Servicio: Cargas y pasajeros<br>Nom. Alt.: PARANA AV./El Indio<br>Obs.: -<br>Actualidad: Paso bajo nivel<br>2019: Paso bajo nivel<br>2023: Paso bajo nivel<br>Tipo Obra: No hay obra proyectada<br>Estado: -<br>Progresiva: -<br>Año estimado de Obra: -<br>Última actualización: enero 2017]]></description>
        <styleUrl>#icon-1784-0F9D58</styleUrl>
        <ExtendedData>
          <Data name="L�nea">
            <value>Belgrano Norte</value>
          </Data>
          <Data name="Ramal">
            <value>Retiro - Villa Rosa</value>
          </Data>
          <Data name="Servicio">
            <value>Cargas y pasajeros</value>
          </Data>
					...
          <coordinates>
            -58.8668,-34.418883,0
*/   

lines= kml.split(/\r?\n/);

var Col2Idx= [];
function out(d) {
	Object.keys(d).forEach(k => { if (Col2Idx.indexOf(k)<0) Col2Idx.push(k); });
	var s= Col2Idx.map(k => d[k]).join("\t");
	console.log(s);
}
function outColNames() {
	var s= Col2Idx.join("\t");
	console.log('#'+s);
}

var t0; var t1; var elProximoSonCoords= false;
var d= {};
folderName= null;
lines.forEach( l => {
	if (l.match(/<Folder/)) {
		folderName= null;
	}
	else if (folderName==null && ( t0= l.match(/<name>([^<]*)/))) {
		folderName= t0[1];
	}	
	else if (folderName != null) {
		if (! d._tengoExtendedData ) {
			if (l.match(/<Placemark/)) { d= {folder: folderName}; }
			else if ( l.match(/<ExtendedData/) ) { d._tengoExtendedData= true; }
			else {
				if ( (t0= l.match(/<([^>]*)>([^<]*)/))) {
					d[t0[1]]= t0[2];
				}
			}
		}
		else {
			if (l.match(/<\/Placemark/)) { out(d); d= {}; }
			else if (l.match(/<coordinates/)) { elProximoSonCoords= true; }
			else if (elProximoSonCoords) {elProximoSonCoords= false;  
				var p= l.trim().split(/,/); 
				d.lat= p[0]; d.lng= p[1]; d.elevation= p[2];
			}
			if ( (t0= l.match(/<Data name="([^"]+)/)) ) { t1= t0[1]; }
			else if ( (t0= l.match(/<value>([^<]+)/))) { d[t1]= t0[1]; }
		}
	}
});

outColNames();
