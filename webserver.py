from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import requests
import json
from signal import signal, SIGINT
from sys import exit
from json.decoder import JSONDecodeError

class helloHandler(BaseHTTPRequestHandler):


    def do_SENDSUCCESS(self):
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.end_headers()
        self.wfile.write('OK'.encode())

    def do_SENDFAILURE(self):
        self.send_response(400)
        self.send_header('content-type', 'text/html')
        self.end_headers()
        self.wfile.write('ERROR'.encode())

    def do_FOOBAR(self):
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.end_headers()
        self.wfile.write('foobar'.encode())

    def do_ADD(self, query):
        params = parse_qs(query)
        print(params)
        global my_dict
        my_dict[params['item'][0]] = params['count'][0]
        self.do_SENDSUCCESS()

    def do_LIST(self):
        global my_dict
        print("in list:", my_dict)
        print("item  count")
        for key, value in my_dict.items():
            print(key, '   ', value)
        self.do_SENDSUCCESS()

    def do_GET(self):
        parsed_url = urlparse(self.path)
        if parsed_url.path == '/':
            self.do_SENDSUCCESS()
        elif parsed_url.path == '/foobar':
            self.do_FOOBAR()
        elif parsed_url.path == '/catalog/add':
            self.do_ADD(parsed_url.query)
        elif parsed_url.path == '/catalog/list':
            self.do_LIST()
        else:
            self.do_SENDFAILURE()


def main():
    with open(file_name, 'r') as json_file:
        try:
            my_dict = json.load(json_file)
        except JSONDecodeError as e:
            print('Error:', e)
            pass
    print("******** My Dictionary read from file=", my_dict)
    PORT = 8080
    server = HTTPServer(('', PORT), helloHandler)
    print('Server running on port %s' % PORT)
    server.serve_forever()

def do_SAVE():
    with open(file_name, 'w') as json_file:
        json.dump(my_dict, json_file)

def sig_HANDLER(signal_received, frame):
    do_SAVE()
    print("Dictionary Saved")
    exit(0)

if __name__ == '__main__':
    my_dict = {}
    file_name = 'catalog.txt'
    signal(SIGINT, sig_HANDLER)
    main()
