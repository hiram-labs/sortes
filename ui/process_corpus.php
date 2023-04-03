<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // sortes bin is put on the PATH is set set during the docker build process
    exec("sortes", $output, $return_val);

    if ($return_val === 0) {
        echo "<h4>" . "Processing complete. Redirecting in 3 seconds..." . "</h4>";
        echo "<pre>" . implode("\n", $output) . "</pre>";
        sleep(3);
    } else {
        echo "<h4>" . "Processing error. Redirecting in 3 seconds..." . "</h4>";
        echo "<pre>" . implode("\n", $output) . "</pre>";
    }
    echo "<script>setTimeout(()=>{window.location.href = '/'},3000);</script>";
    exit;
}
?>



