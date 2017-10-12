var lrTable = null;
var algorithm = null;

function query(lrTable, steps) {

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

    var algorithm = new Algorithm(graph, lrTable);
    algorithm.answers = algorithm.query(startNodes, steps);

    return algorithm;
}

function performQuery(steps) {

    algorithm = query(lrTable, steps);

    document.getElementById("answers").innerHTML = "Answers: " + algorithm.answers.toString();

    var gssTraces = '';
    var levels = Object.keys(algorithm.gss.levels).length;

    function printTrace(currentNode, gss) {

        var traces = [];
        for (var k = 0; k < currentNode.previousNodes.length; k++) {

            var previousNodeIndex = currentNode.previousNodes[k];
            var previousNode = gss.find(previousNodeIndex);
            traces.push(printTrace(previousNode, gss));
        }

        var accepted = "";

        if (currentNode.accepted) {

            accepted = " style='color:#FFCC00;font-weigh:bold;'";
        }

        var square = " style='border:1px solid #000;min-width:18px;display:inline-block;text-align:center;padding:3px;'";
        var circle = " style='border:1px solid #000;border-radius:50px;min-width:18px;display:inline-block;text-align:center;padding:3px;'";

        var nodeString = " &larr; <span" + square + ">" + currentNode.edge + "</span> &larr; <span" + accepted + "><span" + circle + ">" + currentNode.node + ", " + currentNode.state + "</span></span>";

        if (traces.length > 0) {

            for (var i = 0; i < traces.length; i++) {

                traces[i] += nodeString;
            }
        }
        else {

            traces = [nodeString];
        }

        return traces;
    }

    for (var i = 0; i < levels - 1; i++) {

        gssTraces += "<div><strong>Level " + i + ":</strong></div>";

        var level = algorithm.gss.levels[i];

        for (var j = 0; j < level.length; j++) {

            var evenOdd = (j % 2) === 0 ? 'even' : 'odd';

            var currentNode = level[j];

            var traces = printTrace(currentNode, algorithm.gss);
            gssTraces += "<div class='" + evenOdd + "'>" + traces.join("</div><div style='margin-top:10px;'>") + "</div>";
        }
    }

    document.getElementById("tracesBase").innerHTML = gssTraces;

    updateGss(algorithm.gss);
}

function continueQuery() {

    var numberOfSteps = parseInt(document.getElementById("numberOfSteps").value);
    if (numberOfSteps < 1) {

        numberOfSteps = 1;
    }

    algorithm.continue(numberOfSteps);

    document.getElementById("answers").innerHTML = "Answers: " + algorithm.answers.toString();

    if (algorithm.infiniteLoop === true) {

        document.getElementById("answers").innerHTML += " - <span style='color:red;'>Infinite loop found</span>";
    }

    var gssTraces = '';
    var levels = Object.keys(algorithm.gss.levels).length;

    for (var i = 0; i < levels - 1; i++) {

        gssTraces += "<div><strong>Level " + i + ":</strong></div>";

        var level = algorithm.gss.levels[i];

        for (var j = 0; j < level.length; j++) {

            var evenOdd = (j % 2) === 0 ? 'even' : 'odd';

            var currentNode = level[j];

            var traces = printTrace(currentNode, algorithm.gss);

            gssTraces += "<div class='" + evenOdd + "'>" + traces.join("</div><div style='margin-top:10px;'>") + "</div>";
        }
    }

    document.getElementById("tracesBase").innerHTML = gssTraces;

    updateGss(algorithm.gss);

    var gssBase = document.getElementById('gssBase');
    gssBase.parentNode.scrollLeft = gssBase.parentNode.scrollWidth;

    var tracesBase = document.getElementById('tracesBase');
    tracesBase.parentNode.scrollTop = tracesBase.parentNode.scrollHeight;

    if (algorithm.completed === true) {

        var bContinue = document.getElementById('bContinue');
        bContinue.innerHTML = 'Completed';
        bContinue.disabled = 'disabled';
    }
}

