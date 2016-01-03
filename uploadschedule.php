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
    $finalSchedule = "";
    $scheduleArray = preg_split('/\r\n|[\r\n]/', $schedule);
    array_pop($scheduleArray);
    $stored_time = "";
    $flag = false;
    //Preliminary d/m/y - m/d/y check
    $mdy = true;
        foreach($scheduleArray as $line){
        if(preg_match('/(\d{2})+\/+(\d{2})+\/+(\d{4})+ - +(\d{2})+\/+(\d{2})+\/+(\d{4})/', $line)){
            $dates = explode('-', $line);
            $intA = intval($dates[0][0]);
            $intC = intval($dates[0][3]);
            if($intA > 1){
                //D/M/Y
                $mdy = false;
                continue;
            }
            if($intC > 1){
                $mdy = true;
                continue;
            }
        }
    }
    foreach($scheduleArray as $line){
        $temp = $line;
        if($flag){
            if(preg_match('/(\d{2})+\/+(\d{2})+\/+(\d{4})+ - +(\d{2})+\/+(\d{2})+\/+(\d{4})/', $temp)){
                $temp = str_replace(' ', '', $temp);
                if(!$mdy){
                    $tempChar = $temp[0];
                    $temp[0] = $temp[3];
                    $temp[3] = $tempChar;
                    
                    $tempChar = $temp[1];
                    $temp[1] = $temp[4];
                    $temp[4] = $tempChar;
                    
                    $tempChar = $temp[11];
                    $temp[11] = $temp[14];
                    $temp[14] = $tempChar;
                    
                    $tempChar = $temp[12];
                    $temp[12] = $temp[15];
                    $temp[15] = $tempChar;
                    
                }
                $finalSchedule = $finalSchedule . $stored_time . '!' . $temp . '&';
                $flag = false;
            }
        }else{
            if(preg_match('/(?:[MTWF]|(?:Th))*\s\d+:\d\d(?:[AP]M)*\s-\s\d+:\d\d(?:[AP]M)*/',$temp)){
                $temp = str_replace(' ', '', $temp);
                $temp = str_replace(':', '', $temp);
                $stored_time = $temp;
                $flag = true;
            }
        }
    }
    if($finalSchedule == ""){
        $finalSchedule = "M1900-2050!01/01/2050-01/01/2050";
    }
    $finalSchedule = rtrim($finalSchedule, "&");
    $finalSchedule = preg_replace('/\&\&+/', '&', $finalSchedule);
    $finalSchedule = preg_replace('/TBA\&/', '', $finalSchedule);
        include 'includes/mysqlconfig.php';
        $conn = new mysqli(constant("HOST"), constant("USER"), constant("PASSWORD"),        constant("DATABASE"));
        if ($conn->connect_error) {
            setcookie("modifier", "scheduleError", time() + 10);
            header('Location: main.html');
        }
        
        $query = $conn->query("SELECT * FROM users WHERE (email='" . $email . "' AND accounttype='" . $platform . "')");
        if(!$query){
            setcookie("modifier", "scheduleError", time() + 10);
            header('Location: main.html');
        }
        if($query->num_rows > 0){
            //USER EXISTS, ONLY UPDATING SCHEDULE
            $query = $conn->query("UPDATE users SET schedule='" . $finalSchedule . "' WHERE (email='" . $email . "' AND accounttype='" . $platform . "')");
            
            if($query){
                setcookie("modifier", "scheduleAdded", time() + 20);
                header('Location: main.html');
            }else{
                setcookie("modifier", "scheduleError", time() + 10);
                header('Location: main.html');
            }
        }else{
            $query = $conn->query("INSERT INTO users 
                (name, accounttype, email, schedule)
                VALUES('" . $name . "', '" . $platform . "', '" . $email . "', '" . $finalSchedule . "')");
            
            if($query){
                $id = $conn->insert_id;
                setcookie("modifier", "scheduleAdded", time() + 10);
                header('Location: main.html');
            }else{
                setcookie("modifier", "scheduleError", time() + 10);
                header('Location: main.html');
            }
        }
?>