import re

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
    return {title : parseType(rawParse)}
