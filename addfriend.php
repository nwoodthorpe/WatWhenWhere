<?php
    include 'includes/mysqlconfig.php';
    $conn = new mysqli(constant("HOST"), constant("USER"), constant("PASSWORD"),        constant("DATABASE"));
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }
    $uid1 = $_GET["uid1"];
    $uid2 = $_GET["uid2"];
    $uid1 = mysqli_real_escape_string($conn, $uid1);
    $uid2 = mysqli_real_escape_string($conn, $uid2);
    $query = $conn->query("INSERT INTO friends 
                (friend1, friend2)
                VALUES('" . $uid1 . "', '" . $uid2. "')");
    if($query){
        echo "success";   
    }else{
        echo "Error adding friend!";   
    }
?>