function printTrace(currentNode, gss) {

    var traces = [];
    for (var k = 0; k < currentNode.previousNodes.length; k++) {

        var previousNodeIndex = currentNode.previousNodes[k];
        var previousNode = gss.find(previousNodeIndex);
        traces.push(printTrace(previousNode, gss));
    }

    var accepted = "";

    if (currentNode.accepted) {

        accepted = " style='color:#FFCC00;font-weigh:bold;'";
    }

    var square = " style='border:1px solid #000;min-width:18px;display:inline-block;text-align:center;padding:3px;'";
    var circle = " style='border:1px solid #000;border-radius:50px;min-width:18px;display:inline-block;text-align:center;padding:3px;'";

    var nodeString = " &larr; <span" + square + ">" + currentNode.edge + "</span> &larr; <span" + accepted + "><span" + circle + ">" + currentNode.node + ", " + currentNode.state + "</span></span>";

    if (traces.length > 0) {

        for (var i = 0; i < traces.length; i++) {

            traces[i] += nodeString;
        }
    }
    else {

        traces = [nodeString];
    }

    return traces;
}

function selectExample() {

    var exampleGraphs = document.getElementById("exampleGraphs");
    var exampleGraph = graphs[parseInt(exampleGraphs.value)];

    var graphText = document.getElementById("graphText");

    graphText.value = '';

    for (var i = 0; i < exampleGraph.length; i++) {

        var edge = exampleGraph[i];
        graphText.value +=  edge[0] + " " + edge[1] + " " + edge[2] + "\n";
    }

    updateGraph();
}

function selectExampleGrammar() {

    var exampleGrammars = document.getElementById("exampleGrammars");
    var exampleGrammar = grammars[parseInt(exampleGrammars.value)];

    var grammarText = document.getElementById("grammarText");

    grammarText.value = '';

    for (var i = 0; i < exampleGrammar.length; i++) {

        var rule = exampleGrammar[i];
        grammarText.value +=  rule[0] + " -> " + rule[1] + "\n";
    }

    updateGrammar();
}

