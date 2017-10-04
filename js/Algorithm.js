var Algorithm = function(graph, lrTable) {

    this.graph = graph;
    this.lrTable = lrTable;

    this.query = function(nodes) {

        this.gss = new Gss(nodes);
        var answers = this.evalLevel(0, 0);
        return answers.filter(function(item, pos) {

            return answers.indexOf(item) === pos;
        });
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

    this.evalLevel = function(level, loopCounter) {
        var answers = [];
        var shouldContinue = false;

        var gssNodes = this.gss.level(level);

        for (var i = 0; i < gssNodes.length; i++) {

            var gssNode = gssNodes[i];
            var graphEdges = this.graph.findEdgesFromNode(gssNode.node);

            for (var j = 0; j < graphEdges.length; j++) {

                var graphEdge = graphEdges[j];

                var action = this.lrTable.states[gssNode.state];
                if (action !== undefined) {
                    action = action[graphEdge.label];

                    if (action !== undefined && action[0].actionType === 'r' && action[0].actionValue !== 0) {

                        this.processReduction(action[0], gssNode);
                    }
                }
            }

            action = this.lrTable.states[gssNode.state];
            if (action !== undefined) {

                action = action['$'];
                if (action !== undefined && action[0].actionType === 'r' && action[0].actionValue !== 0) {

                    this.processReduction(action[0], gssNode);
                }
            }
        }

        var gssLevelString = [];

        gssNodes = this.gss.level(level);

        for (i = 0; i < gssNodes.length; i++) {

            gssNode = gssNodes[i];
            var acceptAction = this.lrTable.states[gssNode.state];

            if (acceptAction !== undefined) {

                acceptAction = acceptAction['$'];

                if (acceptAction !== undefined && acceptAction[0].actionType === 'r' && acceptAction[0].actionValue === 0) {

                    for (j = 0; j < gssNode.previousNodes.length; j++) {

                        var previousGssNode = this.gss.find(gssNode.previousNodes[j]);
                        answers.push("(" + previousGssNode.node + ", " + gssNode.node + ")");
                    }
                    gssNode.accepted = true;
                }
            }


            gssLevelString.push(gssNode.state + "" + gssNode.edge + "" + gssNode.node + "" + gssNode.accepted);
        }

        var gssLevelHash = gssLevelString.join(', ');

        var duplicated = this.gss.registerLevel(gssLevelHash, level);

        if (duplicated === true) {

            loopCounter ++;
        }
        else {

            loopCounter = 0;
        }

        if (loopCounter >= this.lrTable.longestRhs) {

            console.log("** LOOP INFINITO ENCONTRADO! **");
        }
        else {

            gssNodes = this.gss.level(level);

            for (i = 0; i < gssNodes.length; i++) {

                gssNode = gssNodes[i];

                graphEdges = this.graph.findEdgesFromNode(gssNode.node);
                for (j = 0; j < graphEdges.length; j++) {

                    graphEdge = graphEdges[j];

                    action = this.lrTable.states[gssNode.state];
                    if (action !== undefined) {

                        action = action[graphEdge.label];

                        if (action !== undefined && action[0].actionType === 's') {

                            this.gss.newNode(gssNode.level + 1, action[0].actionValue, graphEdge.label, graphEdge.destination, [gssNode.index]);
                            shouldContinue = true;
                        }
                    }
                }
            }

            if (shouldContinue === true) {

                answers = answers.concat(this.evalLevel(level + 1, loopCounter));
            }
            else {

                console.log ('** PARANDO! **');
            }
        }

        return answers;
    };
};