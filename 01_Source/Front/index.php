<?php
require_once __DIR__ . '/vendor/autoload.php';
//require_once 'Application.php';

use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Silex\Application;

$app = new Silex\Application();


$app->get('/', function(){
            return "this is index page\n";
});

$app->POST('/v2/humidity', function(Application $app, Request $request) {
            
            
            return "this is humidity page\n";
            });


$app->GET('/get/v2/humidity', function(Application $app, Request $request) {
            
            
            return new Response('How about implementing updateHumidityInformation as a GET method ?');
            });


$app->run();
