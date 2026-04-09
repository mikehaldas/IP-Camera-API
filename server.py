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
from viewtron import ViewtronEvent
import xmltodict
import base64
import csv
import socket
import os
import threading
import time
import sys

# ====================== CONFIG ======================
SERVER_PORT = 5002
API_POST_URL = '/API'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "events.csv")
IMG_DIR = os.path.join(BASE_DIR, "images")
RAW_POST_DIR = os.path.join(BASE_DIR, "raw_posts")

os.makedirs(IMG_DIR, exist_ok=True)
os.makedirs(RAW_POST_DIR, exist_ok=True)

# save LPR images in IMG_DIR
SAVE_IMAGES = True

# print raw HTTP Posts to files for debugging
DEBUG_SAVE_RAW = True

# print keep alive posts for debugging
DEBUG_KEEPALIVE = False

# ====================== TRAJECT CONFIG ======================
# save all raw traject XML posts (set to 0 for unlimited)
TRAJECT_RAW_SAVE_MAX = 0

# ====================== TRAJECT SESSION STATE ======================
traject_lock = threading.Lock()
traject_post_count = 0         # total traject posts this session
traject_raw_saved = 0          # how many raw posts we've saved so far
traject_timestamps = []        # recent timestamps for rate calculation
traject_targets = {}           # targetId -> {first_seen, last_seen, post_count, last_type, last_rect}
traject_session_start = None   # when first traject post arrived


def handle_traject(text, client_ip, headers):
    """Handle a traject (smart track) post. Updates live console, saves limited raw XML."""
    global traject_post_count, traject_raw_saved, traject_session_start

    now = time.time()

    # parse out traject fields from XML
    target_id = "?"
    target_type = "?"
    rect_str = "?"
    source = "IPC"
    try:
        data = xmltodict.parse(text)
        config = data.get('config', {})
        version = config.get('@version', '')

        # determine source (IPC v1.x vs NVR v2.0)
        if version.startswith('2'):
            source = "NVR"
            device_info = config.get('deviceInfo', {})
            ch = device_info.get('channelId', '?')
            source = f"NVR-ch{ch}"

        # device name
        device_name = config.get('deviceName', '') or config.get('deviceInfo', {}).get('deviceName', '')
        if isinstance(device_name, dict):
            device_name = device_name.get('#text', '') or device_name.get('value', '')

        # parse traject items
        traject_data = config.get('traject', {})
        items = traject_data.get('item', []) if isinstance(traject_data, dict) else []
        if not isinstance(items, list):
            items = [items] if items else []

        if items:
            item = items[0]
            if isinstance(item, dict):
                tid = item.get('targetId', {})
                target_id = tid.get('#text', str(tid)) if isinstance(tid, dict) else str(tid)

                tt = item.get('targetType', {})
                target_type = tt.get('#text', str(tt)) if isinstance(tt, dict) else str(tt)

                rect = item.get('rect', {})
                x1 = rect.get('x1', {})
                y1 = rect.get('y1', {})
                x2 = rect.get('x2', {})
                y2 = rect.get('y2', {})
                # xmltodict may return dicts with #text or plain strings
                x1 = x1.get('#text', str(x1)) if isinstance(x1, dict) else str(x1)
                y1 = y1.get('#text', str(y1)) if isinstance(y1, dict) else str(y1)
                x2 = x2.get('#text', str(x2)) if isinstance(x2, dict) else str(x2)
                y2 = y2.get('#text', str(y2)) if isinstance(y2, dict) else str(y2)
                rect_str = f"({x1},{y1})-({x2},{y2})"
    except Exception as e:
        pass  # still count the post even if parsing fails

    with traject_lock:
        traject_post_count += 1
        if traject_session_start is None:
            traject_session_start = now
            print()  # blank line before first traject output

        # rate calculation (posts in last 2 seconds)
        traject_timestamps.append(now)
        cutoff = now - 2.0
        while traject_timestamps and traject_timestamps[0] < cutoff:
            traject_timestamps.pop(0)
        rate = len(traject_timestamps) / 2.0

        # per-target tracking
        if target_id not in traject_targets:
            traject_targets[target_id] = {
                'first_seen': now, 'last_seen': now,
                'post_count': 0, 'last_type': target_type, 'last_rect': rect_str
            }
        t = traject_targets[target_id]
        t['last_seen'] = now
        t['post_count'] += 1
        t['last_type'] = target_type
        t['last_rect'] = rect_str

        # save raw XML (unlimited when TRAJECT_RAW_SAVE_MAX=0)
        if TRAJECT_RAW_SAVE_MAX == 0 or traject_raw_saved < TRAJECT_RAW_SAVE_MAX:
            traject_raw_saved += 1
            ts = dt.now().strftime("%Y-%m-%d_%H-%M-%S.%f")[:-3]
            safe_ip = client_ip.replace('.', '-')
            raw_file = f"{RAW_POST_DIR}/traject_{ts}_{safe_ip}.xml"
            try:
                with open(raw_file, 'w', encoding='utf-8') as f:
                    f.write("=== HEADERS ===\n")
                    for h, v in headers:
                        f.write(f"{h}: {v}\n")
                    f.write(f"\n=== BODY ===\n")
                    f.write(text)
            except:
                pass

        # live updating console line
        active_targets = sum(1 for t in traject_targets.values() if now - t['last_seen'] < 3.0)
        line = f"[traject] {source} | id={target_id} type={target_type} rect={rect_str} | {rate:.1f}/sec | targets: {active_targets} active, {len(traject_targets)} total | #{traject_post_count}"
        sys.stdout.write(f"\r{line:<120}")
        sys.stdout.flush()


