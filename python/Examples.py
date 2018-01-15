import re

from DataGraph import *
from LR import *

def prepareExampleGraph(DG, file):
    file = open(file, "r")
    for line in file:
        lineData = line.split(' ', 2)

        origin = re.sub('\\n$', '', lineData[0])
        edge = re.sub('\\n$', '', lineData[1])
        destination = re.sub('\\n$', '', lineData[2])

        DG.addNode(origin, edge, destination)
        if edge == '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>' or edge == '<http://www.w3.org/2000/01/rdf-schema#subClassOf>':
            DG.addNode(destination, edge + '-1', origin)

    for label in DG.nodes:
        vertex = DG.nodes[label]
        vertex.edges.append(GraphEdge('$', vertex))

def new_complete_graph(n, predicates):
    """ Generates a complete with n nodes. """
    graph = DataGraph()
    for i in range(1, n + 1):
        s = str(i)
        for p in predicates:
            for j in range(1, n+1):
                o = str(j)
                graph.addNode(s, p, o)
    return graph

def new_linear_graph(n, predicates):
    """ Generates a linear graph with n nodes. """
    graph = DataGraph()
    for i in range(1,n):
        s = str(i)
        for p in predicates:
            o = str(i+1)
            # print s, p, o
            graph.addNode(s, p, o)
    return graph

def new_string_graph(n, predicates):
    """ Generates a linear graph with n nodes. """
    graph = DataGraph()
    for i in range(1,n):
        s = str(i)
        for p in predicates:
            o = str(i+1)
            # print s, p, o
            graph.addNode(s, p, o)
    return graph

def new_string_graph(half_size):
        g = DataGraph()
        if half_size > 0:
            for i in range(1,half_size+1):
                g.addNode(str(i), 'a', str(i+1))
            for i in range(half_size + 1,half_size * 2 + 1):
                g.addNode(str(i), 'b', str(i+1))
        return g

def new_tree_graph(h, m, predicates):
    """ Generates a m-ary tree with h of height. """
    def rec(D, h, m, t, predicates):
        if h > 1:
            s = str(t)
            for j in range(1,m+1):
                for p in predicates:
                    o = t+'.'+str(j)
                    D.addNode(s,p,o)
                rec(D, h-1, m, t+'.'+str(j), predicates)

    graph = DataGraph()
    rec(graph, h, m, 'root', predicates)
    return graph

def new_top_down_tree_graph(h, m, level = 0):
    """ Generates a m-ary tree with h of height. """
    def rec(D, h, m, t, level):
        if h > 1:
            s = str(t)
            for j in range(1,m+1):
                D.addNode(s, ('a' if level%2==0 else 'b'), t+'.'+str(j))
                rec(D, h-1, m, t+'.'+str(j), level + 1)

    graph = DataGraph()
    rec(graph, h, m, 'root', level)
    return graph

def new_bottom_up_tree_graph(h, m, level = 0):
    """ Generates a m-ary tree with h of height. """
    def rec(D, h, m, t, level):
        if h > 1:
            s = str(t)
            for j in range(1,m+1):
                D.addNode(t+'.'+str(j), ('a' if h%2==0 else 'b'), s)
                rec(D, h-1, m, t+'.'+str(j), level + 1)

    graph = DataGraph()
    rec(graph, h, m, 'root', level)
    return graph

