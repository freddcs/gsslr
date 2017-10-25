import time

class GSS:
    def __init__(self):
        self.levels = []
        self.numberOfNodes = 0
        
    def addNode(self, level, state, vertex, predecessor):
        if len(self.levels) <= level:
            self.levels.append([]);
            
        gssNodes = self.levels[level]
        
        gssNode = None
        for node in gssNodes:
            if node.state == state and node.vertex.vertexLabel == vertex.vertexLabel:
                gssNode = node
                break;
            
        if gssNode == None:
            gssNode = GSSNode(state, vertex, predecessor)
            gssNode.label = self.numberOfNodes
            gssNodes.append(gssNode)
            self.numberOfNodes += 1
        else:
            if level > 0 and predecessor not in gssNode.predecessors:
                gssNode.predecessors.append(predecessor)
        
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
                gss += str(node) + '\n'
            gss += '\n'
        return gss

class GSSNode:
    def __init__(self, state, vertex, predecessor):
        self.state = state
        self.vertex = vertex
        
        self.predecessors = []
        if state > 0:
            self.predecessors.append(predecessor)
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
        self.hash = edgeLabel + gssNode.vertex.vertexLabel + str(gssNode.state)
    
    def __eq__(self, other):
        return (self.hash == other.hash)

    def __ne__(self, other):
        return not self.__eq__(other)