def print_traject_stats():
    """Print traject session summary on shutdown."""
    with traject_lock:
        if traject_post_count == 0:
            return

        print(f"\n\n{'='*70}")
        print(f"TRAJECT SESSION SUMMARY")
        print(f"{'='*70}")
        print(f"Total traject posts received: {traject_post_count}")
        print(f"Raw XML posts saved:          {traject_raw_saved}")
        print(f"Unique target IDs:            {len(traject_targets)}")

        if traject_session_start:
            duration = time.time() - traject_session_start
            print(f"Session duration:             {duration:.1f}s")
            if duration > 0:
                print(f"Average post rate:            {traject_post_count / duration:.1f}/sec")

        if traject_targets:
            print(f"\nPer-target breakdown:")
            print(f"  {'ID':<10} {'Type':<10} {'Posts':<8} {'Duration':<12} {'Rate':<10} {'Last Rect'}")
            print(f"  {'-'*10} {'-'*10} {'-'*8} {'-'*12} {'-'*10} {'-'*20}")
            for tid, info in sorted(traject_targets.items(), key=lambda x: x[1]['first_seen']):
                dur = info['last_seen'] - info['first_seen']
                rate = info['post_count'] / dur if dur > 0 else 0
                dur_str = f"{dur:.1f}s" if dur > 0 else "<1s"
                rate_str = f"{rate:.1f}/sec" if dur > 0 else "—"
                print(f"  {tid:<10} {info['last_type']:<10} {info['post_count']:<8} {dur_str:<12} {rate_str:<10} {info['last_rect']}")
        print(f"{'='*70}\n")


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

    # Viewtron IP cameras send HTTP Posts but we will put a GET handler here anyway.
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

        # confirm camera is sending Keep Aline posts for debugging
        if length == 0 and DEBUG_KEEPALIVE:
            print(f"KEEP-ALIVE received from {client_ip} at {dt.now().strftime('%H:%M:%S')}")
            return

        body = self.rfile.read(length)
        text = body.decode('utf-8', errors='replace')

        # save the raw HTTP Header and Body for debugging (skip traject — handled separately)
        if DEBUG_SAVE_RAW and '<traject type="list"' not in text:
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

        # no need to do any further processing if the post does not contain XML data
        if '<?xml' not in text:
            return

        # === TRAJECT POSTS === (detect before alarm routing — no CSV, no images)
        if '<traject type="list"' in text:
            header_list = list(self.headers.items())
            handle_traject(text, client_ip, header_list)
            return

        try:
            VT = ViewtronEvent(text)
            if VT is None:
                return

            print(f"[{VT.category}] {VT.get_alarm_type()} from {client_ip}")
            alarm_descript = VT.get_alarm_description()
            print(f"Alarm Description: {alarm_descript}")
            VT.set_ip_address(client_ip)

            # process license plate recognition events
            if VT.category == 'lpr':
                print("LPR event detected!")
                plate = VT.get_plate_number()
                print(f"Plate Number: {plate}")

                # v2.0 vehicle type includes car attributes
                if hasattr(VT, 'get_car_brand') and VT.get_car_brand():
                    print(f"Vehicle: {VT.get_car_color()} {VT.get_car_brand()} {VT.get_car_model()} ({VT.get_car_type()})")

                if VT.is_plate_authorized():
                    print("Is plate authorized: Yes")
                    plate_auth = "Authorized Plate"
                else:
                    print("Is plate authorized: NO!")
                    plate_auth = "Plate NOT Authorized"
            # process face detection events
            elif VT.category == 'face':
                print("Face Detection event!")
                if hasattr(VT, 'get_face_age') and VT.get_face_age():
                    print(f"Face: {VT.get_face_age()} {VT.get_face_sex()}, glasses={VT.get_face_glasses()}, mask={VT.get_face_mask()}")
                plate_auth = "N/A"
                plate = "N/A"
            else:
                plate_auth = "N/A"
                plate = "N/A"

            # Does the event contain images and should we save them?
            if VT.images_exist() and SAVE_IMAGES:
                print("Post has images.")
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
                            print(f" {name} saved in {IMG_DIR}")
                        except Exception as e:
                            print(f" {name} save failed: {e}")

            # prepare the new record and add it to the CSV file log
            row = [
                VT.get_ip_cam(), client_ip, VT.get_alarm_type(), VT.get_alarm_description(),
                plate, plate_auth, VT.get_time_stamp_formatted(),
                f"{IMG_DIR}{VT.get_time_stamp()}-target.jpg",
                f"{IMG_DIR}{VT.get_time_stamp()}-overview.jpg"
            ]

            with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
                csv.writer(f).writerow(row)

            print(f"Adding record to {CSV_FILE}\n")
        except Exception as e:
            print(f"ERROR: {e}")

# ================ START Server ======================
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True  # allows Ctrl-C to work cleanly

if __name__ == "__main__":
    ip = get_lan_ip()
    server_address = ('', SERVER_PORT)
    httpd = ThreadedHTTPServer(server_address, handler)

    print(f"\nViewtron LPR Camera API Server RUNNING (multi-threaded)")
    print(f"http://{ip}:{SERVER_PORT}{API_POST_URL}")
    print("Ready to accept HTTP Posts from IP cameras...\n")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()
        print_traject_stats()
        print("Server stopped.")
