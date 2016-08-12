#!/usr/bin/python
import threading, sys, socket, re
class IRCClient(object):
	"""docstring for IRCClient"""
	def __init__(self, host, port):
		self.host = host
		self.port = port
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			self.client.connect((self.host, self.port))
		except socket.error as err_msg:
			print 'Connection Failed:' + str(err_msg)

		threading.Thread(target=self.chat_msg).start()
		threading.Thread(target=self.show_msg).start()

	def chat_msg(self):
		while True:
			msg_chat = 'SENDMSG:'+raw_input()

			if re.search('QUIT',msg_chat):
				self.client.sendall('QUIT')
				self.client.close()
				print 'Disconnected'

			self.client.sendall(msg_chat)

	def show_msg(self):
		while True:
			msg = self.client.recv(4096)
			print msg

if __name__ == '__main__':
	a = IRCClient('128.199.97.172', 9999)