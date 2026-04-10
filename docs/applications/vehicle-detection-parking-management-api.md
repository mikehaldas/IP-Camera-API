---
title: "Vehicle Detection & Parking Management API"
sidebar_label: "Vehicle & Parking"
description: "Detect vehicles and monitor parking violations with Viewtron IP camera API. Configure illegal parking zones and receive webhook alerts when vehicles park in prohibited areas."
keywords:
  - vehicle detection camera api
  - parking detection api
  - parking violation camera
  - illegal parking detection
  - pvd camera api
  - ndaa compliant vehicle detection
sidebar_position: 10
---

# Vehicle Detection & Parking Management API

Viewtron AI security cameras include built-in illegal parking detection (PVD) that runs entirely on the camera hardware — no cloud service or external AI software required. When a vehicle parks in a designated prohibited zone and remains beyond a configurable time threshold, the camera sends an HTTP POST webhook to your server with the detection event data, including images of the violation.

Parking violation detection (PVD) is distinct from [license plate recognition (LPR)](/docs/applications/license-plate-recognition-camera-api) — PVD detects the presence of a stationary vehicle in a prohibited zone, while LPR reads the plate number from a moving or stationary vehicle. PVD is also distinct from general vehicle detection via [intrusion detection](/docs/applications/human-detection-intrusion-api), which detects a vehicle entering a zone but does not track how long it remains parked. All Viewtron IP cameras and NVRs are NDAA compliant.

:::note Testing Status
PVD (illegal parking detection) has not been fully tested via HTTP Post webhook delivery. The camera configuration endpoint `GetSmartPvdConfig` is confirmed working, and the IPC smartType `PVD` is documented. The webhook XML format is expected to follow the same `CommonImagesLocation` pattern as other IPC smart detection events. This page will be updated as testing is completed.
:::

## What You Can Build

- **No-parking zone enforcement** — detect vehicles that park in fire lanes, handicapped zones, or restricted areas
- **Loading zone monitoring** — alert when a vehicle exceeds the allowed time in a loading dock or delivery zone
- **Fire lane compliance** — automated monitoring of fire lanes with violation logging and image capture
- **Parking lot management** — track illegal parking in reserved spots, employee-only areas, or visitor zones
- **Tow company integration** — automatically notify towing services when a parking violation exceeds a threshold
- **Municipal parking enforcement** — log violations with timestamped images for citation evidence

## How It Works

1. **Configure a parking violation zone** on the camera — define a polygon region where parking is prohibited
2. **Set the dwell time threshold** — configure how long a vehicle must remain parked before triggering an alert
3. **Enable HTTP POST webhooks** — point the camera at your server's IP and port
4. **Your server receives XML** when a violation occurs — the POST includes the PVD event data with images
5. **Parse the event** using the [Viewtron Python SDK](/docs/getting-started/python-sdk) (`pip install viewtron`) or raw XML parsing
6. **Take action** — save violation images, log to CSV, send alerts, or trigger enforcement workflows

## Event Data Included

Each parking violation webhook POST is expected to contain:

| Field | Description |
|-------|-------------|
| `smartType` | `PVD` (IPC illegal parking detection) |
| `boundary` | Polygon coordinates of the prohibited parking zone |
| `rect` | Bounding box of the detected vehicle |
| `eventId` / `targetId` | Unique IDs for the event and tracked target |
| `status` | `SMART_START`, `SMART_PROCEDURE`, or `SMART_STOP` |
| `sourceBase64Data` | Full-frame JPEG image (base64 encoded) |
| `targetBase64Data` | Cropped vehicle JPEG image (base64 encoded) |
| `currentTime` | Detection timestamp |

## Quick Start Example

This standalone script listens for parking violation events, prints details to the console, saves images, and logs to CSV:

