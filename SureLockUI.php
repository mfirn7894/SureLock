<?php

$msg = null;

if (isset($_POST['button'])) {

	$code = rand(1,9) . rand(0,9) . rand(0,9) . rand(0,9) . rand(0,9) . rand(0,9);
	$fp = fopen(### INSERT doorCodeFilePath HERE ###, 'a+');
	$success = fwrite($fp,"{$code}\n");
	fclose($fp);
	$msg = "One time code for guest entry or shipping label: " . $code;
}
?>
<html>
<style>
h1 {text-align:left;
font-family:"Arial", Helvetica, sans-serif;
font-size:50;
}
body {text-align:center;
background-image: url(https://pixabay.com/static/uploads/photo/2016/01/01/07/57/new-york-1116320_960_720.jpg);
background-repeat: no-repeat;
background-size: 100% 100%;
}
#section {text-align:center;
color:white;
font-family:"Arial", Helvetica, sans-serif;
background-color:#003B75;
	  margin-top: 40px;
    margin-bottom: 100px;
}
</style>
<head>
	<title>Doorman</title>
</head>
<h1>SureLock Code Manager</h1>
<body>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<div id="section">
<br>
<p>Press "Generate Code" below to generate the one time use code.</p>
<p>Then, add the code to the "Special Shipping Instructions" section on your orders.</p>
	<?php if ($msg != null) : ?>
	<p><strong><?php echo $msg; ?></strong></p>
	<?php endif; ?>
	<form method="POST">
		<input type="submit" name="button" value="Generate Code"/>
	</form>
<br>
</div>
</body>
</html>