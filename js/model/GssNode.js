var GssNode = function(index, label, level, state, edge, node, previousNodes) {
    this.index = index;
    this.label = label;
    this.level = level;
    this.state = state;
    this.edge = edge;
    this.node = node;
    this.previousNodes = previousNodes;
    this.accepted = false;
};