function updateGraph() {

    var graph_div = document.getElementById("graphBase");
    graph_div.innerHTML = '<svg id="graphD3" width="' + graph_div.clientWidth + '" height="' + graph_div.clientHeight + '"></svg>';

    //create somewhere to put the force directed graph
    var svg = d3.select("#graphD3")
        .call(d3.zoom().on("zoom", function () {
            svg.attr("transform", d3.event.transform)
        }));


    svg.height = graph_div.clientHeight;
    svg.width = graph_div.clientWidth;

    svg.innerHTML = '';

    var graphString = document.getElementById("graphText").value;
    var graphData = graphString.split("\n");

    var nodes_data =  [];
    var edges_data = [];
    var links_data = [];

    for (var i = 0; i < graphData.length; i++) {

        var edgeString = graphData[i];

        if (edgeString.trim() !== '') {
            var edgeData = edgeString.split(" ");
            var edgeName = edgeData.join('');

            nodes_data.push({"name":edgeData[0], "label": edgeData[0]});
            nodes_data.push({"name":edgeData[2], "label": edgeData[2]});
            edges_data.push({"name":edgeName, "label": edgeData[1]});

            links_data.push({"source": edgeData[0], "target": edgeName, "start": true});
            links_data.push({"source": edgeName, "target": edgeData[2]});
        }
    }

    nodes_data = nodes_data.filter(function(item, pos) {

        var firstPos = nodes_data.map(function(el) {
            return el.name;
        }).indexOf(item.name);

        return firstPos === pos;
    });

    var allNodes = nodes_data.concat(edges_data);

    var simulation = d3.forceSimulation().nodes(allNodes);

    simulation.force("charge_force", d3.forceManyBody())
        .force("center_force", d3.forceCenter(svg.width / 2, svg.height / 2));

    svg.append("defs").selectAll("marker")
        .data(["seta"])
        .enter().append("marker")
        .attr("id", function(d) { return d; })
        .attr("viewBox", "0 -5 10 10")
        .attr("refX", 23)
        .attr("refY", -5)
        .attr("markerWidth", 6)
        .attr("markerHeight", 6)
        .attr("orient", "auto")
        .append("path")
        .attr("d", "M0,-5L10,0L0,5");

    var link = svg.append("g").selectAll("path")
        .data(links_data)
        .enter().append("path")
        .attr("class", "link")
        .attr("marker-end", function(d) { return d.start ? "" : "url(#seta)"; });

    var node = svg.append("g")
        .attr("class", "nodes")
        .selectAll("circle")
        .data(nodes_data)
        .enter()
        .append("circle")
        .call(d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended));

    var edge = svg.append("g")
        .attr("class", "edges")
        .selectAll("rect")
        .data(edges_data)
        .enter()
        .append("rect")
        .call(d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended));

    var nodeLabel = svg.append("g").selectAll("text")
        .data(nodes_data)
        .enter().append("text")
        .attr("x", "-4px")
        .attr("y", "5px")
        .text(function(d) { return d.label; });

    var edgeLabel = svg.append("g").selectAll("text")
        .data(edges_data)
        .enter().append("text")
        .attr("x", "-4px")
        .attr("y", "5px")
        .text(function(d) { return d.label; });

    function tickActions() {

        link.attr("d", function(d) {
            var dx = d.target.x - d.source.x,
                dy = d.target.y - d.source.y,
                dr = Math.sqrt(dx * dx + dy * dy);
            return "M" + d.source.x + "," + d.source.y + "A" + dr + "," + dr + " 0 0,1 " + d.target.x + "," + d.target.y;
        });

        //update circle positions each tick of the simulation
        /*node
            .attr("cx", function(d) { return d.x; })
            .attr("cy", function(d) { return d.y; });*/

        node.attr("cx", function(d) { return d.x = Math.max(10, Math.min(graph_div.clientWidth - 10, d.x)); })
            .attr("cy", function(d) { return d.y = Math.max(10, Math.min(graph_div.clientHeight - 10, d.y)); });

        edge
            .attr("x", function(d) { return d.x - 10; })
            .attr("y", function(d) { return d.y - 10; })
            .attr("width", function(d) { return 20; })
            .attr("height", function(d) { return 20; });

        //update link positions
        //simply tells one end of the line to follow one node around
        //and the other end of the line to follow the other node around
        link
            .attr("x1", function(d) { return d.source.x; })
            .attr("y1", function(d) { return d.source.y; })
            .attr("x2", function(d) { return d.target.x; })
            .attr("y2", function(d) { return d.target.y; });

        nodeLabel.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
        edgeLabel.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
    }

    simulation.on("tick", tickActions);

    function dragstarted(d) {

        if (!d3.event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
    }

    function dragged(d) {

        d.fx = d3.event.x;
        d.fy = d3.event.y;
    }

    function dragended(d) {

        if (!d3.event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
    }

    //Create the link force
    //We need the id accessor to use named sources and targets
    var link_force =  d3.forceLink(links_data).id(function(d) { return d.name; }).distance(40);

    simulation.force("links", link_force);
}

function updateGrammar() {

    var grammarString = document.getElementById("grammarText").value;
    var grammar = new Grammar(grammarString);
    lrTable = new LRTable(new LRClosureTable(grammar));

    document.getElementById('lrTableView').innerHTML = formatLRTable(lrTable);
}

function updateGss(gss) {

    var levels = Object.keys(gss.levels).length;

    console.log(gss.highestLevelLength);

    document.getElementById("gssBase").innerHTML = "<svg id='gssD3' width='" + (levels * 170 - 100) + "' height='" + (gss.highestLevelLength * 55 + 11) + "'></svg>";

    //create somewhere to put the force directed graph
    var svg = d3.select("#gssD3"),
        width = +svg.attr("width"),
        height = +svg.attr("height");

    svg.innerHTML = '';

    var gssKeys = Object.keys(gss.gss);

    var levels_data = [];
    var nodes_data = [];
    var accepted_nodes_data = [];
    var edges_data = [];
    var links_data = [];

    var level = null;
    var y = 50;
    for (var i = 0; i < gssKeys.length; i++) {

        var gssNode = gss.gss[gssKeys[i]];

        if (level !== gssNode.level) {

            level = gssNode.level;
            y = 50;

            levels_data.push({"name": "U" + level, label: "U" + level, type: "node", "x": 25 + gssNode.level * 170, "y": 10});
        }

        var currentNode = {"name": gssNode.index, label: gssNode.node + ", I" + gssNode.state, type: "node", "x": 25 + gssNode.level * 170, "y": y};

        if (gssNode.accepted) {

            accepted_nodes_data.push(currentNode);
        }
        else {

            nodes_data.push(currentNode);
        }

        var edge = {"name": gssNode.index + "l", label: gssNode.edge, type: "edge", "x": 25 + gssNode.level * 170 - 50, "y": y};
        edges_data.push(edge);

        links_data.push({"source": currentNode, "target": edge});

        for (j = 0; j < gssNode.previousNodes.length; j++) {

            var previousData = nodes_data.filter(function(item, pos) {

                return item.name === gssNode.previousNodes[j];
            })[0];

            links_data.push({"source": edge, "target": previousData});
        }

        y += 50;
    }

    svg.append("defs").selectAll("marker")
        .data(["setaReta"])
        .enter().append("marker")
        .attr("id", function(d) { return d; })
        .attr("viewBox", "0 -5 10 10")
        .attr("refX", 40)
        .attr("refY", 0)
        .attr("markerWidth", 6)
        .attr("markerHeight", 6)
        .attr("orient", "auto")
        .append("path")
        .attr("d", "M0,-5L10,0L0,5");

    var link = svg.append("g").selectAll("line")
        .data(links_data)
        .enter().append("line")
        .attr("class", "link")
        .attr('x1', function(d) { return d.source.x; })
        .attr('y1', function(d) { return d.source.x; })
        .attr('x2', function(d) { return d.target.x; })
        .attr('y2', function(d) { return d.target.x; })
        .attr("marker-end", "url(#setaReta)");

    var levelLabel = svg.append("g").selectAll("text")
        .data(levels_data)
        .enter().append("text")
        .attr("x", "-8px")
        .attr("y", "5px")
        .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; })
        .text(function(d) { return d.label; });

    var node = svg.append("g")
        .attr("class", "gssNodes")
        .selectAll("circle")
        .data(nodes_data)
        .enter()
        .append("circle")
        .attr("cx", function(d) { return d.x; }).attr("cy", function(d) { return d.y; });

    var acceptedNode = svg.append("g")
        .attr("class", "acceptedGssNodes")
        .selectAll("circle")
        .data(accepted_nodes_data)
        .enter()
        .append("circle")
        .attr("cx", function(d) { return d.x; }).attr("cy", function(d) { return d.y; });

    var edgeNode = svg.append("g")
        .attr("class", "gssNodes")
        .selectAll("rect")
        .data(edges_data)
        .enter()
        .append("rect")
        .attr("x", function(d) { return d.x - 20; })
        .attr("y", function(d) { return d.y - 20; });

    var nodeLabel = svg.append("g").selectAll("text")
        .data(nodes_data.concat(accepted_nodes_data))
        .enter().append("text")
        .attr("x", "-15px")
        .attr("y", "5px")
        .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; })
        .text(function(d) { return d.label; });

    var edgeLabel = svg.append("g").selectAll("text")
        .data(edges_data)
        .enter().append("text")
        .attr("x", "-4px")
        .attr("y", "5px")
        .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; })
        .text(function(d) { return d.label; });

    //update link positions
    //simply tells one end of the line to follow one node around
    //and the other end of the line to follow the other node around
    link
        .attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });
}

