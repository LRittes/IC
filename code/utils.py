import yaml
import os
import time
from random import randint

from ahp_implement import ahp as ahpImp
from ahp_lib import ahp as ahpLib
from const import *

def create_directory(path):
    try:
        os.makedirs(path, exist_ok=True)
    except Exception as e:
        print(f'Erro ao criar o diretório "{path}": {e}')

def saveNewRequisition(req, knownReq=False):
    if knownReq:
        idetifier = 1
    else:
        idetifier = len(KNOWSREQS) + 1
    
    create_directory(dataDir)
    
    try:
        with open(reqFilePath,'r') as file:
            data = yaml.load(file,Loader=yaml.FullLoader)
            
            if knownReq:
                idetifier = len(data['requisitions']) + 1
            else:
                idetifier = 1 + len(data['requisitions'])
    except FileNotFoundError:
        data = {}
    
    if 'requisitions' in data:
        data['requisitions'].update({f'id_{idetifier}': {'criterions': req}})
    else:
        data['requisitions'] = {f'id_{idetifier}': {'criterions': req}}
    
    with open(reqFilePath,'w') as file:
        yaml.dump(data,file, default_flow_style=False, allow_unicode=True)
    
    return idetifier

def saveAlternatives(id, alternativesDict):
    curretTest = f'req_{id}_alters_{alternativesDict["amount"]}'
    try:
        create_directory(dirPathAlters)
        create_directory(dirPathAlters + curretTest + '/' + positionDir)
        create_directory(dirPathAlters + curretTest + '/' + valueDir)
        
    except Exception as e:
        print(f'Erro ao criar o diretório "{dirPathAlters}": {e}')
        
    with open(f'{dirPathAlters}{curretTest}/{positionDir}req_{id}_alters_{alternativesDict["amount"]}.yml','w') as file:
        
        yaml.dump({'alternatives': alternativesDict['position']}
            ,file, default_flow_style=False, allow_unicode=True)

    with open(f'{dirPathAlters}{curretTest}/{valueDir}req_{id}_alters_{alternativesDict["amount"]}.yml','w') as file:
        
        yaml.dump({'alternatives': alternativesDict['value']}
            ,file, default_flow_style=False, allow_unicode=True)

def getAlternatives(id, amount, knowData = False):
    if knowData:
        dirPath = dirPathKnownAlters
    else:
        dirPath = dirPathAlters
    position = []
    value = []
    
    dirPathReqAlters = f'{dirPath}req_{id}_alters_{amount}'
    fileNameAlters = f'req_{id}_alters_{amount}.yml'
    
    # with open(dirPathReqAlters + '/position/' + fileNameAlters, 'r') as file:
    #     data = yaml.load(file,Loader=yaml.FullLoader)
    #     position = data['alternatives']
    
    with open(dirPathReqAlters + '/value/' + fileNameAlters, 'r') as file:
        data = yaml.load(file,Loader=yaml.FullLoader)
        value = data['alternatives']
    
    return {'value': value, 'position': position}

def generateSampleTest(db, alternativesValue):
    saveKnownTestCase()
    
    for reqs in range(NUM_TEST):
        newReq = generateRequisition(db)
        id = saveNewRequisition(newReq)
        
        amountAux = NUM_ALTERNATIVES[0]
        alterPos , alterValue = generateAlternatives(db,alternativesValue,0, amountAux)
        saveAlternatives(id, {'position': alterPos, 'value': alterValue, 'amount': amountAux})
        
        for amount in NUM_ALTERNATIVES[1:]:
            alters = getAlternatives(id, amountAux,False)
            amountAux = amount
            
            alterPos , alterValue = generateAlternatives(db,alternativesValue,len(alters['value']), amount)
            
            saveAlternatives(id, {'position': alters['position'] + alterPos, 'value': alters['value'] + alterValue, 'amount': amount })
            
def saveKnownTestCase():
    reqs: dict = getAllRequisitions(True)
    
    for identify, req in reqs.items():
        id = saveNewRequisition(req['criterions'], True)
        alters = getAlternatives(id, 5,True)    
        saveAlternatives(id, {'position': alters['position'], 'value': alters['value'], 'amount': len(alters['value'])})

def generateRequisition(database):
    newReq = {}
    for idx, criterio in enumerate(getCriterions(database)):
        newReq[criterio] = {'valor': database[idx]['valores'][randint(0,len(database[idx]['valores'])) - 1], 'peso': randint(1,9)}
    return newReq  

# Erro: não está pegando os mesmos valores
def generateAlternatives(database, alternatives,initialRange, amount):
    altsValue = []
    altsPos = []
    criterionsList =  getCriterionsIsList(alternatives)
    for n in range(initialRange,amount):
        altPos = {'company': f'company{n}',
                  'criterions': {}}
        altValue = {'company': f'company{n}',
                  'criterions': {}}
        for idx, criterio in enumerate(getCriterions(database)):
             
           
            if criterio in criterionsList:
                l = generateListOptions(database,idx)
                altPos['criterions'][f'{criterio}Pos'] =  l
                altValue['criterions'][criterio] = l
                continue
            
            
            dbValues = list(set(database[getCriterionIdxInDB(database,criterio)]['valores']))
            dbValues.sort()
            amountOptions = len(dbValues)
            if amountOptions > 0:
                idxCriterio = randint(0, len(dbValues) - 1)
            else:
                idxCriterio = 0
            
                
            altPos['criterions'][f'{criterio}Pos'] =  idxCriterio
            altValue['criterions'][criterio] = dbValues[idxCriterio]
            # print(dbValues, DB[idx]['valores'][idxCriterio], dbValues[idxCriterio])
        altsValue.append(altValue)
        altsPos.append(altPos)
    
    return altsPos, altsValue

