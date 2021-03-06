var graphs = [
    {
        graph:
            [
                ['a', '(', 'b'],
                ['b', ')', 'c'],
                ['b', '(', 'd'],
                ['d', ')', 'e'],
                ['e', ')', 'f'],
                ['f', ')', 'g']
            ],
        startingNodes: ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    },
    {
        graph:
            [
                ['a', '(', 'a'],
                ['a', ')', 'b'],
                ['b', ')', 'c'],
                ['c', ')', 'd'],
                ['d', ')', 'e']
            ],
        startingNodes: ['a', 'b', 'c', 'd', 'e']
    },
    {
        graph:
            [
                ['a', '(', 'b'],
                ['b', '(', 'c'],
                ['c', '(', 'd'],
                ['d', '(', 'e'],
                ['e', '(', 'f'],
                ['f', ')', 'g'],
                ['g', ')', 'h'],
                ['h', ')', 'i'],
                ['i', ')', 'j'],
                ['j', ')', 'k'],
                ['b', ')', 'c'],
                ['b', ')', 'd'],
                ['b', ')', 'e'],
                ['b', ')', 'f'],
                ['b', ')', 'g'],
                ['b', ')', 'h'],
                ['b', ')', 'i'],
                ['b', ')', 'j']
            ],
        startingNodes: ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    },
    {
        graph:
            [
                ['a', '(', 'b'],
                ['b', '(', 'c'],
                ['c', '(', 'a'],
                ['c', ')', 'd'],
                ['d', ')', 'e'],
                ['e', ')', 'd'],
                ['d', ')', 'f']
            ],
        startingNodes: ['a', 'b', 'c', 'd', 'e', 'f']
    },
    {
        graph:
            [
                ['a', '(', 'a'],
                ['a', ')', 'b'],
                ['b', ')', 'b']
            ],
        startingNodes: ['a', 'b']
    },
    {
        graph:
            [
                ['n1', 'a', 'n2'],
                ['n2', 'a', 'n3'],
                ['n3', 'b', 'n4']
            ],
        startingNodes: ['n1', 'n2', 'n3', 'n4']
    },
    {
        graph:
            [
                ['n1', 'a', 'n2'],
                ['n1', 'b', 'n2'],
                ['n2', 'a', 'n3'],
                ['n3', 'a', 'n4'],
                ['n4', 'b', 'n4'],
                ['n4', 'a', 'n3']
            ],
        startingNodes: ['n1', 'n2', 'n3', 'n4']
    }
];

var grammars = [
    [
        ['S\'', 'S'],
        ['S', '( P )'],
        ['P', '\'\''],
        ['P', '( P )']
    ],
    [
        ['S\'', 'A'],
        ['A', 'a A'],
        ['A', 'b']
    ]
];