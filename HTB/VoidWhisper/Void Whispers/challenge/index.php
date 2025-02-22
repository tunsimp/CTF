<?php spl_autoload_register(function ($name) {
    if (preg_match('/Controller$/', $name)) {
        $name = "controllers/{$name}";
    } elseif (preg_match('/Model$/', $name)) {
        $name = "models/{$name}";
    }
    include_once "{$name}.php";
});

$router = new Router();
$router->new('GET', '/', 'IndexController@index');
$router->new('POST', '/update', 'IndexController@updateSetting');

die($router->match());
