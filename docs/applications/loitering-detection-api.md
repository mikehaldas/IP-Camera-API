---
title: "Loitering Detection Camera API"
sidebar_label: "Loitering Detection"
description: "Configure loitering detection on Viewtron IP cameras to alert when people or vehicles dwell in a defined zone beyond a configurable time threshold. Receive webhook events with images."
keywords:
  - loitering detection api
  - dwell time detection camera
  - loitering camera api
  - security camera dwell time alert
  - ndaa compliant loitering detection
  - suspicious activity detection camera
sidebar_position: 11
---

# Loitering Detection Camera API

Viewtron AI security cameras include built-in loitering detection that runs entirely on the camera hardware — no cloud service or external AI software required. When a person or vehicle remains in a defined zone beyond a configurable time threshold, the camera sends an HTTP POST webhook to your server with the detection event data, including a full-frame overview image and a cropped image of the loitering target.

Loitering detection differs from [intrusion detection](/docs/applications/human-detection-intrusion-api) in that it measures dwell time — an intrusion event fires immediately when a target enters a zone, while a loitering event only fires after the target has remained in the zone for longer than the configured time threshold. This makes loitering detection ideal for identifying suspicious behavior where brief presence is normal but prolonged presence is not. All Viewtron IP cameras and NVRs are NDAA compliant.

## What You Can Build

- **ATM security monitoring** — alert when someone lingers near an ATM beyond a normal transaction time
- **Retail loss prevention** — detect customers dwelling in high-theft areas for extended periods
- **Restricted area monitoring** — identify unauthorized individuals loitering near secure entrances, server rooms, or utility areas
- **Public safety alerts** — monitor bus stops, park benches, or public spaces for extended occupancy
- **Loading dock security** — detect unauthorized vehicles dwelling in delivery zones beyond permitted times
- **Progressive response** — combine with [active deterrent](/docs/applications/active-deterrent-sound-light-alarm-api) to escalate from light activation to siren based on dwell duration

## How It Works

