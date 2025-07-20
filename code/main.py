import os

from utils import *


# salvar acuracia do mse de cada req em metrics 

# gerar gráficos

# pegar os dados dos dados conhecido e salvar suas métricas

# runAHPTests(KNOWSREQS[0],{'value':alternativesKnownValue,'position': alternativeKnownPosition})
# saveKnownTestCase()
# generateAlternatives(DB,alternativesKnownValue,0,1)

# if not os.path.exists('./data/requisitions.yml'):
generateSampleTest(DB, alternativesKnownValue)
    
for idFull, crit in getAllRequisitions().items():
    id, req = idFull[3:], crit['criterions']
    for amount in NUM_ALTERNATIVES:
        # if int(id) < 7 and amount > 6:
        #     continue
        alters = getAlternatives(id,amount)

        metrics  = runAHPTests(req,alters)
        # print(alters)

        # saveMetrics(id,amount, metrics)



req = {
      '1M+ requisicao': {
        'peso': 9,
        'valor': 0.2
      },
      'Arredondamento da duracao':{
        'peso': 9,
        'valor': 1
      },
      'Cold Starts':{
        'peso': 9,
        'valor': 1
      },
      'Execution Time':{
        'peso': 9,
        'valor': 5
      },
      'Memory':{
        'peso': 1,
        'valor': 128
      }
}

alternatives =[
    {'company':'company1',
         'criterions':{
            '1M+ requisicao':  0.2,
            'Arredondamento da duracao': 1,
            'Cold Starts': 1,
            'Execution Time': 5,
            'Memory': [128, 256, 384, 512, 640, 768]
             }
         },
    {'company':'company2',
         'criterions':{
            '1M+ requisicao':  0.2,
            'Arredondamento da duracao': 100,
            'Cold Starts': 1,
            'Execution Time': 5,
            'Memory': [128, 256, 384, 512, 640, 768]
             }
         },
    {'company':'company3',
         'criterions':{
            '1M+ requisicao':  0.4,
            'Arredondamento da duracao': 100,
            'Cold Starts': 1,
            'Execution Time': 5,
            'Memory': [128, 256, 384, 512, 640, 768]
             }
         },
    {'company':'company4',
         'criterions':{
            '1M+ requisicao':  0.4,
            'Arredondamento da duracao': 100,
            'Cold Starts': 1,
            'Execution Time': 9,
            'Memory': [128, 256, 384, 512, 640, 768]
             }
         },
    {'company':'company5',
         'criterions':{
            '1M+ requisicao':  0.4,
            'Arredondamento da duracao': 100,
            'Cold Starts': 2,
            'Execution Time': 9,
            'Memory': [128, 256, 384, 512, 640, 768]
             }
         },
]

# alternativesPos =[
#     {'company':'company1',
#          'criterions':{
#             '1M+ requisicaoPos':  0,
#             'Arredondamento da duracaoPos': 0,
#             'Cold StartsPos': 0,
#             'Execution TimePos': 0,
#             'MemoryPos': [128, 256, 384, 512, 640, 768]
#              }
#          },
#     {'company':'company2',
#          'criterions':{
#             '1M+ requisicaoPos':  0,
#             'Arredondamento da duracaoPos': 1,
#             'Cold StartsPos': 0,
#             'Execution TimePos': 0,
#             'MemoryPos': [128, 256, 384, 512, 640, 768]
#              }
#          },
#     {'company':'company3',
#          'criterions':{
#             '1M+ requisicaoPos':  1,
#             'Arredondamento da duracaoPos': 1,
#             'Cold StartsPos': 0,
#             'Execution TimePos': 0,
#             'MemoryPos': [128, 256, 384, 512, 640, 768]
#              }
#          },
#     {'company':'company4',
#          'criterions':{
#             '1M+ requisicaoPos':  1,
#             'Arredondamento da duracaoPos': 1,
#             'Cold StartsPos': 0,
#             'Execution TimePos': 1,
#             'MemoryPos': [128, 256, 384, 512, 640, 768]
#              }
#          },
#     {'company':'company5',
#          'criterions':{
#             '1M+ requisicaoPos':  1,
#             'Arredondamento da duracaoPos': 1,
#             'Cold StartsPos': 1,
#             'Execution TimePos': 1,
#             'MemoryPos': [128, 256, 384, 512, 640, 768]
#              }
#          },
# ]

# ahpI = ahpImp.AHP(req, DB, alternatives)
# rankingAhpI = ahpI.ranking_alternatives(ahpI.organize_db())
# rankingAhpI.sort(key=ahpI.returnPtsFromList,reverse=True)
# ahpI.show_rank()

# # rankingAhpL = ahpLib.rankingAlternatives(req,DB,alternativesPos)
# # rankingAhpL.sort(key=ahpI.returnPtsFromList,reverse=True)
# print('-'*70)
# ahpLib.showRanking(req,DB,alternativesPos)
  
