<?php
$servername = "localhost";
$username = "root";
$password = "";
$database = "login";

$conn = mysqli_connect($servername, $username, $password, $database);
if (!$conn) {
    die("Connection failed: " . mysqli_connect_error());
}

if (isset($_GET['delete'])) {
    $email = $_GET['delete'];
    $sql = "DELETE FROM register1 WHERE email='$email'";
    mysqli_query($conn, $sql);
    header("Location: display.php");
    exit();
}

$sql = "SELECT * FROM register1";
$result = mysqli_query($conn, $sql);
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>User Records</title>
    <style>
        body {
            margin: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: url('back.jpg') no-repeat center center fixed;
            background-size: cover;
            padding: 40px;
            color: #333;
        }

        .container {
            max-width: 1000px;
            margin: auto;
            background-color: rgba(255, 255, 255, 0.95);
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.3);
            opacity: 80%;
        }

        h2 {
            text-align: center;
            color: #2c3e50;
            margin-bottom: 30px;
            font-size: 32px;
            text-shadow: 1px 1px 2px #fff;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
        }

        th, td {
            padding: 14px 16px;
            text-align: center;
        }

        th {
            background-color: #34495e;
            color: white;
            font-size: 16px;
        }

        tr:nth-child(even) {
            background-color: #f4f6f7;
        }

        tr:hover {
            background-color: #dfe6e9;
        }

        .btn {
            padding: 8px 16px;
            font-size: 14px;
            font-weight: 600;
            border: none;
            border-radius: 8px;
            text-decoration: none;
            transition: 0.3s ease;
        }

        .edit-btn {
            background-color: #27ae60;
            color: white;
        }

        .edit-btn:hover {
            background-color: #1e8449;
        }

        .delete-btn {
            background-color: #e74c3c;
            color: white;
        }

        .delete-btn:hover {
            background-color: #c0392b;
        }

        .action-buttons {
            display: flex;
            justify-content: center;
            gap: 10px;
        }

        @media (max-width: 600px) {
            table, thead, tbody, th, td, tr {
                display: block;
            }

            th {
                display: none;
            }

            td {
                text-align: right;
                position: relative;
                padding-left: 50%;
            }

            td::before {
                content: attr(data-label);
                position: absolute;
                left: 0;
                width: 50%;
                padding-left: 15px;
                font-weight: bold;
                text-align: left;
            }

            .action-buttons {
                flex-direction: column;
                align-items: center;
            }
        }
    </style>
</head>
<body>

<div class="container">
    <h2>User Records</h2>

    <table>
        <thead>
            <tr>
                <th>Username</th>
                <th>Email</th>
                <th>Password</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
        <?php while ($row = mysqli_fetch_assoc($result)) { ?>
            <tr>
                <td data-label="Username"><?= htmlspecialchars($row['uname1']) ?></td>
                <td data-label="Email"><?= htmlspecialchars($row['email']) ?></td>
                <td data-label="Password"><?= htmlspecialchars($row['upswd1']) ?></td>
                <td data-label="Actions">
                    <div class="action-buttons">
                        <a href="edit.php?email=<?= urlencode($row['email']) ?>" class="btn edit-btn">Edit</a>
                        <a href="display.php?delete=<?= urlencode($row['email']) ?>" class="btn delete-btn" onclick="return confirm('Are you sure you want to delete this user?')">Delete</a>
                    </div>
                </td>
            </tr>
        <?php } ?>
        </tbody>
    </table>
</div>

</body>
</html>
