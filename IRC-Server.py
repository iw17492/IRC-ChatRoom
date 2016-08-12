#!/usr/bin/python
import threading, sys, socket, re

class IRCServer(threading.Thread):
	def __init__(self, host, port):
		threading.Thread.__init__(self)
		self.host = host
		self.port = port
		self.listConn = []
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		try:
			self.server.bind((self.host, self.port))
			self.listConn.append(self.server)
		except socket.error as err_msg:
			print 'Bind Failed: ' + str(err_msg)
			sys.exit()

		self.server.listen(10)

	def chat(self, conn, addr):#2
		while True:
			recv_msg = conn.recv(4096)
			msg_content = re.search(r'SENDMSG:(?P<smg>[\s\S]*)', recv_msg).group('smg')
			reply_msg = 'SENDMSG:['+ str(addr[0]) +']:' + msg_content

			if re.search('QUIT',recv_msg):
				conn.close()
				self.listConn.remove(conn)
				recv_msg = str(addr[0]) + 'Disconnected'
				for c in self.listConn:
					if c != conn and c!= self.server:
						c.sendall(recv_msg)

			for c in self.listConn:
				if c != conn and c!= self.server:
					c.sendall(reply_msg)

	def run(self):#1
		print'Waiting for connections on port: ' , self.port
		while True:
			newc, addr = self.server.accept()
			print newc, addr
			self.listConn.append(newc)
			threading.Thread(target=self.chat, args=(newc, addr)).start()
			
if __name__ == '__main__':
	server = IRCServer('128.199.97.172', 9999)
	#server = IRCServer('127.0.0.1', 9999)
	server.run()

