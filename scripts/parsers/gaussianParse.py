import re
import json
import parsers.parseTools as pt
import os

def gaussianparse(filename):
    filename = filename
    MainDict = {}
    UnitDict = {}

    with open(filename,'r') as File:
        Rawfile = File.read()
    #Main Data
    MainDict['RHF_Energy']                  =pt.parseFlags(Rawfile,'SCF Done:  E\(RHF\) =\s*','\sA.*cycles',reFlags=0)
    MainDict['Stoichiometry']               =pt.parseFlags(Rawfile,'Stoichiometry[\s]+','(?=\n)',reFlags=0)
    MainDict['Coordinates']                 = {}
    MainDict['Coordinates']['Center_Number']= []
    MainDict['Coordinates']['Atomic_Number']= []
    MainDict['Coordinates']['Cart_Coords']  = []
    #Metadata
    MainDict['Timestamp']                   ='PlaceHolder'
    MainDict['Source']                      ='Gaussian' #what software is the file from?
    MainDict['InputString']                 ='PlaceHolder' #what were the input parameters for the software
    #Units
    MainDict['Units'] = {}
    UnitDict = MainDict['Units']
    UnitDict['RHF_Energy']                  ='Units'
    UnitDict['Coordinates']                 ={}
    UnitDict['Coordinates']['Cart_Coords']  ='Units'

    tablestr = pt.parseFlags(Rawfile,r'Coordinates in L301:\s+\n',r'FixB:')
    print(pt.parseTable(tablestr))

    return MainDict
