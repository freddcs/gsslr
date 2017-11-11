import re

from DataGraph import *
from examples.dbWine import *
from examples.dbPeoplePets import *
from LR import *

def prepareExampleGraph(DG, file):
    file = open(file, "r")
    for line in file:
        lineData = line.split(' ', 2)

        origin = re.sub('\\n$', '', lineData[0])
        edge = re.sub('\\n$', '', lineData[1])
        destination = re.sub('\\n$', '', lineData[2])

        DG.addNode(origin, edge, destination)
        DG.addNode(destination, edge + '-1', origin)

    for label in DG.nodes:
        vertex = DG.nodes[label]
        vertex.edges.append(GraphEdge('$', vertex))

def CreateParsingTable(grammar):
    parsingTable = []

    if grammar == 'ex0':
        parsingTable.append({})
        parsingTable[0]['('] = Action('shift', 2, None)
        parsingTable[0]['S'] = Action('goto', 1, None)
        parsingTable.append({})
        parsingTable[1]['$'] = Action('accept', None, None)
        parsingTable.append({})
        parsingTable[2]['('] = Action('shift', 4, None)
        parsingTable[2][')'] = Action('reduce', None, 2)
        parsingTable[2]['P'] = Action('goto', 3, None)
        parsingTable.append({})
        parsingTable[3][')'] = Action('shift', 5, None)
        parsingTable.append({})
        parsingTable[4]['('] = Action('shift', 4, None)
        parsingTable[4][')'] = Action('reduce', None, 2)
        parsingTable[4]['P'] = Action('goto', 6, None)
        parsingTable.append({})
        parsingTable[5]['$'] = Action('reduce', None, 1)
        parsingTable.append({})
        parsingTable[6][')'] = Action('shift', 7, None)
        parsingTable.append({})
        parsingTable[7][')'] = Action('reduce', None, 3)

        rules = [
            Rule('S\'', 1),
            Rule('S', 3),
            Rule('P', 0),
            Rule('P', 3)
        ]

    elif grammar == 'Q1':
        parsingTable.append({})
        parsingTable[0]['<http://www.w3.org/2000/01/rdf-schema#subClassOf>'] = Action('shift', 2, None)
        parsingTable[0]['<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>'] = Action('shift', 3, None)
        parsingTable[0]['S'] = Action('goto', 1, None)

        parsingTable.append({})
        parsingTable[1]['$'] = Action('accept', None, None)

        parsingTable.append({})
        parsingTable[2]['<http://www.w3.org/2000/01/rdf-schema#subClassOf>'] = Action('shift', 6, None)
        parsingTable[2]['<http://www.w3.org/2000/01/rdf-schema#subClassOf>-1'] = Action('shift', 5, None)
        parsingTable[2]['<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>'] = Action('shift', 7, None)
        parsingTable[2]['S'] = Action('goto', 4, None)

        parsingTable.append({})
        parsingTable[3]['<http://www.w3.org/2000/01/rdf-schema#subClassOf>'] = Action('shift', 10, None)
        parsingTable[3]['<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>'] = Action('shift', 11, None)
        parsingTable[3]['<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>-1'] = Action('shift', 9, None)
        parsingTable[3]['S'] = Action('goto', 8, None)

        parsingTable.append({})
        parsingTable[4]['<http://www.w3.org/2000/01/rdf-schema#subClassOf>-1'] = Action('shift', 12, None)

        parsingTable.append({})
        parsingTable[5]['$'] = Action('reduce', None, 2)

        parsingTable.append({})
        parsingTable[6]['<http://www.w3.org/2000/01/rdf-schema#subClassOf>'] = Action('shift', 6, None)
        parsingTable[6]['<http://www.w3.org/2000/01/rdf-schema#subClassOf>-1'] = Action('shift', 14, None)
        parsingTable[6]['<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>'] = Action('shift', 7, None)
        parsingTable[6]['S'] = Action('goto', 13, None)

        parsingTable.append({})
        parsingTable[7]['<http://www.w3.org/2000/01/rdf-schema#subClassOf>'] = Action('shift', 10, None)
        parsingTable[7]['<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>'] = Action('shift', 11, None)
        parsingTable[7]['<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>-1'] = Action('shift', 16, None)
        parsingTable[7]['S'] = Action('goto', 15, None)

        parsingTable.append({})
        parsingTable[8]['<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>-1'] = Action('shift', 17, None)
        parsingTable.append({})
        parsingTable[9]['$'] = Action('reduce', None, 4)

        parsingTable.append({})
        parsingTable[10]['<http://www.w3.org/2000/01/rdf-schema#subClassOf>'] = Action('shift', 6, None)
        parsingTable[10]['<http://www.w3.org/2000/01/rdf-schema#subClassOf>-1'] = Action('shift', 19, None)
        parsingTable[10]['<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>'] = Action('shift', 7, None)
        parsingTable[10]['S'] = Action('goto', 18, None)

        parsingTable.append({})
        parsingTable[11]['<http://www.w3.org/2000/01/rdf-schema#subClassOf>'] = Action('shift', 10, None)
        parsingTable[11]['<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>'] = Action('shift', 11, None)
        parsingTable[11]['<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>-1'] = Action('shift', 21, None)
        parsingTable[11]['S'] = Action('goto', 20, None)

        parsingTable.append({})
        parsingTable[12]['$'] = Action('reduce', None, 1)

        parsingTable.append({})
        parsingTable[13]['<http://www.w3.org/2000/01/rdf-schema#subClassOf>-1'] = Action('shift', 22, None)

        parsingTable.append({})
        parsingTable[14]['<http://www.w3.org/2000/01/rdf-schema#subClassOf>-1'] = Action('reduce', None, 2)

        parsingTable.append({})
        parsingTable[15]['<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>-1'] = Action('shift', 23, None)

        parsingTable.append({})
        parsingTable[16]['<http://www.w3.org/2000/01/rdf-schema#subClassOf>-1'] = Action('reduce', None, 4)

        parsingTable.append({})
        parsingTable[17]['$'] = Action('reduce', None, 3)

        parsingTable.append({})
        parsingTable[18]['<http://www.w3.org/2000/01/rdf-schema#subClassOf>-1'] = Action('shift', 24, None)

        parsingTable.append({})
        parsingTable[19]['<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>-1'] = Action('reduce', None, 2)

        parsingTable.append({})
        parsingTable[20]['<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>-1'] = Action('shift', 25, None)

        parsingTable.append({})
        parsingTable[21]['<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>-1'] = Action('reduce', None, 4)

        parsingTable.append({})
        parsingTable[22]['<http://www.w3.org/2000/01/rdf-schema#subClassOf>-1'] = Action('reduce', None, 1)

        parsingTable.append({})
        parsingTable[23]['<http://www.w3.org/2000/01/rdf-schema#subClassOf>-1'] = Action('reduce', None, 3)

        parsingTable.append({})
        parsingTable[24]['<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>-1'] = Action('reduce', None, 1)

        parsingTable.append({})
        parsingTable[25]['<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>-1'] = Action('reduce', None, 3)

        rules = [
            Rule('S\'', 1),
            Rule('S', 3),
            Rule('S', 2),
            Rule('S', 3),
            Rule('S', 2)
        ]

    elif grammar == 'Q2':

        parsingTable.append({})
        parsingTable[0]['<http://www.w3.org/2000/01/rdf-schema#subClassOf>'] = Action('shift', 3, None)
        parsingTable[0]['S'] = Action('goto', 1, None)
        parsingTable[0]['SC'] = Action('goto', 2, None)

        parsingTable.append({})
        parsingTable[1]['$'] = Action('accept', None, None)

        parsingTable.append({})
        parsingTable[2]['<http://www.w3.org/2000/01/rdf-schema#subClassOf>'] = Action('shift', 6, None)
        parsingTable[2]['$'] = Action('reduce', None, 3)
        parsingTable[2]['S2'] = Action('goto', 4, None)
        parsingTable[2]['SC'] = Action('goto', 5, None)

        parsingTable.append({})
        parsingTable[3]['<http://www.w3.org/2000/01/rdf-schema#subClassOf>'] = Action('reduce', None, 7)
        parsingTable[3]['$'] = Action('reduce', None, 7)

        parsingTable.append({})
        parsingTable[4]['$'] = Action('reduce', None, 1)

        parsingTable.append({})
        parsingTable[5]['<http://www.w3.org/2000/01/rdf-schema#subClassOf>-1'] = Action('shift', 9, None)
        parsingTable[5]['<http://www.w3.org/2000/01/rdf-schema#subClassOf>'] = Action('shift', 6, None)
        parsingTable[5]['B'] = Action('goto', 8, None)
        parsingTable[5]['B2'] = Action('goto', 7, None)
        parsingTable[5]['SC'] = Action('goto', 10, None)

        parsingTable.append({})
        parsingTable[6]['<http://www.w3.org/2000/01/rdf-schema#subClassOf>-1'] = Action('reduce', None, 7)
        parsingTable[6]['<http://www.w3.org/2000/01/rdf-schema#subClassOf>'] = Action('reduce', None, 7)

        parsingTable.append({})
        parsingTable[7]['$'] = Action('reduce', None, 2)

        parsingTable.append({})
        parsingTable[8]['<http://www.w3.org/2000/01/rdf-schema#subClassOf>-1'] = Action('shift', 12, None)
        parsingTable[8]['SC_'] = Action('goto', 11, None)

        parsingTable.append({})
        parsingTable[9]['$'] = Action('reduce', None, 6)

        parsingTable.append({})
        parsingTable[10]['<http://www.w3.org/2000/01/rdf-schema#subClassOf>-1'] = Action('shift', 15, None)
        parsingTable[10]['<http://www.w3.org/2000/01/rdf-schema#subClassOf>'] = Action('shift', 6, None)
        parsingTable[10]['B'] = Action('goto', 14, None)
        parsingTable[10]['B2'] = Action('goto', 13, None)
        parsingTable[10]['SC'] = Action('goto', 10, None)

        parsingTable.append({})
        parsingTable[11]['$'] = Action('reduce', None, 5)

        parsingTable.append({})
        parsingTable[12]['$'] = Action('reduce', None, 8)

        parsingTable.append({})
        parsingTable[13]['<http://www.w3.org/2000/01/rdf-schema#subClassOf>-1'] = Action('reduce', None, 4)

        parsingTable.append({})
        parsingTable[14]['<http://www.w3.org/2000/01/rdf-schema#subClassOf>-1'] = Action('shift', 17, None)
        parsingTable[14]['SC_'] = Action('goto', 16, None)

        parsingTable.append({})
        parsingTable[15]['<http://www.w3.org/2000/01/rdf-schema#subClassOf>-1'] = Action('reduce', None, 6)

        parsingTable.append({})
        parsingTable[16]['<http://www.w3.org/2000/01/rdf-schema#subClassOf>-1'] = Action('reduce', None, 5)

        parsingTable.append({})
        parsingTable[17]['<http://www.w3.org/2000/01/rdf-schema#subClassOf>-1'] = Action('reduce', None, 8)

        rules = [
            Rule('S\'', 1),
            Rule('S', 2),
            Rule('S2', 2),
            Rule('S2', 0),
            Rule('B', 2),
            Rule('B2', 2),
            Rule('B2', 1),
            Rule('SC', 1),
            Rule('SC_', 1)
        ]

    return parsingTable, rules
