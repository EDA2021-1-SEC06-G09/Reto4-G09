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
from DISClib.Algorithms.Graphs import dijsktra
from DISClib.Algorithms.Graphs import prim
assert cf



# Construccion de modelos
def initCatalog():
    '''Countries: Mapa de hash que tiene como key el nombre de un pais y valor un diccionario con:
     ['info']-> informacion del csv del pais
     ['landing_points']-> landing points en el pais

     landing_points: mapa de hash que tiene como key el nombre de la ciudad y valor:
     ['info']-> informacion del csv del LP
     ['cables']-> cables en el LP

     Connections: grafo en el formato:
     vertice: (nombre ciudad)-(nombre cable)
     arco: distancia entre 2 ciudades

     LP-Name: mapa usado para conseguir nombre de ciudad y pais que corresponden a un ID numerico de un LP
     llave-> id del landing point
     valor-> tupla (pais, ciudad)
    '''
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

    catalog['cables'] = mp.newMap(numelements=2000,
                                  maptype='PROBING',
                                  comparefunction=compareCountries)

    catalog['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                         directed=False,
                                         size=3263)

    catalog['LP-Name'] = mp.newMap(numelements=1280, maptype='PROBING')

    return catalog


# Funciones para agregar informacion al catalogo
def addCountry(catalog, country):
    countryvalue = newCountry(country)
    mp.put(catalog['countries'], country['CountryName'], countryvalue)
    addVertex(catalog, country['CapitalName'], False)


def addLandingPoint(catalog, landingpoint):
    LPCity = landingpoint['name'].split(", ")[0]
    LPCountry = landingpoint['name'].split(', ')[-1]
    LPvalue = newLP(landingpoint)

    mp.put(catalog['landing_points'], LPCity, LPvalue)
    country = me.getValue(mp.get(catalog['countries'], LPCountry))
    lt.addLast(country['landing_points'], landingpoint)

    tuplaPaisCity = (LPCountry, LPCity)
    mp.put(catalog['LP-Name'], landingpoint['landing_point_id'], tuplaPaisCity)
    



def addCable(catalog, connection):
    if not mp.contains(catalog['cables'], connection['cable_id']):
        filteredcable = dict(filter(lambda elem: elem[0] != 'origin' and elem[0]!= 'destination', connection.items()))
        mp.put(catalog['cables'], connection['cable_id'], filteredcable)
        filteredcable.clear()


def addConnection(catalog, connection):
    #añade las conexiones del csv y ademas hace la conexion entre el landing point y su ciudad capital
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
        LPvalue = newCapitalLP(infoPais['CapitalName'], pais)
        mp.put(catalog['landing_points'], infoPais['CapitalName'], LPvalue)
    
    LPcapital = me.getValue(mp.get(catalog['landing_points'], infoPais['CapitalName']))

    #Hasta aca solo se han creado variables y anadido las capitales al mapa landing points
    

    weightstr = connection['cable_length']
    try:
        weight = int(weightstr.split()[0].replace(",", ""))
        if origin == 'Cancún-Caribbean Express (CX)':
            print(weight)
    except:
        weight = 9999999
        #para lidiar con distancias n.a.

    addVertex(catalog, origin)
    addVertex(catalog, destination)
    addEdge(catalog, origin, destination, weight)
    if not isCapital(catalog, connection['origin']):
        capitalFormat = formatVertex(infoPais['CapitalName'], connection['cable_name'])
        addVertex(catalog, capitalFormat)
        addEdge(catalog, capitalFormat, origin, weight=0.1)
        #anade comunicacion entre LP costero y capital
        if (len(LPcapital['info']) == 1):
            #if not lt.isPresent(LPcapital['cables'], connection):
            lt.addLast(LPcapital['cables'], connection)
            #anade el cable a la lista de cables de la capital
 
    

    
def sameLPcables(catalog):
    #conecta los cables que pertenecen a un mismo landing point entre ellos
    setvalores = mp.valueSet(catalog['landing_points'])
    setLlaves = mp.keySet(catalog['landing_points'])
    for valor in lt.iterator(setvalores):
        i=1
        while i <= lt.size(valor['cables']):
            cable1 = lt.getElement(valor['cables'], i)
            i+=1

        for cable2 in lt.iterator(valor['cables']):
            LP_cable2 = formatVertex(valor['info']['name'].split(", ")[0], cable2['cable_name'])
            LP_cable1 = formatVertex(valor['info']['name'].split(", ")[0], cable1['cable_name'])
            try:
                addEdge(catalog,LP_cable1 , LP_cable2, weight=0.1)
            except:
                pass



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


