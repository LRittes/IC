NUM_TEST = 1
NUM_ALTERNATIVES = [5]
HB = 'HB'
LB = 'LB'
NB = 'NB'

dataDir = 'data/'
filenameReq = 'requisitions.yml'
reqFilePath = dataDir + filenameReq
dataKnowDir = 'known_data/'
filenameKnownReq = 'knowns_requisitions.yml'
knownReqFilePath = dataKnowDir + filenameKnownReq

metricsDir = 'metrics/'

alternativesDir = 'alternatives/'
dirPathAlters = dataDir + alternativesDir
dirPathKnownAlters = dataKnowDir + alternativesDir
positionDir = 'position/'
valueDir = 'value/'

graphDir = 'graph/'

RANKINGTEST = ['company0','company1','company2','company3','company4']

DB = [
        {
            'pi': 'tempo de computacao free',
            'tipo': 'HB',
            'valores': [400000]
        },
        {
            'pi': '1GB/segundo +',
            'tipo': 'LB',
            'valores': [2.5e-06,1.6e-05]
        },
        {
            'pi': 'Arredondamento da duracao',
            'tipo': 'LB',
            'valores': [1, 100]
        },
        {
            'pi': 'Requisicao free/mes',
            'tipo': 'HB',
            'valores': [1000000, 2000000]
        },
        {
            'pi': '1M+ requisicao',
            'tipo': 'LB',
            'valores': [0.20, 0.40]
        },
        {
            'pi': 'Scalability',
            'tipo': 'HB',
            'valores': [1]
        },
        {
            'pi': 'Concurrency',
            'tipo': 'HB',
            'valores': [1000,1001]
        },
        {
            'pi': 'Cold Starts',
            'tipo': 'LB',
            'valores': [1, 2, 5]
        },
        {
            'pi': 'Memory',
            'tipo': 'NB',
            'valores': [128, 256, 384, 512, 640, 768, 896, 1024, 1152, 1280, 1408, 1536, 1664, 1792, 1920, 2048, 2176, 2304, 2432, 2560, 2688, 2816, 2944, 3072, 3200, 3328, 3456, 3584, 3712, 3840, 3968, 4096, 4224, 4352, 4480, 4608, 4736, 4864, 4992, 5120, 5248, 5376, 5504, 5632, 5760, 5888, 6016, 6144, 6272, 6400, 6528, 6656, 6784, 6912, 7040, 7168, 7296, 7424, 7552, 7680, 7808, 7936, 8064, 8192, 8320, 8448, 8576, 8704, 8832, 8960, 9088, 9216, 9344, 9472, 9600, 9728, 9856, 9984, 10112, 10240, 10368, 10496, 10624, 10752, 10880, 11008, 11136, 11264, 11392, 11520, 11648, 11776, 11904, 12032, 12160, 12288, 12416, 12544, 12672, 12800, 12928, 13056, 13184, 13312, 13440, 13568, 13696, 13824, 13952, 14080]
        },
        {
            'pi': 'Execution Time',
            'tipo': 'HB',
            'valores': [5, 9, 15, 30]
        },
        {
            'pi': 'funcoes max',
            'tipo': 'HB',
            'valores': [1000, 1001]
        }
    ]


KNOWSREQS = [{
        'tempo de computacao free': {'valor': 400000, 'peso': 1},
        '1GB/segundo +': {'valor': 0.000016, 'peso': 9},
        'Arredondamento da duracao': {'valor': 1, 'peso': 1},
        'Requisicao free/mes': {'valor': 1000000, 'peso': 1},
        '1M+ requisicao': {'valor': 0.20, 'peso': 9},
        'Concurrency': {'valor': 1001, 'peso': 1},
        'Scalability': {'valor': 1, 'peso': 1},
        'Cold Starts': {'valor': 1, 'peso': 9},
        'Memory': {'valor': 128, 'peso': 1},
        'Execution Time': {'valor': 5, 'peso': 1},
        'funcoes max': {'valor': 1001, 'peso': 1}
    },{
        'tempo de computacao free': {'valor': 400000, 'peso': 1},
        '1GB/segundo +': {'valor': 0.000016, 'peso': 1},
        'Arredondamento da duracao': {'valor': 1, 'peso': 1},
        'Requisicao free/mes': {'valor': 2000000, 'peso': 9},
        '1M+ requisicao': {'valor': 0.20, 'peso': 1},
        'Concurrency': {'valor': 1001, 'peso': 1},
        'Scalability': {'valor': 1, 'peso': 1},
        'Cold Starts': {'valor': 1, 'peso': 1},
        'Memory': {'valor': 128, 'peso': 9},
        'Execution Time': {'valor': 5, 'peso': 9},
        'funcoes max': {'valor': 1001, 'peso': 1}
    },{
        'tempo de computacao free': {'valor': 400000, 'peso': 1},
        '1GB/segundo +': {'valor': 0.000016, 'peso': 1},
        'Arredondamento da duracao': {'valor': 1, 'peso': 9},
        'Requisicao free/mes': {'valor': 1000000, 'peso': 1},
        '1M+ requisicao': {'valor': 0.20, 'peso': 1},
        'Concurrency': {'valor': 1001, 'peso': 9},
        'Scalability': {'valor': 1, 'peso': 1},
        'Cold Starts': {'valor': 1, 'peso': 1},
        'Memory': {'valor': 128, 'peso': 1},
        'Execution Time': {'valor': 5, 'peso': 1},
        'funcoes max': {'valor': 1001, 'peso': 9}
    },{
        'tempo de computacao free': {'valor': 400000, 'peso': 1},
        '1GB/segundo +': {'valor': 0.000016, 'peso': 9},
        'Arredondamento da duracao': {'valor': 1, 'peso': 9},
        'Requisicao free/mes': {'valor': 1000000, 'peso': 9},
        '1M+ requisicao': {'valor': 0.20, 'peso': 1},
        'Concurrency': {'valor': 1001, 'peso': 1},
        'Scalability': {'valor': 1, 'peso': 1},
        'Cold Starts': {'valor': 1, 'peso': 1},
        'Memory': {'valor': 128, 'peso': 1},
        'Execution Time': {'valor': 5, 'peso': 1},
        'funcoes max': {'valor': 1001, 'peso': 1}
    },{
        'tempo de computacao free': {'valor': 400000, 'peso': 1},
        '1GB/segundo +': {'valor': 0.000016, 'peso': 1},
        'Arredondamento da duracao': {'valor': 1, 'peso': 1},
        'Requisicao free/mes': {'valor': 1000000, 'peso': 1},
        '1M+ requisicao': {'valor': 0.20, 'peso': 1},
        'Concurrency': {'valor': 1001, 'peso': 1},
        'Scalability': {'valor': 1, 'peso': 1},
        'Cold Starts': {'valor': 1, 'peso': 9},
        'Memory': {'valor': 1664, 'peso': 9},
        'Execution Time': {'valor': 5, 'peso': 9},
        'funcoes max': {'valor': 1001, 'peso': 1}
    },]

