<?php

class Graph {

    /**
     * @var GraphEdge[][]
     */
    private static $graph;

    /**
     * @var string[]
     */
    private static $nodes;


    public static function create($graph) {

        foreach ($graph as $node) {

            self::$nodes[] = $node[0];
            self::$graph[$node[0]][] = new GraphEdge($node[0], $node[1], $node[2]);
        }

        self::$nodes = array_unique(self::$nodes);
    }

    /**
     * @param string $node
     * @return GraphEdge[]
     */
    public static function findEdgesFromNode($node) {

        return empty(self::$graph[$node]) === true ? [] : self::$graph[$node];
    }

    public static function printGraph($example) {

        $arquivo = uniqid("/tmp/graph") . '.gv';
        $fp = fopen($arquivo, 'w');

        fwrite($fp,  "digraph G {");

        foreach (self::$graph as $index => $edges) {

            foreach ($edges as $edge) {

                fwrite($fp, "\"$edge->node\" -> \"$edge->destination\" [label=\"$edge->label\"];");
            }
        }

        fwrite($fp, "}");

        fclose($fp);

        exec("dot -Tpng $arquivo -o resultados/example-$example-graph.png  &> /dev/null &");
    }

    public static function getNodes() {

        return self::$nodes;
    }
}