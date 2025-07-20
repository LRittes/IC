import numpy as np
import sys
import os

# Caminho do diretório pai
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from topsis import topsis
from test import Topsis

from const import *
from utils import *

# alts = alternativesKnownValue
# print(alts)

# # Matriz de decisão: [Custo, Qualidade, Prazo]
# alternativas = [
#     [25000, 7, 30],
#     [28000, 9, 25],
#     [26000, 6, 20],
#     [22000, 8, 35]
# ]

# pesos = [0.3, 0.4, 0.3]  # Importância relativa dos critérios
# criterios = ['min', 'max', 'min']  # Custo, benefício, custo

# scores, ranking = topsis(alternativas, pesos, criterios)

# print("Scores:", scores)
# print("Ranking (melhor para pior):", ranking)


# Exemplo de uso
if __name__ == "__main__":
    # Exemplo: Seleção de fornecedores com 4 alternativas e 5 critérios
    # Critérios: Custo, Qualidade, Entrega, Serviço, Reputação
    # Alternativas: Fornecedor A, B, C e D

    req = KNOWSREQS[0] 
    
    
    # print(decision_matrix)
    # print(pesosNorm)
    # print(criteria_types)
    
    # Executar TOPSIS
    # similarity, ranking = topsis(decision_matrix, pesosNorm, criteria_types)
    
    # # decision_matrix = np.array([
    # #     [7, 5.5, 6, 8],    # Fornecedor A
    # #     [8, 5, 7, 8],    # Fornecedor B
    # #     [8, 7.2, 8, 9],    # Fornecedor C
    # #     [ 6, 4.3, 5, 6],     # Fornecedor D
    # #     [ 7, 4, 8, 5],     # Fornecedor D
    # #     [ 9, 6.5, 8, 9],     # Fornecedor D
    # #     [ 9, 8.2, 7, 9],     # Fornecedor D
    # #     [ 5, 4.9, 7, 8],     # Fornecedor D
    # #     [ 8, 7.5, 5, 9],     # Fornecedor D
        
    # # ])
    
    # # # Pesos dos critérios (soma deve ser 1)
    # # weights = np.array([0.25, 0.3, 0.2, 0.25])
    
    # # # Tipos de critérios ('min' para custo, 'max' para os outros critérios)
    # # criteria_types = ['max', 'min', 'max', 'max']
    
    # # Executar TOPSIS
    # # similarity, ranking = topsis(decision_matrix, weights, criteria_types)

    # # Exibir resultados
    # print("Pontuações de similaridade:", similarity)
    # print("Ranking (do melhor para o pior):", ranking)
    # print("\nClassificação dos fornecedores:")
    # for i, idx in enumerate(ranking):
    #     print(f"{i+1}º lugar: Fornecedor {chr(65+idx)} com pontuação {similarity[idx]:.4f}")
        
    topsis_analyzer = Topsis(decision_matrix, pesosNorm, criteria_types)
    scores, ranking = topsis_analyzer.evaluate()
    

    print("\nRanking Final (do melhor para o pior):")
    for i, rank_idx in enumerate(ranking):
        print(f"(Índice da Alternativa: {rank_idx}) com pontuação {scores[rank_idx]:.4f}")