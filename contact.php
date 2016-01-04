<?php
    if(!isset($_GET["message"]) || !isset($_GET["name"]) || !isset($_GET["email"])){
        echo "Check all the fields are correctly filled in and try again!";
        die();
    }
    $email = $_GET["email"];
    $message = $_GET["message"];
    $name = $_GET["name"];
    if($email == ""|| $message == "" || $name == ""){
        echo "Check all the fields are correctly filled in and try again!";
        die();
    }

    $message = wordwrap($message, 70);
    
    mail("contact@watwhenwhere.ca","A Message From " . $name,$message,"From: $email\n");
    echo "success";
?>