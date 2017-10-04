<?php

class Algoritmo {

    public static function query($nodes) {

        GSS::create($nodes);
        return array_unique(self::evalLevel(0, null, null));
    }

    /**
     * @param $level
     * @return string[]
     */
    private static function evalLevel($level, $loopHash, $loopLevels) {

        if ($_SESSION['debug'] > 0) echo "\n\n*****************\nProcessando o nível $level\n*****************\n";

        $answers = [];
        $continue = false;

        $gssNodes = GSS::level($level);
        foreach ($gssNodes as $gssNode) {

            $graphEdges = Graph::findEdgesFromNode($gssNode->node);

            foreach ($graphEdges as $graphEdge) {

                $action = Automaton::getAction($gssNode->state, $graphEdge->label);
                if ($action->action === Automaton::ACTION_REDUCE) {

                    self::processReduction($action, $gssNode, $graphEdge->label);
                }
            }

            // Is there a reduction if we consider the path ends at this node?
            $action = Automaton::getAction($gssNode->state, '$');
            if ($action->action === Automaton::ACTION_REDUCE) {

                self::processReduction($action, $gssNode, '$');
            }
        }

        $gssLevelString = [];

        $gssNodes = GSS::level($level);
        foreach ($gssNodes as $gssNode) {

            // Is the current GSS node pointing to an accepted answer?
            $acceptAction = Automaton::getAction($gssNode->state, '$');

            if ($acceptAction->action === Automaton::ACTION_ACCEPT) {

                $previousGssNode = GSS::getGssNode($gssNode->previousNodes[0]);

                // Concatenate the answer with the destination node.
                $answers[] = "({$previousGssNode->node}, $gssNode->node)";
                $gssNode->accepted = true;
            }

            $gssLevelString[] = "[$gssNode->state$gssNode->edge$gssNode->node$gssNode->accepted]";
        }

        $gssLevelHash = implode(', ', $gssLevelString);

        if (GSS::registerLevel($gssLevelHash, $level) === false) {

            echo "\n\n** LOOP INFINITO ENCONTRADO! **\n\n";
        }
        else {

            $gssNodes = GSS::level($level);
            foreach ($gssNodes as $gssNode) {

                $graphEdges = Graph::findEdgesFromNode($gssNode->node);
                foreach ($graphEdges as $graphEdge) {

                    // Are there shifts to perform on this GSS level?
                    $action = Automaton::getAction($gssNode->state, $graphEdge->label);
                    if ($action->action === Automaton::ACTION_SHIFT) {

                        // Create a new node on the next level with the new state, labeled after the current symbol and pointing to the
                        // edge's destination.
                        GSS::newNode($gssNode->level + 1, $action->state, $graphEdge->label, $graphEdge->destination, [$gssNode->index]);

                        if ($_SESSION['debug'] > 0) {
                            echo "\nNó '$gssNode->node', estado 'I$gssNode->state' ...\nLendo o caracter '$graphEdge->label'. Ação: Shift para o estado 'I$action->state': \n";
                        }

                        $continue = true;
                    }
                }
            }

            if ($_SESSION['debug'] > 1) {
                GSS::printGssScreen();
            }

            if ($continue === true) {

                if ($_SESSION['debug'] > 0) {

                    echo "\nEnter para continuar ...\n";
                    $handle = fopen("php://stdin", "r");
                    fgets($handle);
                    fclose($handle);
                }

                $answers = array_merge($answers, self::evalLevel($level + 1, $loopHash, $loopLevels));
            }
            else {

                // Não há mais entradas
            }
        }

        return $answers;
    }

    /**
     * @param AutomatonAction $action
     * @param GssNode         $gssNode
     * @param string          $edgeLabel
     */
    private static function processReduction($action, $gssNode, $edgeLabel) {

        $rule = Automaton::$reduceRules[$action->rule];

        // Go back |RHS| nodes in the GSS
        $reductionRoots = GSS::up($gssNode->index, $rule->rhsSize);

        foreach ($reductionRoots as $reductionRoot) {

            $goto = Automaton::getAction($reductionRoot->state, $rule->lhs);

            // Create a new node with the result of the goto from the
            // parsing table, labeled after the LHS and same with
            // destination as the original GSS node.
            GSS::newNode($gssNode->level, $goto->state, $rule->lhs, $gssNode->node, [$reductionRoot->index]);
        }

        $rhs = $action->rule === 0 ? 'S -> ( P )' : ($action->rule === 1 ? 'P -> \lambda' : 'P -> ( P )');

        if ($_SESSION['debug'] > 0) echo "\nNó '$gssNode->node', estado 'I$gssNode->state'. Lendo o caracter '$edgeLabel' ...\nReduzindo pela regra 'r$action->rule: $rhs': \n";
    }
}