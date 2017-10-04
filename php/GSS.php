<?php

class GSS {

    /**
     * @var GssNode[]
     */
    private static $gss;
    /**
     * @var GssNode[][]
     */
    private static $levels;
    public static $levelsHash;
    public static $levelHashCodes;

    public static function create ($nodes) {

        self::$gss = [];
        self::$levels = [];
        self::$levelsHash = [];
        self::$levelHashCodes = [];

        foreach ($nodes as $node) {

            self::newNode(0, 0, '', $node, []);
        }
    }

    /**
     * @param integer $level
     * @return GssNode[]
     */
    public static function level ($level) {

        if (empty(self::$levels[$level]) === true) {

            self::$levels[$level] = [];
        }

        return self::$levels[$level];
    }

    public static function getGssNode($index) {

        return self::$gss[$index];
    }

    /**
     * @param $gssNodeIndex
     * @param $jumps
     * @return GSSNode[]
     */
    public static function up ($gssNodeIndex, $jumps) {

        $gssNode = self::find($gssNodeIndex);

        if ($jumps > 0) {

            $nodes = [];

            foreach ($gssNode->previousNodes as $previousNode) {

                $nodes = array_merge($nodes, self::up($previousNode, $jumps - 1));
            }

            return $nodes;
        }

        return [$gssNode];
    }

    /**
     * @param integer $gssNodeIndex
     * @return GssNode
     */
    private static function find ($gssNodeIndex) {

        return $gssNodeIndex === null ? null : self::$gss[$gssNodeIndex];
    }

    public static function newNode ($level, $state, $edge, $node, $predecessors) {

        $nodeIndex = "$level-$state-$edge-$node";

        if (isset(self::$gss[$nodeIndex]) === false) {

            $gssNodeLabel = 'v' . count(self::$gss);

            $newNode = new GssNode($nodeIndex, $gssNodeLabel, $level, $state, $edge, $node, $predecessors);
            self::$gss[$nodeIndex] = $newNode;
            self::$levels[$level][] = $newNode;
        }
        else {

            $gssNode = self::$gss[$nodeIndex];
            $gssNode->previousNodes = array_unique(array_merge($gssNode->previousNodes, $predecessors));
        }
    }

    public static function printGssScreen() {

        echo "\nGSS:\n\n";

        $levels = count(self::$levels);

        for ($i = 0; $i < $levels; $i ++) {

            $nodes = self::level($i);

            echo "Level U$i\n";
            foreach ($nodes as $node) {

                $ancestors = self::up($node->index, 1);

                $ancestorString = '';
                if (empty($ancestors) === false) {

                    foreach ($ancestors as $ancestor) {

                        $ancestorString .= "($ancestor->label)";
                    }

                    $ancestorString .= ' <-- ';
                }

                $nodeString = "(I$node->state, $node->node)";
                if ($node->accepted === true) $nodeString = "($nodeString)";

                echo "$node->label: {$ancestorString}[$node->edge] <-- $nodeString\n";
            }
            echo "\n";
        }
    }

    public static function getLevelWithSameHash($hash) {

        if (isset(self::$levelsHash[$hash]) === true) {

            return self::$levelsHash[$hash];
        }

        return null;
    }

    public static function getHashForLevel($level) {

        return self::$levelHashCodes[$level];
    }

    /**
     * @param string  $hash
     * @param integer $level
     * @return boolean
     */
    public static function registerLevel($hash, $level) {

        if (empty(self::$levelsHash[$hash]) === false) {

            $duplicate = self::$levelsHash[$hash];

            if (self::$levelHashCodes[$duplicate - 1] === self::$levelHashCodes[$level - 1]) {

                return false;
            }
        }

        self::$levelsHash[$hash] = $level;
        self::$levelHashCodes[$level] = $hash;

        return true;
    }

    public static function printGss($example) {

        $arquivo = uniqid("/tmp/gss") . '.gv';
        $fp = fopen($arquivo, 'w');

        fwrite($fp,  "digraph G {
        style=filled;
        color=white;");

        $colors = ["#000000", "#222222", "#444444", "#666666", "#888888", "#AAAAAA", "#CCCCCC", "#DDDDDD"];

        $previousList = [];
        for ($level = 0; $level < count(self::$levels); $level ++) {

            $x = $level*150+70;
            fwrite($fp, "\"U$level\" [shape=square style=filled color=white label=\"U$level\" pos=\"$x,50\"];");

            $color = $colors[((int) $level % count($colors))];

            $gssNodes = self::level($level);


            foreach ($gssNodes as $index => $gssNode) {

                $x = $level*150;
                $y = - $index*70;

                $edge = '';
                if (empty($gssNode->edge) === false) {

                    $edge = "\"l$gssNode->label\" [shape=square label=\"$gssNode->edge\", pos=\"$x,$y\"];
                    $gssNode->label -> l$gssNode->label [penwidth=0.5 label=\"$gssNode->label\"];";
                }

                $ancestors = self::up($gssNode->index, 1);
                if (empty($ancestors) === false) {

                    foreach ($ancestors as $ancestor) {

                        $previousList[] = "l$gssNode->label -> $ancestor->label [color=\"$color\"];";
                    }
                }

                $x += 70;

                $accepted = $gssNode->accepted ? ' style=dashed' : '';

                fwrite($fp, "\n\"$gssNode->label\" [shape=circle label=\"I$gssNode->state, $gssNode->node\", pos=\"$x,$y\"$accepted]; $edge");
            }
        }

        fwrite($fp, implode("\n", $previousList));

        fwrite($fp, "\n}");

        fclose($fp);

        exec("dot -Kneato -n -Tpng $arquivo -o resultados/example-$example-gss.png  &> /dev/null &");
    }
}