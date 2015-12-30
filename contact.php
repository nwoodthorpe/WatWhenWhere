<?php
    $email = $_GET["email"];
    $message = $_GET["message"];
    $name = $_GET["name"];

    mail("contact@watwhenwhere.ca", "A Message From " + $name,  "Sent from " + $email + ":  " + $message);
    echo "success";
?>