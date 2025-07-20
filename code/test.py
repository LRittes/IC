from ahp_implement_v2.ahp import AHP as AHPV2
from ahp_implement.ahp import AHP as AHPV1
from topsis.topsis import Topsis

from const import *
from utils import *
import time

# start_time1 = time.perf_counter()
# ahpI = ahpImp.AHP(KNOWSREQS[0], DB, alternativesKnownValue)
# end_time1 = time.perf_counter()
# # ahpI.show_rank()


# start_time2 = time.perf_counter()
# ahpI2 = ahpImp2.AHP(KNOWSREQS[0], DB, alternativesKnownValue)
# end_time2 = time.perf_counter()

# # ahpI2.show_rank()


# execution_time1 = end_time1 - start_time1
# execution_time2 = end_time2 - start_time2

# print(f"O programa levou {execution_time1} segundos para executar.")
# print(f"O programa levou {execution_time2} segundos para executar.")

for idFull, crit in getAllRequisitions(True).items():
    id, req = idFull[3:], crit['criterions']
    # for amount in NUM_ALTERNATIVES:
    if int(id) < 15:
        continue
    # print(req)
    alters = getAlternatives(id,10, True)
    # ahpI = AHPV2(req, DB, alters['value'])
    # ahpI.show_rank()
    
    # print('-'*70)
    
    topsis_analyzer = Topsis(req, alters['value'], DB)
    scores, ranking, ranked_names = topsis_analyzer.evaluate()
    for i, name in enumerate(ranked_names):
            rank_idx = ranking[i]
            print(f"{name}:  {scores[rank_idx]:.4f}")
    
    
    # ahpIV1 = AHPV1(req, DB, alters['value'])
    # ahpIV1.show_rank()

    
    
        # metrics  = runAHPTests(req,alters)