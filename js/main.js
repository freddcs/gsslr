var lrTable = null;
var algorithm = null;

function query(lrTable) {
    var graphString = document.getElementById('graphText').value;
    var graphData = graphString.split("\n");
    var graphNodes = [];
    var startingNodes = [];

    for (var i = 0; i < graphData.length; i++) {
        var edgeString = graphData[i];

        if (edgeString.trim() !== '') {
            var edgeData = edgeString.split(' ');

            graphNodes.push([edgeData[0], edgeData[1], edgeData[2]]);
            startingNodes.push(edgeData[0]);
            startingNodes.push(edgeData[2]);
        }
    }

    var graph = new Graph(graphNodes);

    var startingNodesString = document.getElementById('startingNodes').value;
    
    if (startingNodesString !== '') {
        startingNodes = startingNodesString.split(' ');
    }

    startingNodes = startingNodes.filter(function(item, pos) {
        return startingNodes.indexOf(item) === pos;
    });

    var algorithm = new Algorithm(graph, lrTable);

    algorithm.prepareQuery(startingNodes, true);

    return algorithm;
}

function performQuery() {
    algorithm = query(lrTable);

    document.getElementById("answers").innerHTML = "Answers: " + algorithm.answers.toString();

    var gssTraces = '';
    var levels = Object.keys(algorithm.gss.levels).length;

    for (var i = 0; i < levels - 1; i++) {
        gssTraces += "<div><strong>Level " + i + ":</strong></div>";

        var level = algorithm.gss.levels[i];

        for (var j = 0; j < level.length; j++) {
            var evenOdd = (j % 2) === 0 ? 'even' : 'odd';
            var currentNode = level[j];
            var traces = printTraces(currentNode, algorithm.gss);
            gssTraces += "<div class='" + evenOdd + "'>" + traces.join("</div><div style='margin-top:10px;'>") + "</div>";
        }
    }

    document.getElementById("tracesBase").innerHTML = gssTraces;

    highlightVertices(algorithm);

    updateGss(algorithm.gss);
}

function continueQuery(stepping) {
    var numberOfSteps = parseInt(document.getElementById("numberOfSteps").value);
    if (numberOfSteps < 1) {
        numberOfSteps = 1;
    }

    registerActions(algorithm.continue(stepping, numberOfSteps), algorithm.level - 1);
    highlightVertices(algorithm);

    document.getElementById("answers").innerHTML = "Answers: " + algorithm.answers.toString();

    if (algorithm.infiniteLoop === true) {
        document.getElementById("answers").innerHTML += " - <span style='color:red;'>Infinite loop found</span>";
    }

    var currentLevel = algorithm.level - 1;
    document.getElementById("tracesBase").innerHTML += "<div><strong>Level " + currentLevel + ":</strong></div>";

    var level = algorithm.gss.levels[currentLevel];

    for (var j = 0; j < level.length; j++) {
        var evenOdd = (j % 2) === 0 ? 'even' : 'odd';
        var currentNode = level[j];
        var traces = printTraces(currentNode, algorithm.gss);
        document.getElementById("tracesBase").innerHTML += "<div class='" + evenOdd + "'>" + traces.join("</div><div style='margin-top:10px;'>") + "</div>";
    }

    updateGss(algorithm.gss);

    var gssBase = document.getElementById('gssBase');
    gssBase.parentNode.scrollLeft = gssBase.parentNode.scrollWidth;

    var tracesBase = document.getElementById('tracesBase');
    tracesBase.parentNode.scrollTop = tracesBase.parentNode.scrollHeight;

    if (algorithm.completed === true) {
        var bContinue = document.getElementById('bContinue');
        bContinue.innerHTML = 'Completed';
        bContinue.disabled = 'disabled';

        var bResume = document.getElementById('bResume');
        bResume.innerHTML = 'Completed';
        bResume.disabled = 'disabled';
    }
}

function highlightVertices(algorithm) {
    var currentLevel = algorithm.level;

    algorithm.gss.level(currentLevel - 1).forEach(function(n) {
        d3.select("#smallGraphBase_" + n.node).attr('style', '');

        if (algorithm.lrTable.grammar.nonterminals.includes(n.edge)) {

        }
    });

    algorithm.gss.level(currentLevel).forEach(function(n) {
        d3.select("#smallGraphBase_" + n.node).attr('style', 'stroke:#00A;fill:#EEF');
    });
}

