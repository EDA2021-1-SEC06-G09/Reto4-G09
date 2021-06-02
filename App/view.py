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
assert cf

def initCatalog():
    return controller.initCatalog()


def loadData(catalog):
    controller.loadData(catalog)


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Identificar clústeres de comunicación")
    print("3- Identificar puntos de conexión críticos")
    print("4- Encontrar ruta más corta (distancia) entre dos paises")
    print("5- Identificar la infraestructura crítica")
    print("6- Analisar impacto del fallo de un landing point")

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
        loadData(catalog)

    elif int(inputs[0]) == 2:
        lp1 = input("Nombre del primer landing point: ")
        lp2 = input("Nombre del segundo landing point: ")
        controller.getClusters(catalog)

    elif int(inputs[0]) == 3:
        pass

    elif int(inputs[0]) == 4:
        ocountry = input("Nombre del país de origen: ")
        dcountry = input("Nombre del país de destino: ")
        pass

    elif int(inputs[0]) == 5:
        pass

    elif int(inputs[0]) == 6:
        landingpoint = input("Nombre del landing point: ")
        pass

    else:
        catalog.clear()
        sys.exit(0)
sys.exit(0)
