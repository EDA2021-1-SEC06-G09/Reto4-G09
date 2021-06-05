"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import graph as gr
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def initCatalog():
    catalog = {'countries': None,
               'landing_points': None,
               'connections': None,
               'LP-Name':None}

    catalog['countries'] = mp.newMap(numelements=239,
                                     maptype='PROBING',
                                     comparefunction=compareCountries)

    catalog['landing_points'] = mp.newMap(numelements=1280,
                                          maptype='PROBING',
                                          comparefunction=compareLandingPointIds)

    catalog['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                         directed=True,
                                         size=3263)

    catalog['LP-Name'] = mp.newMap(numelements=1280, maptype='PROBING')

    return catalog


# Funciones para agregar informacion al catalogo
def addCountry(catalog, country):
    countryvalue = newCountry(country)
    mp.put(catalog['countries'], country['CountryName'], countryvalue)


def addLandingPoint(catalog, landingpoint):
    LPCity = landingpoint['name'].split(", ")[0]
    LPCountry = landingpoint['name'].split(', ')[-1]
    LPvalue = newLP(landingpoint)

    mp.put(catalog['landing_points'], LPCity, LPvalue)
    country = me.getValue(mp.get(catalog['countries'], LPCountry))
    lt.addLast(country['landing_points'], landingpoint)

    tuplaPaisCity = (LPCountry, LPCity)
    mp.put(catalog['LP-Name'], landingpoint['landing_point_id'], tuplaPaisCity)

    


def addConnection(catalog, connection):
    ciudad = me.getValue(mp.get(catalog['LP-Name'], connection['origin']))[1]
    ciudadDestino = me.getValue(mp.get(catalog['LP-Name'], connection['destination']))[1]
    pais = me.getValue(mp.get(catalog['LP-Name'], connection['origin']))[0]
    origin = formatVertex(ciudad, connection['cable_name'])
    destination = formatVertex(ciudadDestino, connection['cable_name'])
    
    valorCiudad = me.getValue(mp.get(catalog['landing_points'], ciudad))
    listaCables = valorCiudad['cables']
    lt.addLast(listaCables, connection)

    infoPais = me.getValue(mp.get(catalog['countries'], pais))['info']
    LPcapital = mp.get(catalog['landing_points'], infoPais['CapitalName'])
    if LPcapital is None:
        LPvalue = newCapitalLP(infoPais['CapitalName'])
        mp.put(catalog['landing_points'], infoPais['CapitalName'], LPvalue)

    
    


    weightstr = connection['cable_length']
    try:
        weight = float(weightstr.split()[0].replace(",", ""))
    except:
        weight = weightstr
    addVertex(catalog, origin)
    addVertex(catalog, destination)
    addEdge(catalog, origin, destination, weight)
    if not isCapital(catalog, connection['origin']):
        capitalFormat = formatVertex(infoPais['CapitalName'], connection['cable_name'])
        addVertex(catalog, capitalFormat)
        addEdge(catalog, capitalFormat, origin, weight=0.1)



    


def addVertex(catalog, vertexname):
    if not gr.containsVertex(catalog['connections'], vertexname):
        gr.insertVertex(catalog['connections'], vertexname)


def addEdge(catalog, origin, destination, weight):
    edge = gr.getEdge(catalog['connections'], origin, destination)
    if edge is None:
        gr.addEdge(catalog['connections'], origin, destination, weight)


def formatVertex(point, cable):
    return point + "-" + cable

# Funciones para creacion de datos
def newCountry(country):
    countryvalue = {'info': country,
                    'landing_points': lt.newList(datastructure='ARRAY_LIST')}
    return countryvalue

def newLP(LP):
    LPvalue = {'info': LP, 'cables': lt.newList(datastructure="ARRAY_LIST")}
    return LPvalue

def newCapitalLP(Capital):
    LPvalue = {'info': None, 'cables': lt.newList(datastructure="ARRAY_LIST")}
    return LPvalue

# Funciones de consulta

def getClusters(catalog, LP1, LP2):
    clust = 0


def isCapital(catalog, idciudad):
    get = mp.get(catalog['LP-Name'], idciudad)
    if get is None:
        return True
    else:
        pais = me.getValue(get)[0]
        info = me.getValue(mp.get(catalog['countries'], pais))
        if me.getValue(get)[1] == info['info']['CapitalName']:
            return True
        else:
            return False
        


# Funciones de comparacion
def compareCountries(country1, keyvaluecountry):
    country2 = keyvaluecountry['key']
    if country1 == country2:
        return 0
    elif country1 > country2:
        return 1
    else:
        return -1

def compareLandingPointIds(id1, keyvaluepoint):
    id2 = keyvaluepoint['key']
    if id1 == id2:
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1

# Funciones de ordenamiento
