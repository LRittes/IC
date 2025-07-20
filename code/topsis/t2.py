# import numpy as np
# from typing import List, Dict, Any

# class Topsis:
#     """
#     Implementação do algoritmo TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution)
#     adaptada para processar dados estruturados de requisições, alternativas e um banco de dados de critérios.
#     """

#     def __init__(self, req: Dict[str, Any], alternatives: List[Dict[str, Any]], db: List[Dict[str, Any]]):
#         """
#         Inicializa a classe Topsis com os dados de entrada estruturados.

#         Parâmetros:
#         -----------
#         req : dict
#             Dicionário da requisição do usuário, contendo os critérios (PIs) desejados,
#             seus pesos e valores ideais. Ex: {'PI': {'peso': 9, 'valor': 100}}
#         alternatives : list[dict]
#             Lista de dicionários, onde cada um representa uma alternativa (empresa) com seus
#             respectivos valores para cada critério.
#         db : list[dict]
#             "Banco de dados" de critérios, contendo o nome ('pi'), o tipo ('HB', 'LB', 'NB')
#             e os valores possíveis.
#         """
#         # --- Validação e Armazenamento dos Dados de Entrada ---
#         if not req:
#             raise ValueError("O dicionário 'req' não pode estar vazio.")
#         if not alternatives:
#             raise ValueError("A lista 'alternatives' não pode estar vazia.")
        
#         self.req = req
#         self.alternatives = alternatives
#         self.db = {item['pi']: item for item in db} # Converte a lista de DB para um dict para busca rápida
        
#         self.criteria_order = list(self.req.keys())
#         self.alternative_names = [alt.get('company', f'Alternativa {i+1}') for i, alt in enumerate(self.alternatives)]

#         # --- Pré-processamento e Preparação dos Dados para o TOPSIS ---
#         self._calculate_weights()
#         self._determine_criteria_type()
#         self._create_decision_matrix()
        
#         # Atributos que serão calculados pelo algoritmo
#         self.normalized_matrix = None
#         self.weighted_matrix = None
#         self.ideal_solution = None
#         self.negative_ideal_solution = None
#         self.distances_pos = None
#         self.distances_neg = None
#         self.scores = None
#         self.ranking = None

#     def _calculate_weights(self):
#         """
#         Calcula os pesos normalizados a partir dos pesos brutos da requisição.
#         A soma final dos pesos será 1.
#         """
#         raw_weights = np.array([self.req[pi]['peso'] for pi in self.criteria_order], dtype=float)
#         total_weight = np.sum(raw_weights)
        
#         if total_weight == 0:
#             raise ValueError("A soma dos pesos na requisição não pode ser zero.")
            
#         self.weights = raw_weights / total_weight

#     def _determine_criteria_type(self):
#         """
#         Determina se cada critério é de 'max' (benefício) ou 'min' (custo)
#         com base no 'tipo' definido no DB.
        
#         - HB (Higher is Better) -> 'max'
#         - LB (Lower is Better) -> 'min'
#         - NB (Nominal is Best) -> 'min' (pois será transformado em uma medida de diferença)
#         """
#         criteria_map = {'HB': 'max', 'LB': 'min', 'NB': 'max'}
#         types = []
#         for pi in self.criteria_order:
#             pi_info = self.db.get(pi)
#             if not pi_info:
#                 raise ValueError(f"O critério '{pi}' da requisição não foi encontrado no DB.")
            
#             pi_type = pi_info.get('tipo')
#             if pi_type not in criteria_map:
#                 raise ValueError(f"Tipo de critério '{pi_type}' para '{pi}' é inválido.")
            
#             types.append(criteria_map[pi_type])
            
#         # Converte para array numpy para uso nos cálculos
#         self.criteria_type = np.array([1 if c == 'max' else -1 for c in types])

