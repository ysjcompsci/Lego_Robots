import SimpleHTTPServer
import SocketServer
import socket
import os
import urllib2

# Port to listen to Snap on
SNAP_PORT = 1330
# Port for EV3 to listen on
EV3_PORT = 8192
# EV3 user ID
EV3_USER = 'robot'
# EV3 IP address
EV3_IP = '10.42.0.3'

class Handler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
	if self.path == '/snap-ev3':
            f = open('snap-ev3.xml', 'rb')
            self.send_response(200)
            self.send_header("Content-type", 'text/xml')
            fs = os.fstat(f.fileno())
            self.send_header("Content-Length", str(fs[6]))
            self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.copyfile(f, self.wfile)
            f.close()
        else:
            url = "http://%s:%d%s" % (EV3_IP, EV3_PORT, self.path)
            print url
            response = urllib2.urlopen(url, timeout=5).read()
            print '%s -> %s' % (self.path, response)
            self.send_response(200)
            self.send_header('Content-Type', 'application/octet-stream')
            self.send_header('Content-Length', str(len(response)))
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(response)
            self.wfile.close()

class TCPServer(SocketServer.TCPServer):
    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)

print "Starting listener on EV3"
#os.system('scp listen.py %s@%s:' % (EV3_USER, EV3_IP))
#os.system('ssh %s@%s -- nohup python listen.py %d &' % (EV3_USER, EV3_IP, EV3_PORT))

httpd = TCPServer(("", SNAP_PORT), Handler)
print "http://snap.berkeley.edu/snapsource/snap.html#open:http://localhost:1330/snap-ev3"
httpd.serve_forever()
