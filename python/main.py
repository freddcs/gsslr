import time
import cProfile
import sys

from DataGraph import *
from GSS import *
from Examples import *
from LR import *
from Algorithm import *

G =  sys.argv[1] if len(sys.argv) >= 2 else 'Q1'
parsingTable, rules = CreateParsingTable(G)

DG = DataGraph()

data = sys.argv[2] if len(sys.argv) >= 3 else 'wine'

prepareExampleGraph(DG, 'examples/' + data + '.dat')

pr = cProfile.Profile()
pr.enable()

answers = GSS_LR(DG, parsingTable, rules)

pr.disable()
 
pr.print_stats(sort='time')

# print answers

print 'Nodes: ' + str(len(DG.nodes))
print 'Triples: ' + str(DG.triplesCount / 2)
print 'Answers: ' + str(len(answers))
