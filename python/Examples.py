from DataGraph import *
from dbWine import *
from LR import *

DG = DataGraph()

exampleWine(DG)

# Exemplo 0
'''DG.addNode('a', '(', 'b')
DG.addNode('b', ')', 'c')
DG.addNode('b', '(', 'd')
DG.addNode('d', ')', 'e')
DG.addNode('e', ')', 'f')
DG.addNode('f', ')', 'g')'''

# Exemplo 1

'''DG.addNode('a', '(', 'a')
DG.addNode('a', ')', 'b')
DG.addNode('b', ')', 'c')
DG.addNode('c', ')', 'd')
DG.addNode('d', ')', 'e')'''

# Exemplo 2

'''DG.addNode('a', '(', 'b')
DG.addNode('b', '(', 'c')
DG.addNode('c', '(', 'd')
DG.addNode('d', '(', 'e')
DG.addNode('e', '(', 'f')
DG.addNode('f', ')', 'g')
DG.addNode('g', ')', 'h')
DG.addNode('h', ')', 'i')
DG.addNode('i', ')', 'j')
DG.addNode('j', ')', 'k')
DG.addNode('b', ')', 'c')
DG.addNode('b', ')', 'd')
DG.addNode('b', ')', 'e')
DG.addNode('b', ')', 'f')
DG.addNode('b', ')', 'g')
DG.addNode('b', ')', 'h')
DG.addNode('b', ')', 'i')
DG.addNode('b', ')', 'j')'''

# Exemplo 3

'''DG.addNode('a', '(', 'b')
DG.addNode('b', '(', 'c')
DG.addNode('c', '(', 'a')
DG.addNode('c', ')', 'd')
DG.addNode('d', ')', 'e')
DG.addNode('e', ')', 'd')
DG.addNode('d', ')', 'f')'''

# Exemplo 4

'''DG.addNode('a', '(', 'a')
DG.addNode('a', '(', 'b')
DG.addNode('b', ')', 'b')'''

def CreateParsingTable(grammar):
    parsingTable = []
    
    # Example 1
    '''parsingTable.append({})
    parsingTable[0]['('] = Action('shift', 2, None)
    parsingTable[0]['S'] = Action('goto', 1, None)
    parsingTable.append({})
    parsingTable[1]['$'] = Action('accept', None, None)
    parsingTable.append({})
    parsingTable[2]['('] = Action('shift', 4, None)
    parsingTable[2][')'] = Action('reduce', None, 2)
    parsingTable[2]['P'] = Action('goto', 3, None)
    parsingTable.append({})
    parsingTable[3][')'] = Action('shift', 5, None)
    parsingTable.append({})
    parsingTable[4]['('] = Action('shift', 4, None)
    parsingTable[4][')'] = Action('reduce', None, 2)
    parsingTable[4]['P'] = Action('goto', 6, None)
    parsingTable.append({})
    parsingTable[5]['$'] = Action('reduce', None, 1)
    parsingTable.append({})
    parsingTable[6][')'] = Action('shift', 7, None)
    parsingTable.append({})
    parsingTable[7][')'] = Action('reduce', None, 3)
    
    rules = [Rule('S\'', 1), Rule('S', 3), Rule('P', 0), Rule('P', 3)]'''
    
    # Q1
    parsingTable.append({})
    parsingTable[0]['next::subClassOf'] = Action('shift', 2, None)
    parsingTable[0]['next::type'] = Action('shift', 3, None)
    parsingTable[0]['S'] = Action('goto', 1, None)
    parsingTable.append({})
    parsingTable[1]['$'] = Action('accept', None, None)
    parsingTable.append({})
    parsingTable[2]['next::subClassOf'] = Action('shift', 6, None)
    parsingTable[2]['next-1::subClassOf'] = Action('shift', 5, None)
    parsingTable[2]['next::type'] = Action('shift', 7, None)
    parsingTable[2]['S'] = Action('goto', 4, None)
    parsingTable.append({})
    parsingTable[3]['next::subClassOf'] = Action('shift', 10, None)
    parsingTable[3]['next::type'] = Action('shift', 11, None)
    parsingTable[3]['next-1::type'] = Action('shift', 9, None)
    parsingTable[3]['S'] = Action('goto', 8, None)
    parsingTable.append({})
    parsingTable[4]['next-1::subClassOf'] = Action('shift', 12, None)
    parsingTable.append({})
    parsingTable[5]['$'] = Action('reduce', None, 2)
    parsingTable.append({})
    parsingTable[6]['next::subClassOf'] = Action('shift', 6, None)
    parsingTable[6]['next-1::subClassOf'] = Action('shift', 14, None)
    parsingTable[6]['next::type'] = Action('shift', 7, None)
    parsingTable[6]['S'] = Action('goto', 13, None)
    parsingTable.append({})
    parsingTable[7]['next::subClassOf'] = Action('shift', 10, None)
    parsingTable[7]['next::type'] = Action('shift', 11, None)
    parsingTable[7]['next-1::type'] = Action('shift', 16, None)
    parsingTable[7]['S'] = Action('goto', 15, None)
    parsingTable.append({})
    parsingTable[8]['next-1::type'] = Action('shift', 17, None)
    parsingTable.append({})
    parsingTable[9]['$'] = Action('reduce', None, 4)
    parsingTable.append({})
    parsingTable[10]['next::subClassOf'] = Action('shift', 6, None)
    parsingTable[10]['next-1::subClassOf'] = Action('shift', 19, None)
    parsingTable[10]['next::type'] = Action('shift', 7, None)
    parsingTable[10]['S'] = Action('goto', 18, None)
    parsingTable.append({})
    parsingTable[11]['next::subClassOf'] = Action('shift', 10, None)
    parsingTable[11]['next::type'] = Action('shift', 11, None)
    parsingTable[11]['next-1::type'] = Action('shift', 21, None)
    parsingTable[11]['S'] = Action('goto', 20, None)
    parsingTable.append({})
    parsingTable[12]['$'] = Action('reduce', None, 1)
    parsingTable.append({})
    parsingTable[13]['next-1::subClassOf'] = Action('shift', 22, None)
    parsingTable.append({})
    parsingTable[14]['next-1::subClassOf'] = Action('reduce', None, 2)
    parsingTable.append({})
    parsingTable[15]['next-1::type'] = Action('shift', 23, None)
    parsingTable.append({})
    parsingTable[16]['next-1::subClassOf'] = Action('reduce', None, 4)
    parsingTable.append({})
    parsingTable[17]['$'] = Action('reduce', None, 3)
    parsingTable.append({})
    parsingTable[18]['next-1::subClassOf'] = Action('shift', 24, None)
    parsingTable.append({})
    parsingTable[19]['next-1::type'] = Action('reduce', None, 2)
    parsingTable.append({})
    parsingTable[20]['next-1::type'] = Action('shift', 25, None)
    parsingTable.append({})
    parsingTable[21]['next-1::type'] = Action('reduce', None, 4)
    parsingTable.append({})
    parsingTable[22]['next-1::subClassOf'] = Action('reduce', None, 1)
    parsingTable.append({})
    parsingTable[23]['next-1::subClassOf'] = Action('reduce', None, 3)
    parsingTable.append({})
    parsingTable[24]['next-1::type'] = Action('reduce', None, 1)
    parsingTable.append({})
    parsingTable[25]['next-1::type'] = Action('reduce', None, 3)
    
    rules = [Rule('S\'', 1), Rule('S', 3), Rule('S', 2), Rule('S', 3), Rule('S', 2)]
    
    return parsingTable, rules
