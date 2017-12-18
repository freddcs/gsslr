var Algorithm = function(graph, lrTable) {
    this.graph = graph;
    this.lrTable = lrTable;
    this.answers = [];
    this.level = 0;
    this.stepping = false;
    this.completed = false;
    this.gss = null;
    this.vertexNode = null;

    var verifyAddedNewAction = function(vertexNode, vertex, state, label, previousVertex, previousState) {
        var newAction = false;

        vertex = '' + vertex;
        state = '' + state;
        previousVertex = '' + previousVertex;
        previousState = '' + previousState;

        if (vertexNode[vertex] === undefined) {
            vertexNode[vertex] = {};
        }

        if (vertexNode[vertex][state] === undefined) {
            vertexNode[vertex][state] = {};
        }

        if (vertexNode[vertex][state][label] === undefined) {
            vertexNode[vertex][state][label] = {};
        }

        if (vertexNode[vertex][state][label][previousVertex] === undefined) {
            vertexNode[vertex][state][label][previousVertex] = {};
        }

        if (vertexNode[vertex][state][label][previousVertex][previousState] !== true) {
            newAction = true;
            vertexNode[vertex][state][label][previousVertex][previousState] = true;
        }

        return newAction;
    };

    this.verifyAddedNewAction = verifyAddedNewAction;

    this.prepareQuery = function(nodes, stepping) {
        this.stepping = stepping;
        this.completed = false;
        this.infiniteLoop = false;
        var vertexNode = {};
        this.vertexNode = vertexNode;

        nodes.forEach(function(n) { verifyAddedNewAction(vertexNode, n, 0, 'Init', 'Init', 'Init'); });

        this.gss = new Gss(nodes);
    };

    this.continue = function(stepping, numberOfSteps) {
        var actions = [];

        if (!stepping) {
            numberOfSteps = 1;
        }

        this.stepping = stepping;

        for (var i = 0; i < numberOfSteps; i++) {
            actions = this.evalLevel();

            if (this.completed === true) {
                break;
            }
        }

        var answers = this.answers;
        this.answers = answers.filter(function(item, pos) {
            return answers.indexOf(item) === pos;
        });

        return actions;
    };

    this.processReduction = function(action, gssNode, newActionFound) {
        var rule = this.lrTable.grammar.rules[action.actionValue];

        // Go back |RHS| nodes in the GSS
        var stepsToReturn = rule.development.length;
        if (stepsToReturn === 1 && rule.development[0] === "''") {
            stepsToReturn = 0;
        }

        var reductionRoots = this.gss.up(gssNode.index, stepsToReturn);

        var repeatedNodes = [];

        for (var i = 0; i < reductionRoots.length; i++) {
            var reductionRoot = reductionRoots[i];

            var goto = this.lrTable.states[reductionRoot.state][rule.nonterminal][0];

            // Create a new node with the result of the goto from the
            // parsing table, labeled after the LHS and same with
            // destination as the original GSS node.
            var repeated = this.gss.newNode(gssNode.level, goto.actionValue, rule.nonterminal, gssNode.node, [reductionRoot.index]);

            if (repeated !== null) {
                repeatedNodes.push(repeated);
            }

            var auxNewActionFound = this.verifyAddedNewAction(this.vertexNode, gssNode.node, goto.actionValue, rule.nonterminal, reductionRoot.node, reductionRoot.state);
            if (!newActionFound) { newActionFound = auxNewActionFound; }
        }

        repeatedNodes = repeatedNodes.filter(function(item, pos) {
            return repeatedNodes.indexOf(item) === pos;
        });

        return {action: newActionFound, repeated: repeatedNodes, reductionRoots: reductionRoots};
    };

    this.addAnswers = function(answerGssNode, gssNode) {
        if (gssNode === null || gssNode === undefined) {
            gssNode = answerGssNode;
        }

        for (j = 0; j < gssNode.previousNodes.length; j++) {
            var previousGssNode = this.gss.find(gssNode.previousNodes[j]);

            if (previousGssNode.previousNodes.length === 0) {
                this.answers.push("(" + previousGssNode.node + ", " + answerGssNode.node + ")");
            } else {
                for (k = 0; k < previousGssNode.previousNodes.length; k++) {
                    this.addAnswers(answerGssNode, previousGssNode);
                }
            }
        }
    };

    this.evalLevel = function() {
        var actions = {reductions: [], accepts: [], shifts: []};
        var newActionFound = false;

        if (this.completed === true) {
            return;
        }

        var shouldContinue = false;

        var gssNodes = this.gss.level(this.level);

        // Search for reductions
        for (var i = 0; i < gssNodes.length; i++) {
            var gssNode = gssNodes[i];
            var graphEdges = this.graph.findEdgesFromNode(gssNode.node);

            for (var j = 0; j < graphEdges.length; j++) {
                var graphEdge = graphEdges[j];

                var action = this.lrTable.states[gssNode.state];
                if (action !== undefined) {
                    action = action[graphEdge.label];

                    if (action !== undefined && action[0].actionType === 'r' && action[0].actionValue !== 0) {
                        var reduction = this.processReduction(action[0], gssNode, newActionFound);

                        reduction.reductionRoots.forEach(function(r) {
                            actions.reductions.push({gssNode: gssNode, graphEdge: {destination: graphEdge.destination, label: graphEdge.label, node: graphEdge.node, reductionRoot: r.node}, action: action[0]});
                        });

                        newActionFound = reduction.action;

                        if (reduction.repeated.length > 0) {
                            gssNodes = gssNodes.concat(reduction.repeated);
                        }
                    }
                }
            }

            action = this.lrTable.states[gssNode.state];
            if (action !== undefined) {
                action = action['$'];
                if (action !== undefined && action[0].actionType === 'r' && action[0].actionValue !== 0) {
                    reduction = this.processReduction(action[0], gssNode);

                    reduction.reductionRoots.forEach(function(r) {
                        actions.reductions.push({gssNode: gssNode, graphEdge: {destination: '', label: '$', node: gssNode.node, reductionRoot: r.node}, action: action[0]});
                    });

                    newActionFound = reduction.action;

                    if (reduction.repeated.length > 0) {
                        gssNodes = gssNodes.concat(reduction.repeated);
                    }
                }
            }
        }

        gssNodes = this.gss.level(this.level);

        // Search for accepts
        for (i = 0; i < gssNodes.length; i++) {
            gssNode = gssNodes[i];
            var acceptAction = this.lrTable.states[gssNode.state];

            if (acceptAction !== undefined) {
                acceptAction = acceptAction['$'];

                if (acceptAction !== undefined && acceptAction[0].actionType === 'r' && acceptAction[0].actionValue === 0) {
                    actions.accepts.push({gssNode: gssNode});
                    this.addAnswers(gssNode, null);
                    gssNode.accepted = true;
                }
            }
        }

        var currentLevelLength = this.gss.level(this.level).length;

        if (this.gss.highestLevelLength < currentLevelLength) {
            this.gss.highestLevelLength = currentLevelLength;
        }

        gssNodes = this.gss.level(this.level);

        // Search for shifts
        for (i = 0; i < gssNodes.length; i++) {
            gssNode = gssNodes[i];

            graphEdges = this.graph.findEdgesFromNode(gssNode.node);
            for (j = 0; j < graphEdges.length; j++) {
                graphEdge = graphEdges[j];

                action = this.lrTable.states[gssNode.state];
                if (action !== undefined) {
                    action = action[graphEdge.label];

                    if (action !== undefined && action[0].actionType === 's') {
                        actions.shifts.push({gssNode: gssNode, graphEdge: graphEdge});
                        this.gss.newNode(gssNode.level + 1, action[0].actionValue, graphEdge.label, graphEdge.destination, [gssNode.index]);
                        shouldContinue = true;
                        var auxNewActionFound = this.verifyAddedNewAction(this.vertexNode, graphEdge.destination, action[0].actionValue, graphEdge.label, gssNode.node, gssNode.state);
                        if (!newActionFound) { newActionFound = auxNewActionFound }
                    }
                }
            }
        }

        // TODO Remover este teste
        newActionFound = true;
        
        if (!newActionFound) {
            console.log("** LOOP INFINITO ENCONTRADO! **");
            this.infiniteLoop = true;
            this.completed = true;
        } else {
            this.level++;
            if (shouldContinue === true) {
                if (this.stepping === false) {
                    this.evalLevel();
                }
            } else {
                this.completed = true;
            }
        }

        return actions;
    };
};
