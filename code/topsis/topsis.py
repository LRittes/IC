import numpy as np
from typing import List, Dict, Any

class Topsis:
    """
    Implementação do algoritmo TOPSIS que primeiro converte a matriz de decisão
    em notas de 1 a 9 baseadas na aderência aos valores da requisição.
    """

    def __init__(self, req: Dict[str, Any], alternatives: List[Dict[str, Any]], db: List[Dict[str, Any]], verbose: bool = False):
        # ... (O construtor e a validação inicial permanecem os mesmos) ...
        if not req:
            raise ValueError("O dicionário 'req' não pode estar vazio.")
        if not alternatives:
            raise ValueError("A lista 'alternatives' não pode estar vazia.")
        
        self.req = req
        self.alternatives = alternatives
        self.db = {item['pi']: item for item in db}
        self.verbose = verbose
        
        self.criteria_order = list(self.req.keys())
        self.alternative_names = [alt.get('company', f'Alternativa {i+1}') for i, alt in enumerate(self.alternatives)]

        # --- Pré-processamento e Preparação dos Dados para o TOPSIS ---
        self._calculate_weights()
        # MODIFICAÇÃO: A criação da matriz agora vem antes da determinação do tipo
        self._create_scoring_decision_matrix() 
        self._determine_criteria_type_post_scoring()
        
        # Atributos que serão calculados pelo algoritmo
        self.normalized_matrix = None
        self.weighted_matrix = None
        self.ideal_solution = None
        self.negative_ideal_solution = None
        self.distances_pos = None
        self.distances_neg = None
        self.scores = None
        self.ranking = None

    def _calculate_weights(self):
        # Este método não muda
        raw_weights = np.array([self.req[pi]['peso'] for pi in self.criteria_order], dtype=float)
        total_weight = np.sum(raw_weights)
        if total_weight == 0:
            raise ValueError("A soma dos pesos na requisição não pode ser zero.")
        self.weights = raw_weights / total_weight

    def _create_scoring_decision_matrix(self):
        """
        MODIFICADO: Cria a matriz de decisão convertendo os valores brutos
        em notas de 1 a 10 de acordo com as regras especificadas.
        """
        num_alternatives = len(self.alternatives)
        num_criteria = len(self.criteria_order)
        matrix = np.zeros((num_alternatives, num_criteria))

        for i, alt in enumerate(self.alternatives):
            for j, pi_name in enumerate(self.criteria_order):
                alt_criterions = alt['criterions']
                req_pi = self.req.get(pi_name)
                db_pi = self.db.get(pi_name)

                if req_pi is None or 'valor' not in req_pi:
                    raise ValueError(f"Critério '{pi_name}' na requisição precisa ter uma chave 'valor'.")
                
                alt_value = alt_criterions.get(pi_name)
                req_value = req_pi['valor']
                pi_type = db_pi['tipo']

                # Trata casos onde o valor da alternativa pode ser uma lista (ex: Memory)
                effective_alt_value = alt_value
                if isinstance(alt_value, list):
                    diffs = np.abs(np.array(alt_value) - req_value)
                    closest_index = np.argmin(diffs)
                    effective_alt_value = alt_value[closest_index]
                
                if isinstance(alt_value, list):
                    try:
                        auxCritList = alt.get('criterions').get(pi_name)
                        auxCritList[auxCritList.index(self.req.get(pi_name).get('valor'))]
                        
                        matrix[i, j] = 9
                    except:
                        matrix[i, j] = 1
                    finally:
                        continue
                                      
                # Aplica as regras de pontuação
                score = 0
                if pi_type == 'HB' or pi_type == 'NB':
                    if effective_alt_value == req_value:
                        score = 9
                    elif effective_alt_value < req_value:
                        score = 1
                    else:  # effective_alt_value > req_value
                        score = 5
                elif pi_type == 'LB':
                    if effective_alt_value == req_value:
                        score = 9
                    elif effective_alt_value > req_value: # Pior caso para custo
                        score = 1
                    else:  # effective_alt_value < req_value (Melhor caso para custo)
                        score = 5
                
                matrix[i, j] = score
        
        self.decision_matrix = matrix

    def _determine_criteria_type_post_scoring(self):
        """
        MODIFICADO: Após a conversão para notas, todos os critérios são de benefício ('max'),
        pois uma nota maior é sempre melhor.
        """
        num_criteria = len(self.criteria_order)
        # Cria um array de '1's, indicando que todos os critérios são 'max'
        self.criteria_type = np.ones(num_criteria, dtype=int)
    
    def _normalize(self):
        self.col_norms = np.linalg.norm(self.decision_matrix, axis=0)
        self.col_norms[self.col_norms == 0] = 1
        self.normalized_matrix = self.decision_matrix / self.col_norms
    
    def _weigh_matrix(self):
        self.weighted_matrix = self.normalized_matrix * self.weights
    
    def _find_ideal_solutions(self):
        self.ideal_solution = np.zeros(self.weighted_matrix.shape[1])
        self.negative_ideal_solution = np.zeros(self.weighted_matrix.shape[1])
        for j in range(self.weighted_matrix.shape[1]):
            if self.criteria_type[j] == 1:
                self.ideal_solution[j] = np.max(self.weighted_matrix[:, j])
                self.negative_ideal_solution[j] = np.min(self.weighted_matrix[:, j])
            else:
                self.ideal_solution[j] = np.min(self.weighted_matrix[:, j])
                self.negative_ideal_solution[j] = np.max(self.weighted_matrix[:, j])
    
    def _calculate_distances(self):
        self.distances_pos = np.sqrt(np.sum((self.weighted_matrix - self.ideal_solution)**2, axis=1))
        self.distances_neg = np.sqrt(np.sum((self.weighted_matrix - self.negative_ideal_solution)**2, axis=1))
    
    def _calculate_scores(self):
        total_distance = self.distances_pos + self.distances_neg
        total_distance[total_distance == 0] = np.finfo(float).eps
        self.scores = self.distances_neg / total_distance
    
    def _rank_alternatives(self):
        self.ranking = np.argsort(self.scores)[::-1]
    
    def _print_header(self, title):
        print("\n" + "="*60); print(f" {title.upper()} ".center(60, "=")); print("="*60)
    
    def _print_initial_data(self):
        self._print_header("Dados de Entrada e Configuração"); print("Critérios em ordem:", self.criteria_order); print("Alternativas:", self.alternative_names); print("Pesos normalizados:", np.round(self.weights, 4)); print("Tipos de critério (pós-transformação):", self.criteria_type)
    
    def _print_step_1_matrix(self):
        self._print_header("Passo 1: Matriz de Decisão (Notas de 1 a 10)"); print("Matriz convertida para notas baseadas na aderência à requisição."); print(self.decision_matrix)
    
    def _print_step_2_normalization(self):
        self._print_header("Passo 2: Normalização da Matriz"); print("Fórmula: rij = xij / sqrt(sum(xij^2)) para cada coluna j."); print("\nNorma Euclidiana de cada coluna:", np.round(self.col_norms, 4)); print("\nMatriz Normalizada:"); print(np.round(self.normalized_matrix, 4))
    
    def _print_step_3_weighting(self):
        self._print_header("Passo 3: Ponderação da Matriz Normalizada"); print("Fórmula: vij = wij * rij."); print("\nMatriz Ponderada:"); print(np.round(self.weighted_matrix, 4))
    
    def _print_step_4_ideal_solutions(self):
        self._print_header("Passo 4: Determinação das Soluções Ideais"); print("A+ (Ideal Positiva): Melhores valores (máximos)."); print("A- (Ideal Negativa): Piores valores (mínimos)."); print("\nSolução Ideal (A+):", np.round(self.ideal_solution, 4)); print("Solução Negativa (A-):", np.round(self.negative_ideal_solution, 4))
    
    def _print_step_5_distances(self):
        self._print_header("Passo 5: Cálculo das Distâncias Euclidianas"); print("S+ : Distância para A+ | S- : Distância para A-."); 
        for i, name in enumerate(self.alternative_names): print(f"\n{name}:\n  - Distância S+: {self.distances_pos[i]:.4f}\n  - Distância S-: {self.distances_neg[i]:.4f}")
    
    def _print_step_6_scores(self):
        self._print_header("Passo 6: Cálculo da Pontuação de Proximidade Relativa (C*)"); print("Fórmula: Ci* = S- / (S+ + S-).");
        for i, name in enumerate(self.alternative_names): print(f"- Pontuação {name}: {self.scores[i]:.4f}")
    
    def _print_step_7_ranking(self):
        self._print_header("Passo 7: Ranking Final"); print("Ordenação da maior para a menor pontuação C*."); ranked_names = [self.alternative_names[i] for i in self.ranking];
        for i, name in enumerate(ranked_names): rank_idx = self.ranking[i]; print(f"{i+1}º Lugar: {name} (Pontuação: {self.scores[rank_idx]:.4f})")
    
    def evaluate(self):
        if self.verbose: self._print_initial_data(); self._print_step_1_matrix()
        self._normalize(); 
        if self.verbose: self._print_step_2_normalization()
        self._weigh_matrix(); 
        if self.verbose: self._print_step_3_weighting()
        self._find_ideal_solutions(); 
        if self.verbose: self._print_step_4_ideal_solutions()
        self._calculate_distances(); 
        if self.verbose: self._print_step_5_distances()
        self._calculate_scores(); 
        if self.verbose: self._print_step_6_scores()
        self._rank_alternatives(); 
        if self.verbose: self._print_step_7_ranking()
        ranked_names = [self.alternative_names[i] for i in self.ranking]; 
        return self.scores, self.ranking, ranked_names