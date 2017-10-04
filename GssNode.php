<?php

class GssNode {

    /**
     * @var string
     */
    public $index;

    /**
     * @var string
     */
    public $label;

    /**
     * @var integer
     */
    public $level;

    /**
     * @var integer
     */
    public $state;

    /**
     * @var string
     */
    public $edge;

    /**
     * @var string
     */
    public $node;

    /**
     * @var integer[]
     */
    public $previousNodes;

    /**
     * @var boolean
     */
    public $accepted;

    public function __construct($index, $label, $level, $state, $edge, $node, $previous) {

        $this->index = $index;
        $this->label = $label;
        $this->level = $level;
        $this->state = $state;
        $this->edge = $edge;
        $this->node = $node;
        $this->previousNodes = $previous;

        $this->accepted = false;
    }

    public function __toString() {

        return "[$this->state$this->edge$this->node$this->accepted]";
    }
}