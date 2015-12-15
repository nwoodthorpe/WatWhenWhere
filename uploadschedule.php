<?php
    if(!isset($_POST["schedule"])){
        header('Location: index.html');   
    }
    session_start();
    $email = $_COOKIE["email"];
    $name = $_COOKIE["name"];
    $platform = $_COOKIE["platform"];
    $timestamp = $_COOKIE["timestamp"];
    $schedule = $_POST["schedule"];
    

    if((time() - $timestamp) > 3600){ //One Hour
        header('Location: index.html');
    }
    if($email == ""){
        header('Location: index.html');
    }
    if(!($platform == "google" or $platform == "facebook")){
        header('Location: index.html');   
    }
    $finalSchedule = "";
    $scheduleArray = preg_split('/\r\n|[\r\n]/', $schedule);
    array_pop($scheduleArray);
    $valid = false;
    $flag = false;
    foreach($scheduleArray as $line){
        if($flag){
            $flag = false;
            $temp = $line;
            $temp = str_replace(' ', '', $temp);
            $temp = str_replace(':', '', $temp);
            $finalSchedule = $finalSchedule . $temp . "&";
        }
        if(($line=="LEC") or ($line=="TUT")){
            $valid = true;
            $flag = true;
            continue;
        }
    }
    $finalSchedule = rtrim($finalSchedule, "&");
    $finalSchedule = preg_replace('/\&\&+/', '&', $finalSchedule);
    if($valid){
        include 'includes/mysqlconfig.php';
        $conn = new mysqli(constant("HOST"), constant("USER"), constant("PASSWORD"),        constant("DATABASE"));
        if ($conn->connect_error) {
            die("Connection failed: " . $conn->connect_error);
        }
        
        $query = $conn->query("SELECT * FROM users WHERE (email='" . $email . "' AND accounttype='" . $platform . "')");
        if(!$query){
            die('Error : ('. $conn->errno .') '. $conn->error);
        }
        if($query->num_rows > 0){
            //USER EXISTS, ONLY UPDATING SCHEDULE
            $query = $conn->query("UPDATE users SET schedule='" . $finalSchedule . "' WHERE (email='" . $email . "' AND accounttype='" . $platform . "')");
            
            if($query){
                setcookie("modifier", "scheduleUpdated", time() + 20);
                header('Location: main.html');
            }else{
                echo "ERROR UPDATING SCHEDULE...";  
            }
        }else{
            $query = $conn->query("INSERT INTO users 
                (name, accounttype, email, schedule)
                VALUES('" . $name . "', '" . $platform . "', '" . $email . "', '" . $finalSchedule . "')");
            
            if($query){
                $id = $conn->insert_id;
                setcookie("uid", $id);
                setcookie("modifier", "scheduleAdded", time() + 10);
                
                header('Location: main.html');
            }else{
                echo "ERROR ADDING USER...";
            }
        }
    }else{
        echo "INVALID SCHEDULE!";   
    }
?>