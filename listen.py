import SimpleHTTPServer
import SocketServer
import socket
import os
import sys
from ev3.lego import MediumMotor

if len(sys.argv) != 2:
    print>>sys.stderr,'Syntax: %s <port>' % (sys.argv[0])
    sys.exit(1)

class Handler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self): 
        parts = self.path[1:].split('/')
        print parts
        if len(parts) == 4 and parts[0] == 'motor':
            print 'Run %s to %s at speed %s' % (parts[1], parts[2], parts[3])
            d = MediumMotor(parts[1])
	    d.run_position_limited(int(parts[2]), int(parts[3]), absolute=False) 

        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write('OK')
        self.wfile.close()

class TCPServer(SocketServer.TCPServer):
    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)

httpd = TCPServer(("", int(sys.argv[1])), Handler)
print 'EV3 ready.'
httpd.serve_forever()