1. **Configure a loitering zone** on the camera — define a polygon region and set the dwell time threshold (seconds)
2. **Enable object filters** — select which target types to monitor (person, vehicle, or both)
3. **Enable HTTP POST webhooks** — point the camera at your server's IP and port
4. **Your server receives XML** when loitering is detected — the POST includes alarm type, zone boundary, target bounding box, and base64 images
5. **Parse the event** using the [viewtron.py](https://github.com/mikehaldas/IP-Camera-API) library or raw XML parsing
6. **Take action** — save images, log to CSV, send alerts, trigger deterrent actions

## Event Data Included

Each loitering detection webhook POST contains:

| Field | Description |
|-------|-------------|
| `smartType` | `LOITER` (IPC loitering detection) |
| `boundary` | Polygon coordinates of the loitering zone |
| `rect` | Bounding box of the loitering target |
| `eventId` / `targetId` | Unique IDs for the event and tracked target |
| `status` | `SMART_START`, `SMART_PROCEDURE`, or `SMART_STOP` |
| `sourceBase64Data` | Full-frame JPEG image (base64 encoded) |
| `targetBase64Data` | Cropped target JPEG image (base64 encoded) |
| `currentTime` | Detection timestamp |

## Webhook XML Example

### IPC Format (v1.x) — LOITER

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<config version="1.7" xmlns="http://www.ipc.com/ver10">
  <smartType type="openAlramObj">LOITER</smartType>
  <deviceName type="string"><![CDATA[Lobby]]></deviceName>
  <currentTime type="tint64">1774792701902505</currentTime>
  <perimeter>
    <perInfo type="list" count="1">
      <item>
        <eventId type="uint32">5012</eventId>
        <targetId type="uint32">4812</targetId>
        <status type="perStatus">SMART_START</status>
        <boundary type="list" count="4">
          <item><point><x type="uint32">1200</x><y type="uint32">800</y></point></item>
          <item><point><x type="uint32">7500</x><y type="uint32">800</y></point></item>
          <item><point><x type="uint32">7500</x><y type="uint32">8500</y></point></item>
          <item><point><x type="uint32">1200</x><y type="uint32">8500</y></point></item>
        </boundary>
        <rect>
          <x1 type="uint32">3200</x1><y1 type="uint32">1500</y1>
          <x2 type="uint32">4800</x2><y2 type="uint32">8200</y2>
        </rect>
      </item>
    </perInfo>
  </perimeter>
  <sourceDataInfo>
    <sourceBase64Length>420000</sourceBase64Length>
    <sourceBase64Data>... (base64 JPEG) ...</sourceBase64Data>
  </sourceDataInfo>
  <listInfo count="1">
    <item>
      <targetImageData>
        <targetBase64Length>65000</targetBase64Length>
        <targetBase64Data>... (base64 JPEG) ...</targetBase64Data>
      </targetImageData>
    </item>
  </listInfo>
</config>
```

## Quick Start Example

This standalone script listens for loitering detection events, prints details to the console, saves images, and logs to CSV:

```python
#!/usr/bin/env python3
"""Loitering Detection Event Receiver — Viewtron IP Camera API"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime as dt
import xmltodict
import base64
import csv
import os

# pip install xmltodict
# Download viewtron.py from https://github.com/mikehaldas/IP-Camera-API
from viewtron import LoiteringDetection

PORT = 5002
IMG_DIR = "images"
CSV_FILE = "loitering_events.csv"
os.makedirs(IMG_DIR, exist_ok=True)


class LoiteringHandler(BaseHTTPRequestHandler):
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

            # Loitering is currently IPC-only (v1.x format)
            if version.startswith('2'):
                # NVR v2.0 loitering forwarding has not been tested
                return

            st = config.get('smartType', {})
            alarm_type = (st.get('#text') or str(st)).strip() if isinstance(st, dict) else str(st).strip()
            if alarm_type != 'LOITER':
                return

            event = LoiteringDetection(body)
            client_ip = self.client_address[0]

            # Print event details
            print(f"\n{'='*60}")
            print(f"[{dt.now():%Y-%m-%d %H:%M:%S}] LOITERING DETECTED")
            print(f"  Camera: {event.get_ip_cam()}")
            print(f"  Source: {client_ip}")
            print(f"  Type: {event.get_alarm_description()}")
            print(f"  Time: {event.get_time_stamp_formatted()}")

            # Save images
            ts = event.get_time_stamp()
            saved_files = []
            for get_img, exists, suffix in [
                (event.get_source_image, event.source_image_exists, "overview"),
                (event.get_target_image, event.target_image_exists, "target"),
            ]:
                if exists() and get_img():
                    path = os.path.join(IMG_DIR, f"{ts}-loitering-{suffix}.jpg")
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
    print(f"Loitering Detection Receiver running on port {PORT}")
    print(f"Images will be saved to {IMG_DIR}/")
    print(f"Events will be logged to {CSV_FILE}")
    print(f"Waiting for loitering events...\n")
    HTTPServer(('', PORT), LoiteringHandler).serve_forever()
```

**To run:**

```bash
pip install xmltodict
# Place viewtron.py in the same directory
python3 loitering_receiver.py
```

Then configure your camera to send HTTP POST events to `http://<your-server-ip>:5002/`. Enable the LOITER detection type in the camera's httpPost subscription settings.

## Relevant API Endpoints

| Endpoint | Purpose | Reference |
|----------|---------|-----------|
| GetSmartLoiteringConfig | Read loitering detection zone and time threshold configuration | [Loitering Detection Config](/docs/api-reference/smart-detection/loitering-detection-config) |
| SetHttpPostConfig | Configure webhook destination | [Webhook Config](/docs/api-reference/alarm/http-post-webhook-config) |
| GetAlarmStatus | Poll current alarm state | [Alarm Status](/docs/api-reference/alarm/alarm-status) |

## Related Applications

- [Human Detection & Intrusion](/docs/applications/human-detection-intrusion-api) — immediate zone entry detection (no dwell time requirement)
- [Vehicle Detection & Parking](/docs/applications/vehicle-detection-parking-management-api) — dwell time detection for vehicles in parking zones (PVD)
- [Active Deterrent](/docs/applications/active-deterrent-sound-light-alarm-api) — trigger sirens and strobe lights when loitering is detected
- [Real-Time Object Tracking](/docs/applications/real-time-object-tracking-api) — continuous position tracking for custom dwell time logic

## Related Products

- [Viewtron AI Security Cameras](https://www.cctvcamerapros.com/AI-security-cameras-s/1512.htm) — IP cameras with built-in loitering detection
- [Viewtron IP Camera NVRs](https://www.cctvcamerapros.com/IP-Camera-NVRs-s/1472.htm) — NVRs with HTTP POST event forwarding

## Questions & Development Inquiries

- **Email:** mike@viewtron.com
- **Phone:** 561-433-8488
- **Forum:** [NVR Webhook Setup Guide](https://videos.cctvcamerapros.com/support/topic/setup-nvr-api-webhooks)

Mike Haldas is available for questions, consultation, and custom software development for Viewtron API related projects. Email details about your project to mike@viewtron.com.
