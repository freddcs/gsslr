var Algorithm = function(graph, lrTable) {

    this.graph = graph;
    this.lrTable = lrTable;
    this.answers = [];
    this.level = 0;
    this.loopCounter = 0;
    this.stepping = false;

    this.query = function(nodes, steps) {

        this.stepping = steps;
        this.completed = false;
        this.infiniteLoop = false;

        this.gss = new Gss(nodes);
        var actions = this.evalLevel();

        var answers = this.answers;
        this.answers = answers.filter(function(item, pos) {

            return answers.indexOf(item) === pos;
        });


        return actions;
    };

    this.continue = function(numberOfSteps) {

        var actions = [];

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

    this.processReduction = function(action, gssNode) {

        var rule = this.lrTable.grammar.rules[action.actionValue];

        // Go back |RHS| nodes in the GSS
        var stepsToReturn = rule.development.length;
        if (stepsToReturn === 1 && rule.development[0] === "''") {

            stepsToReturn = 0;
        }

        var reductionRoots = this.gss.up(gssNode.index, stepsToReturn);

        for (var i = 0; i < reductionRoots.length; i++) {

            var reductionRoot = reductionRoots[i];

            var goto = this.lrTable.states[reductionRoot.state][rule.nonterminal][0];

            // Create a new node with the result of the goto from the
            // parsing table, labeled after the LHS and same with
            // destination as the original GSS node.
            this.gss.newNode(gssNode.level, goto.actionValue, rule.nonterminal, gssNode.node, [reductionRoot.index]);
        }
    };

    this.addAnswers = function(answerGssNode, gssNode) {

        if (gssNode === null || gssNode === undefined) {

            gssNode = answerGssNode;
        }

        for (j = 0; j < gssNode.previousNodes.length; j++) {

            var previousGssNode = this.gss.find(gssNode.previousNodes[j]);

            if (previousGssNode.previousNodes.length === 0) {

                this.answers.push("(" + previousGssNode.node + ", " + answerGssNode.node + ")");
            }
            else {

                for (k = 0; k < previousGssNode.previousNodes.length; k++) {

                    this.addAnswers(answerGssNode, previousGssNode);
                }
            }
        }
    };

    this.evalLevel = function() {

        var actions = {reductions: [], accepts: [], shifts: []};

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

                        actions.reductions.push({gssNode: gssNode, graphEdge: graphEdge, action: action[0]});
                        this.processReduction(action[0], gssNode);
                    }
                }
            }

            action = this.lrTable.states[gssNode.state];
            if (action !== undefined) {

                action = action['$'];
                if (action !== undefined && action[0].actionType === 'r' && action[0].actionValue !== 0) {

                    actions.reductions.push({gssNode: gssNode, graphEdge: {node: gssNode.node, label: '$', destination: ''}, action: action[0]});
                    this.processReduction(action[0], gssNode);
                }
            }
        }

        var gssLevelString = [];

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

            gssLevelString.push(gssNode.state + "" + gssNode.edge + "" + gssNode.node + "" + gssNode.accepted);
        }

        var gssLevelHash = gssLevelString.join(', ');

        var duplicated = this.gss.registerLevel(gssLevelHash, this.level);

        if (duplicated === true) {

            this.loopCounter ++;
        }
        else {

            this.loopCounter = 0;
        }

        var currentLevelLength = this.gss.level(this.level).length;

        if (this.gss.highestLevelLength < currentLevelLength) {

            this.gss.highestLevelLength = currentLevelLength;
        }

        if (1 === 2 && this.loopCounter >= this.lrTable.longestRhs) {

            console.log("** LOOP INFINITO ENCONTRADO! **");
            this.infiniteLoop = true;
            this.completed = true;
        }
        else {

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
                        }
                    }
                }
            }

            this.level++;
            if (shouldContinue === true) {

                if (this.stepping === false) {

                    this.evalLevel();
                }
            }
            else {

                this.completed = true;
            }
        }

        return actions;
    };
};