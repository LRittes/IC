from pyDecision.algorithm import ahp_method
import numpy as np
from const import *


def create_Matrix(arr, default_value=0):
        return [[default_value for _ in arr] for _ in arr]

def matrix_evaluations(req,db):
        weights = {}
        for criterionReq in req:
            for criterionDb in db:
                if criterionReq == criterionDb['pi']:
                    uniqueValues = list(set(criterionDb['valores']))
                    uniqueValues.sort()
                    matrix = create_Matrix(uniqueValues)
                    evaluate_each_criterion(matrix,uniqueValues, criterionDb['tipo'], req[criterionReq]['valor'])
                    
                    weights[criterionReq] =  matrix
                    break
        return weights

def evaluate_each_criterion(matrix,uniqueValues,criterion_type,req_value):
        if criterion_type == HB:
            evaluate_against_wish_value = [ 9 if value == req_value else 5 if value > req_value else 1 for value in uniqueValues ]
            for lin in range(len(uniqueValues)):
                for i in range(len(uniqueValues)):
                    if lin == i:
                        matrix[i][lin] = 1
                    else:
                        matrix[i][lin] = evaluate_against_wish_value[i] / evaluate_against_wish_value[lin]
        elif criterion_type == NB:
            evaluate_against_wish_value = [ 9 if value == req_value else 1 for value in uniqueValues ]
            for lin in range(len(uniqueValues)):
                for i in range(len(uniqueValues)):  
                    if lin == i:
                        matrix[i][lin] = 1
                    else:
                        matrix[i][lin] = evaluate_against_wish_value[i] / evaluate_against_wish_value[lin]
        elif criterion_type == LB:
            evaluate_against_wish_value = [ 9 if value == req_value else 5 if value < req_value else 1 for value in uniqueValues ]
            for lin in range(len(uniqueValues)):
                for i in range(len(uniqueValues)):  
                    if lin == i:
                        matrix[i][lin] = 1
                    else:
                        matrix[i][lin] = evaluate_against_wish_value[i] / evaluate_against_wish_value[lin]

def evaluation_req(req):
    weightsReq = [[] for _ in req.keys()]
    idx = 0
    for criterion, value in req.items():
        for criterion2, value2 in req.items():
            weightsReq[idx].append(value['peso']/value2['peso'])
        idx += 1
    weight_derivation = 'mean' # 'mean'; 'geometric' or 'max_eigen'

    dataset = np.array(weightsReq)

    weights = ahp_method(dataset, wd = weight_derivation)    

    weightsDict = {}
    idx = 0
    
    for criterion in req.keys():
        weightsDict[criterion] = weights[idx]
        idx += 1 
    
    return weightsDict

def evaluation_alters(weightsAlters:dict):
    weightAlter_final = {}
    for criterion, weightAlter in weightsAlters.items():
        weight_derivation = 'mean' # 'mean'; 'geometric' or 'max_eigen'
       
        dataset = np.array(weightAlter)
        weights = ahp_method(dataset, wd = weight_derivation)
    
        weightAlter_final[criterion] = weights
    return weightAlter_final


def rankingAlternatives(req, db, alternatives):
    evaluationReq = evaluation_req(req)
    evaluationAlters = evaluation_alters(matrix_evaluations(req,db))
    ranking = []
    totPts = 0
    for alter in alternatives:
        ptsFinal = 0
        for criterion, pos in alter['criterions'].items():
            
            if type(pos) == list:
                try:
                    pos.index(req[criterion[:-3]]['valor'])
                    ptsFinal += evaluationReq[criterion[:-3]]
                except:
                    ptsFinal += 0
            else:
                ptsFinal += evaluationAlters[criterion[:-3]][pos] * evaluationReq[criterion[:-3]]
        totPts += ptsFinal
        ranking.append({'company': alter['company'], 'pts': ptsFinal})
        
    # for alterIdx in range(len(ranking)):
    #     ranking[alterIdx]['pts'] = ranking[alterIdx]['pts'] / totPts  
    
    return ranking 

def returnPtsFromList(dici):
    return dici['pts']

def showRanking(req,db,alternatives):
    ranking = rankingAlternatives(req,db,alternatives)
    ranking.sort(key=returnPtsFromList,reverse=True)
    for rank in ranking:
        print(f'{rank["company"]} {rank["pts"]}')
