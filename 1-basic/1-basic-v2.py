import socket 

class HTTPRequestHandler:
    def __init__(self, request):
        self.request = request
        self.request_method = None
        self.path = None
        self.request_version = None
        self.headers_set = []

    def parse_request(self):
        request = self.request.decode()
        request_line = request.splitlines()[0]
        request_line = request_line.rstrip('\r\n')
        (self.request_method,
         self.path,
         self.request_version
        ) = request_line.split()

    def finish_response(self, result):
        status, *response_headers = self.headers_set
        response = 'HTTP/1.1 {status}\r\n'.format(status=status)
        for header in response_headers:
            response += '{0}: {1}\r\n'.format(*header)
        response += '\r\n'
        for data in result:
            response += data
        return response

    def handler(self):
        self.parse_request()
        result = 'Hello,World'
        status = 200
        self.headers_set = [status,("Content-type","text/html"),("Content-Length", str(len(result)))]
        response = self.finish_response(result)
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




