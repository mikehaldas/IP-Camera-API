#!/usr/bin/python3
"""
A simple HTTP server to integrate with the HTTP Post / XML API of Viewtron IP cameras.
Viewtron IP cameras have the ability to send an HTTP Post to an external server
when an alarm event occurs. Alarm events include human detection, car detection,
face detection / facial recognition, license plate detection / automatic license plate recogition.
All of the server connection information is configured on the Viewtron IP camera.
You can find Viewtron IP cameras at https://www.Viewtron.com

NOTE: This server ONLY handles license plate recognition at this time. Support for
human detection, vehicle detection, intrusion detection, line crossing detection, face detection,
facial recognition is under development.

Written and maintained by Mike Haldas
mike@cctvcamerapros.net
"""

from socketserver import ThreadingMixIn
from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime as dt
from viewtron import *
import xmltodict
import base64
import csv
import socket
import os
import threading
import time

# ====================== CONFIG ======================
SERVER_PORT = 5002
API_POST_URL = '/API'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "events.csv")
IMG_DIR = os.path.join(BASE_DIR, "images")
RAW_POST_DIR = os.path.join(BASE_DIR, "raw_posts")

os.makedirs(IMG_DIR, exist_ok=True)
os.makedirs(RAW_POST_DIR, exist_ok=True)

# print raw HTTP Posts to files?
DEBUG_SAVE_RAW = False

class_lookup = {
    'VEHICE':  {'class': LPR},
    'VEHICLE': {'class': LPR},
    'VFD':     {'class': FaceDetection},
    'VSD':     {'class': VideoMetadata},
    'AOILEAVE':{'class': IntrusionExit},
    'AOIENTRY':{'class': IntrusionEntry},
    'PEA':     {'class': IntrusionDetection}
}

def get_lan_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

class handler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"OK")

    def do_POST(self):
        # ===  XML RESPONSE  (this is what keeps the camera alive forever) ===
        success_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<config version="1.0" xmlns="http://www.ipc.com/ver10">
  <status>success</status>
</config>'''

        self.send_response(200)
        self.send_header('Content-Type', 'application/xml')
        self.send_header('Content-Length', str(len(success_xml)))
        self.end_headers()
        self.wfile.write(success_xml.encode('utf-8'))

        # === READ BODY ===
        length = int(self.headers.get('Content-Length', 0))
        client_ip = self.client_address[0]

        if length == 0:
            print(f"KEEP-ALIVE received from {client_ip} at {dt.now().strftime('%H:%M:%S')}")
            return

        body = self.rfile.read(length)
        text = body.decode('utf-8', errors='replace')

        if DEBUG_SAVE_RAW:
            ts = dt.now().strftime("%Y-%m-%d_%H-%M-%S.%f")[:-3]
            safe_ip = client_ip.replace('.', '-')
            raw_file = f"{RAW_POST_DIR}/raw_{ts}_{safe_ip}.xml"
            try:
                with open(raw_file, 'w', encoding='utf-8') as f:
                    f.write("=== HEADERS ===\n")
                    for h, v in self.headers.items():
                        f.write(f"{h}: {v}\n")
                    f.write("\n=== BODY ===\n")
                    f.write(text)
                print(f"SAVED: {raw_file}")
            except Exception as e:
                print(f"SAVE FAILED: {e}")

        if '<?xml' not in text:
            return

        try:
            data = xmltodict.parse(text)
            config = data.get('config', {})
            st = config.get('smartType', {})
            if isinstance(st, dict):
                alarm_type = st.get('#text') or st.get('value') or st.get('@type') or ''
            else:
                alarm_type = str(st)
            alarm_type = alarm_type.strip()
            print(f"alarm_type: [{alarm_type}] from {client_ip}")

            if alarm_type not in class_lookup:
                return

            #VT = LPR(text)
            VT = class_lookup[alarm_type]['class'](text)
            alarm_descript = VT.get_alarm_description()
            print(f"Alarm Description: {alarm_descript}")
            VT.set_ip_address(client_ip)
            plate = VT.get_plate_number() or "UNKNOWN"
            print(f"PLATE: {plate}")

            if VT.images_exist():
                for get_img, exists, suffix in [
                    (VT.get_source_image, VT.source_image_exists, "overview"),
                    (VT.get_target_image, VT.target_image_exists, "target")
                ]:
                    if exists() and get_img():
                        try:
                            img_data = base64.b64decode(get_img())
                            name = f"{VT.get_time_stamp()}-{suffix}.jpg"
                            path = os.path.join(IMG_DIR, name)
                            with open(path, "wb") as f:
                                f.write(img_data)
                            print(f" {name} saved")
                        except Exception as e:
                            print(f" {name} save failed: {e}")

            row = [
                VT.get_ip_cam(), client_ip, VT.get_alarm_type(), VT.get_alarm_description(),
                plate, VT.get_time_stamp_formatted(),
                f"{IMG_DIR}{VT.get_time_stamp()}-target.jpg",
                f"{IMG_DIR}{VT.get_time_stamp()}-overview.jpg"
            ]
            with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
                csv.writer(f).writerow(row)

            print(f"SUCCESS: {plate}\n")
        except Exception as e:
            print(f"ERROR: {e}")

# ================ START Server ======================

# Make HTTPServer multi-threaded
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True  # allows Ctrl-C to work cleanly

if __name__ == "__main__":
    ip = get_lan_ip()
    server_address = ('', SERVER_PORT)
    httpd = ThreadedHTTPServer(server_address, handler)

    print(f"\nViewtron LPR Server RUNNING (multi-threaded)")
    print(f"http://{ip}:{SERVER_PORT}{API_POST_URL}")
    print("Ready to accept events from unlimited cameras simultaneously...\n")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()
        print("Server stopped.")
