import re
import json
import parsers.parseTools as pt
import os
from parsers.gaussianParse import gaussianparse

def mainparse(filename,program='autodetect'):
    ###Set PlaceHolder values
    filename = filename
    MainDict = {}
    UnitDict = {}

    with open(filename,'r') as File:
        Rawfile = File.read()
    #Main Data
    MainDict['RHF_Energy']                  ='Can be found in Gaussian and Molpro .log files'
    MainDict['Stoichiometry']               ='Can be found in Gaussian,Molpro,and Dalton files'
    MainDict['Coordinates']                 = {}
    MainDict['Coordinates']['Center_Number']= 'Can be found in Gaussian,Molpro,and Dalton files'
    MainDict['Coordinates']['Atomic_Number']= 'Can be found in Gaussian,Molpro,and Dalton files'
    MainDict['Coordinates']['Cart_Coords']  = 'Can be found in Gaussian,Molpro,and Dalton files'

    ###Determine file type
    if program == 'gaussian':
        return gaussianparse(filename)
    elif program == 'autodetect':
        if filename.split('.')[-1] == 'log':
            return gaussianparse(filename)
