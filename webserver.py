from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

class helloHandler(BaseHTTPRequestHandler):

    my_dict = {}

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

    def do_ADD(self, query):
        params = parse_qs(query)
        print(params)
        self.my_dict[params['item'][0]] = params['count'][0]

    def do_LIST(self):
        print('calling list')
        print("item  count")
        for key, value in self.my_dict.items():
            print(key, '   ', value)

    def do_GET(self):
        #print(self.path)
        #print("my_dict = ", self.my_dict)
        parsed_url = urlparse(self.path)
        if parsed_url.path == '/':
            self.do_YAY()
        elif parsed_url.path == '/foobar':
            self.do_FOOBAR()
        elif parsed_url.path == '/catalog/add':
            self.do_ADD(parsed_url.query)
            #print(self.my_dict)
        elif parsed_url.path == '/catalog/list':
            self.do_LIST()
        else:
            print('path not found')

def main():
    PORT = 8080
    server = HTTPServer(('', PORT), helloHandler)
    print('Server running on port %s' % PORT)
    server.serve_forever()

if __name__ == '__main__':
    main()
