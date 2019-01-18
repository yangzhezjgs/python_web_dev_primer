class Frame:
    def __init__(self):
        self.url_map = {}

    def route(self, path):
        def decorator(func):
            self.url_map[path] = func
            return func
        return decorator

    def wsgi(self, environ, start_response):
        url = environ['PATH_INFO']
        if url in self.url_map:
            status = '200 OK'
            response_headers = [('Content-Type','text/plain')]
            start_response(status, response_headers)
            return self.url_map[url]()
        else:
            status = '404 Not Found'
            response_headers = [('Content-Type','text/plain')]
            start_response(status, response_headers)
            return '404 Not Found'

    def __call__(self, environ, start_response):
        return self.wsgi(environ, start_response)