alternativeKnownPosition = [
        {'company':'company0',
         'criterions':{
            'tempo de computacao freePos': 0,
            '1GB/segundo +Pos': 0,
            'Arredondamento da duracaoPos': 0,
            'Requisicao free/mesPos': 0,
            '1M+ requisicaoPos': 0,
            'ConcurrencyPos': 0,
            'ScalabilityPos': 0,
            'Cold StartsPos': 0,
            'MemoryPos': [x for x in range(128, 10241, 128)],
            'Execution TimePos': 2,
            'funcoes maxPos': 1
        }},
         {'company':'company1',
         'criterions':{
            'tempo de computacao freePos': 0,
            '1GB/segundo +Pos': 1,
            'Arredondamento da duracaoPos': 1,
            'Requisicao free/mesPos': 1,
            '1M+ requisicaoPos': 1,
            'ConcurrencyPos': 1,
            'ScalabilityPos': 0,
            'Cold StartsPos': 1,
            'MemoryPos': [x for x in range(128, 4097, 128)],
            'Execution TimePos': 0,
            'funcoes maxPos': 0
        }},
         {'company':'company2',
         'criterions':{
            'tempo de computacao freePos': 0,
            '1GB/segundo +Pos': 0,
            'Arredondamento da duracaoPos': 0,
            'Requisicao free/mesPos': 0,
            '1M+ requisicaoPos': 0,
            'ConcurrencyPos': 1,
            'ScalabilityPos': 0,
            'Cold StartsPos': 2,
            'MemoryPos': [x for x in range(128, 1537, 128)],
            'Execution TimePos': 0,
            'funcoes maxPos': 0
        }},
    ]

alternativesKnownValue = [
        {'company':'company0',
         'criterions':{
            'tempo de computacao free': 400000,
            '1GB/segundo +': 0.000016,
            'Arredondamento da duracao': 1,
            'Requisicao free/mes': 1000000,
            '1M+ requisicao': 0.20,
            'Concurrency': 1000,
            'Scalability': 1,
            'Cold Starts': 1,
            'Memory': [x for x in range(128, 
                                         10241,
                                       
                                        128)],
            'Execution Time': 15,
            'funcoes max': 1001
        }},
         {'company':'company1',
         'criterions':{
            'tempo de computacao free': 400000,
            '1GB/segundo +': 0.0000025,
            'Arredondamento da duracao': 100,
            'Requisicao free/mes': 2000000,
            '1M+ requisicao': 0.40,
            'Concurrency': 1001,
            'Scalability': 1,
            'Cold Starts': 2,
            'Memory': [x for x in range(128,
                                        4097,
                                        128)],
            'Execution Time': 5,
            'funcoes max': 1000
        }},
         {'company':'company2',
         'criterions':{
            'tempo de computacao free': 400000,
            '1GB/segundo +': 0.000016,
            'Arredondamento da duracao': 1,
            'Requisicao free/mes': 1000000,
            '1M+ requisicao': 0.20,
            'Concurrency': 1001,
            'Scalability': 1,
            'Cold Starts': 5,
            'Memory': [x for x in range(128, 
                                        1537,
                                        128)],
            'Execution Time': 5,
            'funcoes max': 1001
        }},
    ]