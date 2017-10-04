var Gss = function (nodes) {
    this.gss = {};
    this.levels = {};
    this.levelsHash = {};
    this.levelHashCodes = {};

    this.newNode = function(level, state, edge, node, predecessors) {

        var nodeIndex = level + '-' + state + '-' + edge + "-" + node;

        if (this.gss[nodeIndex] === undefined) {

            var gssNodeLabel = "v" + Object.keys(this.gss).length;
            var newNode = new GssNode(nodeIndex, gssNodeLabel, level, state, edge, node, predecessors);
            this.gss[nodeIndex] = newNode;

            if (this.levels[level] === undefined) {

                this.levels[level] = [];
            }

            this.levels[level].push(newNode);
        }
        else {

            var gssNode = this.find(nodeIndex);
            gssNode.previousNodes = gssNode.previousNodes.concat(predecessors);
            gssNode.previousNodes = gssNode.previousNodes.filter(function(item, pos) {

                return gssNode.previousNodes.indexOf(item) === pos;
            });
        }
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

    this.getLevelWithSameHash = function(hash) {

        if (this.levelsHash[hash] !== undefined) {

            return this.levelsHash[hash];
        }
    };

    this.getHashForLevel = function(level) {

        return this.levelHashCodes[level];
    };

    this.registerLevel = function(hash, level) {

        var duplicated = false;
        if (this.levelsHash[hash] !== undefined) {

            duplicated = true;
        }

        this.levelsHash[hash] = level;
        this.levelHashCodes[level] = hash;

        return duplicated;
    };

    for (var i = 0; i < nodes.length; i++) {

        this.newNode(0, 0, "", nodes[i], []);
    }
};