<?php

include_once('AutomatonAction.php');
include_once('ReduceRule.php');
include_once('GssNode.php');
include_once('GraphEdge.php');
include_once('Automaton.php');
include_once('GSS.php');
include_once('Graph.php');
include_once('Examples.php');
include_once('Algoritmo.php');

ini_set('memory_limit','6G');

$debug = 0;
$example = 1;
$algorithmType = 'l';
$nodes = 100;

if (isset($argv[1]) === true) {

    $debug = (int) $argv[1];
}

if (isset($argv[2]) === true) {

    $example = $argv[2];
}

if (isset($argv[3]) === true) {

    $nodes = $argv[3];
}

$_SESSION['debug'] = $debug;

echo "\nphp main.php [debug: 0, 1 ou 2] [exemplo 1, 2, 3, 4 ou 5] [número de nós]\n";
echo "Ex: php main.php 0 l 4 50\n";
echo "\n*************************************************************************\n";
echo "Executando o Exemplo $example\n";
echo "*************************************************************************\n\n";

echo "Inicializando ... ";

$executionStartTime = microtime(true);
$startNode = Examples::buildExample($example, $nodes);
$executionEndTime = microtime(true);
$memoriaGrafo = memory_get_peak_usage(true);

echo "Nós: " . count(Graph::getNodes());
echo " (" . ($executionEndTime - $executionStartTime) . " s - " .($memoriaGrafo / 1024 / 1024) . " MB)\n\n";

echo "Pesquisando ... ";

$executionStartTime = microtime(true);

$answers = Algoritmo::query(Graph::getNodes());

$executionEndTime = microtime(true);

asort($answers);

echo "Pronto.\nRespostas: " . implode(', ', $answers) . "\n";
echo "Tempo de execução: " . ($executionEndTime - $executionStartTime) . " segundos\n";
echo "Memória usada pelo algoritmo: " . ((memory_get_peak_usage(true) - $memoriaGrafo) / 1024 / 1024) . " MB\n\n";

if (!file_exists('resultados')) {

    mkdir('resultados', 0777, true);
}

Graph::printGraph($example);
GSS::printGSS($example);

echo "Exibir o GSS resultante? s/[n] ";
$handle = fopen ("php://stdin", "r");
$line = fgets($handle);
fclose($handle);

$html = "<html><body style='text-align:center;'>Grafo de dados:<br /><img src='graph.png' /><br />Respostas: " . implode(', ', $answers) . "<br/>GSS:<br /><img src='gss.png' /></body></html>";
file_put_contents("resultados/example-$example-result.htm", $html);

echo "\nPara ver o grafo e o GSS resultante do teste, abra o arquivo resultados/example-$example-result.htm em um navegador";

if (trim($line) === 's'){

    GSS::printGssScreen();
}