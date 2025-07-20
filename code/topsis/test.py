import numpy as np

class Topsis:
    """
    Implementação do algoritmo TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution)
    para análise de decisão multicritério.

    Atributos:
    ----------
    decision_matrix : np.ndarray
        Matriz (m x n) com as alternativas nas linhas e os critérios nas colunas.
    weights : np.ndarray
        Array (1 x n) com os pesos de cada critério. A soma dos pesos deve ser 1.
    criteria_type : np.ndarray
        Array (1 x n) indicando o tipo de cada critério: 1 para benefício (quanto maior, melhor)
        e -1 para custo (quanto menor, melhor).
    """

    def __init__(self, decision_matrix: np.ndarray, alternatives: list):
        """
        Inicializa a classe Topsis com os dados de entrada.

        Parâmetros:
        -----------
        decision_matrix : np.ndarray ou list[list]
            A matriz de decisão (m alternativas x n critérios).
        weights : list
            A lista de pesos para cada critério.
        criteria_type : list
            Lista de strings ('max' para benefício, 'min' para custo) para cada critério.
        """
        # --- Validação e Conversão dos Dados de Entrada ---
        self.decision_matrix = np.array(decision_matrix, dtype=float)
        self.alternatives = np.array(alternatives)
        
        if self.decision_matrix.shape[1] != len(self.weights):
            raise ValueError("O número de colunas da matriz de decisão deve ser igual ao número de pesos.")
        
        if self.decision_matrix.shape[1] != len(criteria_type):
            raise ValueError("O número de colunas da matriz de decisão deve ser igual ao número de tipos de critério.")
        
        if not np.isclose(np.sum(self.weights), 1.0):
            raise ValueError("A soma dos pesos dos critérios deve ser igual a 1.")

        # Converte 'max'/'min' para 1/-1 para facilitar os cálculos
        self.criteria_type = np.array([1 if c.lower() == 'max' else -1 for c in criteria_type])

        # Atributos que serão calculados
        self.normalized_matrix = None
        self.weighted_matrix = None
        self.ideal_solution = None
        self.negative_ideal_solution = None
        self.distances_pos = None
        self.distances_neg = None
        self.scores = None
        self.ranking = None

    def _normalize(self):
        """
        Passo 2: Normaliza a matriz de decisão usando a normalização vetorial.
        """
        # Calcula a norma de cada coluna (critério)
        col_norms = np.linalg.norm(self.decision_matrix, axis=0)
        # Evita divisão por zero para colunas com todos os valores iguais a 0
        col_norms[col_norms == 0] = 1
        self.normalized_matrix = self.decision_matrix / col_norms

    def _weigh_matrix(self):
        """
        Passo 3: Multiplica a matriz normalizada pelos pesos dos critérios.
        """
        self.weighted_matrix = self.normalized_matrix * self.weights

    def _find_ideal_solutions(self):
        """
        Passo 4: Encontra a solução ideal positiva (melhor) e negativa (pior).
        """
        self.ideal_solution = np.zeros(self.weighted_matrix.shape[1])
        self.negative_ideal_solution = np.zeros(self.weighted_matrix.shape[1])

        for j in range(self.weighted_matrix.shape[1]):
            if self.criteria_type[j] == 1:  # Critério de benefício (max)
                self.ideal_solution[j] = np.max(self.weighted_matrix[:, j])
                self.negative_ideal_solution[j] = np.min(self.weighted_matrix[:, j])
            else:  # Critério de custo (min)
                self.ideal_solution[j] = np.min(self.weighted_matrix[:, j])
                self.negative_ideal_solution[j] = np.max(self.weighted_matrix[:, j])

    def _calculate_distances(self):
        """
        Passo 5: Calcula a distância euclidiana de cada alternativa para as soluções ideais.
        """
        # Distância para a solução ideal positiva (S+)
        self.distances_pos = np.sqrt(np.sum((self.weighted_matrix - self.ideal_solution)**2, axis=1))
        # Distância para a solução ideal negativa (S-)
        self.distances_neg = np.sqrt(np.sum((self.weighted_matrix - self.negative_ideal_solution)**2, axis=1))

    def _calculate_scores(self):
        """
        Passo 6: Calcula a pontuação de proximidade relativa para cada alternativa.
        """
        # Evita divisão por zero
        total_distance = self.distances_pos + self.distances_neg
        total_distance[total_distance == 0] = np.finfo(float).eps  # Adiciona um valor pequeno se a soma for zero
        
        self.scores = self.distances_neg / total_distance

    def _rank_alternatives(self):
        """
        Passo 7: Rankeia as alternativas com base em suas pontuações (do maior para o menor).
        """
        # argsort retorna os índices que ordenariam o array. [::-1] inverte para ordem decrescente.
        self.ranking = np.argsort(self.scores)[::-1]
        
    def evaluate(self) -> tuple[np.ndarray, np.ndarray]:
        """
        Executa o fluxo completo do algoritmo TOPSIS e retorna as pontuações e o ranking.

        Retorna:
        --------
        tuple:
            - scores (np.ndarray): A pontuação de proximidade relativa para cada alternativa (índice 0 = alternativa 0).
            - ranking (np.ndarray): Os índices das alternativas ordenados do melhor para o pior.
        """
        if self.scores is not None:
            return self.scores, self.ranking
            
        self._normalize()
        self._weigh_matrix()
        self._find_ideal_solutions()
        self._calculate_distances()
        self._calculate_scores()
        self._rank_alternatives()
        
        return self.scores, self.ranking