function registerActions(actions, level) {
    var debugBase = document.getElementById('debugBase');

    debugBase.innerHTML += '<div><strong>Level U' + level + ':</strong></div>';

    var reductions = '';
    var accepts = '';
    var shifts = '';
    var i = 0;

    if (actions.reductions.length > 0) {
        actions.reductions.forEach(function(r) {
            var rule = algorithm.lrTable.grammar.rules[r.action.actionValue];
            var rhs = rule.development.join(' ');
            if (rhs === "''") {
                rhs = '&lambda;';
            }

            reductions += '<tr' + (i++ % 2 === 0 ? ' class="even"' : '') + '><td>' + r.gssNode.label + '</td><td>i' + r.gssNode.state + '</td><td>'
                + r.graphEdge.node + '</td><td>' + r.graphEdge.label + '</td><td>' + r.graphEdge.destination + '</td><td>REDUCE</td><td>'
                + 'r' + r.action.actionValue + ': ' + rule.nonterminal + ' &rarr; ' + rhs
                + '</td></tr>';
        });
    }

    if (actions.accepts.length > 0) {
        actions.accepts.forEach(function(a) {
            accepts += '<tr' + (i++ % 2 === 0 ? ' class="even"' : '') + '><td>' + a.gssNode.label + '</td><td>i' + a.gssNode.state + '</td><td>' + a.gssNode.node + '</td><td>$</td><td>&nbsp;</td><td>ACCEPT</td><td>&nbsp;</td></tr>';
        });
    }

    if (actions.shifts.length > 0) {
        actions.shifts.forEach(function(s) {
            accepts += '<tr' + (i++ % 2 === 0 ? ' class="even"' : '') + '><td>' + s.gssNode.label + '</td><td>i' + s.gssNode.state + '</td><td>' + s.gssNode.node + '</td><td>' + s.graphEdge.label + '</td><td>' + s.graphEdge.destination + '</td><td>SHIFT</td><td>&nbsp;</td></tr>';
        });
    }

    if (reductions !== '' || accepts !== '' || shifts !== '') {
        debugBase.innerHTML +=
            '<table class="actionsTable"><thead><tr><th>Node</th><th>State</th><th>Origin</th><th>Edge</th><th>Destination</th><th>Action</th><th>Details</th></tr></thead><tbody>'
            + reductions + accepts + shifts
            + '</tbody></table>';
    }

    debugBase.parentNode.scrollTop = debugBase.parentNode.scrollHeight;
}

function printTraces(currentNode, gss) {
    var traces = [];
    for (var k = 0; k < currentNode.previousNodes.length; k++) {
        var previousNodeIndex = currentNode.previousNodes[k];
        var previousNode = gss.find(previousNodeIndex);
        traces.push(printTraces(previousNode, gss));
    }

    var accepted = "";

    if (currentNode.accepted) {
        accepted = " style='color:#00CC00;font-weigh:bold;'";
    }

    var square = " style='border:1px solid #000;min-width:18px;display:inline-block;text-align:center;padding:3px;'";
    var circle = " style='border:1px solid #000;border-radius:50px;min-width:18px;display:inline-block;text-align:center;padding:3px;'";

    var nodeString = " &larr; <span" + square + ">" + currentNode.edge + "</span> &larr; <span" + accepted + "><span" + circle + ">" + currentNode.node + ", " + currentNode.state + "</span></span>";

    if (traces.length > 0) {
        for (var i = 0; i < traces.length; i++) {
            traces[i] += nodeString;
        }
    } else {

        traces = [nodeString];
    }

    return traces;
}

