<?php
$uname = $_POST['unames'];
$upswd = $_POST['upds'];

if (!empty($uname) && !empty($upswd)) {
    $host = "localhost";
    $dbusername = "root";
    $dbpassword = "";
    $dbname = "login";

    $conn = new mysqli($host, $dbusername, $dbpassword, $dbname);

    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }

    $sql = "SELECT * FROM register1 WHERE uname1 = ? AND upswd1 = ?";
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("ss", $uname, $upswd);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($result->num_rows == 1) {
        echo "Login successful! Welcome, " . $uname;
        // Redirect to the Streamlit app URL with the username as a parameter
        header("Location: http://localhost:8501?username=" . urlencode($uname)); // Modified line
        exit;
    } else {
        echo "Invalid username or password!";
    }

    $stmt->close();
    $conn->close();
} else {
    echo "All fields are required!";
}
?>