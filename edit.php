<?php
$servername = "localhost";
$username = "root";
$password = "";
$database = "login";

$conn = mysqli_connect($servername, $username, $password, $database);

if (!$conn) {
    die("Connection failed: " . mysqli_connect_error());
}

if (isset($_GET['email'])) {
    $email = $_GET['email'];
    $sql = "SELECT * FROM register1 WHERE email='$email'";
    $result = mysqli_query($conn, $sql);
    $user = mysqli_fetch_assoc($result);
} else {
    echo "Email not specified.";
    exit;
}

if (isset($_POST['update'])) {
    $new_uname = $_POST['uname1'];
    $new_pass1 = $_POST['upswd1'];
    $new_pass2 = $_POST['upswd2'];

    $update_sql = "UPDATE register1 SET uname1='$new_uname', upswd1='$new_pass1', upswd2='$new_pass2' WHERE email='$email'";
    mysqli_query($conn, $update_sql);

    header("Location: display.php");
    exit;
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>Edit User</title>
    <style>
        * {
            box-sizing: border-box;
        }
        body {
            margin: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(120deg, #d4fc79, #96e6a1);
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100vh;
        }
        .form-container {
            background-color: white;
            padding: 30px 40px;
            width: 400px;
            border-radius: 15px;
            box-shadow: 0px 10px 25px rgba(0, 0, 0, 0.2);
        }
        h2 {
            text-align: center;
            margin-bottom: 25px;
            color: #2c3e50;
        }
        label {
            font-weight: 500;
            color: #333;
        }
        input[type="text"],
        input[type="password"] {
            width: 100%;
            padding: 12px;
            margin: 10px 0 20px;
            border: 1px solid #ccc;
            border-radius: 8px;
            transition: all 0.3s ease;
        }
        input[type="text"]:focus,
        input[type="password"]:focus {
            border-color: #27ae60;
            box-shadow: 0 0 8px rgba(39, 174, 96, 0.2);
        }
        input[type="submit"] {
            background-color: #27ae60;
            color: white;
            border: none;
            padding: 12px;
            width: 100%;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            transition: background 0.3s;
        }
        input[type="submit"]:hover {
            background-color: #219150;
        }
    </style>
</head>
<body>

<div class="form-container">
    <h2>Edit User</h2>
    <form method="POST">
        <label>Username:</label>
        <input type="text" name="uname1" value="<?= htmlspecialchars($user['uname1']) ?>" required>

        <label>Password:</label>
        <input type="password" name="upswd1" value="<?= htmlspecialchars($user['upswd1']) ?>" required>

        <label>Confirm Password:</label>
        <input type="password" name="upswd2" value="<?= htmlspecialchars($user['upswd2']) ?>" required>

        <input type="submit" name="update" value="Update">
    </form>
</div>

</body>
</html>