def CreateParsingTable(grammar):
    parsingTable = []

    if grammar == 'ex0':
        parsingTable.append({})
        parsingTable[0]['('] = [Action('shift', 2, None)]
        parsingTable[0]['S'] = [Action('goto', 1, None)]
        parsingTable.append({})
        parsingTable[1]['$'] = [Action('accept', None, None)]
        parsingTable.append({})
        parsingTable[2]['('] = [Action('shift', 4, None)]
        parsingTable[2][')'] = [Action('reduce', None, 2)]
        parsingTable[2]['P'] = [Action('goto', 3, None)]
        parsingTable.append({})
        parsingTable[3][')'] = [Action('shift', 5, None)]
        parsingTable.append({})
        parsingTable[4]['('] = [Action('shift', 4, None)]
        parsingTable[4][')'] = [Action('reduce', None, 2)]
        parsingTable[4]['P'] = [Action('goto', 6, None)]
        parsingTable.append({})
        parsingTable[5]['$'] = [Action('reduce', None, 1)]
        parsingTable.append({})
        parsingTable[6][')'] = [Action('shift', 7, None)]
        parsingTable.append({})
        parsingTable[7][')'] = [Action('reduce', None, 3)]

        rules = [
            Rule('S\'', 1),
            Rule('S', 3),
            Rule('P', 0),
            Rule('P', 3)
        ]

    elif grammar == 'Q1':
        parsingTable.append({})
        parsingTable[0]['<http://www.w3.org/2000/01/rdf-schema#subClassOf>'] = [Action('shift', 2, None)]
        parsingTable[0]['<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>'] = [Action('shift', 3, None)]
        parsingTable[0]['S'] = [Action('goto', 1, None)]

        parsingTable.append({})
        parsingTable[1]['$'] = [Action('accept', None, None)]

        parsingTable.append({})
        parsingTable[2]['<http://www.w3.org/2000/01/rdf-schema#subClassOf>'] = [Action('shift', 6, None)]
        parsingTable[2]['<http://www.w3.org/2000/01/rdf-schema#subClassOf>-1'] = [Action('shift', 5, None)]
        parsingTable[2]['<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>'] = [Action('shift', 7, None)]
        parsingTable[2]['S'] = [Action('goto', 4, None)]

        parsingTable.append({})
        parsingTable[3]['<http://www.w3.org/2000/01/rdf-schema#subClassOf>'] = [Action('shift', 10, None)]
        parsingTable[3]['<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>'] = [Action('shift', 11, None)]
        parsingTable[3]['<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>-1'] = [Action('shift', 9, None)]
        parsingTable[3]['S'] = [Action('goto', 8, None)]

        parsingTable.append({})
        parsingTable[4]['<http://www.w3.org/2000/01/rdf-schema#subClassOf>-1'] = [Action('shift', 12, None)]

        parsingTable.append({})
        parsingTable[5]['$'] = [Action('reduce', None, 2)]

        parsingTable.append({})
        parsingTable[6]['<http://www.w3.org/2000/01/rdf-schema#subClassOf>'] = [Action('shift', 6, None)]
        parsingTable[6]['<http://www.w3.org/2000/01/rdf-schema#subClassOf>-1'] = [Action('shift', 14, None)]
        parsingTable[6]['<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>'] = [Action('shift', 7, None)]
        parsingTable[6]['S'] = [Action('goto', 13, None)]

        parsingTable.append({})
        parsingTable[7]['<http://www.w3.org/2000/01/rdf-schema#subClassOf>'] = [Action('shift', 10, None)]
        parsingTable[7]['<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>'] = [Action('shift', 11, None)]
        parsingTable[7]['<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>-1'] = [Action('shift', 16, None)]
        parsingTable[7]['S'] = [Action('goto', 15, None)]

        parsingTable.append({})
        parsingTable[8]['<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>-1'] = [Action('shift', 17, None)]
        parsingTable.append({})
        parsingTable[9]['$'] = [Action('reduce', None, 4)]

        parsingTable.append({})
        parsingTable[10]['<http://www.w3.org/2000/01/rdf-schema#subClassOf>'] = [Action('shift', 6, None)]
        parsingTable[10]['<http://www.w3.org/2000/01/rdf-schema#subClassOf>-1'] = [Action('shift', 19, None)]
        parsingTable[10]['<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>'] = [Action('shift', 7, None)]
        parsingTable[10]['S'] = [Action('goto', 18, None)]

        parsingTable.append({})
        parsingTable[11]['<http://www.w3.org/2000/01/rdf-schema#subClassOf>'] = [Action('shift', 10, None)]
        parsingTable[11]['<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>'] = [Action('shift', 11, None)]
        parsingTable[11]['<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>-1'] = [Action('shift', 21, None)]
        parsingTable[11]['S'] = [Action('goto', 20, None)]

        parsingTable.append({})
        parsingTable[12]['$'] = [Action('reduce', None, 1)]

        parsingTable.append({})
        parsingTable[13]['<http://www.w3.org/2000/01/rdf-schema#subClassOf>-1'] = [Action('shift', 22, None)]

        parsingTable.append({})
        parsingTable[14]['<http://www.w3.org/2000/01/rdf-schema#subClassOf>-1'] = [Action('reduce', None, 2)]

        parsingTable.append({})
        parsingTable[15]['<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>-1'] = [Action('shift', 23, None)]

        parsingTable.append({})
        parsingTable[16]['<http://www.w3.org/2000/01/rdf-schema#subClassOf>-1'] = [Action('reduce', None, 4)]

        parsingTable.append({})
        parsingTable[17]['$'] = [Action('reduce', None, 3)]

        parsingTable.append({})
        parsingTable[18]['<http://www.w3.org/2000/01/rdf-schema#subClassOf>-1'] = [Action('shift', 24, None)]

        parsingTable.append({})
        parsingTable[19]['<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>-1'] = [Action('reduce', None, 2)]

        parsingTable.append({})
        parsingTable[20]['<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>-1'] = [Action('shift', 25, None)]

        parsingTable.append({})
        parsingTable[21]['<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>-1'] = [Action('reduce', None, 4)]

        parsingTable.append({})
        parsingTable[22]['<http://www.w3.org/2000/01/rdf-schema#subClassOf>-1'] = [Action('reduce', None, 1)]

        parsingTable.append({})
        parsingTable[23]['<http://www.w3.org/2000/01/rdf-schema#subClassOf>-1'] = [Action('reduce', None, 3)]

        parsingTable.append({})
        parsingTable[24]['<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>-1'] = [Action('reduce', None, 1)]

        parsingTable.append({})
        parsingTable[25]['<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>-1'] = [Action('reduce', None, 3)]

        rules = [
            Rule('S\'', 1),
            Rule('S', 3),
            Rule('S', 2),
            Rule('S', 3),
            Rule('S', 2)
        ]

    elif grammar == 'Q2':

        parsingTable.append({})
        parsingTable[0]['<http://www.w3.org/2000/01/rdf-schema#subClassOf>'] = [Action('shift', 3, None)]
        parsingTable[0]['S'] = [Action('goto', 1, None)]
        parsingTable[0]['SC'] = [Action('goto', 2, None)]

        parsingTable.append({})
        parsingTable[1]['$'] = [Action('accept', None, None)]

        parsingTable.append({})
        parsingTable[2]['<http://www.w3.org/2000/01/rdf-schema#subClassOf>'] = [Action('shift', 6, None)]
        parsingTable[2]['$'] = [Action('reduce', None, 3)]
        parsingTable[2]['S2'] = [Action('goto', 4, None)]
        parsingTable[2]['SC'] = [Action('goto', 5, None)]

        parsingTable.append({})
        parsingTable[3]['<http://www.w3.org/2000/01/rdf-schema#subClassOf>'] = [Action('reduce', None, 7)]
        parsingTable[3]['$'] = [Action('reduce', None, 7)]

        parsingTable.append({})
        parsingTable[4]['$'] = [Action('reduce', None, 1)]

        parsingTable.append({})
        parsingTable[5]['<http://www.w3.org/2000/01/rdf-schema#subClassOf>-1'] = [Action('shift', 9, None)]
        parsingTable[5]['<http://www.w3.org/2000/01/rdf-schema#subClassOf>'] = [Action('shift', 6, None)]
        parsingTable[5]['B'] = [Action('goto', 8, None)]
        parsingTable[5]['B2'] = [Action('goto', 7, None)]
        parsingTable[5]['SC'] = [Action('goto', 10, None)]

        parsingTable.append({})
        parsingTable[6]['<http://www.w3.org/2000/01/rdf-schema#subClassOf>-1'] = [Action('reduce', None, 7)]
        parsingTable[6]['<http://www.w3.org/2000/01/rdf-schema#subClassOf>'] = [Action('reduce', None, 7)]

        parsingTable.append({})
        parsingTable[7]['$'] = [Action('reduce', None, 2)]

        parsingTable.append({})
        parsingTable[8]['<http://www.w3.org/2000/01/rdf-schema#subClassOf>-1'] = [Action('shift', 12, None)]
        parsingTable[8]['SC_'] = [Action('goto', 11, None)]

        parsingTable.append({})
        parsingTable[9]['$'] = [Action('reduce', None, 6)]

        parsingTable.append({})
        parsingTable[10]['<http://www.w3.org/2000/01/rdf-schema#subClassOf>-1'] = [Action('shift', 15, None)]
        parsingTable[10]['<http://www.w3.org/2000/01/rdf-schema#subClassOf>'] = [Action('shift', 6, None)]
        parsingTable[10]['B'] = [Action('goto', 14, None)]
        parsingTable[10]['B2'] = [Action('goto', 13, None)]
        parsingTable[10]['SC'] = [Action('goto', 10, None)]

        parsingTable.append({})
        parsingTable[11]['$'] = [Action('reduce', None, 5)]

        parsingTable.append({})
        parsingTable[12]['$'] = [Action('reduce', None, 8)]

        parsingTable.append({})
        parsingTable[13]['<http://www.w3.org/2000/01/rdf-schema#subClassOf>-1'] = [Action('reduce', None, 4)]

        parsingTable.append({})
        parsingTable[14]['<http://www.w3.org/2000/01/rdf-schema#subClassOf>-1'] = [Action('shift', 17, None)]
        parsingTable[14]['SC_'] = [Action('goto', 16, None)]

        parsingTable.append({})
        parsingTable[15]['<http://www.w3.org/2000/01/rdf-schema#subClassOf>-1'] = [Action('reduce', None, 6)]

        parsingTable.append({})
        parsingTable[16]['<http://www.w3.org/2000/01/rdf-schema#subClassOf>-1'] = [Action('reduce', None, 5)]

        parsingTable.append({})
        parsingTable[17]['<http://www.w3.org/2000/01/rdf-schema#subClassOf>-1'] = [Action('reduce', None, 8)]

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

    elif grammar == 'G0':

            parsingTable.append({})
            parsingTable[0]['a'] = [Action('shift', 2, None), Action('reduce', None, 3)]
            parsingTable[0]['$'] = [Action('reduce', None, 3)]
            parsingTable[0]['S'] = [Action('goto', 1, None)]

            parsingTable.append({})
            parsingTable[1]['a'] = [Action('shift', 2, None), Action('reduce', None, 3)]
            parsingTable[1]['$'] = [Action('accept', None, None), Action('reduce', None, 3)]
            parsingTable[1]['S'] = [Action('goto', 3, None)]

            parsingTable.append({})
            parsingTable[2]['a'] = [Action('shift', 5, None), Action('reduce', None, 3)]
            parsingTable[2]['b'] = [Action('reduce', None, 3)]
            parsingTable[2]['S'] = [Action('goto', 4, None)]

            parsingTable.append({})
            parsingTable[3]['a'] = [Action('shift', 2, None), Action('reduce', None, 2), Action('reduce', None, 3)]
            parsingTable[3]['$'] = [Action('reduce', None, 2), Action('reduce', None, 3)]
            parsingTable[3]['S'] = [Action('goto', 3, None)]

            parsingTable.append({})
            parsingTable[4]['a'] = [Action('shift', 5, None), Action('reduce', None, 3)]
            parsingTable[4]['b'] = [Action('shift', 6, None), Action('reduce', None, 3)]
            parsingTable[4]['S'] = [Action('goto', 7, None)]

            parsingTable.append({})
            parsingTable[5]['a'] = [Action('shift', 5, None), Action('reduce', None, 3)]
            parsingTable[5]['b'] = [Action('reduce', None, 3)]
            parsingTable[5]['S'] = [Action('goto', 8, None)]

            parsingTable.append({})
            parsingTable[6]['a'] = [Action('reduce', None, 1)]
            parsingTable[6]['$'] = [Action('reduce', None, 1)]

            parsingTable.append({})
            parsingTable[7]['a'] = [Action('shift', 5, None), Action('reduce', None, 2), Action('reduce', None, 3)]
            parsingTable[7]['b'] = [Action('reduce', None, 2), Action('reduce', None, 3)]
            parsingTable[7]['S'] = [Action('goto', 7, None)]

            parsingTable.append({})
            parsingTable[8]['a'] = [Action('shift', 5, None), Action('reduce', None, 3)]
            parsingTable[8]['b'] = [Action('shift', 9, None), Action('reduce', None, 3)]
            parsingTable[8]['S'] = [Action('goto', 7, None)]

            parsingTable.append({})
            parsingTable[9]['a'] = [Action('reduce', None, 1)]
            parsingTable[9]['b'] = [Action('reduce', None, 1)]

            rules = [
                Rule('S\'', 1),
                Rule('S', 3),
                Rule('S', 2),
                Rule('S', 0)
            ]

    elif grammar == 'G2':

        parsingTable.append({})
        parsingTable[0]['a'] = [Action('shift', 2, None)]
        parsingTable[0]['$'] = [Action('reduce', None, 2)]
        parsingTable[0]['S'] = [Action('goto', 1, None)]

        parsingTable.append({})
        parsingTable[1]['$'] = [Action('accept', None, None)]

        parsingTable.append({})
        parsingTable[2]['a'] = [Action('shift', 4, None)]
        parsingTable[2]['b'] = [Action('reduce', None, 2)]
        parsingTable[2]['S'] = [Action('goto', 3, None)]

        parsingTable.append({})
        parsingTable[3]['b'] = [Action('shift', 5, None)]

        parsingTable.append({})
        parsingTable[4]['a'] = [Action('shift', 4, None)]
        parsingTable[4]['b'] = [Action('reduce', None, 2)]
        parsingTable[4]['S'] = [Action('goto', 6, None)]

        parsingTable.append({})
        parsingTable[5]['a'] = [Action('shift', 2, None)]
        parsingTable[5]['$'] = [Action('reduce', None, 2)]
        parsingTable[5]['S'] = [Action('goto', 7, None)]

        parsingTable.append({})
        parsingTable[6]['b'] = [Action('shift', 8, None)]

        parsingTable.append({})
        parsingTable[7]['$'] = [Action('reduce', None, 1)]

        parsingTable.append({})
        parsingTable[8]['a'] = [Action('shift', 4, None)]
        parsingTable[8]['b'] = [Action('reduce', None, 2)]
        parsingTable[8]['S'] = [Action('goto', 9, None)]

        parsingTable.append({})
        parsingTable[9]['b'] = [Action('reduce', None, 1)]

        rules = [
            Rule('S\'', 1),
            Rule('S', 4),
            Rule('S', 0)
        ]
        
    elif grammar == 'G2_2':

        parsingTable.append({})
        parsingTable[0]['a'] = [Action('shift', 3, None)]
        parsingTable[0]['$'] = [Action('reduce', None, 6)]
        parsingTable[0]['S'] = [Action('goto', 1, None)]
        parsingTable[0]['A'] = [Action('goto', 2, None)]

        parsingTable.append({})
        parsingTable[1]['$'] = [Action('accept', None, None)]

        parsingTable.append({})
        parsingTable[2]['a'] = [Action('shift', 7, None)]
        parsingTable[2]['b'] = [Action('reduce', None, 6)]
        parsingTable[2]['S'] = [Action('goto', 5, None)]
        parsingTable[2]['A'] = [Action('goto', 6, None)]
        parsingTable[2]['R'] = [Action('goto', 4, None)]

        parsingTable.append({})
        parsingTable[3]['a'] = [Action('reduce', None, 2)]
        parsingTable[3]['b'] = [Action('reduce', None, 2)]
        parsingTable[3]['$'] = [Action('reduce', None, 2)]

        parsingTable.append({})
        parsingTable[4]['$'] = [Action('reduce', None, 1)]

        parsingTable.append({})
        parsingTable[5]['a'] = [Action('shift', 10, None)]
        parsingTable[5]['P'] = [Action('goto', 8, None)]
        parsingTable[5]['B'] = [Action('goto', 9, None)]

        parsingTable.append({})
        parsingTable[6]['a'] = [Action('shift', 7, None)]
        parsingTable[6]['b'] = [Action('reduce', None, 6)]
        parsingTable[6]['S'] = [Action('goto', 12, None)]
        parsingTable[6]['A'] = [Action('goto', 6, None)]
        parsingTable[6]['R'] = [Action('goto', 11, None)]

        parsingTable.append({})
        parsingTable[7]['a'] = [Action('reduce', None, 2)]
        parsingTable[7]['b'] = [Action('reduce', None, 2)]

        parsingTable.append({})
        parsingTable[8]['$'] = [Action('reduce', None, 3)]
        
        parsingTable.append({})
        parsingTable[9]['a'] = [Action('shift', 3, None)]
        parsingTable[9]['$'] = [Action('reduce', None, 6)]
        parsingTable[9]['S'] = [Action('goto', 13, None)]
        parsingTable[9]['A'] = [Action('goto', 2, None)]
        
        parsingTable.append({})
        parsingTable[10]['a'] = [Action('reduce', None, 5)]
        parsingTable[10]['$'] = [Action('reduce', None, 5)]
        
        parsingTable.append({})
        parsingTable[11]['b'] = [Action('reduce', None, 1)]
        
        parsingTable.append({})
        parsingTable[12]['b'] = [Action('shift', 16, None)]
        parsingTable[12]['P'] = [Action('goto', 14, None)]
        parsingTable[12]['B'] = [Action('goto', 15, None)]
        
        parsingTable.append({})
        parsingTable[13]['$'] = [Action('reduce', None, 4)]
        
        parsingTable.append({})
        parsingTable[14]['b'] = [Action('reduce', None, 3)]
        
        parsingTable.append({})
        parsingTable[15]['a'] = [Action('shift', 7, None)]
        parsingTable[15]['b'] = [Action('reduce', None, 6)]
        parsingTable[15]['S'] = [Action('goto', 17, None)]
        parsingTable[15]['A'] = [Action('goto', 6, None)]
        
        parsingTable.append({})
        parsingTable[16]['a'] = [Action('reduce', None, 5)]
        parsingTable[16]['b'] = [Action('reduce', None, 5)]
        
        parsingTable.append({})
        parsingTable[17]['b'] = [Action('reduce', None, 4)]

        rules = [
            Rule('S\'', 1),
            Rule('S', 2),
            Rule('A', 1),
            Rule('R', 2),
            Rule('P', 2),
            Rule('B', 1),
            Rule('S', 0)
        ]


    return parsingTable, rules
