<?php	function display($title, $node, $bar, $fname, $menubar) {
		$file=fopen($fname, "r");
		while(!feof($file)) 
			$page.=fgets($file, filesize($fname));
		$page=str_replace('$title', $title, $page);
		$page=str_replace('$node', $node, $page);
		$page=str_replace('$bar', $bar, $page);
		$page=str_replace('$menubar', $menubar, $page);

		echo $page;
	}
?>
