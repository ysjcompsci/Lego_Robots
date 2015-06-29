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
    def respond(self, reply):
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(reply)
        self.wfile.close()

    def find_sensor(self, driver_name):
        for s in range(0, 4):
            dir = '/sys/class/lego-sensor/sensor%d' % s
            f = open('%s/driver_name' % dir, 'r')
            if f.readline().strip() == driver_name:
                return dir

        return None            

    def do_GET(self): 
        parts = self.path[1:].split('/')
        print parts
        if len(parts) == 4 and parts[0] == 'motor':
            print 'Run %s to %s at speed %s' % (parts[1], parts[2], parts[3])
            d = MediumMotor(parts[1])
            d.run_position_limited(int(parts[2]), int(parts[3]), absolute=False)
            self.respond('OK')
        elif len(parts) == 2 and parts[0] == 'say':
            phrase = parts[1]
            phrase = phrase.replace('%20', ' ')
            print 'Say %s' % phrase
            os.system('espeak -a 200 -s 130 -v en-sc --stdout "%s" | aplay' % phrase)
            self.respond('OK')
        elif len(parts) == 2 and parts[0] == 'ir-sensor' and parts[1] == 'proximity':
            dir = self.find_sensor('lego-ev3-ir')
            f = open('%s/value0' % dir, 'r')
            v = f.readline().strip()
            f.close()
            self.respond(v)
        elif len(parts) == 2 and parts[0] == 'touch-sensor' and parts[1] == 'level':
            dir = self.find_sensor('lego-ev3-touch')
            f = open('%s/value0' % dir, 'r')
            v = f.readline().strip()
            f.close()
            self.respond(v)

class TCPServer(SocketServer.TCPServer):
    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)

httpd = TCPServer(("", int(sys.argv[1])), Handler)
print 'EV3 ready.'
httpd.serve_forever()
