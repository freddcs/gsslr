var Automaton = function() {

    this.parsingTable = {};
    this.reduceRules = [];

    this.getAction = function(currentState, symbol) {

        var actionPair = this.parsingTable[symbol][currentState];
        var action = new AutomatonAction();

        if (actionPair.length >= 1) {

            switch (actionPair[0]) {

                case "a":
                    action.action = "ACCEPT";
                    break;

                case "g":
                    action.action = "GOTO";
                    action.state = parseInt(actionPair.substring(1));
                    break;

                case "r":
                    action.action = "REDUCE";
                    action.rule = parseInt(actionPair.substring(1)) - 1;
                    break;

                case "s":
                    action.action = "SHIFT";
                    action.state = parseInt(actionPair.substring(1));
                    break;
            }
        }
        else {

            action.action = "ERROR";
        }

        return action;
    }
};