function showPage(page) {

    var graphs = document.getElementById('graphs');
    var grammars = document.getElementById('grammars');
    var process = document.getElementById('process');

    graphs.style.display = 'none';
    grammars.style.display = 'none';
    process.style.display = 'none';

    switch (page) {

        case 1:
            graphs.style.display = 'block';
            break;

        case 2:
            grammars.style.display = 'block';
            break;

        case 3:
            var bContinue = document.getElementById('bContinue');
            bContinue.innerHTML = 'Continue';
            bContinue.disabled = '';
            document.getElementById("numberOfSteps").value = 1;

            performQuery(true);
            process.style.display = 'block';
            break;
    }
}

function toggleTableView() {

    var tableView = document.getElementById('lrTableView');

    if (tableView.style.display === 'none') {

        tableView.style.display = 'block';
    }
    else {

        tableView.style.display = 'none';
    }
}

function initialize() {

    var exampleGraphs = document.getElementById("exampleGraphs");

    exampleGraphs.innerHTML = "";

    for (var i = 0; i < graphs.length; i++) {

        exampleGraphs.innerHTML += "<option value='" + i + "'>Example " + i + "</option>";
    }

    var exampleGrammars = document.getElementById("exampleGrammars");

    exampleGrammars.innerHTML = "";

    for (i = 0; i < grammars.length; i++) {

        exampleGrammars.innerHTML += "<option value='" + i + "'>Example " + i + "</option>";
    }

    var janelas = document.getElementsByClassName('janela');
    for (i = 0; i < janelas.length; i++) {
        janelas[i].style.height = (window.innerHeight - 100) + "px";
    }

    var conteudoJanelas = document.getElementsByClassName('corpo');
    for (i = 0; i < conteudoJanelas.length; i++) {

        conteudoJanelas[i].style.height = (conteudoJanelas[i].parentNode.clientHeight - 115) + "px";
    }

    showPage(1);

    selectExample();
    selectExampleGrammar();
}