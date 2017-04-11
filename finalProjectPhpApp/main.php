<?php
include "Client.php";

$client = new Client();

function recv_msg_loop()
{
	global $client;
	
	while(1)
	{
		$res = $client->recv_msg();
		if($res != null)
		{
			handle_msg($res);
		}
	}
}

function handle_msg($msg)
{
	$cmd = $msg['cmd'];
	echo "$cmd <br/>";
	ob_flush();
	flush();
	$drone_num = $msg['droneNum'];
	switch($cmd)
	{
		case "takeoff":
		{
			echo "drone $drone_num is in takeoff<br/>";
			ob_flush();
			flush();
			break;
		}
		case "land":
		{
			echo "drone $drone_num is in land<br/>";
			ob_flush();
			flush();
			break;
		}
		case "rtl":
		{
			echo "drone $drone_num is in rtl<br/>";
			ob_flush();
			flush();
			break;
		}
		case "landFin":
		{
			echo "drone $drone_num has landed<br/>";
			ob_flush();
			flush();
			break;
		}
	}
}

$json_array = array('cmd' => 'query',
					'query_num' => '1');
$client->send_msg($json_array);
recv_msg_loop();


?>