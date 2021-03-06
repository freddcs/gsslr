from LR import *
from Examples import *
from GSS import *

def GSS_LR(DG, parsingTable, rules):
    gss = CreateGSS(DG)
    
    level = 0
    visitedPairs = set()
    reductionEdges = set()
    answers = set()

    while (True):
        changed = False

        if level >= len(gss.levels):
            break
        
        gssNodes = gss.levels[level]
        nodeKeys = gssNodes.keys()

        if processReduces(gssNodes, nodeKeys, set(), parsingTable, rules, gss, level, reductionEdges) == True:
            changed = True

        if processAccepts(level, gssNodes, parsingTable, gss, answers) == True:
            changed = True
        
        if processShifts(gssNodes, parsingTable, gss, level, visitedPairs) == True:
            changed = True

        if not changed:
            break;
        

        level += 1

        # Retornar triplas (Node, Nao-Terminal, Node)
        # Manter consistencia entre o grafo de dados com o algoritmo. Tentar representar como Node X Edge X Nodes
    
    return gss, answers

# Process Reductions
def processReduces(gssNodes, nodeKeys, addedNodesKeys, parsingTable, rules, gss, level, reductionEdges):
    changed = False
    newNodesKeys = set()
    for nodeIndex in nodeKeys:
        gssNode = gssNodes[nodeIndex]
        for edge in gssNode.vertex.edges:
            if edge.edgeLabel in parsingTable[gssNode.state]:
                for action in parsingTable[gssNode.state][edge.edgeLabel]:
                    if action.action == 'reduce':
                        rule = rules[action.rule]
                        reductionRoots = gss.up(gssNode, rule.rhsSize)

                        for reductionRoot in reductionRoots:
                            destinationState = parsingTable[reductionRoot.state][rule.lhs][0].state

                            reductionIndex = str(level) + '-' +  str(destinationState) + '-' + gssNode.nodeIndex + '-' + rule.lhs + '-' + reductionRoot.nodeIndex
                            if reductionIndex not in gss.reductionIndexes:
                                gss.reductionIndexes.add(reductionIndex)
                                
                                newGssNode = gss.addNode(level, destinationState, gssNode.vertex, rule.lhs, reductionRoot)

                                newNodeIndex = gssNode.vertex.vertexLabel + str(destinationState)

                                reductionLabel = reductionRoot.vertex.vertexLabel + str(reductionRoot.state) + rule.lhs + gssNode.vertex.vertexLabel + str(gssNode.state)
                                if reductionLabel not in reductionEdges:
                                    reductionEdges.add(reductionLabel)
                                    changed = True

                                newNodesKeys.add(newGssNode.nodeIndex)

    if len(newNodesKeys) > 0:
        addedNodesKeys = addedNodesKeys.union(newNodesKeys)
        if processReduces(gssNodes, newNodesKeys, addedNodesKeys, parsingTable, rules, gss, level, reductionEdges) == True:
            changed = True

    return changed

# Process Accepts
def processAccepts(level, gssNodes, parsingTable, gss, answers):
    changed = False
    for nodeIndex in gssNodes:
        gssNode = gssNodes[nodeIndex]
        if '$' in parsingTable[gssNode.state]:
            for action in parsingTable[gssNode.state]['$']:
                if action.action == 'accept':
                    reductionRoots = gss.up(gssNode, 1)
                    for reductionRoot in reductionRoots:
                        answer = '(' + reductionRoot.vertex.vertexLabel + ', ' + gssNode.vertex.vertexLabel + ')'
                        if answer not in answers:
                            answers.add(answer)
                            changed = True
    return changed

# Process Shifts
def processShifts(gssNodes, parsingTable, gss, level, visitedPairs):
    changed = False
    for nodeIndex in gssNodes:
        gssNode = gssNodes[nodeIndex]
        for edge in gssNode.vertex.edges:
            if edge.edgeLabel in parsingTable[gssNode.state]:
                for action in parsingTable[gssNode.state][edge.edgeLabel]:
                    if action.action == 'shift':
                        gss.addNode(level + 1, action.state, edge.destination, edge.edgeLabel, gssNode)

                        visitedPair = gssNode.vertex.vertexLabel + str(gssNode.state) + str(edge.destination.vertexLabel) + str(action.state)
                        if visitedPair not in visitedPairs:
                            visitedPairs.add(visitedPair)
                            changed = True
    return changed
