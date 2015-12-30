<?php
    $email = $_GET["email"];
    $message = $_GET["message"];
    $name = $_GET["name"];

    $message = wordwrap($message, 70);

    mail("contact@watwhenwhere.ca","A Message From " . $name,$message,"From: $email\n");
    echo "success";
?>