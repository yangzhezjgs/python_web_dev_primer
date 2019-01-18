from wsgi import create_server
from frame import Frame
app = Frame()

@app.route('/')
def index():
    return 'index'

@app.route('/hello')
def hello():
    return 'hello word'

if __name__ == "__main__":
    server = create_server('localhost', 8888, app)
    server.server_forever()