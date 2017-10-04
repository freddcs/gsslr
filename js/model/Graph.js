var Graph = function(graph) {

    this.graph = {};
    this.nodes = [];

    this.findEdgesFromNode = function(node) {

        return this.graph[node] === undefined ? [] : this.graph[node];
    };

    this.nodes = [];

    for (var i = 0; i < graph.length; i ++) {

        var graphEdge = graph[i];
        this.nodes.push([0]);
        this.nodes.push(graphEdge[2]);

        if (this.graph[graphEdge[0]] === undefined) {

            this.graph[graphEdge[0]] = [];
        }

        this.graph[graphEdge[0]].push(new GraphEdge(graphEdge[0], graphEdge[1], graphEdge[2]));
    }

    var nodes = this.nodes;
    this.nodes = this.nodes.filter(function(item, pos) {

        return nodes.indexOf(item) === pos;
    });
};