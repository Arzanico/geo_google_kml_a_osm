# La funcion tiene como objetivo limpiar algunas cuestiones del texto.
# Tambien genera el formato de tipeo a tipo "Camello"
# Si hubiese una convencion para los nombre, de tablas, variables, etc. Aqui se puede incluir el formato
# Otro tema importante es el enconding del texto, aqui para generalizar esta en utf-8 pero sin acentos y si la virgulilla de la ñ

def upFLetter(word):
    """
    :param word: input type string
    :return: output type string
    """
    wL = [x for x in word]
    wL[0] = wL[0].upper()
    word = ''.join([l for l in wL])
    return word

def camelTiping(word):
    """
    :param word: input type string
    :return: output type string
    """
    word = word.strip()
    if len(word.split()):
        compWord = word.split()
        newCompWord = [compWord[0]]
        for w in compWord[1:]:
            w = w.capitalize()
            newCompWord.append(w)
        word = ''.join([x for x in newCompWord])
    else:
        return word
    return word


def transform(word=None, uFL=None, isCamel=None):
    """
    :param word: input del texto que se desea tranformar
    :param uFL: booleno que indica si el string de salida (output), lleva la primer letra en mayuscula
    :param isCamel: booleno que indica si el string de salida (output), sigue el patron de tipeo camello
    :return: la funcion retorna un string
    """
    word = word.strip()
    word = word.replace('.', '')
    intab = "áéíóúñÁÉÍÓÚÑ"
    outtab = "aeiounAEIOUN"
    trantab = str.maketrans(intab, outtab)
    word = word.translate(trantab)
    if isCamel:
        word = camelTiping(word)
    elif uFL:
        word = upFLetter(word)
    return word


def reverseDict(d=None, retRep=False):
    """
    :param d: input type dict()
    :param retRep: input type Bool : este parametro indica si se quieren guardar
    los valores repetidos del dic transformado
    :return: la funcion devuelve un diccionario y una lista de tuplas en caso que retRep = True
    """
    if not d:
        return False
    elif type(d) != dict:
        return False
    revDic = dict()
    if retRep:
        retRep = list()
        for i in d.items():
            if i[1] in revDic:
                retRep.append(i)
                continue
            revDic.update({i[1]:i[0]})
        return ((revDic, retRep))
    else:
        for i in d.items():
            revDic.update({i[1]:i[0]})
        return revDic


