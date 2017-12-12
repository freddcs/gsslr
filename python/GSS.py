import time

class GSS:
    def __init__(self):
        self.levels = []
        self.numberOfNodes = 0
        self.reductionIndexes = set();
        
    def addNode(self, level, state, vertex, linkEdge, predecessor):
        if len(self.levels) <= level:
            self.levels.append({});
            
        gssNodes = self.levels[level]
        
        nodeIndex = vertex.vertexLabel + str(state)
        if nodeIndex in gssNodes:
            gssNode = gssNodes[nodeIndex]
            
            if level > 0:
                predecessorIndex = linkEdge + predecessor.nodeIndex
                gssNode.predecessors[predecessorIndex] = GSSLink(linkEdge, predecessor)
        else:
            gssNode = GSSNode(state, vertex, nodeIndex, linkEdge, predecessor)
            gssNode.label = self.numberOfNodes
            gssNodes[nodeIndex] = gssNode
            self.numberOfNodes += 1

        gssNode.up = {}
        
        return gssNode

    def up(self, gssNode, jumps):

        if jumps in gssNode.up:
            return gssNode.up[jumps]

        reductionRoots = []
        
        if jumps > 0:
            gssNodes = []
                
            for predecessorLinkKey in gssNode.predecessors:
                predecessorLink = gssNode.predecessors[predecessorLinkKey]
                gssNodes = gssNodes + self.up(predecessorLink.gssNode, jumps - 1)

            gssNode.up[jumps] = gssNodes
            return gssNodes
        else:
            return [gssNode]
        
    def __repr__(self):
        gss = 'GSS:\n'
        for level, nodes in enumerate(self.levels):
            gss += 'U' + str(level) + ':\n'
            for node in nodes:
                gss += str(nodes[node]) + '\n'
            gss += '\n'
        return gss

class GSSNode:
    def __init__(self, state, vertex, nodeIndex, linkEdge, predecessor):
        self.state = state
        self.vertex = vertex
        self.nodeIndex = nodeIndex
        self.up = {}
        
        self.predecessors = {}
        if state > 0:
            predecessorIndex = linkEdge + predecessor.nodeIndex;
            if predecessorIndex not in self.predecessors:
                self.predecessors[predecessorIndex] = GSSLink(linkEdge, predecessor)
        self.label = 0

    def __repr__(self):
        previous = ''
        for predecessor in self.predecessors:
            previous += predecessor.edgeLabel + '<- v' + str(predecessor.gssNode.label) + ' '
            
        return 'v' + str(self.label) + '(' + self.vertex.vertexLabel + ', I' + str(self.state) + ', [ ' + previous + ']) '
    
class GSSLink:
    def __init__(self, edgeLabel, gssNode):
        self.edgeLabel = edgeLabel
        self.gssNode = gssNode

def CreateGSS(DG):
    gss = GSS()
    
    for key, value in DG.nodes.items():
        gssNode = gss.addNode(0, 0, value, None, None)

    return gss
