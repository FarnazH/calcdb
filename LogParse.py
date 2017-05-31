import re
import json
def parseFlags(string,startFlag,endFlag,reFlags=0):
    Pattern = r"{}(.*?){}".format(startFlag, endFlag)
    return re.search(Pattern,string,flags=reFlags).group(1)

def cleanList(string):
    stringList = string.split()
    cleanList = []
    for item in stringList:
        cleanList.append(item.strip())
    return cleanList

def parseTable(string):
    lines = string.split("\n")
    #remove empty lines
    for idx,line in enumerate(lines):
        if line == "" or re.match("^\s*$",line):
            del lines[idx]

    dArray = {}
    finalArray=[]

    for idx,line in enumerate(lines):
        whitespace = re.match("\s*(?!\s)",line).group()
        if idx == 0:
            titleWhitespace = whitespace
            ArrayIndex = cleanList(line)
           # for idx,item in enumerate(ArrayIndex):
           #     ArrayIndex[idx]=int(item)
            ArrayItemNumber = len(line.split())
        elif whitespace == titleWhitespace:
            ArrayIndex = line.split()
            ArrayItemNumber = len(line.split())
        else:
            line = cleanList(line)
            for idx,item in enumerate(reversed(ArrayIndex)):
                if item not in dArray:
                    dArray[item]=[]
                dArray[item].append(line[-(idx+1)])
    
    keylist=[]

    for key in dArray.keys():
        try: 
            keylist.append(int(key))
        except:return dArray

    for key in sorted(keylist):
        finalArray.append(dArray[str(key)])
    
    return finalArray

def equivLine(string,name):
    pattern = r"({}.*?)(\d(.\d*)?).*\n".format(name)
    return re.search(pattern,string).group(2)

def multiEquivLine(string):
    Dict = {}
    List=string.split()
    keyList = []
    valueList = []
    itemmarker = 0
    j=0
    ###Fixes edge case where equal sign is not at end of string due to negative number
    newList=[]
    for i in range(len(List)):
        if re.search("=-",List[i]):
            tempstring = List[i].split('=')
            newList.append(tempstring[0]+'=')
            newList.append(tempstring[1])
        else:
            newList.append(List[i])
    List = []
    List = newList
    ###

    for i in range(len(List)):
        if List[i][-1] == "=":
            if i == 0:
                tempList = List[0].strip('=')
            else:
                tempList = List[itemmarker:(i-1)]
                tempList.append(List[i].strip('='))
            itemmarker = i+1
            keyList.append("".join(tempList))
            valueList.append(List[i+1])
            i = i+2
    for idx,key in enumerate(keyList):
        Dict[key] = valueList[idx]
    return Dict

def raw(Input):
    return Input

def mainParse(string,startFlag,Endflag,reFlags=0, parseType=raw):
    rawParse = parseFlags(string,startFlag,Endflag,reFlags)
    return parseType(rawParse)

def dictParse(title,string,startFlag,Endflag,reFlags=0, parseType=raw):
    rawParse = parseFlags(string,startFlag,Endflag,reFlags)
    MainDict[title] = parseType(rawParse)



filename = "LOG.log"
MainDict = {}

with open(filename, "r") as File:
    RawFile = File.read()

#####Pull Out Values#####

#TODO: Put in loop

###PopulationAnalysis###

PopulationRaw = parseFlags(RawFile,"Population analysis using the SCF density","Leave Link  601",reFlags=re.DOTALL)

dictParse('ElectronicState',PopulationRaw,"The electronic state is","\.")


dictParse('OccupiedEigenvalues',PopulationRaw,"Alpha  occ. eigenvalues --","Alpha virt. eigenvalues --",reFlags=re.S,parseType=cleanList)

dictParse('VirtualEigenvalues ',PopulationRaw,"Alpha virt. eigenvalues --","Condensed",reFlags=re.S,parseType=cleanList)

dictParse('CondensedAtoms', PopulationRaw,"Condensed to atoms \(all electrons\):","Mulliken charges:",reFlags=re.S,parseType=parseTable)

dictParse('MullikenCharges',PopulationRaw,"Mulliken charges:","Sum of Mulliken charges =",reFlags=re.S, parseType=parseTable)

dictParse('MullikenChargesSum',PopulationRaw,"Sum of Mulliken charges =","\n")

MainDict['ElectronicSpatialExtent'] = equivLine(PopulationRaw,"Electronic spatial extent")

MainDict['Charge'] = equivLine(PopulationRaw,"Charge")

dictParse('DipoleMoment',PopulationRaw,"Dipole moment[^\n]*:","Quadrupole moment",reFlags=re.S,parseType=multiEquivLine)

dictParse('QuadrupoleMoment',PopulationRaw,"Quadrupole moment[^\n]*:","Traceless Quadrupole",reFlags=re.S,parseType=multiEquivLine)

dictParse('TracelessQuadrupoleMoment',PopulationRaw,"Traceless Quadrupole moment[^\n]*:","Octapole moment",reFlags=re.S,parseType=multiEquivLine)

dictParse('OctapoleMoment',PopulationRaw,"Octapole moment[^\n]*:","Hexadecapole moment",reFlags=re.S,parseType=multiEquivLine)

dictParse('HexadecapoleMoment',PopulationRaw,"Hexadecapole moment[^\n]*:","N-N",reFlags=re.S,parseType=multiEquivLine)

dictParse('N-N',PopulationRaw,r'.(?=N-N)','Symmetry',reFlags=re.S,parseType=multiEquivLine)

symdict = {}
for symmetry in ['AG','B1G','B2G','B3G']:
    symdict['{}'.format(symmetry)]= equivLine(PopulationRaw,'{}'.format(symmetry))

MainDict['SymmetryEnergy']=symdict

###Energy###
dictParse('E(RHF)',RawFile,"SCF Done:  E\(RHF\) =\s*","\sA.*cycles")
dictParse("SCF_Other",RawFile,"after.*cycles","Leave Link  502",reFlags=re.S,parseType=multiEquivLine)


###OptimizedStructure###
###Frequency###

print(json.dumps(MainDict,indent=4))
