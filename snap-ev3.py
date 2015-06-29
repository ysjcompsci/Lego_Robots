import SimpleHTTPServer
import SocketServer
import socket
import os
import urllib2

# Port to listen to Snap on
SNAP_PORT = 1330
# Port for EV3 to listen on
EV3_PORT = 8192
# EV3 user ID and IP address
EV3_CONNECTION = 'root@10.42.0.51'

class Handler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def send_head(self):
	if self.path == '/snap-ev3':
            f = open('snap-ev3.xml', 'rb')
            self.send_response(200)
            self.send_header("Content-type", 'text/xml')
            fs = os.fstat(f.fileno())
            self.send_header("Content-Length", str(fs[6]))
            self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            return f
        else:
            SimpleHTTPServer.SimpleHTTPRequestHandler.send_head(self)
            urllib2.urlopen("http://10.42.0.51:%d%s" % (EV3_PORT, self.path), timeout=5).read()
        
class TCPServer(SocketServer.TCPServer):
    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)

print "Starting listener on EV3"
os.system('scp listen.py %s:' % EV3_CONNECTION)
os.system('ssh %s -- nohup python listen.py %d &' % (EV3_CONNECTION, EV3_PORT))

httpd = TCPServer(("", SNAP_PORT), Handler)
print "http://snap.berkeley.edu/snapsource/snap.html#open:http://localhost:1330/snap-ev3"
httpd.serve_forever()
