<?php

class ReduceRule {

    /**
     * @var string
     */
    public $lhs;

    /**
     * @var integer
     */
    public $rhsSize;

    public function __construct($lhs, $rhsSize) {

        $this->lhs = $lhs;
        $this->rhsSize = $rhsSize;
    }
}