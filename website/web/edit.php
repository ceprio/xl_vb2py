<?php	include("config.inc");
	include("language.inc");
	include("display.inc");

	$t=$title;

	$menubar = implode('', file('menubar.html'));

	if (!$title) {
		
		//No node title given
		//
		$title=$invparam;
		$node=$invparam_d;
		$bar='<a href="index.php">index</a>';
	} else if (!$_COOKIE['wikiticket']) {

		// No login cookie present
		//
		$title=$invlogin;
		$node=$invlogin_d;
		$bar="<a href=\"login.php?title=$t\">log in</a> - <a href=\"index.php?title=$t\">cancel</a>";
	} else if ($node) {

		// Update node data
		//

		// Read old data
		//
		$file=fopen($nodedir.$t.".wiki", "a+"); fseek($file, 0);
		$old=fgets($file, 65536); 
		if ($rev=="on") {
			$mod1=fgets($file, 99); 
			$mod2=fgets($file, 99);
		}
		fclose($file);

		// Write new data
		//
		$file=fopen($nodedir.$t.".wiki", "w+");
		$node=stripslashes(ereg_replace("(\r\n|\n|\r)","<br>", $node));	// Linebreak to <br>
		fputs($file, $node."\n");

		// Update modification data
		//
		if ($rev=="on") {
			$user=$_COOKIE['wikiticket']; 
			fputs($file, "$user - ".date("j/n/y - h:i a")."\n");
			if ($mod1) fputs($file, $mod1); if ($mod2) fputs($file, $mod2);
		}
		fclose($file);

		$title=$success;
		$node='<b>'.$t.'</b>'.$success_d;
		$bar="<a href=\"index.php?title=$t\">node</a>";

	} else {

		// Node edit form
		//

		$node='<form method="post" action="edit.php"><textarea wrap="soft" name="node" style="width: 100%; height: 200px;">';

		$file=fopen($nodedir.$t.".wiki", "a+"); fseek($file, 0);
		if (filesize($nodedir.$t.".wiki")) {

			// Read current node data (if present)
			//
			$node.=fgets($file, 65536);
			$node=substr($node, 0, strlen($node)-1);		// Remove terminating linebreak
			$node=stripslashes(ereg_replace("<br>","\n", $node));	// <br> to linebreak
		}
		
		$node.="</textarea><input name=\"rev\" type=\"checkbox\" checked>$track<br><input type=\"submit\" name=\"submit\" value=\"Submit\"><input type=\"hidden\" name=\"title\" value=\"$t\"><form>";

		$bar="<a href=\"index.php?title=$t\">$return</a>";
		fclose($file);
	}

	display($title, $node, $bar, $template, $menubar);
?>
