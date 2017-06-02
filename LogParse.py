import re
import json
def parseFlags(string,startFlag,endFlag,reFlags=re.S):
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

def mainParse(string,startFlag,Endflag,reFlags=re.S, parseType=raw):
    rawParse = parseFlags(string,startFlag,Endflag,reFlags)
    return parseType(rawParse)

def dictParse(title,string,startFlag,Endflag,reFlags=re.S, parseType=raw):
    rawParse = parseFlags(string,startFlag,Endflag,reFlags)
    MainDict[title] = parseType(rawParse)



filename = "LOG.log"
MainDict = {}

with open(filename, "r") as File:
    RawFile = File.read()

#####Pull Out Values#####

###PopulationAnalysis###

PopulationRaw = parseFlags(RawFile,"Population analysis using the SCF density","Leave Link  601")

ArgumentList = [
#Population Analysis
['ElectronicState',          PopulationRaw,"The electronic state is","\."],
['OccupiedEigenvalues',      PopulationRaw,"Alpha  occ. eigenvalues --","Alpha virt. eigenvalues --",dict(parseType=cleanList)],
['VirtualEigenvalues ',      PopulationRaw,"Alpha virt. eigenvalues --","Condensed",dict(parseType=cleanList)],
['CondensedAtoms',           PopulationRaw,"Condensed to atoms \(all electrons\):","Mulliken charges:",dict(parseType=parseTable)],
['MullikenCharges',          PopulationRaw,"Mulliken charges:","Sum of Mulliken charges =",dict(parseType=parseTable)],
['MullikenChargesSum',       PopulationRaw,"Sum of Mulliken charges =","\n"],
['DipoleMoment',             PopulationRaw,"Dipole moment[^\n]*:","Quadrupole moment",dict(parseType=multiEquivLine)],
['QuadrupoleMoment',         PopulationRaw,"Quadrupole moment[^\n]*:","Traceless Quadrupole",dict(parseType=multiEquivLine)],
['TracelessQuadrupoleMoment',PopulationRaw,"Traceless Quadrupole moment[^\n]*:","Octapole moment",dict(parseType=multiEquivLine)],
['OctapoleMoment',           PopulationRaw,"Octapole moment[^\n]*:","Hexadecapole moment",dict(parseType=multiEquivLine)],
['HexadecapoleMoment',       PopulationRaw,"Hexadecapole moment[^\n]*:","N-N",dict(parseType=multiEquivLine)],
['N-N',                      PopulationRaw,r'.(?=N-N)','Symmetry',dict(parseType=multiEquivLine)],
#Energy
['E(RHF)',RawFile,"SCF Done:  E\(RHF\) =\s*","\sA.*cycles",dict(reFlags=0)],
["SCF_Other",RawFile,"after.*cycles","Leave Link  502",dict(parseType=multiEquivLine)],
###OptimizedStructure###
###Frequency###
]

for item in ArgumentList:
    args=[]
    kwargs={}
    for sub in item:
        if type(sub) == dict:
            kwargs = sub
        else:
            args.append(sub)
    dictParse(*args,**kwargs)

#SymmetryEnergies have a unique format
symdict = {}
for symmetry in ['AG','B1G','B2G','B3G']:
    symdict['{}'.format(symmetry)]= equivLine(PopulationRaw,'{}'.format(symmetry))
MainDict['SymmetryEnergy']=symdict

#Basic single line info, should incorporate into main list
MainDict['ElectronicSpatialExtent'] = equivLine(PopulationRaw,"Electronic spatial extent")
MainDict['Charge'] = equivLine(PopulationRaw,"Charge")

print(json.dumps(MainDict,indent=4))

with open("parsed.json",'w') as File:
    json.dump(MainDict,File, indent=4)
