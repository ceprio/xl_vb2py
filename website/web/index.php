<?php	include("config.inc");
	include("language.inc");
	include("display.inc");

	if (!$title) $title=$index;

	$terms="!-=+\\\"$%^\(\)@ \w"; 	// Characters allowed in node links. Regexp.

	$menubar = implode('', file('menubar.html'));

	// Read node data.
	//

	if (file_exists($nodedir.$title.".wiki")) {
		$file=fopen($nodedir.$title.".wiki", "r");
		$node=fgets($file, 65536);
		$node=preg_replace (
			array (
				"/\[([$terms]+)\]/",
				"/\[([$terms]+)\|([$terms]+)\]/"),
			array (
				"<a href=\"?title=\\1\">\\1</a>",
				"<a href=\"?title=\\2\">\\1</a>"), $node);

		$str=fgets($file, 99); 
		if ($str) {
			$node.="<br><br>$revhistory";
			while ($str) {
				$node.="<br>".$str;
				$str=fgets($file, 99);
			}
		}
		fclose($file);
	} else {
		$node=$empty;			
	}

	$bar="<a href=\"index.php\">$index</a> - <a href=\"list.php\">$all</a> - <a href=\"edit.php?title=$title\">$edit</a> - ";
	if ($_COOKIE['wikiticket']) $bar.="<a href=\"login.php?logging_out=1&title=$title\">$logout</a>";
	else $bar.="<a href=\"login.php?title=$title\">$login</a>";

	display($title, $node, $bar, $template, $menubar); 
?>
