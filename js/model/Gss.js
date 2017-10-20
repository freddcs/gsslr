var Gss = function (nodes) {
    this.gss = {};
    this.levels = {};
    this.highestLevelLength = nodes.length;

    this.newNode = function(level, state, edge, node, predecessors) {
        var nodeIndex = level + '-' + state + '-' + edge + "-" + node;
        var gssNode = null;

        if (this.gss[nodeIndex] === undefined) {
            var gssNodeLabel = "v" + Object.keys(this.gss).length;
            var newNode = new GssNode(nodeIndex, gssNodeLabel, level, state, edge, node, predecessors);
            this.gss[nodeIndex] = newNode;

            if (this.levels[level] === undefined) {
                this.levels[level] = [];
            }

            this.levels[level].push(newNode);
        } else {
            gssNode = this.find(nodeIndex);
            var previousNodes = gssNode.previousNodes.concat(predecessors);
            previousNodes = previousNodes.filter(function(item, pos) {
                return previousNodes.indexOf(item) === pos;
            });

            if (arraysIdentical(previousNodes, gssNode.previousNodes)) {
                gssNode = null;
            } else {
                gssNode.previousNodes = previousNodes;
            }
        }

        return gssNode;
    };

    this.level = function(level) {
        if (this.levels[level] === undefined) {
            this.levels[level] = [];
        }

        return this.levels[level];
    };

    this.find = function(gssNodeIndex) {
        return gssNodeIndex === null ? null : this.gss[gssNodeIndex];
    };

    this.up = function (gssNodeIndex, jumps) {
        var gssNode = this.find(gssNodeIndex);

        if (jumps > 0) {
            var nodes = [];

            for (var i = 0; i < gssNode.previousNodes.length; i++) {
                nodes = nodes.concat(this.up(gssNode.previousNodes[i], jumps - 1));
            }

            return nodes;
        }

        return [gssNode];
    };

    for (var i = 0; i < nodes.length; i++) {
        this.newNode(0, 0, "", nodes[i], []);
    }
};