```python
#!/usr/bin/env python3
"""Parking Violation Detection Receiver — Viewtron IP Camera API"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime as dt
import xmltodict
import base64
import csv
import os

# pip install xmltodict
# pip install viewtron
from viewtron import IllegalParking

PORT = 5002
IMG_DIR = "images"
CSV_FILE = "parking_violations.csv"
os.makedirs(IMG_DIR, exist_ok=True)


class ParkingViolationHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Respond with success XML to keep connection alive
        response = '<?xml version="1.0" encoding="UTF-8"?>\n'
        response += '<config version="1.0" xmlns="http://www.ipc.com/ver10">\n'
        response += '  <status>success</status>\n</config>'
        self.send_response(200)
        self.send_header('Content-Type', 'application/xml')
        self.send_header('Content-Length', str(len(response)))
        self.end_headers()
        self.wfile.write(response.encode())

        # Read POST body
        length = int(self.headers.get('Content-Length', 0))
        if length == 0:
            return
        body = self.rfile.read(length).decode('utf-8', errors='replace')
        if '<?xml' not in body:
            return

        try:
            data = xmltodict.parse(body)
            config = data.get('config', {})
            version = config.get('@version', '')

            # PVD is currently IPC-only (v1.x format)
            if version.startswith('2'):
                # NVR v2.0 PVD forwarding has not been tested
                return

            st = config.get('smartType', {})
            alarm_type = (st.get('#text') or str(st)).strip() if isinstance(st, dict) else str(st).strip()
            if alarm_type != 'PVD':
                return

            event = IllegalParking(body)
            client_ip = self.client_address[0]

            # Print event details
            print(f"\n{'='*60}")
            print(f"[{dt.now():%Y-%m-%d %H:%M:%S}] PARKING VIOLATION DETECTED")
            print(f"  Camera: {event.get_ip_cam()}")
            print(f"  Source: {client_ip}")
            print(f"  Type: {event.get_alarm_description()}")
            print(f"  Time: {event.get_time_stamp_formatted()}")

            # Save images
            ts = event.get_time_stamp()
            saved_files = []
            for get_img, exists, suffix in [
                (event.get_source_image, event.source_image_exists, "overview"),
                (event.get_target_image, event.target_image_exists, "vehicle"),
            ]:
                if exists() and get_img():
                    path = os.path.join(IMG_DIR, f"{ts}-parking-violation-{suffix}.jpg")
                    with open(path, "wb") as f:
                        f.write(base64.b64decode(get_img()))
                    saved_files.append(path)
                    print(f"  Image: {path}")

            # Log to CSV
            with open(CSV_FILE, 'a', newline='') as f:
                csv.writer(f).writerow([
                    event.get_time_stamp_formatted(),
                    event.get_ip_cam(),
                    event.get_alarm_type(),
                    event.get_alarm_description(),
                    client_ip,
                    "|".join(saved_files),
                ])
            print(f"  Logged to {CSV_FILE}")

        except Exception as e:
            print(f"Error: {e}")

    def log_message(self, format, *args):
        pass  # Suppress default HTTP log output

if __name__ == '__main__':
    print(f"Parking Violation Receiver running on port {PORT}")
    print(f"Images will be saved to {IMG_DIR}/")
    print(f"Events will be logged to {CSV_FILE}")
    print(f"Waiting for parking violation events...\n")
    HTTPServer(('', PORT), ParkingViolationHandler).serve_forever()
```

**To run:**

```bash
pip install xmltodict
# pip install viewtron
python3 parking_receiver.py
```

Then configure your camera to send HTTP POST events to `http://<your-server-ip>:5002/`. Enable the PVD detection type in the camera's httpPost subscription settings.

## Relevant API Endpoints

| Endpoint | Purpose | Reference |
|----------|---------|-----------|
| GetSmartPvdConfig | Read parking violation detection zone configuration | [Parking Violation Config](/docs/api-reference/smart-detection/parking-violation-detection-config) |
| SetHttpPostConfig | Configure webhook destination | [Webhook Config](/docs/api-reference/alarm/http-post-webhook-config) |
| GetAlarmStatus | Poll current alarm state | [Alarm Status](/docs/api-reference/alarm/alarm-status) |

## Related Applications

- [License Plate Recognition](/docs/applications/license-plate-recognition-camera-api) — read plate numbers from vehicles (distinct from parking detection)
- [Human Detection & Intrusion](/docs/applications/human-detection-intrusion-api) — detect vehicles entering zones (without dwell time tracking)
- [Loitering Detection](/docs/applications/loitering-detection-api) — dwell time detection for people (similar concept to PVD for vehicles)
- [Relay Control & IoT Automation](/docs/applications/relay-control-iot-automation-api) — trigger gates or barriers based on vehicle detection

## Related Products

- [Viewtron AI Security Cameras](https://www.cctvcamerapros.com/AI-security-cameras-s/1512.htm) — IP cameras with built-in vehicle detection and parking violation monitoring
- [Viewtron IP Camera NVRs](https://www.cctvcamerapros.com/IP-Camera-NVRs-s/1472.htm) — NVRs with HTTP POST event forwarding

## Questions & Development Inquiries

- **Email:** mike@viewtron.com
- **Phone:** 561-433-8488
- **Forum:** [NVR Webhook Setup Guide](https://videos.cctvcamerapros.com/support/topic/setup-nvr-api-webhooks)

Mike Haldas is available for questions, consultation, and custom software development for Viewtron API related projects. Email details about your project to mike@viewtron.com.
