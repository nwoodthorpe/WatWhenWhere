<?php
    if(!isset($_GET["message"]) || !isset($_GET["name"]) || !isset($_GET["email"])){
        echo "Fill in all the boxes please!";
        die();
    }
    $email = $_GET["email"];
    $message = $_GET["message"];
    $name = $_GET["name"];
    if($email == ""|| $message == "" || $name == ""){
        echo "Fill in all the boxes please!";
        die();
    }

    $message = wordwrap($message, 70);
    
    mail("contact@watwhenwhere.ca","A Message From " . $name,$message,"From: $email\n");
    echo "success";
?>