def newCapitalLP(Capital, pais):
    #klk
    string = Capital + ', ' + pais
    info = {'name': string}
    LPvalue = {'info': info, 'cables': lt.newList(datastructure="ARRAY_LIST")}
    return LPvalue


# Funciones de consulta
def getClusters(catalog, LP1, LP2):
    SCCc = scc.KosarajuSCC(catalog['connections'])
    numComponentes1 = scc.connectedComponents(SCCc)
    boolean = False
    infoLP1 = me.getValue(mp.get(catalog['landing_points'], LP1))
    infoLP2 = me.getValue(mp.get(catalog['landing_points'], LP2))
    for cable1 in lt.iterator(infoLP1['cables']):
        cable_LP1 = formatVertex(LP1, cable1['cable_name'])
        for cable2 in lt.iterator(infoLP2['cables']):
            cable_LP2 = formatVertex(LP2, cable2['cable_name'])

            boolean = scc.stronglyConnected(SCCc, cable_LP1, cable_LP2)
            if boolean:
                break
    
    return numComponentes1, boolean


def isCapital(catalog, idciudad):
    '''Funcion para determinar si una ciudad es capital o no'''
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
        

def prueba(catalog):
    print(gr.adjacentEdges(catalog['connections'], formatVertex('Barranquilla', 'America Movil Submarine Cable System-1 (AMX-1)')))
    print(me.getValue(mp.get(catalog['landing_points'], 'Bogota'))['cables'])


def Req2(catalog):
    #con las capitales retorna resultados extranos, por como se agregan cables a la lista de la capital en la funcion addconection
    valores = mp.valueSet(catalog['landing_points'])
    for valor in lt.iterator(valores):
        if lt.size(valor['cables']) > 1:
            try:
                print('El landing point en ', valor['info']['name'], ' con identificador ', valor['info']['landing_point_id'], ' tiene ', lt.size(valor['cables']), ' cables.')
            except:
                print('El landing point en ', valor['info']['name'], ' con identificador ', '----', ' tiene ', lt.size(valor['cables']), ' cables.')


def Req3(catalog, pais1, pais2):
    #Retorna resultados extranos a veces tomando paths sin sentido porque se aprovecha del hecho de que ahora mismo la distancia
    #entre una capital y un lp costero es 0.1
    capital1 = me.getValue(mp.get(catalog['countries'], pais1))['info']['CapitalName']

    cables1 = me.getValue(mp.get(catalog['landing_points'], capital1))['cables']
    cable1 = lt.getElement(cables1, 1)['cable_name']

    capital2 = me.getValue(mp.get(catalog['countries'], pais2))['info']['CapitalName']
    cables2 = me.getValue(mp.get(catalog['landing_points'], capital2))['cables']
    cable2 = lt.getElement(cables2, 1)['cable_name']

    LP1 = formatVertex(capital1, cable1)
    LP2 = formatVertex(capital2, cable2)
    search = dijsktra.Dijkstra(catalog['connections'], LP1)
    distancia = dijsktra.distTo(search, LP2)

    path = dijsktra.pathTo(search, LP2)
    return path, distancia


def getCriticalInfrastructure(catalog):
    mst = prim.PrimMST(catalog['connections'])
    print(gr.numVertices(mst))
    pass



def getAffectedCountries(catalog, landingpoint):
    lp = me.getValue(mp.get(catalog['landing_points'], landingpoint))
    affectedcountries = lt.newList('ARRAY_LIST')
    for cable in lt.iterator(lp['cables']):
        #O(N) donde N es la cantidad de cables que se conectan con ese landing point
        vertexname = landingpoint + "-" + cable['cable_name']
        affectedvertices = gr.adjacents(catalog['connections'], vertexname)
        for vertex in lt.iterator(affectedvertices):
            #O(M) donde M es la la cantidad de vertices adyacentes al nodo específico
            vertexcountry = me.getValue(mp.get(catalog['landing_points'], vertex.split("-")[0]))['info']["name"].split(", ")[-1]
            if not lt.isPresent(affectedcountries, vertexcountry):
                lt.addLast(affectedcountries, vertexcountry)
    return affectedcountries



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
