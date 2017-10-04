<?php

class Examples {

    /**
     * @param $exampleNumber
     * @param $nodes
     * @return string
     */
    public static function buildExample($exampleNumber, $nodes) {

        switch ($exampleNumber) {
            case 1: return self::buildExample1();
            case 2: return self::buildExample2();// die("Este exemplo causa um loop infinito\n");
            case 3: return self::buildExample3();
            case 4: return self::buildExample4($nodes);
            case 5: return self::buildExample5($nodes);
            case 6: return self::buildExample6();
            case 7: return self::buildExample7();
            default: return self::buildExample8();
        }
    }

    /**
     * Grafo simples.
     *
     * @return string
     */
    private static function buildExample1 () {

        Automaton::$parsingTable = [
            '(' => ['s2', '',  's4', '',   's4', '',   '',   ''],
            ')' => ['',   '',  'r2', 's5', 'r2', '',   's7', 'r3'],
            '$' => ['',   'a', '',   '',   '',   'r1', '',   ''],
            'S' => ['g1', '',  '',   '',   'r0', 'r1', '',   ''],
            'P' => ['',   '',  'g3', '',   'g6', '',   '',   '']
        ];

        Automaton::$reduceRules = [
            new ReduceRule('S', 3),
            new ReduceRule('P', 0),
            new ReduceRule('P', 3)
        ];

        Graph::create(
            [
                ['a', '(', 'b'],
                ['b', '(', 'd'],
                ['d', ')', 'e'],
                ['e', ')', 'f'],
                ['b', ')', 'c']
            ]
        );

        return 'a';
    }

    /**
     * Exemplo com loop.
     *
     * @return string
     */
    private static function buildExample2 () {

        Automaton::$parsingTable = [
            '(' => ['s2', '',  's4', '',   's4', '',   '',   ''],
            ')' => ['',   '',  'r2', 's5', 'r2', '',   's7', 'r3'],
            '$' => ['',   'a', '',   '',   '',   'r1', '',   ''],
            'S' => ['g1', '',  '',   '',   'r0', 'r1', '',   ''],
            'P' => ['',   '',  'g3', '',   'g6', '',   '',   '']
        ];

        Automaton::$reduceRules = [
            new ReduceRule('S', 3),
            new ReduceRule('P', 0),
            new ReduceRule('P', 3)
        ];

        Graph::create(
            [
                ['a', '(', 'a'],
                ['a', ')', 'b'],
                ['b', ')', 'c'],
                ['c', ')', 'd'],
                ['d', ')', 'e']
            ]
        );

        return 'a';
    }

    /**
     * Exemplo com várias soluções.
     *
     * @return string
     */
    private static function buildExample3 () {

        Automaton::$parsingTable = [
            '(' => ['s2', '',  's4', '',   's4', '',   '',   ''],
            ')' => ['',   '',  'r2', 's5', 'r2', '',   's7', 'r3'],
            '$' => ['',   'a', '',   '',   '',   'r1', '',   ''],
            'S' => ['g1', '',  '',   '',   'r0', 'r1', '',   ''],
            'P' => ['',   '',  'g3', '',   'g6', '',   '',   '']
        ];

        Automaton::$reduceRules = [
            new ReduceRule('S', 3),
            new ReduceRule('P', 0),
            new ReduceRule('P', 3)
        ];

        Graph::create(
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
                ['b', ')', 'j'],
            ]
        );

