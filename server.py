#!/usr/bin/python3
"""
A simple HTTP server to integrate with the HTTP Post / XML API of Viewtron IP cameras.
Viewtron IP cameras have the ability to send an HTTP Post to an external server
when an alarm event occurs. Alarm events include human detection, car detection,
face detection / facial recognition, license plate detection / automatic license plate recogition.
All of the server connection information is configured on the Viewtron IP camera.
You can find Viewtron IP cameras at https://www.Viewtron.com

Written and maintained by Mike Haldas
mike@cctvcamerapros.net
"""

from viewtron import ViewtronServer
from datetime import datetime as dt
import base64
import csv
import os
import sys

# ====================== CONFIG ======================
SERVER_PORT = 5002

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "events.csv")
IMG_DIR = os.path.join(BASE_DIR, "images")
RAW_POST_DIR = os.path.join(BASE_DIR, "raw_posts")

os.makedirs(IMG_DIR, exist_ok=True)
os.makedirs(RAW_POST_DIR, exist_ok=True)

# save LPR images in IMG_DIR
SAVE_IMAGES = True

# save raw HTTP Posts to files for debugging
DEBUG_SAVE_RAW = True


# ====================== CALLBACKS ======================

def on_raw(text, client_ip):
    """Called for every POST body — saves raw XML for debugging."""
    if not DEBUG_SAVE_RAW:
        return
    ts = dt.now().strftime("%Y-%m-%d_%H-%M-%S.%f")[:-3]
    safe_ip = client_ip.replace('.', '-')
    raw_file = f"{RAW_POST_DIR}/raw_{ts}_{safe_ip}.xml"
    try:
        with open(raw_file, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"SAVED: {raw_file}")
    except Exception as e:
        print(f"SAVE FAILED: {e}")


def on_event(VT, client_ip):
    """Called for each parsed alarm event."""

    # Traject — just log a summary line
    if VT.category == 'traject':
        if VT.targets:
            t = VT.targets[0]
            r = t['rect']
            sys.stdout.write(f"\r[traject] {VT.source} | id={t['target_id']} type={t['target_type']} rect=({r['x1']},{r['y1']})-({r['x2']},{r['y2']})    ")
            sys.stdout.flush()
        return

    print(f"[{VT.category}] {VT.get_alarm_type()} from {client_ip}")
    print(f"Alarm Description: {VT.get_alarm_description()}")

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


def on_connect(client_ip):
    """Called when a camera first sends a keepalive."""
    print(f"Camera connected: {client_ip}")


# ====================== START ======================

if __name__ == "__main__":
    server = ViewtronServer(
        port=SERVER_PORT,
        on_event=on_event,
        on_connect=on_connect,
        on_raw=on_raw,
    )
    server.serve_forever()
