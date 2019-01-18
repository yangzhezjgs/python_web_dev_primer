import socket 

class HTTPRequestHandler:
    def __init__(self, request):
        self.request = request
    
    def handler(self):
        response = "HTTP/1.1 200 OK\n\n Hello, World!"
        return response.encode()

class TCPServer:
    def __init__(self, host, port, RequestHandler):
        self.host = host
        self.port = port 
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.RequestHandler = RequestHandler
        self.setup()

    def setup(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host,self.port))
        self.socket.listen(1)

    def server_forever(self):
        print("servering http on port {}".format(self.port))
        while True:
            client_connection, client_address = self.socket.accept()
            request = client_connection.recv(1024)
            print(request.decode())
            http_response = self.RequestHandler(request).handler()
            client_connection.sendall(http_response)
            client_connection.close()

if __name__ == "__main__":
    server = TCPServer('localhost', 8888, HTTPRequestHandler)
    server.server_forever()




