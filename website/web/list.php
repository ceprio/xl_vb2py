<?php	include("config.inc");
	include("language.inc");
	include("display.inc");

	$title=$nodelist;

	$menubar = implode('', file('menubar.html'));

	// Read node data.
	//
	if ($dir=opendir($nodedir)) {
		while ($file=readdir($dir)) {
			if (strstr($file, ".wiki")) {
				$file=substr($file, 0, strlen($file)-5);
	                	$node.="<a href=\"index.php?title=$file\">$file</a><br>";
			}
		}
		closedir($dir);
	}

	display($title, $node, $bar, $template, $menubar); 
?>