#     def _create_decision_matrix(self):
#         """
#         Cria a matriz de decisão (m x n) a partir dos dados das alternativas,
#         tratando os critérios 'NB' (Nominal is Best) de forma especial.
#         """
#         num_alternatives = len(self.alternatives)
#         num_criteria = len(self.criteria_order)
#         matrix = np.zeros((num_alternatives, num_criteria))

#         for i, alt in enumerate(self.alternatives):
#             for j, pi_name in enumerate(self.criteria_order):
#                 alt_value = alt['criterions'].get(pi_name)
#                 pi_info = self.db.get(pi_name)
                
#                 if alt_value is None:
#                     raise ValueError(f"Alternativa '{self.alternative_names[i]}' não possui o critério '{pi_name}'.")

#                 if isinstance(alt_value, list):
#                     try:
#                         auxCritList = alt.get('criterions').get(pi_name)
#                         valueReqInList = auxCritList[auxCritList.index(self.req.get(pi_name).get('valor'))]
                        
#                         matrix[i, j] = valueReqInList
#                     except:
#                         matrix[i, j] = 0
                   
#                 else:
#                     matrix[i, j] = alt_value
#         self.decision_matrix = matrix

#     def _normalize(self):
#         """Passo 2: Normaliza a matriz de decisão."""
#         col_norms = np.linalg.norm(self.decision_matrix, axis=0)
#         col_norms[col_norms == 0] = 1
#         self.normalized_matrix = self.decision_matrix / col_norms

#     def _weigh_matrix(self):
#         """Passo 3: Pondera a matriz normalizada."""
#         self.weighted_matrix = self.normalized_matrix * self.weights

#     def _find_ideal_solutions(self):
#         """Passo 4: Encontra as soluções ideais positiva e negativa."""
#         self.ideal_solution = np.zeros(self.weighted_matrix.shape[1])
#         self.negative_ideal_solution = np.zeros(self.weighted_matrix.shape[1])

#         for j in range(self.weighted_matrix.shape[1]):
#             if self.criteria_type[j] == 1:  # Benefício (max)
#                 self.ideal_solution[j] = np.max(self.weighted_matrix[:, j])
#                 self.negative_ideal_solution[j] = np.min(self.weighted_matrix[:, j])
#             else:  # Custo (min)
#                 self.ideal_solution[j] = np.min(self.weighted_matrix[:, j])
#                 self.negative_ideal_solution[j] = np.max(self.weighted_matrix[:, j])

#     def _calculate_distances(self):
#         """Passo 5: Calcula as distâncias euclidianas."""
#         self.distances_pos = np.sqrt(np.sum((self.weighted_matrix - self.ideal_solution)**2, axis=1))
#         self.distances_neg = np.sqrt(np.sum((self.weighted_matrix - self.negative_ideal_solution)**2, axis=1))

#     def _calculate_scores(self):
#         """Passo 6: Calcula a pontuação de proximidade relativa."""
#         total_distance = self.distances_pos + self.distances_neg
#         total_distance[total_distance == 0] = np.finfo(float).eps
#         self.scores = self.distances_neg / total_distance

#     def _rank_alternatives(self):
#         """Passo 7: Rankeia as alternativas."""
#         self.ranking = np.argsort(self.scores)[::-1]
        
#     def evaluate(self) -> tuple[np.ndarray, np.ndarray, list]:
#         """
#         Executa o fluxo completo do algoritmo TOPSIS.

#         Retorna:
#         --------
#         tuple:
#             - scores (np.ndarray): A pontuação final para cada alternativa.
#             - ranking (np.ndarray): Os índices das alternativas ordenados do melhor para o pior.
#             - names (list): Os nomes das alternativas na ordem do ranking.
#         """
#         if self.scores is not None:
#             ranked_names = [self.alternative_names[i] for i in self.ranking]
#             return self.scores, self.ranking, ranked_names
            
#         self._normalize()
#         self._weigh_matrix()
#         self._find_ideal_solutions()
#         self._calculate_distances()
#         self._calculate_scores()
#         self._rank_alternatives()
        
