function query(lrTable) {

    lrTable.longestRhs = 0;
    lrTable.grammar.rules.forEach(function(r) { if (r.development.length > lrTable.longestRhs) lrTable.longestRhs = r.development.length; });

    var graphString = document.getElementById("graphText").value;
    var graphData = graphString.split("\n");

    var graphNodes =  [];
    var startNodes = [];

    for (var i = 0; i < graphData.length; i++) {

        var edgeString = graphData[i];

        if (edgeString.trim() !== '') {
            var edgeData = edgeString.split(" ");

            graphNodes.push([edgeData[0], edgeData[1], edgeData[2]]);
            startNodes.push(edgeData[0]);
            startNodes.push(edgeData[2]);
        }
    }

    var graph = new Graph(graphNodes);

    startNodes = startNodes.filter(function(item, pos) {
        return startNodes.indexOf(item) === pos;
    });

    console.log(graph);
    console.log(startNodes);
    console.log(lrTable);

    var algorithm = new Algorithm(graph, lrTable);
    algorithm.answers = algorithm.query(startNodes);

    return algorithm;
}