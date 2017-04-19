<?php

include "class.Client.php";

$client = new Client();
$json_array = array('cmd' => 'query',
					'query_num' => '1');
$client->send_msg($json_array)

?>