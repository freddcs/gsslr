import time

from DataGraph import *
from GSS import *
from Examples import *
from LR import *
from Algorithm import *

resultadosEsperados = {}
resultadosEsperados['Q1'] = {}
resultadosEsperados['Q1']['skos'] = 810
resultadosEsperados['Q1']['generations'] = 2164
resultadosEsperados['Q1']['travel'] = 2499
resultadosEsperados['Q1']['univ-bench'] = 2540
resultadosEsperados['Q1']['foaf'] = 4118
resultadosEsperados['Q1']['people-pets'] = 9472
resultadosEsperados['Q1']['funding'] = 17634
resultadosEsperados['Q1']['atom-primitive'] = 15454
resultadosEsperados['Q1']['biomedical'] = 15156
resultadosEsperados['Q1']['pizza'] = 56195
resultadosEsperados['Q1']['wine'] = 66572

resultadosEsperados['Q2'] = {}
resultadosEsperados['Q2']['skos'] = 1
resultadosEsperados['Q2']['generations'] = 0
resultadosEsperados['Q2']['travel'] = 63
resultadosEsperados['Q2']['univ-bench'] = 81
resultadosEsperados['Q2']['foaf'] = 10
resultadosEsperados['Q2']['people-pets'] = 37
resultadosEsperados['Q2']['funding'] = 1158
resultadosEsperados['Q2']['atom-primitive'] = 122
resultadosEsperados['Q2']['biomedical'] = 2871
resultadosEsperados['Q2']['pizza'] = 1262
resultadosEsperados['Q2']['wine'] = 133

resultadosEsperados['linear'] = {}
resultadosEsperados['linear'][0] = 0
resultadosEsperados['linear'][10] = 30
resultadosEsperados['linear'][20] = 110
resultadosEsperados['linear'][30] = 240
resultadosEsperados['linear'][40] = 420
resultadosEsperados['linear'][50] = 650
resultadosEsperados['linear'][60] = 930
resultadosEsperados['linear'][70] = 1260
resultadosEsperados['linear'][80] = 1640
resultadosEsperados['linear'][90] = 2070
resultadosEsperados['linear'][100] = 2550
resultadosEsperados['linear'][110] = 3080
resultadosEsperados['linear'][120] = 3660
resultadosEsperados['linear'][130] = 4290
resultadosEsperados['linear'][140] = 4970
resultadosEsperados['linear'][150] = 5700
resultadosEsperados['linear'][160] = 6480
resultadosEsperados['linear'][170] = 7310
resultadosEsperados['linear'][180] = 8190
resultadosEsperados['linear'][190] = 9120
resultadosEsperados['linear'][200] = 10100
resultadosEsperados['linear'][225] = 12769
resultadosEsperados['linear'][250] = 15750
resultadosEsperados['linear'][275] = 19044
resultadosEsperados['linear'][300] = 22650
resultadosEsperados['linear'][325] = 26569
resultadosEsperados['linear'][350] = 30800
resultadosEsperados['linear'][375] = 35344
resultadosEsperados['linear'][400] = 40200
resultadosEsperados['linear'][425] = 45369
resultadosEsperados['linear'][450] = 50850

resultadosEsperados['tree'] = {}
resultadosEsperados['tree'][1] = 0
resultadosEsperados['tree'][2] = 3
resultadosEsperados['tree'][3] = 11
resultadosEsperados['tree'][4] = 27
resultadosEsperados['tree'][5] = 75
resultadosEsperados['tree'][6] = 171
resultadosEsperados['tree'][7] = 427
resultadosEsperados['tree'][8] = 939
resultadosEsperados['tree'][9] = 2219
resultadosEsperados['tree'][10] = 4779
resultadosEsperados['tree'][11] = 10923
resultadosEsperados['tree'][12] = 23211
resultadosEsperados['tree'][13] = 51883
resultadosEsperados['tree'][15] = 240299
resultadosEsperados['tree'][16] = 502443

resultadosEsperados['complete'] = {}
resultadosEsperados['complete'][0] = 0
resultadosEsperados['complete'][10] = 100
resultadosEsperados['complete'][20] = 400
resultadosEsperados['complete'][30] = 900
resultadosEsperados['complete'][40] = 1600
resultadosEsperados['complete'][50] = 2500
resultadosEsperados['complete'][60] = 3600
resultadosEsperados['complete'][70] = 4900
resultadosEsperados['complete'][80] = 6400
resultadosEsperados['complete'][90] = 8100
resultadosEsperados['complete'][110] = 12100
resultadosEsperados['complete'][130] = 16900
resultadosEsperados['complete'][150] = 22500
resultadosEsperados['complete'][170] = 28900
resultadosEsperados['complete'][190] = 36100
resultadosEsperados['complete'][200] = 40000
resultadosEsperados['complete'][225] = 50625
resultadosEsperados['complete'][250] = 62500
resultadosEsperados['complete'][275] = 75625
resultadosEsperados['complete'][300] = 90000
resultadosEsperados['complete'][325] = 105625
resultadosEsperados['complete'][350] = 122500
resultadosEsperados['complete'][375] = 140625
resultadosEsperados['complete'][400] = 160000

iterations = 1

# Ontologies

examples = ['skos', 'generations', 'travel', 'univ-bench', 'foaf', 'people-pets', 'funding', 'atom-primitive', 'biomedical', 'pizza', 'wine']

print 'Grammar,Ontology,Time (ms),results'

for G in ['Q1', 'Q2']:
    parsingTable, rules = CreateParsingTable(G)

    for ontology in examples:
        DG = DataGraph()

        prepareExampleGraph(DG, 'examples/' + ontology + '.dat')

        now = lambda: int(round(time.time() * 1000))

        totalTime = 0

        for i in range(iterations):
            start = now()
            answers = GSS_LR(DG, parsingTable, rules)
            totalTime += now() - start

        # print answers
        print '%s,%s,%s,%s,%s' % (len(answers) == resultadosEsperados[G][ontology], G, ontology, str(totalTime / iterations), str(len(answers)))

print 'Grammar,Graph type,Length,Time (ms),Results'

for G in ['G0', 'G2']:
    parsingTable, rules = CreateParsingTable(G)

    # for graphType in ['linear', 'tree', 'complete']:
    for graphType in ['tree']:

        if graphType == 'complete':
            examples = [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,225,250,275,300,325,350,375,400]
            #examples = [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 20,30,40,50,60,70,80,90]
            examples = [2]
        elif graphType == 'linear':
            examples = [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,225,250,275,300,325,350,375,400]
            
        else:
            examples = [1,2,3,4,5,6,7,8,9,10,11,12,13,15,16,17]
            examples = [2]

        for e in examples:

            if graphType == 'complete':
                DG = new_complete_graph(e, ['a', 'b'])
            elif graphType == 'linear':
                DG = new_linear_graph(e, ['a', 'b'])
            else:
                DG = new_tree_graph(e, 2, ['a', 'b'])

            print 'GRAFO'
            print DG

            now = lambda: int(round(time.time() * 1000))

            totalTime = 0

            for i in range(iterations):
                start = now()
                gss, answers = GSS_LR(DG, parsingTable, rules)
                totalTime += now() - start

            # print answers
            #print '%s,%s,%s,%s,%s,%s' % (len(answers) == resultadosEsperados[graphType][e], G, graphType, str(e), str(totalTime / iterations), str(len(answers)))
            
            print e
            print 'NumberOfNodes: ', gss.numberOfNodes
            print 'Answers: ', answers
