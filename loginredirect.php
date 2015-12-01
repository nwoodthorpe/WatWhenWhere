<?php
    if(!isset($_POST["email"])){ //Simple check to see if user is authorized
        header('Location: index.html');
    }
    include 'includes/mysqlconfig.php';
    $conn = new mysqli(constant("HOST"), constant("USER"), constant("PASSWORD"),        constant("DATABASE"));
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }

    $platform = $_POST["platform"];
    $email = $_POST["email"];
    $name = $_POST["name"];
    if($email == ""){
        header('Location: index.html');   
    }
    $query = $conn->query("SELECT * FROM users WHERE (email='" . $email ."' AND accounttype='" . $platform . "')");
    if($query->num_rows > 0){
        $row = $query->fetch_assoc();
        
        setcookie("source", "new");
        setcookie("platform", $platform);
        setcookie("email", $email);
        setcookie("timestamp", time());
        setcookie("name", $name);
        setcookie("uid", $row["uid"]);
        
        if($row["schedule"] == ""){
            setcookie("source", "existing");
            header('Location: uploadschedule.html');   
        }else{
            header('Location: main.html');   
        }
    }else{
        setcookie("source", "new");
        setcookie("platform", $platform);
        setcookie("email", $email);
        setcookie("timestamp", time());
        setcookie("name", $name);
        header('Location: uploadschedule.html'); 
    }

    mysqli_close($conn);
?>