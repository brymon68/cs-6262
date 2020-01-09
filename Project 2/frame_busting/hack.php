<!DOCTYPE html>
<html>
<body>

<?php
$redirect_url = $_GET['url'];
header("Location: " . $redirect_url);
?>

<a href="http://bank.example.com/redirect?url=http://gt-evil.com">Click here to log in</a>

</body>
</html>
