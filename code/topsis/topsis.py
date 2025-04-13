import numpy as np

def topsis(matrix, weights, criteria):
    """
    matrix: matriz de decisão (alternativas x critérios)
    weights: pesos dos critérios (lista ou array)
    criteria: lista com 'max' (benefício) ou 'min' (custo) para cada critério
    """
    matrix = np.array(matrix, dtype=float)
    weights = np.array(weights, dtype=float)

    # Etapa 1: Normalização
    norm_matrix = matrix / np.sqrt((matrix ** 2).sum(axis=0))

    # Etapa 2: Matriz ponderada
    weighted_matrix = norm_matrix * weights

    # Etapa 3: Soluções ideal positiva e negativa
    ideal_positive = np.max(weighted_matrix, axis=0) * (np.array(criteria) == 'max') + \
                     np.min(weighted_matrix, axis=0) * (np.array(criteria) == 'min')
    
    ideal_negative = np.min(weighted_matrix, axis=0) * (np.array(criteria) == 'max') + \
                     np.max(weighted_matrix, axis=0) * (np.array(criteria) == 'min')

    # Etapa 4: Distância às soluções ideais
    dist_pos = np.linalg.norm(weighted_matrix - ideal_positive, axis=1)
    dist_neg = np.linalg.norm(weighted_matrix - ideal_negative, axis=1)

    # Etapa 5: Escore de similaridade relativa
    score = dist_neg / (dist_pos + dist_neg)

    return score, np.argsort(score)[::-1]  # Retorna escore e ranking (maior = melhor)