        return 'a';
    }

    /**
     * Exemplo com muitos nós.
     *
     * @return string
     */
    private static function buildExample4 ($numberOfNodes) {

        Automaton::$parsingTable = [
            '(' => ['s2', '',  's4', '',   's4', '',   '',   ''],
            ')' => ['',   '',  'r2', 's5', 'r2', '',   's7', 'r3'],
            '$' => ['',   'a', '',   '',   '',   'r1', '',   ''],
            'S' => ['g1', '',  '',   '',   'r0', 'r1', '',   ''],
            'P' => ['',   '',  'g3', '',   'g6', '',   '',   '']
        ];

        Automaton::$reduceRules = [
            new ReduceRule('S', 3),
            new ReduceRule('P', 0),
            new ReduceRule('P', 3)
        ];

        $graph = [];

        for ($i = 0; $i < $numberOfNodes; $i ++) {

            $edge = $i < $numberOfNodes / 2 ? '(' : ')';
            $d = $i + 1;
            $graph[] =  ["n$i", $edge, "n$d"];
        }

        Graph::create($graph);

        return 'n0';
    }

    /**
     * Exemplo com muitos nós.
     *
     * @return string
     */
    private static function buildExample5 ($numberOfNodes) {

        Automaton::$parsingTable = [
            '(' => ['s2', '',  's4', '',   's4', '',   '',   ''],
            ')' => ['',   '',  'r2', 's5', 'r2', '',   's7', 'r3'],
            '$' => ['',   'a', '',   '',   '',   'r1', '',   ''],
            'S' => ['g1', '',  '',   '',   'r0', 'r1', '',   ''],
            'P' => ['',   '',  'g3', '',   'g6', '',   '',   '']
        ];

        Automaton::$reduceRules = [
            new ReduceRule('S', 3),
            new ReduceRule('P', 0),
            new ReduceRule('P', 3)
        ];

        $graph = [];

        for ($i = 0; $i < $numberOfNodes; $i ++) {

            $edge = $i < $numberOfNodes / 2 ? '(' : ')';
            $d = $i + 1;
            $graph[] =  ["n$i", $edge, "n$d"];

            if ($i > 0 && $i < ($numberOfNodes + 2) / 2) {

                $graph[] = ["n$i", ')', "d$i-0"];

                for ($j = 0; $j < $i; $j ++) {

                    $d = $j + 1;
                    $graph[] = ["d$i-$j", ')', "d$i-$d"];
                }
            }
        }

        Graph::create($graph);

        return 'n0';
    }

    /**
     * Exemplo com loop.
     *
     * @return string
     */
    private static function buildExample6 () {

        Automaton::$parsingTable = [
            '(' => ['s2', '',  's4', '',   's4', '',   '',   ''],
            ')' => ['',   '',  'r2', 's5', 'r2', '',   's7', 'r3'],
            '$' => ['',   'a', '',   '',   '',   'r1', '',   ''],
            'S' => ['g1', '',  '',   '',   'r0', 'r1', '',   ''],
            'P' => ['',   '',  'g3', '',   'g6', '',   '',   '']
        ];

        Automaton::$reduceRules = [
            new ReduceRule('S', 3),
            new ReduceRule('P', 0),
            new ReduceRule('P', 3)
        ];

        Graph::create(
            [
                ['a', '(', 'b'],
                ['b', '(', 'c'],
                ['c', '(', 'a'],
                ['c', ')', 'd'],
                ['d', ')', 'e'],
                ['e', ')', 'd'],
                ['d', ')', 'f']
            ]
        );

        return 'a';
    }

    /**
     * Exemplo com loop.
     *
     * @return string
     */
    private static function buildExample7 () {

        Automaton::$parsingTable = [
            '(' => ['s2', '',  's4', '',   's4', '',   '',   ''],
            ')' => ['',   '',  'r2', 's5', 'r2', '',   's7', 'r3'],
            '$' => ['',   'a', '',   '',   '',   'r1', '',   ''],
            'S' => ['g1', '',  '',   '',   'r0', 'r1', '',   ''],
            'P' => ['',   '',  'g3', '',   'g6', '',   '',   '']
        ];

        Automaton::$reduceRules = [
            new ReduceRule('S', 3),
            new ReduceRule('P', 0),
            new ReduceRule('P', 3)
        ];

        Graph::create(
            [
                ['a', '(', 'a'],
                ['a', ')', 'b'],
                ['b', ')', 'b']
            ]
        );

        return 'a';
    }

    /**
     * Exemplo com loop.
     *
     * @return string
     */
    private static function buildExample8 () {

        Automaton::$parsingTable = [
            '(' => ['s2', '',  's4', '',   's4', '',   '',   ''],
            ')' => ['',   '',  'r2', 's5', 'r2', '',   's7', 'r3'],
            '$' => ['',   'a', '',   '',   '',   'r1', '',   ''],
            'S' => ['g1', '',  '',   '',   'r0', 'r1', '',   ''],
            'P' => ['',   '',  'g3', '',   'g6', '',   '',   '']
        ];

        Automaton::$reduceRules = [
            new ReduceRule('S', 3),
            new ReduceRule('P', 0),
            new ReduceRule('P', 3)
        ];

        Graph::create(
            [
                ['a', '(', 'b'],
                ['b', '(', 'c'],
                ['c', '(', 'a'],
                ['c', ')', 'd'],
                ['d', ')', 'e'],
                ['e', ')', 'f'],
                ['f', ')', 'g'],
                ['g', ')', 'h'],
                ['h', ')', 'i'],
                ['i', ')', 'j'],
                ['j', ')', 'k'],
                ['k', ')', 'l'],
                ['l', ')', 'm'],
                ['m', ')', 'n']
            ]
        );

        return 'a';
    }
}