function selectExampleGraph() {
    var exampleGraphs = document.getElementById("exampleGraphs");
    var exampleGraph = graphs[parseInt(exampleGraphs.value)].graph;
    var startingNodes = graphs[parseInt(exampleGraphs.value)].startingNodes;
    var graphText = document.getElementById("graphText");
    var startingNodesText = document.getElementById("startingNodes");

    graphText.value = '';

    for (var i = 0; i < exampleGraph.length; i++) {
        var edge = exampleGraph[i];
        graphText.value +=  edge[0] + " " + edge[1] + " " + edge[2] + "\n";
    }

    startingNodesText.value = startingNodes.join(' ');

    updateGraph('graphBase');
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

function updateGraph(graphBaseId) {
    var svgId = graphBaseId + "graphD3";
    var graphBase = document.getElementById(graphBaseId);
    graphBase.innerHTML = '<svg id="' + svgId+ '" width="' + graphBase.clientWidth + '" height="' + graphBase.clientHeight + '"></svg>';

    //create somewhere to put the force directed graph
    var svg = d3.select("#" + svgId)
        .call(d3.zoom().on("zoom", function () {
            svg.attr("transform", d3.event.transform)
        }));


    svg.height = graphBase.clientHeight;
    svg.width = graphBase.clientWidth;

    svg.innerHTML = '';

    var graphString = document.getElementById("graphText").value;
    var graphData = graphString.split("\n");

    var nodes_data = [];
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

    var link = svg.append("g")
        .attr('class', 'links')
        .selectAll("path")
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
        .attr("id", function(d) { return graphBaseId + "_" + d.label; })
        .on("mouseover", mouseover)
        .on("mouseout", mouseout)
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

    // Define the div for the tooltip
    var div = d3.select("#" + graphBaseId).append("div")
        .attr("class", "tooltip")
        .style("opacity", 0);

    function tickActions() {
        link.attr("d", function(d) {
            var dx = d.target.x - d.source.x,
                dy = d.target.y - d.source.y,
                dr = Math.sqrt(dx * dx + dy * dy);
            return "M" + d.source.x + "," + d.source.y + "A" + dr + "," + dr + " 0 0,1 " + d.target.x + "," + d.target.y;
        });

        //update circle positions each tick of the simulation
        node
            .attr("cx", function(d) { return d.x; })
            .attr("cy", function(d) { return d.y; });

        /*node.attr("cx", function(d) { return d.x = Math.max(10, Math.min(graphBase.clientWidth - 10, d.x)); })
            .attr("cy", function(d) { return d.y = Math.max(10, Math.min(graphBase.clientHeight - 10, d.y)); });*/

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

    var dragging = false;
    function mouseover(d) {
        setTimeout(
            function() {
                if (!dragging && algorithm !== null) {
                    var visitedStates = [];

                    var vertexNode = algorithm.vertexNode[d.label];

                    var keyNames = Object.keys(vertexNode);
                    for (var i in keyNames) {
                        var keyNames2 = Object.keys(vertexNode[keyNames[i]]);
                        for (var j in keyNames2) {
                            var keyNames3 = Object.keys(vertexNode[keyNames[i]][keyNames2[j]]);
                            for (var k in keyNames3) {
                                var previousNode = keyNames2[j] === 'Init' ? '' :  '&larr; ' + keyNames2[j] + ' i<sub>' + keyNames3[k] + '</sub>';
                                visitedStates.push(d.label + ': i<sub>' + keyNames[i] + '</sub>' + previousNode);
                            }
                        }
                    }

                    if (visitedStates.length === 0) {
                        visitedStates.push("None");
                    }

                    div.transition().duration(200).style("opacity", .9);
                    div.html(visitedStates.join('<br/>'));
                }
            },
            1000
        );
    }

    function mouseout(d) {
        div.transition()
            .duration(500)
            .style("opacity", 0);
    }

    function dragstarted(d) {
        dragging = true;
        if (!d3.event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
    }

    function dragged(d) {
        dragging = true;
        d.fx = d3.event.x;
        d.fy = d3.event.y;
    }

    function dragended(d) {
        dragging = false;
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

    var tableHtml = formatLRTable(lrTable);
    var rules = [];

    var rCounter = 0;
    lrTable.grammar.rules.forEach(function (r) {
        rules.push('r<sub>' + (rCounter++) + '</sub>: ' + r.nonterminal + ' &rarr; ' + r.development.join(' ').replace("''", '&lambda;'));
    });

    document.getElementById('lrTableView').innerHTML
        = "<div><strong>Grammar:</strong></div><div style='white-space:nowrap;'>" + rules.join('<br/>') + "</div>"
        + "<div>" + tableHtml + "</div>";
}

function updateGss(gss) {
    var levels = Object.keys(gss.levels).length;

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

            levels_data.push({name: "U" + level, label: "U" + level, type: "node", x: 25 + gssNode.level * 170, y: 10});
        }

        var currentNode = {id: gssNode.label, name: gssNode.index, label: gssNode.node + ", i" + gssNode.state, type: "node", x: 25 + gssNode.level * 170, y: y};

        if (gssNode.accepted) {
            accepted_nodes_data.push(currentNode);
        } else {
            nodes_data.push(currentNode);
        }

        var edge = {name: gssNode.index + "l", label: gssNode.edge, type: "edge", x: 25 + gssNode.level * 170 - 50, y: y};
        edges_data.push(edge);

        links_data.push({source: currentNode, target: edge});

        for (j = 0; j < gssNode.previousNodes.length; j++) {
            var previousData = nodes_data.filter(function(item, pos) {
                return item.name === gssNode.previousNodes[j];
            })[0];

            links_data.push({source: edge, target: previousData});
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

    svg.append("g").selectAll("text")
        .data(levels_data)
        .enter().append("text")
        .attr("x", "-8px")
        .attr("y", "5px")
        .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; })
        .text(function(d) { return d.label; });

    svg.append("g")
        .attr("class", "gssNodes")
        .selectAll("circle")
        .data(nodes_data)
        .enter()
        .append("circle")
        .attr("cx", function(d) { return d.x; }).attr("cy", function(d) { return d.y; });

    svg.append("g")
        .attr("class", "acceptedGssNodes")
        .selectAll("circle")
        .data(accepted_nodes_data)
        .enter()
        .append("circle")
        .attr("cx", function(d) { return d.x; }).attr("cy", function(d) { return d.y; });

    svg.append("g")
        .attr("class", "gssNodes")
        .selectAll("rect")
        .data(edges_data)
        .enter()
        .append("rect")
        .attr("x", function(d) { return d.x - 20; })
        .attr("y", function(d) { return d.y - 20; });

    svg.append("g").selectAll("text")
        .data(nodes_data.concat(accepted_nodes_data))
        .enter().append("text")
        .attr("x", "-15px")
        .attr("y", "5px")
        .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; })
        .text(function(d) { return d.label; });

    svg.append("g").selectAll("text")
        .data(nodes_data.concat(accepted_nodes_data))
        .enter().append("text")
        .attr("transform", function(d) { return "translate(" + (d.x + 20) + "," + (d.y - 10) + ")"; })
        .text(function(d) { return d.id; });

    svg.append("g").selectAll("text")
        .data(edges_data)
        .enter().append("text")
        .attr("transform", function(d) { return "translate(" + (d.x - 5) + "," + (d.y + 5) + ")"; })
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
            if (algorithm !== null) { algorithm.vertexNode = {}; }
            break;

        case 2:
            grammars.style.display = 'block';
            break;

        case 3:
            var bContinue = document.getElementById('bContinue');
            bContinue.innerHTML = 'Continue';
            bContinue.disabled = '';

            var bResume = document.getElementById('bResume');
            bResume.innerHTML = 'Resume';
            bResume.disabled = '';

            var bResume = document.getElementById('bResume');
            bResume.disabled = '';

            document.getElementById("numberOfSteps").value = 1;
            document.getElementById('debugBase').innerHTML = '';

            process.style.display = 'block';

            updateGraph('smallGraphBase');
            performQuery();

            break;
    }
}

function toggleView(viewId) {
    var view = document.getElementById(viewId);

    if (view.style.display === 'none') {
        view.style.display = 'block';
    } else {
        view.style.display = 'none';
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

    selectExampleGraph();
    selectExampleGrammar();
}

function arraysIdentical(a, b) {
    var i = a.length;
    if (i != b.length) return false;
    while (i--) {
        if (a[i] !== b[i]) return false;
    }
    return true;
};