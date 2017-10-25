class Action:
    def __init__(self, action, state, rule):
        self.action = action
        self.state = state
        self.rule = rule
        
class Rule:
    def __init__(self, lhs, rhsSize):
        self.lhs = lhs
        self.rhsSize = rhsSize