#         ranked_names = [self.alternative_names[i] for i in self.ranking]
        
#         return self.scores, self.ranking, ranked_names

from topsis import Topsis

# --- Exemplo de Uso com os Dados Fornecidos ---
if __name__ == '__main__':
    # 1. Requisição do Usuário
    req = {
      '1M+ requisicao': { 'peso': 9, 'valor': 0.2 },
      'Arredondamento da duracao':{ 'peso': 8, 'valor': 1 },
      'Cold Starts':{ 'peso': 7, 'valor': 1 },
      'Execution Time':{ 'peso': 6, 'valor': 5 },
      'Memory':{ 'peso': 1, 'valor': 128 }
    }

    # 2. Alternativas Disponíveis
    alternatives =[
        {'company':'company1', 'criterions':{ '1M+ requisicao': 0.2, 'Arredondamento da duracao': 1, 'Cold Starts': 1, 'Execution Time': 5, 'Memory': [128, 256, 384, 512] }},
        {'company':'company2', 'criterions':{ '1M+ requisicao': 0.2, 'Arredondamento da duracao': 100, 'Cold Starts': 1, 'Execution Time': 5, 'Memory': [128, 256, 384, 512] }},
        {'company':'company3', 'criterions':{ '1M+ requisicao': 0.4, 'Arredondamento da duracao': 100, 'Cold Starts': 1, 'Execution Time': 5, 'Memory': [128, 256, 384, 512] }},
        {'company':'company4', 'criterions':{ '1M+ requisicao': 0.4, 'Arredondamento da duracao': 100, 'Cold Starts': 1, 'Execution Time': 9, 'Memory': [ 256, 384, 512] }},
        {'company':'company5', 'criterions':{ '1M+ requisicao': 0.4, 'Arredondamento da duracao': 100, 'Cold Starts': 2, 'Execution Time': 9, 'Memory': [128,256, 384, 512] }},
    ]

    # 3. Banco de Dados de Critérios (PIs)
    DB = [
        {'pi': 'Arredondamento da duracao', 'tipo': 'LB', 'valores': [1, 100]},
        {'pi': '1M+ requisicao', 'tipo': 'LB', 'valores': [0.20, 0.40]},
        {'pi': 'Cold Starts', 'tipo': 'LB', 'valores': [1, 2, 5]},
        {'pi': 'Memory', 'tipo': 'NB', 'valores': [128, 256, 384, 512]},
        {'pi': 'Execution Time', 'tipo': 'LB', 'valores': [5, 9, 15, 30]}
    ]

    # --- Execução da Análise ---
    try:
        topsis_analyzer = Topsis(req, alternatives, DB)
        
        # Dados pré-processados para verificação
        # print("--- Dados Pré-processados para TOPSIS ---")
        # print("\nOrdem dos Critérios:", topsis_analyzer.criteria_order)
        # print("\nPesos Normalizados:", np.round(topsis_analyzer.weights, 4))
        # print("\nTipos de Critério (1=max, -1=min):", topsis_analyzer.criteria_type)
        # print("\nMatriz de Decisão Gerada:")
        # print(topsis_analyzer.decision_matrix)
        
        # Executar a avaliação
        scores, ranking, ranked_names = topsis_analyzer.evaluate()
        
        # print("\n\n--- Resultados da Análise TOPSIS ---")
        # print("\nPontuações Finais (quanto maior, melhor):")
        # for i, name in enumerate(topsis_analyzer.alternative_names):
        #     print(f"- {name}: {scores[i]:.4f}")

        # print("\nRanking Final (do melhor para o pior):")
        for i, name in enumerate(ranked_names):
            rank_idx = ranking[i]
            print(f"{name}:  {scores[rank_idx]:.4f}")

    except ValueError as e:
        print(f"Erro ao processar dados: {e}")