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
        
def addGraphNode(graph, source, edge, destination):
    if source not in graph:
        graph[source] = []
        
    graph[source].append(GraphNode(source, edge, destination))
                             
    return
