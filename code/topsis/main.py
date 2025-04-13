from topsis import topsis
import numpy as np
import sys
import os

# Caminho do diretório pai
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from const import *



req = KNOWSREQS[0] 
pis = []
for key, value in req.items():
    pis.append((key, value['valor'], value['peso']))

pis = np.array(pis)
pesosNorm = pis[:, 2].astype(float)
pesosNorm = pesosNorm / pesosNorm.sum()


alts = alternativesKnownValue
print(alts)

# Matriz de decisão: [Custo, Qualidade, Prazo]
alternativas = [
    [25000, 7, 30],
    [28000, 9, 25],
    [26000, 6, 20],
    [22000, 8, 35]
]

pesos = [0.3, 0.4, 0.3]  # Importância relativa dos critérios
criterios = ['min', 'max', 'min']  # Custo, benefício, custo

# scores, ranking = topsis(alternativas, pesos, criterios)

# print("Scores:", scores)
# print("Ranking (melhor para pior):", ranking)