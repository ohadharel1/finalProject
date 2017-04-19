<?php

	class Client
	{
		private $host = "132.74.211.89";
		private $port = 10002;
		private $socket = null;

		function __construct()
		{
			$this->socket = socket_create(AF_INET, SOCK_STREAM, 0) or die("Could not create socket\n");
			socket_connect($this->socket, $this->host, $this->port) or die("Could not connect to server\n");
		}

		function send_msg($dict)
		{
			$msg = json_encode($dict, $assoc = true);
			socket_write($this->socket, $msg, strlen($msg)) or die("Could not send data to server\n");
		}

		function recv_msg()
		{
			$res = socket_read($this->socket, 1024) or die("Could not read server response\n");
			$dict = json_decode($res, $assoc = true);
			return $dict;
		}

		function close()
		{
			socket_close($this->$socket);
		}
	}

?>
