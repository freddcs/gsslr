<?php

class GraphEdge {

    /**
     * @var string
     */
    public $node;

    /**
     * @var string
     */
    public $label;

    /**
     * @var string
     */
    public $destination;

    public function __construct($node, $label, $destination) {

        $this->node = $node;
        $this->label = $label;
        $this->destination = $destination;
    }
}