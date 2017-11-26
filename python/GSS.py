import time

class GSS:
    def __init__(self):
        self.levels = []
        self.numberOfNodes = 0
        
    def addNode(self, level, state, vertex, predecessor):
        if len(self.levels) <= level:
            self.levels.append({});
            
        gssNodes = self.levels[level]
        
        nodeIndex = vertex.vertexLabel + str(state)
        if nodeIndex in gssNodes:
            gssNode = gssNodes[nodeIndex]
            
            if level > 0:
                gssNode.predecessors.add(predecessor)
        else:
            gssNode = GSSNode(state, vertex, predecessor)
            gssNode.label = self.numberOfNodes
            gssNodes[nodeIndex] = gssNode
            self.numberOfNodes += 1
        
        return gssNode
    
    def up(self, gssNode, jumps):
        reductionRoots = []
        
        if jumps > 0:
            gssNodes = []
            for predecessorLink in gssNode.predecessors:
                gssNodes = gssNodes + self.up(predecessorLink.gssNode, jumps - 1)
                
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
    def __init__(self, state, vertex, predecessor):
        self.state = state
        self.vertex = vertex
        
        self.predecessors = set()
        if state > 0:
            self.predecessors.add(predecessor)
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
        self.hash = hash(edgeLabel + gssNode.vertex.vertexLabel + str(gssNode.state))
    
    def __hash__(self):
        return self.hash
    
    def __eq__(self, other):
        return (self.hash == other.hash)
    
def CreateGSS(DG):
    gss = GSS()
    
    for key, value in DG.nodes.items():
        gssNode = gss.addNode(0, 0, value, None)

    return gss
