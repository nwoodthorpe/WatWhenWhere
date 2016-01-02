<?php
    include 'includes/mysqlconfig.php';
    $conn = new mysqli(constant("HOST"), constant("USER"), constant("PASSWORD"), constant("DATABASE"));
    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }
    $ids = explode(",", $_GET["ids"]);
    $schedules = array();
    foreach($ids as $id){
        $query = $conn->query("SELECT schedule FROM users WHERE uid=$id");
        if($query && $query->num_rows > 0){
            $row = $query->fetch_assoc();
            $sched = $row["schedule"];
            array_push($schedules, $sched);
        }else{
            echo "ERROR: NO EXISTING USER";
        }
    }
    $algoOutput = "\"" . implode("\" \"", $schedules) . "\"";
    $testinput = 'python python_modules/run.py ' . $algoOutput;
    echo shell_exec($testinput);
?>