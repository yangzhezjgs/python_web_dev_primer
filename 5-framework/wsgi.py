import os
import io
import sys
import socket
#from hello import application

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
            response += str(data)
        return response

    def handler(self):
        self.parse_request()
        result = 'Hello,World'
        status = 200
        self.headers_set = [status,("Content-type","text/html"),("Content-Length", str(len(result)))]
        response = self.finish_response(result)
        return response.encode()

class WSGIRequestHandler(HTTPRequestHandler):
    def __init__(self, request, application):
        HTTPRequestHandler.__init__(self, request)
        self.env = {}
        self.application = application

    def get_env(self):
        self.env['wsgi.version'] = (1,0)
        self.env['wsgi.url_scheme'] = 'http'
        self.env['wsgi.input'] = io.StringIO(self.request.decode())
        self.env['wsgi.errors'] = sys.stderr
        self.env['wsgi.multithread'] = False
        self.env['wsgi.multiprocess'] = False
        self.env['REQUEST_METHOD'] = self.request_method
        self.env['PATH_INFO'] = self.path
        self.env['SERVER_NAME'] = 'localhost'
        self.env['SERVER_PORT'] = '8888'

    def handler(self):
        self.parse_request()
        self.get_env()
        env = self.env
        result = self.application(env, self.start_response)
        response = self.finish_response(result)
        return response.encode()
    
    def start_response(self, status, response_headers, exc_info=None):
        server_headers = [
            ('Date','2019-1-17'),
            ('Server','myserver')
        ]
        self.headers_set = [status, response_headers + server_headers]


class TCPServer:
    def __init__(self, host, port, RequestHandler, application):
        self.host = host
        self.port = port 
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.RequestHandler = RequestHandler
        self.application = application
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
            http_response = self.RequestHandler(request, self.application).handler()
            client_connection.sendall(http_response)
            client_connection.close()

def create_server(host, port ,application):
    server = TCPServer(host, port , WSGIRequestHandler, application)
    return server
'''
if __name__ == "__main__":
    server = TCPServer('localhost', 8888, WSGIRequestHandler, application)
    server.server_forever()
'''



