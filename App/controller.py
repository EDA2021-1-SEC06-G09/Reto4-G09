﻿"""
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
 """

import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo
def initCatalog():
    return model.initCatalog()

# Funciones para la carga de datos
def loadData(catalog):
    loadCountries(catalog)
    loadLandingPoints(catalog)
    loadConnections(catalog)


def loadCountries(catalog):
    countriesfile = cf.data_dir + "countries.csv"
    inputfile = csv.DictReader(open(countriesfile, encoding='utf-8'), delimiter=",")
    for country in inputfile:
        model.addCountry(catalog, country)


def loadLandingPoints(catalog):
    landingpointsfile = cf.data_dir + "landing_points.csv"
    inputfile = csv.DictReader(open(landingpointsfile, encoding='utf-8'), delimiter=",")
    for landingpoint in inputfile:
        model.addLandingPoint(catalog, landingpoint)


def loadConnections(catalog):
    connectionsfile = cf.data_dir + "connections.csv"
    inputfile = csv.DictReader(open(connectionsfile, encoding='utf-8-sig'), delimiter=",")
    for connection in inputfile:
        model.addCable(catalog, connection)
        model.addConnection(catalog, connection)

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
def getClusters(catalog):
    model.getClusters(catalog)
