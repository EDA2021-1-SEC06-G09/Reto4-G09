"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import stack
from DISClib.ADT import map as mp
from DISClib.ADT import graph as gr
assert cf


def initCatalog():
    return controller.initCatalog()


def loadData(catalog):
    return controller.loadData(catalog)


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printReq3(pila):
    i = 1
    tamano = stack.size(pila)
    while i <= tamano:
        cable = stack.pop(pila)
        print('Desde ', cable['vertexA'].split('-')[0], ' hasta ', cable['vertexB'].split('-')[0], ' con una distancia de ', cable['weight'])
        i+=1


def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Identificar clústeres de comunicación")
    print("3- Identificar puntos de conexión críticos")
    print("4- Encontrar ruta más corta (distancia) entre dos paises")
    print("5- Identificar la infraestructura crítica")
    print("6- Analisar impacto del fallo de un landing point")
    print("Presione cualquier otro número para salir\n")

catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        catalog = initCatalog()
        firstandlast = loadData(catalog)
        print("\nNúmero total de landing points:", mp.size(catalog['landing_points']),
              "\nNúmero total de connecciones:", gr.numEdges(catalog['connections']),
              "\nNúmero total de paises:", mp.size(catalog['countries']))
        firstlp = firstandlast[0]
        print("\nPrimer landing point cargado:\n",
              "Identificador:", firstlp['id'],
              "- Nombre:", firstlp['name'],
              "- Latitud:", firstlp['latitude'],
              "- Longitud:", firstlp['longitude'])
        lastcountry = firstandlast[1]
        print("\nÚltimo país cargado:\n",
              "Nombre:", lastcountry['CountryName'],
              "- Población:", lastcountry['Population'],
              "- Usuarios de Internet:", lastcountry['Internet users'], "\n")

    elif int(inputs[0]) == 2:
        lp1 = input("Nombre del primer landing point: ")
        lp2 = input("Nombre del segundo landing point: ")
        retorno = controller.getClusters(catalog, lp1, lp2)
        print('Hay ', retorno[0], ' clusters.')
        if retorno[1]:
            print("Los dos landing points pertenecen a un mismo cluster")
        else:
            print("Los dos landing points no pertenecen a un mismo cluster")

    elif int(inputs[0]) == 3:
        print(controller.Req2(catalog))

    elif int(inputs[0]) == 4:
        ocountry = input("Nombre del país de origen: ")
        dcountry = input("Nombre del país de destino: ")
        retorno = controller.Req3(catalog, ocountry, dcountry)
        print(printReq3(retorno[0]))
        print('La distancia total es de ', retorno[1])

    elif int(inputs[0]) == 5:
        pass

    elif int(inputs[0]) == 6:
        landingpoint = input("Nombre del landing point: ")
        controller.getAffectedCountries(catalog, landingpoint)

    else:
        catalog.clear()
        sys.exit(0)
sys.exit(0)
