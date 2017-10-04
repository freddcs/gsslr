<?php

class Automaton {

    public static $parsingTable;

    /**
     * @var ReduceRule[]
     */
    public static $reduceRules;

    const ACTION_ACCEPT = 'ACCEPT';
    const ACTION_ERROR  = 'ERROR';
    const ACTION_GOTO   = 'GOTO';
    const ACTION_REDUCE = 'REDUCE';
    const ACTION_SHIFT  = 'SHIFT';

    /**
     * @param integer $currentState
     * @param string $symbol
     * @return AutomatonAction
     * @throws Exception
     */
    public static function getAction($currentState, $symbol) {

        $actionPair = self::$parsingTable[$symbol][$currentState];

        $action = new AutomatonAction();

        if (strlen($actionPair) >= 1) {

            switch ($actionPair[0]) {

                case 'a':
                    $action->action = self::ACTION_ACCEPT;
                    break;

                case 'g':
                    $action->action = self::ACTION_GOTO;
                    $action->state = (int) substr($actionPair, 1);
                    break;

                case 'r':
                    $action->action = self::ACTION_REDUCE;
                    $action->rule = ((int) substr($actionPair, 1)) - 1;
                    break;

                case 's':
                    $action->action = self::ACTION_SHIFT;
                    $action->state = (int) substr($actionPair, 1);
                    break;

                default:
                    throw new Exception("Undefined action '$actionPair'");
            }
        }
        else {

            $action->action = self::ACTION_ERROR;
        }

        return $action;
    }
}