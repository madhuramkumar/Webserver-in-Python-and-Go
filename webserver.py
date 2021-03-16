from http.server import HTTPServer, BaseHTTPRequestHandler

class helloHandler(BaseHTTPRequestHandler):

    def do_YAY(self):
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.end_headers()
        self.wfile.write('Hello World!'.encode())

    def do_FOOBAR(self):
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.end_headers()
        self.wfile.write('foobar'.encode())


    def do_GET(self):
        if self.path == '/':
            do_YAY(self)
        elif self.path == '/foobar':
            do_FOOBAR(self)

def main():
    PORT = 8080
    server = HTTPServer(('', PORT), helloHandler)
    print('Server running on port %s' % PORT)
    server.serve_forever()

if __name__ == '__main__':
    main()