def generateList(limitValue):
    return [x for x in range(128, limitValue, 128)]

def getCriterions(db: list[dict]):
    critReturn = []
    for crit in db:
        critReturn.append(crit['pi'])
    return critReturn

def getCriterionIdxInDB(db, criterion):
    for idx, criterionDB in enumerate(db):
        if criterionDB['pi'] == criterion:
            return idx 

def getCriterionsIsList(alternatives: list):
    if len(alternatives) == 0:
        return []
    
    criterions = []
    
    for criterion, value in alternatives[0]['criterions'].items():
        if type(value) == list:
            criterions.append(criterion)
    return criterions


def generateListOptions(database, idx):
    n_values = randint(5, len(set(database[idx]['valores'])) - 1)
    l = []
    for _ in range(n_values):
        random = randint(0, len(set(database[idx]['valores'])) - 1)
        while list(set(database[idx]['valores']))[random] in l:
                random = randint(0, len(set(database[idx]['valores'])) - 1)
        l.append(list(set(database[idx]['valores']))[random])
    l.sort()
    
    return l

def getAllRequisitions(knowData = False):
    if knowData:
        path = knownReqFilePath
    else:
        path = reqFilePath
    
    with open(path, 'r') as file:
         data = yaml.load(file,Loader=yaml.FullLoader)
    return data['requisitions']

def accuracy(rankingI:list , rankingL:list):
    # accI = 0
    # accL = 0
    acc = 0
    
    for alterIdx in range(len(rankingL)):
        # if alterIdx > 4:
        #     break
        # if rankingL[alterIdx]['company'] == RANKINGTEST[alterIdx]:
        #     accL += 1
        # if rankingI[alterIdx]['company'] == RANKINGTEST[alterIdx]:
        #     accI += 1
        if rankingL[alterIdx]["company"] == rankingI[alterIdx]["company"]:
            acc += 1
    return acc/len(rankingL)
    # {"Lib": accL / len(rankingL), "Imp": accI / len(rankingI)}

def getCompanyInRank(company, rankL):
    for alter in rankL:
        if alter['company'] == company:
            return alter

def mseRank(rankI: list, rankL: list):
    mse = 0
    
    for alterIdx in range(len(rankL)):
        value = getCompanyInRank(rankI[alterIdx]['company'], rankL)['pts'] - rankI[alterIdx]['pts']
        mse += value * value
        
    return mse/len(rankL)

def saveMetrics(id, amount, metricsData: dict):
    metricsFile = f'req_{id}.yaml'
    try:
        create_directory(dataDir + metricsDir)
        
    except Exception as e:
        print(f'Erro ao criar o diretório "{metricsDir}": {e}')
    
    try:
        with open(dataDir + metricsDir + metricsFile,'r') as file:
            data = yaml.load(file,Loader=yaml.FullLoader)
    except Exception as e:
        data = {}
    
    
    if 'metrics' in data:
        data['metrics'].append({ 'amount': amount,'time': {'implementation': metricsData['imp'], 'library': metricsData['lib']}, 'accuracy':{ 'accuracyAll': metricsData['accuracyAll'], 'accuracy3': metricsData['accuracy3']}})
                                # 'accuracy_all_Lib': metricsData['accuracy_all_Lib'], 'accuracy_all_Imp': metricsData['accuracy_all_Imp'], 'accuracy_3_first_Lib': metricsData['accuracy_3_first_Lib'], 'accuracy_3_first_Imp': metricsData['accuracy_3_first_Imp']})
    else:
        data['metrics'] = [{ 'amount': amount,'time': {'implementation': metricsData['imp'], 'library': metricsData['lib']}, 'accuracy':{ 'accuracyAll': metricsData['accuracyAll'], 'accuracy3': metricsData['accuracy3']}}]
                            # 'accuracy_all_Lib': metricsData['accuracy_all_Lib'], 'accuracy_all_Imp': metricsData['accuracy_all_Imp'], 'accuracy_3_first_Lib': metricsData['accuracy_3_first_Lib'], 'accuracy_3_first_Imp': metricsData['accuracy_3_first_Imp']}]
    
    with open(dataDir + metricsDir + metricsFile,'w') as file:
        yaml.dump(data ,file, default_flow_style=False, allow_unicode=True)

def runAHPTests(req, alternatives):
    # print(req, alternatives)
    ahpI = ahpImp.AHP(req, DB, alternatives['value'])
    
    startTimeI = time.time()
    rankingAhpI = ahpI.ranking_alternatives(ahpI.organize_db())
    endTimeI = time.time()
    timeI = endTimeI - startTimeI
    
    rankingAhpI.sort(key=ahpI.returnPtsFromList,reverse=True)
    ahpI.show_rank()
    
    startTimeL = time.time()
    rankingAhpL = ahpLib.rankingAlternatives(req,DB,alternatives['position'])
    endTimeL = time.time()
    timeL = endTimeL - startTimeL
    
    rankingAhpL.sort(key=ahpI.returnPtsFromList,reverse=True)
    
    print('-'*70)
    # ahpLib.showRanking(req,DB,alternatives['position'])
    # mse = mseRank(rankingAhpI,rankingAhpL)
    # print('-'*70)
    
    accAll = accuracy(rankingAhpI,rankingAhpL)
    
    acc3 = accuracy(rankingAhpI[:3],rankingAhpL[:3])
    # print(accAll)
    # print(acc3)
    

    data = {'imp': timeI, 'lib': timeL, 'accuracyAll': accAll, 'accuracy3': acc3} 
            # 'accuracy_all_Lib': accAll['Lib'], 'accuracy_all_Imp': accAll['Imp'], 'accuracy_3_first_Lib': acc3['Lib'], 'accuracy_3_first_Imp': acc3['Imp']}

    
    return data