from utils import *

# --- Exemplo de Uso ---
if __name__ == '__main__':
    # Problema: Escolher o melhor carro entre 4 alternativas.
    # Alternativas: [Carro A, Carro B, Carro C, Carro D]
    # Critérios:
    # 1. Preço (Custo)
    # 2. Consumo de Combustível (Custo) - km/l, então será benefício
    # 3. Conforto (Benefício) - nota de 1 a 10
    # 4. Segurança (Benefício) - nota de 1 a 10

    # Matriz de Decisão (4 alternativas x 4 critérios)
    decision_matrix = np.array([
        # Preço, Consumo, Conforto, Segurança
        [25000, 10,  8, 9],  # Carro A
        [22000, 12,  7, 8],  # Carro B
        [30000, 15,  9, 10], # Carro C
        [27000, 11,  8, 8]   # Carro D
    ])

    # Pesos dos critérios (devem somar 1)
    # Ex: Preço (40%), Consumo (20%), Conforto (25%), Segurança (15%)
    weights = [0.40, 0.20, 0.25, 0.15]

    # Tipos de critério
    # Preço é 'min' (custo), os outros são 'max' (benefício)
    criteria_type = ['min', 'max', 'max', 'max']
    
    # alts = []
    # for alt in alternativesKnownValue:
    #     altAux = alt['criterions']
    #     critsAlt = []
        
    #     for key, value in altAux.items():
    #         if type(value) == list:
    #             reqValue = req[key]['valor']
    #             if reqValue in value:
    #                 critsAlt.append( reqValue)
    #             else:
    #                 critsAlt.append(0)
    #         else:
    #             critsAlt.append(value)
        
    #     critsAlt = np.array(critsAlt)
    #     alts.append(critsAlt)
    
    # alts = np.array(alts)
    # print(alts)
    
    # # Matriz de decisão
    # decision_matrix = alts
        
    # # Pesos dos critérios (soma deve ser 1)
    
    # pis = []
    # for key, value in req.items():
    #     pis.append((key, value['valor'], value['peso']))

    # pis = np.array(pis)
    # pesosNorm = pis[:, 2].astype(float)
    # pesosNorm = pesosNorm / pesosNorm.sum()
    
    # # Tipos de critérios ('min' para custo, 'max' para os outros critérios)
    # criteria_types = []
    # for row in DB:
    #     if row['tipo'] == 'LB':
    #         criteria_types.append('min')
    #     else:
    #         criteria_types.append('max')

    # Criar e executar a análise TOPSIS
    topsis_analyzer = Topsis(decision_matrix, weights, criteria_type)
    scores, ranking = topsis_analyzer.evaluate()
    
    alternative_names = ["Carro A", "Carro B", "Carro C", "Carro D"]
    
    print("--- Análise TOPSIS para Escolha de Carro ---")
    print("\nMatriz de Decisão:")
    print(decision_matrix)
    print("\nPesos dos Critérios:", weights)
    print("Tipos dos Critérios:", criteria_type)

    print("\n--- Resultados ---")
    for i, alt_name in enumerate(alternative_names):
        print(f"Pontuação da Alternativa '{alt_name}': {scores[i]:.4f}")

    print("\nRanking Final (do melhor para o pior):")
    for i, rank_idx in enumerate(ranking):
        print(f"{i+1}º Lugar: {alternative_names[rank_idx]} (Índice da Alternativa: {rank_idx}) com pontuação {scores[rank_idx]:.4f}")