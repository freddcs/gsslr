import time

from DataGraph import *
from GSS import *
from Examples import *
from LR import *
from Algorithm import *

iterations = 5

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
        print '%s,%s,%s,%s' % (G, ontology, str(totalTime / iterations), str(len(answers)))

print 'Graph type,Length,Time (ms),Results'

for G in ['G0', 'G2']:
    parsingTable, rules = CreateParsingTable(G)

    for graphType in ['linear', 'tree', 'complete']:

        if graphType == 'complete':
            examples = [0,10,20,30,40,50,60,70,80,90,110,130,150,170,190,200,225,250,275,300,325,350,375,400]
        elif graphType == 'linear':
            examples = [0,10,20,30,40,50,60,70,80,90,110,130,150,170,190,200,225,250,275,300,325,350,375,400]
        else:
            examples = [1,2,3,4,5,6,7,8,9,10,11,12]

        for e in examples:

            if graphType == 'complete':
                DG = new_complete_graph(e, ['a', 'b'])
            elif graphType == 'linear':
                DG = new_linear_graph(e, ['a', 'b'])
            else:
                DG = new_tree_graph(e, 2, ['a', 'b'])

            now = lambda: int(round(time.time() * 1000))

            totalTime = 0

            for i in range(iterations):
                start = now()
                answers = GSS_LR(DG, parsingTable, rules)
                totalTime += now() - start

            # print answers
            print '%s,%s,%s,%s,%s' % (G, graphType, str(e), str(totalTime / iterations), str(len(answers)))