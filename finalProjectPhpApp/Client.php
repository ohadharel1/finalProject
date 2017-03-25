<?php
	
	class Client
	{
		var $host = "127.0.0.1"
		var $port = 10002
		var $socket = null
		
		function __construct()
		{
			$this->$socket = socket_create(AF_INET, SOCK_STREAM, 0) or die("Could not create socket\n");
			$result = socket_connect($this->$socket, $this->$host, $this->$port) or die("Could not connect to server\n");
		}
		
		function send_msg($dict)
		{
			$msg = json_encode($dict, $assoc = true);
			socket_write($this->$socket, $msg, strlen($msg)) or die("Could not send data to server\n");
		}
		
		function recv_msg()
		{
			$res = socket_read($this->$socket, 1024) or die("Could not read server response\n");
			$dict = json_decode($res, $assoc = true);
			return $dict;
		}
		
		function close()
		{
			socket_close($this->$socket);
		}
	}
	
?>