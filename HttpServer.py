import socket
import time
import threading

# def thread_server(self,conn,addr):
# 	print("Got Connection from: ", str(addr))
# 	data = conn.recv(1024)
# 	data_in_str = bytes.decode(data)
#
# 	request_method = data_in_str.split(' ')[0]  # HEAD / GET
# 	print("Method: ", str(request_method))
# 	print("Request Body: ", str(data_in_str))
#
# 	if request_method == 'GET' or request_method == 'HEAD':
# 		file_requested = data_in_str.split(' ')[1]  # file wanted
# 		file_requested = file_requested.split('?')[0]
# 		if file_requested == '/':
# 			file_requested = '/index.html'
# 		file_requested = self.file + "\\" + file_requested[1:]
# 		print("Serving web page [", file_requested, "]")
#
# 		try:
# 			file_handler = open(file_requested, 'rb')
# 			if (request_method == 'GET'):
# 				response_content = file_handler.read()
# 			file_handler.close()
#
# 			response_headers = self._gen_headers(200)
#
# 		except Exception as e:
# 			print('Warning, file not found. Serving response code 404\n', e)
# 			response_headers = self._gen_headers(404)
# 			if (request_method == 'GET'):
# 				response_content = b'<html><body><p>Error 404: File not found</p><p>Python HTTP server</p></body></html>'
# 		server_response = response_headers.encode()
# 		if (request_method == 'GET'):
# 			server_response += response_content
# 		conn.send(server_response)
# 		print('Closing connection with client')
# 		conn.close()
# 	else:
# 		print('Unknown HTTP request method: ', request_method)

class Server(object):
	def __init__(self, port):
		self.host = '127.0.0.1'
		self.port = port
		self.file = 'D:\HttpServer'
	def activate_server(self):
		self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		try:
			print ("Starting server on {} : {}".format(self.host,self.port))
			self.socket.bind((self.host,self.port))
		except Exception as e :
			print ("Warning: Could not aquite port: {} \n".format(self.port))
			print ("Trying another port...")

			user_port = self.port
			self.port=8080

			try:
				print("Starting server on {} : {}".format(self.host, self.port))
				self.socket.bind((self.host,self.port))

			except Exception as e:
				print ("Failed..")
				self.shutdown()
				import sys
				sys.exit(1)
		print ("Connecting to server on port: {} ".format(str(self.port)))
		print ("Press Ctrl+C to shut down the server and exit")
		self._wait_for_connections()

	def shutdown(self):
		try:
			print("Shutting down the server")
			self.socket.shutdown(socket.SHUT_RDWR)

		except Exception as e:
			print("Warning: could not shut down the socket. Maybe it was already closed?", e)

	def _gen_headers(self,code):
		h=''
		if (code == 200):
			h = 'HTTP/1.1 200 OK\n'
		elif (code == 404):
			h = 'HTTP/1.1 404 Not Found\n'

		current_date = time.strftime('%a, %d %b %Y %H:%M:%S',time.localtime())
		h+= 'Date: {} \n'.format(current_date)
		h+= 'Server: Simple-Python-HTTP-Server\n'
		h+= 'Connection: Close\n\n'

		return h

	def _wait_for_connections(self):
		while True:
			print ("Awaiting for new connection")
			self.socket.listen(3)
			conn,addr = self.socket.accept()
			print ("Got Connection from: ",str(addr))
			data = conn.recv(1024)
			data_in_str = bytes.decode(data)

			request_method = data_in_str.split(' ')[0] #HEAD / GET
			print ("Method: ",str(request_method))
			print ("Request Body: ", str(data_in_str))

			if request_method == 'GET' or request_method == 'HEAD':
				file_requested = data_in_str.split(' ')[1] #file wanted
				file_requested = file_requested.split('?')[0]
				if file_requested == '/':
					file_requested == '\index.html'
				file_requested = 'D:\\HttpServer\\index.html'
				print("Serving web page [", file_requested, "]")

				try:
					file_handler = open(file_requested,'rb')
					if (request_method == 'GET'):
						response_content = file_handler.read()
					file_handler.close()

					response_headers = self._gen_headers(200)

				except Exception as e:
					print ('Warning, file not found. Serving response code 404\n',e)
					response_headers = self._gen_headers(404)
					if (request_method == 'GET'):
						response_content = b'<html><body><p>Error 404: File not found</p><p>Python HTTP server</p></body></html>'
				server_response = response_headers.encode()
				if (request_method == 'GET'):
					server_response+=response_content
				print (server_response)
				conn.send(server_response)
				print ('Closing connection with client')
				conn.close()
			else:
				print ('Unknown HTTP request method: ',request_method)

print ('Starting web server..')
s=Server(1337)
s.activate_server()


