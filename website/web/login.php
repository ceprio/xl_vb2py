<?php	include("config.inc");
	include("language.inc");
	include("display.inc");

	// Returns the index of a given user
	//
	function fseekuser($file, $user) {		
		while ($user."\n"!=$str) { 
			$str=fgets($file, 99); 
			if (!$str) {$user=""; break;}
			$i++; 				
		}
		return $i;
	}

	$t=$title;	// Preserve the last node.

	$menubar = implode('', file('menubar.html'));

	if ($logging_out) {		

		// Log out
		//
		setcookie("wikiticket", "", time());
		$title=$loggedout;
		$node=$loggedout_d;
		$bar="<a href=\"index.php?title=$t\">$index</a> - <a href=\"login.php?title=$t\">$login</a>";

	} else if ($pass) {

		// Log in
		//

		// Get user number
		//
		$file=fopen($nodedir."logins.txt", "r");
		$index=fseekuser($file, $user);
		fclose($file);

		// Check against password
		//

		$file=fopen($nodedir."passwords.txt", "r");
		for ($j=0;$j<$index;$j++)
			$str=fgets($file, 99);
		fclose($file);

		if (md5($pass."\n")."\n"!=$str) {
			$title=$invpass;
			$node=$invpass_d;
			$bar="<a href=\"login.php?title=$t\">$login</a> - <a href=\"index.php?title=$t\">$return</a>";
		} else {						
		
			// Log user in for a month or so
			//

			setcookie("wikiticket", $user, time()+5184000);

			$title=$loggedin.$user;
			$node=$loggedin_d;
			$bar="<a href=\"index.php?title=$t\">$return</a> - <a href=\"login.php?logging_out=1&title=$t\">$logout</a>";
		}

	} else {
		$title=$login;
		$node="<form method=\"post\" action=\"login.php\">";
		$node.="Username: <input name=\"user\" type=\"text\"><br>";
		$node.="Password: <input type=\"password\" name=\"pass\"><br>";
		$node.="<input type=\"hidden\" name=\"title\" value=\"$t\">";
		$node.="<input type=\"submit\" value=\"$login\"></form>";
		$node.=$cookies;
		$bar="<a href=\"index.php?title=$t\">$return</a>";
	}

	display($title, $node, $bar, $template, $menubar);
?>
