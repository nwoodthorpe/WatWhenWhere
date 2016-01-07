<?php
    $ip = $_GET["ip"];
    
    $path = $_SERVER['DOCUMENT_ROOT'];
    $path .= '/includes/mysqlconfig.php';
    include($path);
        
    $conn = new mysqli(constant("HOST"), constant("USER"), constant("PASSWORD"),        constant("DATABASE"));
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
        echo "shit";
    }
    
    $ip = mysqli_real_escape_string($conn, $ip);
    if($ip == "" || $ip == null){
        echo "shitt";
        die();
    }
    $query = $conn->query("INSERT INTO compare (datetime, ip)
    VALUES(NOW(), '" . $ip . "')");
    if($query){
        echo "recorded";
    }else{
        echo "shit";
    }
?>