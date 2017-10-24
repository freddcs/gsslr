class DataGraph:
    def __init__(self):
        self.nodes = {}
        
    def addNode(self, sourceLabel, edgeLabel, destinationLabel):
        if (sourceLabel not in self.nodes):
            self.nodes[sourceLabel] = GraphNode(sourceLabel)
                
        if (destinationLabel not in self.nodes):
            self.nodes[destinationLabel] = GraphNode(destinationLabel)
                
        self.nodes[sourceLabel].edges.append(GraphEdge(edgeLabel, self.nodes[destinationLabel]))
        
class GraphNode:
    def __init__(self, vertexLabel):
        self.vertexLabel = vertexLabel
        self.edges = [GraphEdge('$', self)]

class GraphEdge:
    def __init__(self, edgeLabel, destination):
        self.edgeLabel = edgeLabel
        self.destination = destination
        
class GSS:
    def __init__(self):
        self.levels = []
        self.numberOfNodes = 0
        
    def addNode(self, level, state, vertex, predecessor):
        if len(self.levels) <= level:
            self.levels.append([]);
            
        gssNode = None
        for index, node in enumerate(self.levels[level]):
            if node.state == state and node.vertex.vertexLabel == vertex.vertexLabel:
                gssNode = node
                break;
            
        if gssNode == None:
            gssNode = GSSNode(state, vertex, predecessor)
            gssNode.label = self.numberOfNodes
            self.levels[level].append(gssNode)
            self.numberOfNodes += 1
        else:
            if predecessor != None and predecessor not in gssNode.predecessors:
                gssNode.predecessors.append(predecessor)
        
        return gssNode
    
    def up(self, gssNode, jumps):
        reductionRoots = []
        
        if jumps > 0:
            gssNodes = []
            for index, predecessorLink in enumerate(gssNode.predecessors):
                gssNodes = gssNodes + self.up(predecessorLink.gssNode, jumps - 1)
                
            return gssNodes
        else:
            return [gssNode]
        
    def __repr__(self):
        gss = 'GSS:\n'
        for level, nodes in enumerate(self.levels):
            gss += 'U' + str(level) + ':\n'
            for index, node in enumerate(nodes):
                gss += str(node) + '\n'
            gss += '\n'
        return gss
    
class Action:
    def __init__(self, action, state, rule):
        self.action = action
        self.state = state
        self.rule = rule
        
class Rule:
    def __init__(self, lhs, rhsSize):
        self.lhs = lhs
        self.rhsSize = rhsSize
        
class GSSNode:
    def __init__(self, state, vertex, predecessor):
        self.state = state
        self.vertex = vertex
        
        self.predecessors = []
        if predecessor != None:
            self.predecessors.append(predecessor)
        self.label = 0

    def __repr__(self):
        previous = ''
        for index, predecessor in enumerate(self.predecessors):
            previous += predecessor.edgeLabel + '<- v' + str(predecessor.gssNode.label) + ' '
            
        return 'v' + str(self.label) + '(' + self.vertex.vertexLabel + ', I' + str(self.state) + ', [ ' + previous + ']) '
    
