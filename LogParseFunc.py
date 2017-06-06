import re
import json
import parseTools as pt
def jsonParse(filename):
    filename = filename
    MainDict = {}

    with open(filename, "r") as File:
        RawFile = File.read()

    #Smaller Section of file, used to find all Population Analysis Values
    PopulationRaw = pt.parseFlags(RawFile,"Population analysis using the SCF density","Leave Link  601")

    ArgumentList = [
    #Population Analysis
    ['ElectronicState',          PopulationRaw,"The electronic state is","\."],
    ['OccupiedEigenvalues',      PopulationRaw,"Alpha  occ. eigenvalues --","Alpha virt. eigenvalues --",dict(parseType=pt.cleanList)],
    ['VirtualEigenvalues ',      PopulationRaw,"Alpha virt. eigenvalues --","Condensed",dict(parseType=pt.cleanList)],
    ['CondensedAtoms',           PopulationRaw,"Condensed to atoms \(all electrons\):","Mulliken charges:",dict(parseType=pt.parseTable)],
    ['MullikenCharges',          PopulationRaw,"Mulliken charges:","Sum of Mulliken charges =",dict(parseType=pt.parseTable)],
    ['MullikenChargesSum',       PopulationRaw,"Sum of Mulliken charges =","\n"],
    ['DipoleMoment',             PopulationRaw,"Dipole moment[^\n]*:","Quadrupole moment",dict(parseType=pt.multiEquivLine)],
    ['QuadrupoleMoment',         PopulationRaw,"Quadrupole moment[^\n]*:","Traceless Quadrupole",dict(parseType=pt.multiEquivLine)],
    ['TracelessQuadrupoleMoment',PopulationRaw,"Traceless Quadrupole moment[^\n]*:","Octapole moment",dict(parseType=pt.multiEquivLine)],
    ['OctapoleMoment',           PopulationRaw,"Octapole moment[^\n]*:","Hexadecapole moment",dict(parseType=pt.multiEquivLine)],
    ['HexadecapoleMoment',       PopulationRaw,"Hexadecapole moment[^\n]*:","N-N",dict(parseType=pt.multiEquivLine)],
    ['N-N',                      PopulationRaw,r'.(?=N-N)','Symmetry',dict(parseType=pt.multiEquivLine)],
    #Energy
    ['E(RHF)',RawFile,"SCF Done:  E\(RHF\) =\s*","\sA.*cycles",dict(reFlags=0)],
    ["SCF_Other",RawFile,"after.*cycles","Leave Link  502",dict(parseType=pt.multiEquivLine)],
    ###OptimizedStructure###
    ###Frequency###
    ###Stoic###
    ['name',RawFile,'Stoichiometry[\s]+','(?=\n)',dict(reFlags=0)]
    ]

    for item in ArgumentList:
        args=[]
        kwargs={}
        for sub in item:
            if type(sub) == dict:
                kwargs = sub
            else:
                args.append(sub)
        MainDict.update(pt.dictParse(*args,**kwargs))


    #SymmetryEnergies have a unique format
    symdict = {}
    for symmetry in ['AG','B1G','B2G','B3G']:
        symdict['{}'.format(symmetry)]= pt.equivLine(PopulationRaw,'{}'.format(symmetry))
    MainDict['SymmetryEnergy']=symdict

    #Basic single line info, should incorporate into main list
    MainDict['ElectronicSpatialExtent'] = pt.equivLine(PopulationRaw,"Electronic spatial extent")
    MainDict['Charge'] = pt.equivLine(PopulationRaw,"Charge")

    #print(json.dumps(MainDict,indent=4))

    with open("parsed.json",'w') as File:
        json.dump(MainDict,File, indent=4)
    
    return MainDict
