from __future__ import print_function
from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver
import socket
import os
import sys
import ev3dev.ev3 as ev3

if len(sys.argv) != 2:
    def eprint(*args, **kwargs):
        print(*args, file=sys.stderr, **kwargs)
    sys.exit(1)

class Handler(BaseHTTPRequestHandler):

    color_sensor_mode = None

    def ensure_color_sensor_mode(self, dir, mode):
        if self.color_sensor_mode == mode:
            return

        f = open('%s/mode' % dir, 'w')
        f.write(mode)
        f.close()

        self.color_sensor_mode = mode

    def respond(self, reply):
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(bytes(reply, 'UTF-8'))

    def find_sensor(self, driver_name):
        for s in range(0, 4):
            dir = '/sys/class/lego-sensor/sensor%d' % s
            f = open('%s/driver_name' % dir, 'r')
            if f.readline().strip() == driver_name:
                return dir

        return None            

    def do_GET(self): 
        parts = self.path[1:].split('/')
        print (parts)
        if len(parts) == 4 and parts[0] == 'mediummotor':
            print ('Run %s to %s at speed %s' % (parts[1], parts[2], parts[3]))
            d = ev3.MediumMotor('out' + parts[1])
            d.run_timed(time_sp=int(parts[2]), speed_sp=int(parts[3]))	    
            #d.run_position_limited(int(parts[2]), int(parts[3]), absolute=False)
            self.respond('OK')
        elif len(parts) == 4 and parts[0] == 'largemotor':
            print ('Run %s to %s at speed %s' % (parts[1], parts[2], parts[3]))
            d = ev3.LargeMotor('out' + parts[1])
            d.run_timed(time_sp=int(parts[2]), speed_sp=int(parts[3]))	    
            #d.run_position_limited(int(parts[2]), int(parts[3]), absolute=False)
            self.respond('OK')

        elif len(parts) == 2 and parts[0] == 'say':
            phrase = parts[1]
            phrase = phrase.replace('%20', ' ')
            print ('Say %s' % phrase)
            os.system('espeak -a 200 -s 130 -v en-sc --stdout "%s" | aplay' % phrase)
            self.respond(bytes('OK', 'UTF-8'))
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
        elif len(parts) == 2 and parts[0] == 'color-sensor' and parts[1] == 'ambient-level':
            dir = self.find_sensor('lego-ev3-color')
            self.ensure_color_sensor_mode(dir, 'COL-AMBIENT')
            f = open('%s/value0' % dir, 'r')
            v = f.readline().strip()
            f.close()
            self.respond(v)
        elif len(parts) == 3 and parts[0] == 'mediumtimed':
            print('Run %s at speed %s' % (parts[1],parts[2]))
            d = ev3.MediumMotor('out' + parts[1])
            d.run_timed(time_sp=int(parts[2]), speed_sp=500)
            self.respond('OK')
        elif len(parts) == 3 and parts[0] == 'largetimed':
            print('Run %s at speed %s' % (parts[1],parts[2]))
            d = ev3.LargeMotor('out' + parts[1])
            d.run_timed(time_sp=int(parts[2]), speed_sp=500)
            self.respond('OK')
        elif len(parts) == 2 and parts[0] == 'mediumon':
            print('Run %s' % (parts[1]))
            d = ev3.MediumMotor('out' + parts[1])
            d.run_forever()
            self.respond('OK')
        elif len(parts) == 2 and parts[0] == 'largeon':
            print('Run %s' % (parts[1]))
            d = ev3.LargeMotor('out' + parts[1])
            d.run_forever()
            self.respond('OK')
        elif len(parts) == 2 and parts[0] == 'mediumoff':
            print('Stop %s' % (parts[1]))
            d = ev3.MediumMotor('out' + parts[1])
            d.stop()
            self.respond('OK')
        elif len(parts) == 2 and parts[0] == 'largeoff':
            print('Stop %s' % (parts[1]))
            d = ev3.LargeMotor('out' + parts[1])
            d.stop()
            self.respond('OK')


class TCPServer(socketserver.TCPServer):
    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)

httpd = TCPServer(("", int(float(sys.argv[1]))), Handler)
print ('EV3 ready.')

print ('http://snap.berkeley.edu/snapsource/snap.html#open:http://localhost:1330/snap-ev3')
httpd.serve_forever()
