<?php	include("config.inc");
	include("display.inc");

	$menubar = implode('', file('menubar.html'));

	if ($user && $pass) {
		$file=fopen($nodedir."logins.txt", "a+");
		fputs($file, $user."\n");
		fclose($file);

		$file=fopen($nodedir."passwords.txt", "a+");
		fputs($file, md5($pass."\n")."\n");
		fclose($file);

		$title="User Added";
		$node="Really.";
	} else {
		$title="Add User";
		$node='<form action="adduser.php" method="post">Username: <input type="text" name="user" value=""><br>Password: <input type="password" name="pass"><br><input type="submit" name="submit" value="Submit"></form>';
	}	

	$bar='<a href="index.php">index</a>';

	display($title, $node, $bar, $template, $menubar); 
?>
