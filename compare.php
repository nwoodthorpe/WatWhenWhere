<?php
    include 'includes/mysqlconfig.php';
    $conn = new mysqli(constant("HOST"), constant("USER"), constant("PASSWORD"), constant("DATABASE"));
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }
    $ids = explode(",", mysqli_real_escape_string($conn, $_GET["ids"]));
    $current_date = $_GET["date"];
    $current_date = mysqli_real_escape_string($conn, $current_date);
    $final_schedule = array();
    
    $schedules = array();
    foreach($ids as $id){
        $query = $conn->query("SELECT schedule FROM users WHERE uid=$id");
        if($query && $query->num_rows > 0){
            $row = $query->fetch_assoc();
            $sched = $row["schedule"];
            array_push($schedules, $sched);
            
        }
    }
    foreach($schedules as $schedule){
        $classes = explode('&', $schedule); //Seperate into classes
        $temp = "";
        foreach($classes as $class){
            $segments = explode('!', $class); //Segments[0] is time, [1] is date
            $dates = explode("-", $segments[1]); //Split the two dates
            $date1 = strtotime($dates[0]);
            $date2 = strtotime($dates[1]);
            $current = strtotime($current_date);
            if(($date1 <= $current) && ($date2 >= $current)){
                $temp = $temp . $segments[0] . "&";
            }
        }
        array_push($final_schedule, $temp);
    }

    $input = "\"" . implode("\" \"", $final_schedule) . "\"";
    $testinput = 'python python_modules/run.py ' . $input;
    echo shell_exec($testinput);
?>