class GSSLink:
    def __init__(self, edgeLabel, gssNode):
        self.edgeLabel = edgeLabel
        self.gssNode = gssNode
        
    def __eq__(self, other):
        return (isinstance(other, self.__class__)
            and self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self.__eq__(other)

def addGraphNode(graph, source, edge, destination):
    if source not in graph:
        graph[source] = []
        
    graph[source].append(GraphNode(source, edge, destination))
                             
    return

def CreateParsingTable(grammar):
    parsingTable = []
    
    # Example 1
    '''parsingTable.append({})
    parsingTable[0]['('] = Action('shift', 2, None)
    parsingTable[0]['S'] = Action('goto', 1, None)
    parsingTable[0]['hasShifts'] = True
    parsingTable.append({})
    parsingTable[1]['$'] = Action('accept', None, None)
    parsingTable[1]['hasAccepts'] = True
    parsingTable.append({})
    parsingTable[2]['('] = Action('shift', 4, None)
    parsingTable[2][')'] = Action('reduce', None, 2)
    parsingTable[2]['P'] = Action('goto', 3, None)
    parsingTable[2]['hasReductions'] = True
    parsingTable[2]['hasShifts'] = True
    parsingTable.append({})
    parsingTable[3][')'] = Action('shift', 5, None)
    parsingTable[3]['hasShifts'] = True
    parsingTable.append({})
    parsingTable[4]['('] = Action('shift', 4, None)
    parsingTable[4][')'] = Action('reduce', None, 2)
    parsingTable[4]['P'] = Action('goto', 6, None)
    parsingTable[4]['hasReductions'] = True
    parsingTable[4]['hasShifts'] = True
    parsingTable.append({})
    parsingTable[5]['$'] = Action('reduce', None, 1)
    parsingTable[5]['hasReductions'] = True
    parsingTable.append({})
    parsingTable[6][')'] = Action('shift', 7, None)
    parsingTable[6]['hasShifts'] = True
    parsingTable.append({})
    parsingTable[7][')'] = Action('reduce', None, 3)
    parsingTable[7]['hasReductions'] = True
    
    rules = [Rule('S\'', 1), Rule('S', 3), Rule('P', 0), Rule('P', 3)]'''
    
    # Q1
    parsingTable.append({})
    parsingTable[0]['next::subClassOf'] = Action('shift', 2, None)
    parsingTable[0]['next::type'] = Action('shift', 3, None)
    parsingTable[0]['S'] = Action('goto', 1, None)
    parsingTable[0]['hasShifts'] = True
    parsingTable.append({})
    parsingTable[1]['$'] = Action('accept', None, None)
    parsingTable[1]['hasAccepts'] = True
    parsingTable.append({})
    parsingTable[2]['next::subClassOf'] = Action('shift', 6, None)
    parsingTable[2]['next-1::subClassOf'] = Action('shift', 5, None)
    parsingTable[2]['next::type'] = Action('shift', 7, None)
    parsingTable[2]['S'] = Action('goto', 4, None)
    parsingTable[2]['hasShifts'] = True
    parsingTable.append({})
    parsingTable[3]['next::subClassOf'] = Action('shift', 10, None)
    parsingTable[3]['next::type'] = Action('shift', 11, None)
    parsingTable[3]['next-1::type'] = Action('shift', 9, None)
    parsingTable[3]['S'] = Action('goto', 8, None)
    parsingTable[3]['hasShifts'] = True
    parsingTable.append({})
    parsingTable[4]['next-1::subClassOf'] = Action('shift', 12, None)
    parsingTable[4]['hasShifts'] = True
    parsingTable.append({})
    parsingTable[5]['$'] = Action('reduce', None, 2)
    parsingTable[5]['hasReductions'] = True
    parsingTable.append({})
    parsingTable[6]['next::subClassOf'] = Action('shift', 6, None)
    parsingTable[6]['next-1::subClassOf'] = Action('shift', 14, None)
    parsingTable[6]['next::type'] = Action('shift', 7, None)
    parsingTable[6]['S'] = Action('goto', 13, None)
    parsingTable[6]['hasShifts'] = True
    parsingTable.append({})
    parsingTable[7]['next::subClassOf'] = Action('shift', 10, None)
    parsingTable[7]['next::type'] = Action('shift', 11, None)
    parsingTable[7]['next-1::type'] = Action('shift', 16, None)
    parsingTable[7]['S'] = Action('goto', 15, None)
    parsingTable[7]['hasShifts'] = True
    parsingTable.append({})
    parsingTable[8]['next-1::type'] = Action('shift', 17, None)
    parsingTable[8]['hasShifts'] = True
    parsingTable.append({})
    parsingTable[9]['$'] = Action('reduce', None, 4)
    parsingTable[9]['hasReductions'] = True
    parsingTable.append({})
    parsingTable[10]['next::subClassOf'] = Action('shift', 6, None)
    parsingTable[10]['next-1::subClassOf'] = Action('shift', 19, None)
    parsingTable[10]['next::type'] = Action('shift', 7, None)
    parsingTable[10]['S'] = Action('goto', 18, None)
    parsingTable[10]['hasShifts'] = True
    parsingTable.append({})
    parsingTable[11]['next::subClassOf'] = Action('shift', 10, None)
    parsingTable[11]['next::type'] = Action('shift', 11, None)
    parsingTable[11]['next-1::type'] = Action('shift', 21, None)
    parsingTable[11]['S'] = Action('goto', 20, None)
    parsingTable[11]['hasShifts'] = True
    parsingTable.append({})
    parsingTable[12]['$'] = Action('reduce', None, 1)
    parsingTable[12]['hasReductions'] = True
    parsingTable.append({})
    parsingTable[13]['next-1::subClassOf'] = Action('shift', 22, None)
    parsingTable[13]['hasShifts'] = True
    parsingTable.append({})
    parsingTable[14]['next-1::subClassOf'] = Action('reduce', None, 2)
    parsingTable[14]['hasReductions'] = True
    parsingTable.append({})
    parsingTable[15]['next-1::type'] = Action('shift', 23, None)
    parsingTable[15]['hasShifts'] = True
    parsingTable.append({})
    parsingTable[16]['next-1::subClassOf'] = Action('reduce', None, 4)
    parsingTable[16]['hasReductions'] = True
    parsingTable.append({})
    parsingTable[17]['$'] = Action('reduce', None, 3)
    parsingTable[17]['hasReductions'] = True
    parsingTable.append({})
    parsingTable[18]['next-1::subClassOf'] = Action('shift', 24, None)
    parsingTable[18]['hasShifts'] = True
    parsingTable.append({})
    parsingTable[19]['next-1::type'] = Action('reduce', None, 2)
    parsingTable[19]['hasReductions'] = True
    parsingTable.append({})
    parsingTable[20]['next-1::type'] = Action('shift', 25, None)
    parsingTable[20]['hasShifts'] = True
    parsingTable.append({})
    parsingTable[21]['next-1::type'] = Action('reduce', None, 4)
    parsingTable[21]['hasReductions'] = True
    parsingTable.append({})
    parsingTable[22]['next-1::subClassOf'] = Action('reduce', None, 1)
    parsingTable[22]['hasReductions'] = True
    parsingTable.append({})
    parsingTable[23]['next-1::subClassOf'] = Action('reduce', None, 3)
    parsingTable[23]['hasReductions'] = True
    parsingTable.append({})
    parsingTable[24]['next-1::type'] = Action('reduce', None, 1)
    parsingTable[24]['hasReductions'] = True
    parsingTable.append({})
    parsingTable[25]['next-1::type'] = Action('reduce', None, 3)
    parsingTable[25]['hasReductions'] = True
    
    rules = [Rule('S\'', 1), Rule('S', 3), Rule('S', 2), Rule('S', 3), Rule('S', 2)]
    
    return parsingTable, rules

def CreateGSS(DG):
    gss = GSS()
    gss.levels.append([])
    
    for key, value in DG.nodes.items():
        gssNode = gss.addNode(0, 0, value, None)

    return gss

def GSS_LR(Q, DG, G):
    parsingTable, rules = CreateParsingTable(G)
    gss = CreateGSS(DG)
    level = 0
    visitedPairs = []
    reductionEdges = []
    answers = []
    changed = False
    
    c = 0;
    while (True):
        
        if level >= len(gss.levels):
            break
        
        gssNodes = gss.levels[level]
        
        print 'Reductions ...'
        
        # Process Reductions
        for index, gssNode in enumerate(gssNodes):
            if 'hasReductions' in parsingTable[gssNode.state]:
                
                for index, edge in enumerate(gssNode.vertex.edges):
                    if edge.edgeLabel in parsingTable[gssNode.state]:
                        action = parsingTable[gssNode.state][edge.edgeLabel]
                        if action.action == 'reduce':
                            rule = rules[action.rule]
                            reductionRoots = gss.up(gssNode, rule.rhsSize)
                            for i, reductionRoot in enumerate(reductionRoots):
                                destinationState = parsingTable[reductionRoot.state][rule.lhs].state
                                predecessor = GSSLink(rule.lhs, reductionRoot)
                                newGssNode = gss.addNode(level, destinationState, gssNode.vertex, predecessor)
                                
                                reductionLabel = reductionRoot.vertex.vertexLabel + rule.lhs + gssNode.vertex.vertexLabel
                                if reductionLabel not in reductionEdges:
                                    reductionEdges.append(reductionLabel)
                                    changed = True
        
        print 'Accepts ...'
        
        # Process Accepts
        for index, gssNode in enumerate(gssNodes):
            if 'hasAccepts' in parsingTable[gssNode.state]:
                if '$' in parsingTable[gssNode.state]:
                    action = parsingTable[gssNode.state]['$']
                    if action.action == 'accept':
                        reductionRoots = gss.up(gssNode, 1)
                        for i, reductionRoot in enumerate(reductionRoots):
                            answer = '(' + reductionRoot.vertex.vertexLabel + ', ' + gssNode.vertex.vertexLabel + ')'
                            if answer not in answers:
                                answers.append(answer)
                                changed = True
                   
        print 'Shifts ...'
                   
        # Process Shifts
        for index, gssNode in enumerate(gssNodes):
            if 'hasShifts' in parsingTable[gssNode.state]:
                for index, edge in enumerate(gssNode.vertex.edges):
                    if edge.edgeLabel in parsingTable[gssNode.state]:
                        action = parsingTable[gssNode.state][edge.edgeLabel]
                        if action.action == 'shift':
                            predecessor = GSSLink(edge.edgeLabel, gssNode)
                            gss.addNode(level + 1, action.state, edge.destination, predecessor)
                            
                            visitedPair = edge.destination.vertexLabel + str(action.state)
                            if visitedPair not in visitedPairs:
                                visitedPairs.append(visitedPair)
                                changed = True
                
        if not changed:
            break;
        
        print str(level) + ": " + str(len(gssNodes))
        
        changed = False
        level += 1
        
        # Retornar triplas (Node, Nao-Terminal, Node)
        
        # Manter consistencia entre o grafo de dados com o algoritmo. Tentar representar como Node X Edge X Nodes
    
    return answers

DG = DataGraph()

from dbWine import *

exampleWine(DG)

# Exemplo 0
'''DG.addNode('a', '(', 'b')
DG.addNode('b', ')', 'c')
DG.addNode('b', '(', 'd')
DG.addNode('d', ')', 'e')
DG.addNode('e', ')', 'f')
DG.addNode('f', ')', 'g')'''

# Exemplo 1

'''DG.addNode('a', '(', 'a')
DG.addNode('a', ')', 'b')
DG.addNode('b', ')', 'c')
DG.addNode('c', ')', 'd')
DG.addNode('d', ')', 'e')'''

# Exemplo 2

'''DG.addNode('a', '(', 'b')
DG.addNode('b', '(', 'c')
DG.addNode('c', '(', 'd')
DG.addNode('d', '(', 'e')
DG.addNode('e', '(', 'f')
DG.addNode('f', ')', 'g')
DG.addNode('g', ')', 'h')
DG.addNode('h', ')', 'i')
DG.addNode('i', ')', 'j')
DG.addNode('j', ')', 'k')
DG.addNode('b', ')', 'c')
DG.addNode('b', ')', 'd')
DG.addNode('b', ')', 'e')
DG.addNode('b', ')', 'f')
DG.addNode('b', ')', 'g')
DG.addNode('b', ')', 'h')
DG.addNode('b', ')', 'i')
DG.addNode('b', ')', 'j')'''

# Exemplo 3

'''DG.addNode('a', '(', 'b')
DG.addNode('b', '(', 'c')
DG.addNode('c', '(', 'a')
DG.addNode('c', ')', 'd')
DG.addNode('d', ')', 'e')
DG.addNode('e', ')', 'd')
DG.addNode('d', ')', 'f')'''

# Exemplo 4

'''DG.addNode('a', '(', 'a')
DG.addNode('a', '(', 'b')
DG.addNode('b', ')', 'b')'''

for label in DG.nodes:
    vertex = DG.nodes[label]
    vertex.edges.append(GraphEdge('$', vertex))

Q = 'QUERY'
G = 'GRAMMAR'

import time
start_time = time.time()

answers = GSS_LR(Q, DG, G)

print answers
print 'Answers: ' + str(len(answers))

print("--- %s seconds ---" % (time.time() - start_time))