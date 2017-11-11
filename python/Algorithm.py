from LR import *
from Examples import *
from GSS import *

def GSS_LR(DG, parsingTable, rules):
    gss = CreateGSS(DG)
    
    level = 0
    visitedPairs = set()
    reductionEdges = set()
    answers = set()
    changed = False
    
    while (True):
        if level >= len(gss.levels):
            break
        
        gssNodes = gss.levels[level]
        nodeKeys = gssNodes.keys()
        
        # Process Reductions
        for nodeIndex in nodeKeys:
            gssNode = gssNodes[nodeIndex]
            for edge in gssNode.vertex.edges:
                if edge.edgeLabel in parsingTable[gssNode.state]:
                    action = parsingTable[gssNode.state][edge.edgeLabel]
                    if action.action == 'reduce':
                        rule = rules[action.rule]
                        reductionRoots = gss.up(gssNode, rule.rhsSize)
                        
                        for reductionRoot in reductionRoots:
                            destinationState = parsingTable[reductionRoot.state][rule.lhs].state
                            
                            predecessor = GSSLink(rule.lhs, reductionRoot)
                            newGssNode = gss.addNode(level, destinationState, gssNode.vertex, predecessor)
                            newNodeIndex = gssNode.vertex.vertexLabel + str(destinationState)
                            if newNodeIndex not in nodeKeys:
                                nodeKeys.append(newNodeIndex)
                            
                            reductionLabel = reductionRoot.vertex.vertexLabel + rule.lhs + gssNode.vertex.vertexLabel
                            if reductionLabel not in reductionEdges:
                                reductionEdges.add(reductionLabel)
                                changed = True

        # Process Accepts
        for nodeIndex in gssNodes:
            gssNode = gssNodes[nodeIndex]
            if '$' in parsingTable[gssNode.state]:
                action = parsingTable[gssNode.state]['$']
                if action.action == 'accept':
                    reductionRoots = gss.up(gssNode, 1)
                    for reductionRoot in reductionRoots:
                        answer = '(' + reductionRoot.vertex.vertexLabel + ', ' + gssNode.vertex.vertexLabel + ')'
                        if answer not in answers:
                            answers.add(answer)
                            changed = True
        
        # Process Shifts
        for nodeIndex in gssNodes:
            gssNode = gssNodes[nodeIndex]
            for edge in gssNode.vertex.edges:
                if edge.edgeLabel in parsingTable[gssNode.state]:
                    action = parsingTable[gssNode.state][edge.edgeLabel]
                    if action.action == 'shift':
                        predecessor = GSSLink(edge.edgeLabel, gssNode)
                        gss.addNode(level + 1, action.state, edge.destination, predecessor)
                        
                        visitedPair = edge.destination.vertexLabel + str(action.state)
                        if visitedPair not in visitedPairs:
                            visitedPairs.add(visitedPair)
                            changed = True

        if not changed:
            break;
        
        changed = False
        level += 1
        
        # Retornar triplas (Node, Nao-Terminal, Node)
        # Manter consistencia entre o grafo de dados com o algoritmo. Tentar representar como Node X Edge X Nodes
    
    return answers
