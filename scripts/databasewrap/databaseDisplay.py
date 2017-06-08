from tables import *
import numpy
import tablesDatabase as td
import os
import LogParseFunc


dataFile = open_file('Database.h5',mode='a')
table = dataFile.root.Molecules

h2 = LogParseFunc.jsonParse('LOG.log')
if os.path.isfile('./Database.h5') == False:
    td.createDatabase()

td.debugDisplay()
td.insertMolecule(h2,table)

dataFile.close()
