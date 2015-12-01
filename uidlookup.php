<?php
    include 'includes/mysqlconfig.php';
    $conn = new mysqli(constant("HOST"), constant("USER"), constant("PASSWORD"), constant("DATABASE"));
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }
    $uid = $_GET["uid"];
    $query = $conn->query("SELECT * FROM users WHERE uid=$uid");
    if($query && $query->num_rows > 0){
        $row = $query->fetch_assoc();
        $name = $row["name"];
        echo $name;
    }else{
        echo "ERROR: NO EXISTING USER";
    }
?>