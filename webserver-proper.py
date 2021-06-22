from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import os
from signal import signal, SIGINT
from sys import exit
from json.decoder import JSONDecodeError

# Catalog is a class that maintains a catalog of items.
class Catalog:

    file_name = 'catalog.txt'

    def __init__(self):
        if os.path.isfile(self.file_name):
            print('Found existing catalog file')
            # If there is an existing catalog saved to disk, then read it.
            with open(self.file_name, 'r') as json_file:
                try:
                    self.data = json.load(json_file)
                except JSONDecodeError as e:
                    print('Error reading previous catalog:', e)
                    self.data = {}
        else:
            print('Did not find previous catalog')
            self.data = {}

    # TODO: Each call to add overwrites the previous.
    def add(self, item, amount):
        self.data[item] = amount

    def contents(self):
        return self.data

    def save(self):
        print('Saving catalog')
        with open(self.file_name, 'w') as json_file:
            json.dump(self.data, json_file)

class Handler(BaseHTTPRequestHandler):

    catalog = None

    def send200(self):
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.end_headers()
        self.wfile.write('OK'.encode())

    def send400(self):
        self.send_response(400)
        self.send_header('content-type', 'text/html')
        self.end_headers()

    def send404(self):
        self.send_response(404)
        self.send_header('content-type', 'text/html')
        self.end_headers()

    def handleAdd(self, query):
        params = parse_qs(query)
        
        # If the `item` or `count` key does not exist, then the request was invalid.
        if 'item' in params.keys() and 'count' in params.keys():
             # Only one value for each key should be present.
            if len(params['item']) != 1 or len(params['count']) != 1:
                self.send400()
                return
                
            self.catalog.add(params['item'][0], params['count'][0])
            self.send200()
        else:
            self.send400()

    def handleList(self):
        # TODO: Return this to the user
        for key, value in self.catalog.contents().items():
            print(key, '   ', value)

        self.send200()

    def do_GET(self):
        parsed_url = urlparse(self.path)
        if parsed_url.path == '/catalog/add':
            self.handleAdd(parsed_url.query)
        elif parsed_url.path == '/catalog/list':
            self.handleList()
        else:
            # 404 means the URL doesn't correspond to anything on this server.
            self.send404()


def main():
    PORT = 8080

    Handler.catalog = Catalog()

    server = HTTPServer(('localhost', PORT), Handler)
    print('Server running on port %s' % PORT)
    server.serve_forever()


def handle_sigterm(signal_received, frame):
    Handler.catalog.save()
    exit(0)

if __name__ == '__main__':
    signal(SIGINT, handle_sigterm)
    main()
