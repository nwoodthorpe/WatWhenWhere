<?php
    include 'includes/mysqlconfig.php';
    $conn = new mysqli(constant("HOST"), constant("USER"), constant("PASSWORD"), constant("DATABASE"));
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }
    if(!isset($_COOKIE["time"])){
        echo "no timestamp";
        die();
    }
    if(!isset($_COOKIE["uid"]) || !isset($_COOKIE["platform"]) || !isset($_COOKIE["email"])){
        echo "cookie error";
        die();
    }
    $id = $_COOKIE["uid"];
    $platform = $_COOKIE["platform"];
    $email = $_COOKIE["email"];

    $query = $conn->query("SELECT * FROM users WHERE (email='" . $email ."' AND accounttype='" . $platform . "' AND uid='" . $id . "')");

    if($query->num_rows == 0){
        echo "no users";
        die();
    }

    //First purge from friends list
    $query = $conn->query("DELETE FROM friends WHERE (friend1='" . $id ."' OR friend2='" . $id . "')");
    if(!$query){
        echo "error deleting friends";
        die();
    }
    
    //Then purge from user list
    $query = $conn->query("DELETE FROM users WHERE uid='" . $id . "'");
    if(!$query){
        echo "error deleting user";
        die();
    }

    //Now finally remove all cookies
    if (isset($_SERVER['HTTP_COOKIE'])) {
        $cookies = explode(';', $_SERVER['HTTP_COOKIE']);
        foreach($cookies as $cookie) {
            $parts = explode('=', $cookie);
            $name = trim($parts[0]);
            setcookie($name, '', time()-1000);
            setcookie($name, '', time()-1000, '/');
        }
    }
    echo "success";
?>