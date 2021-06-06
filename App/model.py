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


from DISClib.DataStructures.edge import weight
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import graph as gr
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Graphs import scc
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def initCatalog():
    catalog = {'countries': None,
               'landing_points': None,
               'cables': None,
               'connections': None}

    catalog['countries'] = mp.newMap(numelements=239,
                                     maptype='PROBING',
                                     comparefunction=compareCountries)

    catalog['landing_points'] = mp.newMap(numelements=1280,
                                          maptype='PROBING',
                                          comparefunction=compareLandingPointIds)

    catalog['cables'] = mp.newMap(numelements=2000,
                                  maptype='PROBING',
                                  comparefunction=compareCountries)

    catalog['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                         directed=False,
                                         size=3263)
    return catalog


# Funciones para agregar informacion al catalogo
def addCountry(catalog, country):
    countryvalue = newCountry(country)
    mp.put(catalog['countries'], country['CountryName'], countryvalue)
    addVertex(catalog, country['CapitalName'], False)


def addLandingPoint(catalog, landingpoint):
    mp.put(catalog['landing_points'], landingpoint['landing_point_id'], landingpoint)
    country = me.getValue(mp.get(catalog['countries'], landingpoint['name'].split(', ')[-1]))
    lt.addLast(country['landing_points'], landingpoint)


def addCable(catalog, connection):
    if not mp.contains(catalog['cables'], connection['cable_id']):
        filteredcable = dict(filter(lambda elem: elem[0] != 'origin' and elem[0]!= 'destination', connection.items()))
        mp.put(catalog['cables'], connection['cable_id'], filteredcable)
        filteredcable.clear()


def addConnection(catalog, connection):
    origin = formatVertex(connection['origin'], connection['cable_id'])
    destination = formatVertex(connection['destination'], connection['cable_id'])
    weight = connection['cable_length']
    addVertex(catalog, origin, True)
    addVertex(catalog, destination, True)
    addEdge(catalog, origin, destination, weight)


def addCapitalEdges(catalog):
    pass


def addVertex(catalog, vertexname, notcapital):
    if not gr.containsVertex(catalog['connections'], vertexname):
        preexistingvertices = gr.vertices(catalog['connections'])
        gr.insertVertex(catalog['connections'], vertexname)
        if notcapital:
            for vertex in lt.iterator(preexistingvertices):
                if vertexname.split('*')[0] == vertex.split('*')[0]:
                    addEdge(catalog, vertexname, vertex, 0.1)
        preexistingvertices.clear()


def addEdge(catalog, origin, destination, weight):
    edge = gr.getEdge(catalog['connections'], origin, destination)
    if edge is None:
        gr.addEdge(catalog['connections'], origin, destination, weight)


# Funciones para creacion de datos
def newCountry(country):
    countryvalue = {'country_info': country,
                    'landing_points': lt.newList('ARRAY_LIST')}
    return countryvalue


def formatVertex(point, cable):
    return point + "*" + cable


# Funciones de consulta
def getClusters(catalog):
    clusters = scc.connectedComponents(scc.KosarajuSCC(catalog['connections']))


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
