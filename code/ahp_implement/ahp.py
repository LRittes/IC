class AHP():
    def __init__(self,req,db,alternatives):
        self.req = req
        self.db = db
        self.alternatives = alternatives
        self.matrix = self.create_Matrix(list(self.req))
        self.HB = 'HB'
        self.NB = 'NB'
        self.LB = 'LB'

    def organize_db(self):
        dbReturn = []
        for criterionReq in self.req:
            for criterionDb in self.db:
                if criterionReq == list(criterionDb.values())[0]:
                    dbReturn.append(criterionDb)
                    break
        return dbReturn

    def evaluate_pis_req(self,matrix,req): 
        for idx, desc in enumerate(req):
            for idxCol, desc2 in enumerate(req):
                criterion_weight_value = req[desc2]['peso']/req[desc]['peso']
                matrix[idxCol][idx] = criterion_weight_value
        
    def normalize_row(self,matrix,cols_tot):
        lenghtMatrix = range(len(matrix))
        for lin in lenghtMatrix:
            for col in lenghtMatrix:
                normalized_weight = matrix[lin][col]/cols_tot[col]
                matrix[lin][col] = normalized_weight

    def sum_row_matrix(self,matrix,req):
        tot_row = [0 for x in range(len(req))]
        for idx, lin in enumerate(matrix):
            tot_row[idx] += sum(lin)
        return tot_row

    def sum_col_matrix(self,matrix):
        tot_col = [0 for x in matrix]
        for lin in matrix:
            for idx, value in enumerate(lin):
                tot_col[idx] += value
        return tot_col

    def create_Matrix(self,arr, default_value=0):
        return [[default_value for _ in arr] for _ in arr]

    def matrix_evaluations(self,req,db):
        weights = []
        for criterionReq in req:
            for criterionDb in db:
                if criterionReq == criterionDb['pi']:
                    uniqueValues = list(set(criterionDb['valores']))
                    uniqueValues.sort()
                    matrix = self.create_Matrix(uniqueValues)
                    self.evaluate_each_criterion(matrix,uniqueValues, criterionDb['tipo'], req[criterionReq]['valor'])
                    
                    sumCol = self.sum_col_matrix(matrix)
                    self.normalize_row(matrix,sumCol)
                    weightPi = [value/len(matrix) for value in self.sum_row_matrix(matrix,uniqueValues)]
                    
                    weights.append(weightPi)
                    break
        return weights

    def evaluate_each_criterion(self,matrix,uniqueValues,criterion_type,req_value):
        if criterion_type == self.HB:
            evaluate_against_wish_value = [ 9 if value == req_value else 5 if value > req_value else 1 for value in uniqueValues ]
            for lin in range(len(uniqueValues)):
                for i in range(len(uniqueValues)):
                    if lin == i:
                        matrix[i][lin] = 1
                    else:
                        matrix[i][lin] = evaluate_against_wish_value[i] / evaluate_against_wish_value[lin]
        elif criterion_type == self.NB:
            evaluate_against_wish_value = [ 9 if value == req_value else 1 for value in uniqueValues ]
            for lin in range(len(uniqueValues)):
                for i in range(len(uniqueValues)):  
                    if lin == i:
                        matrix[i][lin] = 1
                    else:
                        matrix[i][lin] = evaluate_against_wish_value[i] / evaluate_against_wish_value[lin]
        elif criterion_type == self.LB:
            evaluate_against_wish_value = [ 9 if value == req_value else 5 if value < req_value else 1 for value in uniqueValues ]
            for lin in range(len(uniqueValues)):
                for i in range(len(uniqueValues)):  
                    if lin == i:
                        matrix[i][lin] = 1
                    else:
                        matrix[i][lin] = evaluate_against_wish_value[i] / evaluate_against_wish_value[lin]

    def ranking_alternatives(self,db:list[dict]):
        self.evaluate_pis_req(self.matrix,self.req)

        sumCol = self.sum_col_matrix(self.matrix)
        self.normalize_row(self.matrix,sumCol)
        
        weightPi = [value/len(self.matrix) for value in self.sum_row_matrix(self.matrix,self.req)]
        
        pis_weights = self.matrix_evaluations(self.req,db)
        dict_pis_weights = {}
        for idx,criterion in enumerate(db):
            uniqueValues = list(set(db[idx]['valores']))
            uniqueValues.sort()
            dict_weight_alternatives = {}
            for i, weight in enumerate(pis_weights[idx]):
                dict_weight_alternatives.update({ uniqueValues[i]: weight })
            
            dict_pis_weights.update({ criterion['pi']: {
                                                        'weight_pi':weightPi[idx],
                                                        'weight_alternatives': dict_weight_alternatives
                                                        }
                                    }
            )
        
        dictPtsRank = []
        
        for idx in range(len(self.alternatives)):
            pts = 0
            for criterion in self.alternatives[idx]['criterions']:
                if type(self.alternatives[idx]['criterions'][criterion]) is list:
                    try:
                        self.alternatives[idx]['criterions'][criterion].index(self.req[criterion]['valor'])       
                        
                        pts += dict_pis_weights.get(criterion)['weight_pi']
                        
                    except:
                        pts += dict_pis_weights.get(criterion)['weight_pi'] * 0
                else:
                    pts += dict_pis_weights.get(criterion)['weight_pi'] * dict_pis_weights.get(criterion).get("weight_alternatives").get(self.alternatives[idx]['criterions'][criterion])
            dictPtsRank.append({'company':self.alternatives[idx]['company'], 'pts':pts})
        
        ptsRank = [dictpts['pts'] for dictpts in dictPtsRank]
        sumTotPts = sum(ptsRank)
        # for dictPts in dictPtsRank:
        #     dictPts['pts'] = dictPts['pts']/sumTotPts
        
        return dictPtsRank


    def returnPtsFromList(self,dici):
        return dici['pts']

    def show_rank(self):
        organizedDb = self.organize_db()
        
        ranks = self.ranking_alternatives(organizedDb)
        ranks.sort(key=self.returnPtsFromList,reverse=True)
        for rank in ranks:
            print(f'{rank["company"]} {rank["pts"]}')