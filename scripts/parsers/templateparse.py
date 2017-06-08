import re
import json
import parseTools as pt
import os

def fileparse(filename):
    filename = filename
    MainDict = {}
    UnitDict = {}

    with open(filename,'r') as File:
        Rawfile = File.read()
    #Main Data
    MainDict['RHF_Energy']                  ='PlaceHolder'
    MainDict['Stoichiometry']               ='PlaceHolder'
    MainDict['Coordinates']                 = {}
    MainDict['Coordinates']['Center_Number']= []
    Maindict['Coordinates']['Atomic_Number']= []
    Maindict['Coordinates']['Cart_Coords']  = []
    #Metadata
    Maindict['Timestamp']                   ='PlaceHolder'
    Maindict['Source']                      ='PlaceHolder' #what software is the file from?
    Maindict['InputString']                 ='PlaceHolder' #what were the input parameters for the software
    #Units
    UnitDict['RHF_Energy']                  ='Units'
    UnitDict['Coordinates']                 ={}
    UnitDict['Coordinates']['Cart_Coords']  ='Units'
