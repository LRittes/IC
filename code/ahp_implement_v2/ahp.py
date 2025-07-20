import numpy as np
from typing import List, Dict, Any

class AHP:
    """
    Uma classe para implementar o método Analytic Hierarchy Process (AHP)
    utilizando a biblioteca NumPy para cálculos matriciais eficientes.
    """
    def __init__(self, req: Dict, db: List[Dict], alternatives: List[Dict]):
        self.req = req
        self.db = db
        self.alternatives = alternatives
        # A matriz de comparação de critérios será criada e calculada depois.
        self.criteria_matrix = None
        
        # Constantes para tipos de critério
        self.HB = 'HB'  # Higher is Better
        self.NB = 'NB'  # Nominal is Better
        self.LB = 'LB'  # Lower is Better

    def organize_db(self) -> List[Dict]:
        """
        Organiza a lista de critérios do banco de dados (db) para corresponder
        à ordem dos critérios na requisição (req).
        """
        db_return = []
        # Garante que a ordem dos critérios seja consistente
        ordered_criteria_keys = list(self.req.keys())
        
        for criterion_key in ordered_criteria_keys:
            for criterion_db in self.db:
                if criterion_key == criterion_db.get('pi'):
                    db_return.append(criterion_db)
                    break
        return db_return

    def _evaluate_criteria_matrix(self) -> np.ndarray:
        """
        Cria a matriz de comparação par a par para os critérios principais
        com base em seus pesos.
        Retorna uma matriz NumPy.
        """
        criteria_keys = list(self.req.keys())
        weights = np.array([self.req[key]['peso'] for key in criteria_keys])
        
        # Utiliza broadcasting do NumPy para criar a matriz de comparação de forma eficiente.
        # O elemento [i, j] será peso[i] / peso[j].
        matrix = weights[:, np.newaxis] / weights
        return matrix

    def _evaluate_alternatives_matrix(self, unique_values: List, criterion_type: str, req_value: Any) -> np.ndarray:
        """
        Cria a matriz de comparação par a par para as alternativas dentro de um único critério.
        """
        scores = []
        if criterion_type == self.HB:
            scores = [9 if v == req_value else 5 if v > req_value else 1 for v in unique_values]
        elif criterion_type == self.NB:
            scores = [9 if v == req_value else 1 for v in unique_values]
        elif criterion_type == self.LB:
            scores = [9 if v == req_value else 5 if v < req_value else 1 for v in unique_values]
        
        scores_np = np.array(scores, dtype=float)
        
        # Evita divisão por zero se todos os scores forem zero, embora improvável com a lógica atual.
        # Retorna a matriz de comparação usando broadcasting.
        # O elemento [i, j] será score[i] / score[j].
        with np.errstate(divide='ignore', invalid='ignore'):
            matrix = scores_np[:, np.newaxis] / scores_np
        
        # Se houver uma divisão por zero (NaN), substitua por 1 (comparando consigo mesmo).
        matrix = np.nan_to_num(matrix, nan=1.0)
        return matrix

    def _calculate_weights(self, matrix: np.ndarray) -> np.ndarray:
        """
        Normaliza a matriz de comparação e calcula os pesos (vetor de prioridade).
        """
        # 1. Somar as colunas da matriz
        
        col_sums = matrix.sum(axis=0)
        
        # 2. Normalizar a matriz dividindo cada elemento pela soma de sua coluna
        # Adiciona uma pequena constante para evitar divisão por zero se uma coluna somar 0
        normalized_matrix = matrix / (col_sums + 1e-9)
        
        # 3. Calcular os pesos (vetor de prioridade) tirando a média das linhas da matriz normalizada
        weights = normalized_matrix.mean(axis=1)
        
        return weights

    def ranking_alternatives(self, db: List[Dict]) -> List[Dict]:
        """
        Calcula a pontuação final e o ranking de cada alternativa.
        """
        # 1. Calcular pesos dos critérios
        self.criteria_matrix = self._evaluate_criteria_matrix()
        criteria_weights = self._calculate_weights(self.criteria_matrix)
        
        # 2. Calcular pesos das alternativas para cada critério
        dict_pis_weights = {}
        for idx, criterion_info in enumerate(db):
            pi_name = criterion_info['pi']
            
            unique_values = sorted(list(set(criterion_info['valores'])))
            
            # Cria e calcula a matriz de comparação para as alternativas neste critério
            alternatives_matrix = self._evaluate_alternatives_matrix(
                unique_values,
                criterion_info['tipo'],
                self.req[pi_name]['valor']
            )
            
            # Calcula os pesos das alternativas para este critério
            alternatives_weights = self._calculate_weights(alternatives_matrix)
            
            dict_pis_weights[pi_name] = {
                'weight_pi': criteria_weights[idx],
                'weight_alternatives': dict(zip(unique_values, alternatives_weights))
            }
            
        # 3. Calcular a pontuação final de cada alternativa
        final_rank = []
        for alternative in self.alternatives:
            total_score = 0.0
            for criterion_name, criterion_value in alternative['criterions'].items():
                pi_data = dict_pis_weights.get(criterion_name)
                if not pi_data:
                    continue

                criterion_weight = pi_data['weight_pi']
                
                # Trata critérios com múltiplos valores (lógica original)
                if isinstance(criterion_value, list):
                    try:
                        # Se o valor desejado estiver na lista, concede o peso total do critério
                        if self.req[criterion_name]['valor'] in criterion_value:
                            total_score += criterion_weight
                    except (ValueError, KeyError):
                        # Se não encontrar, a pontuação para este critério é zero.
                        pass 
                else:
                    # Para valores únicos, multiplica o peso do critério pelo peso da alternativa
                    alternative_weight = pi_data['weight_alternatives'].get(criterion_value, 0.0)
                    total_score += criterion_weight * alternative_weight
            
            final_rank.append({'company': alternative['company'], 'pts': total_score})
            
        return final_rank

    def show_rank(self):
        """
        Executa o processo de AHP e imprime o ranking final das alternativas.
        """
        # Garante que o DB esteja na ordem correta
        organized_db = self.organize_db()
        
        
        ranks = self.ranking_alternatives(organized_db)
        
        # Ordena o ranking da maior pontuação para a menor
        ranks.sort(key=lambda item: item['pts'], reverse=True)
        
        print("Ranking Final das Alternativas:")
        for rank in ranks:
            # Formata a pontuação para melhor legibilidade
            print(f'{rank["company"]}: {rank["pts"]:.4f}')