---
title: "Human Detection & Intrusion Detection API"
sidebar_label: "Human Detection"
description: "Use the Viewtron IP camera HTTP API to detect humans and vehicles entering intrusion zones. Receive real-time webhook notifications with images and bounding boxes."
keywords:
  - ip camera human detection api
  - security camera intrusion detection
  - perimeter security camera api
  - camera that detects people
  - person detection camera api
  - ndaa compliant camera with api
sidebar_position: 1
---

# Human Detection & Intrusion Detection API

Viewtron AI security cameras include built-in human detection and intrusion detection that runs entirely on the camera hardware — no cloud service or external AI software required. When a person, vehicle, or motorcycle enters a defined intrusion zone, the camera sends an HTTP POST webhook to your server with the detection event data, including a full-frame overview image, a cropped image of the detected target, bounding box coordinates, and target classification (person, car, or motorcycle).

This is the most commonly used AI detection feature in the Viewtron API. You can configure up to 4 intrusion zones per camera, each with independent object filters and sensitivity settings. All Viewtron IP cameras and NVRs are NDAA compliant.

## What You Can Build

- **Automated intruder alerts** — send email, SMS, or push notifications with snapshot images when a person enters a restricted area
- **Presence-based automation** — turn on lights, activate relays, or trigger recordings when humans are detected
- **Custom alarm logic** — filter by target type (person vs car vs motorcycle) to reduce false alarms
- **Security dashboards** — aggregate intrusion events across multiple cameras with images and timestamps
- **Integration with access control** — connect to VMS, alarm panels, or building management systems
- **Dwell time tracking** — combine with [real-time traject data](/docs/applications/real-time-object-tracking-api) for continuous position monitoring

## How It Works

1. **Configure an intrusion zone** on the camera — define a polygon region and enable object filters (person, car, motor)
2. **Enable HTTP POST webhooks** — point the camera or NVR at your server's IP and port
3. **Your server receives XML** when a detection occurs — the POST includes alarm type, target coordinates, zone boundary, and base64 images
4. **Parse the event** using the [viewtron.py](https://github.com/mikehaldas/IP-Camera-API) library or raw XML parsing
5. **Take action** — save images, log to CSV, send alerts, trigger relays

## Event Data Included

Each intrusion detection webhook POST contains:

| Field | Description |
|-------|-------------|
| `smartType` | `PEA` (IPC) or `regionIntrusion` (NVR) |
| `targetType` | `person`, `car`, or `motor` |
| `rect` | Bounding box of the detected target (x1, y1, x2, y2) |
| `boundary` / `pointGroup` | Polygon coordinates of the intrusion zone |
| `eventId` / `targetId` | Unique IDs for the event and tracked target |
| `status` | `SMART_START`, `SMART_PROCEDURE`, or `SMART_STOP` |
| `sourceBase64Data` | Full-frame JPEG image (base64 encoded, ~500 KB) |
| `targetBase64Data` | Cropped target JPEG image (base64 encoded, ~50-80 KB) |
| `currentTime` | Detection timestamp |

## Object Filters

Each intrusion zone can independently filter by target type with per-object sensitivity (1-100):

| Object | Description | Default Sensitivity |
|--------|-------------|-------------------|
| `person` | Human detection | 50 |
| `car` | Vehicle (car/truck) detection | 50 |
| `motor` | Motorcycle/bicycle detection | 50 |

Disable any object type to ignore it entirely, or adjust sensitivity to control the detection threshold.

## Webhook XML Examples

### NVR Format (v2.0) — regionIntrusion

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="2.0.0" xmlns="http://www.ipc.com/ver10">
    <messageType>alarmData</messageType>
    <deviceInfo>
        <deviceName><![CDATA[Front Door]]></deviceName>
        <ip><![CDATA[192.168.0.55]]></ip>
        <mac><![CDATA[58:5B:69:40:F4:0D]]></mac>
        <channelId>1</channelId>
    </deviceInfo>
    <smartType>regionIntrusion</smartType>
    <currentTime>1772056914604000</currentTime>
    <eventInfo>
        <item>
            <eventId>916</eventId>
            <targetId>716</targetId>
            <boundary>area</boundary>
            <pointGroup>
                <item><x>1590</x><y>3080</y></item>
                <item><x>4715</x><y>3181</y></item>
                <item><x>4772</x><y>9217</y></item>
                <item><x>416</x><y>9141</y></item>
            </pointGroup>
            <rect><x1>3096</x1><y1>3715</y1><x2>4005</x2><y2>9861</y2></rect>
        </item>
    </eventInfo>
    <sourceDataInfo>
        <sourceBase64Length>400924</sourceBase64Length>
        <sourceBase64Data>... (base64 JPEG) ...</sourceBase64Data>
    </sourceDataInfo>
    <targetListInfo>
        <item>
            <targetId>716</targetId>
            <targetType>person</targetType>
            <targetImageData>
                <targetBase64Length>78796</targetBase64Length>
                <targetBase64Data>... (base64 JPEG) ...</targetBase64Data>
            </targetImageData>
        </item>
    </targetListInfo>
</config>
```

### IPC Format (v1.x) — PEA

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<config version="1.7" xmlns="http://www.ipc.com/ver10">
  <smartType type="openAlramObj">PEA</smartType>
  <deviceName type="string"><![CDATA[FaceCam]]></deviceName>
  <currentTime type="tint64">1774792701902505</currentTime>
  <perimeter>
    <perInfo type="list" count="1">
      <item>
        <eventId type="uint32">2357</eventId>
        <targetId type="uint32">2157</targetId>
        <status type="perStatus">SMART_START</status>
        <boundary type="list" count="5">
          <item><point><x type="uint32">450</x><y type="uint32">466</y></point></item>
          <!-- additional polygon points -->
        </boundary>
        <rect>
          <x1 type="uint32">4403</x1><y1 type="uint32">694</y1>
          <x2 type="uint32">5909</x2><y2 type="uint32">8125</y2>
        </rect>
      </item>
    </perInfo>
  </perimeter>
  <!-- sourceDataInfo and listInfo with base64 images -->
</config>
```

## Quick Start Example

This standalone script listens for human detection events, prints details to the console, saves images, and logs to CSV:

```python
#!/usr/bin/env python3
"""Human Detection Event Receiver — Viewtron IP Camera API"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime as dt
import xmltodict
import base64
import csv
import os

# pip install xmltodict
# Download viewtron.py from https://github.com/mikehaldas/IP-Camera-API
from viewtron import (IntrusionDetection, RegionIntrusion)

PORT = 5002
IMG_DIR = "images"
CSV_FILE = "intrusion_events.csv"
os.makedirs(IMG_DIR, exist_ok=True)

class IntrusionHandler(BaseHTTPRequestHandler):
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

            # Route to the correct viewtron.py class
            if version.startswith('2'):
                msg_type = str(config.get('messageType', ''))
                smart_type = str(config.get('smartType', ''))
                if msg_type != 'alarmData' or smart_type != 'regionIntrusion':
                    return
                event = RegionIntrusion(body)
            else:
                st = config.get('smartType', {})
                alarm_type = (st.get('#text') or str(st)).strip() if isinstance(st, dict) else str(st).strip()
                if alarm_type != 'PEA':
                    return
                event = IntrusionDetection(body)

            client_ip = self.client_address[0]

            # Print event details
            print(f"\n{'='*60}")
            print(f"[{dt.now():%Y-%m-%d %H:%M:%S}] INTRUSION DETECTED")
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
                    path = os.path.join(IMG_DIR, f"{ts}-intrusion-{suffix}.jpg")
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
    print(f"Human Detection Receiver running on port {PORT}")
    print(f"Images will be saved to {IMG_DIR}/")
    print(f"Events will be logged to {CSV_FILE}")
    print(f"Waiting for intrusion events...\n")
    HTTPServer(('', PORT), IntrusionHandler).serve_forever()
```

**To run:**

```bash
pip install xmltodict
# Place viewtron.py in the same directory
python3 intrusion_receiver.py
```

Then configure your camera or NVR to send HTTP POST events to `http://<your-server-ip>:5002/`.

## Relevant API Endpoints

| Endpoint | Purpose | Reference |
|----------|---------|-----------|
| GetSmartPerimeterConfig | Read intrusion zone configuration | [Intrusion Detection Config](/docs/api-reference/smart-detection/intrusion-perimeter-detection-config) |
| SetHttpPostConfig | Configure webhook destination | [Webhook Config](/docs/api-reference/alarm/http-post-webhook-config) |
| GetAlarmStatus | Poll current alarm state | [Alarm Status](/docs/api-reference/alarm/alarm-status) |

## Related Applications

- [Home Assistant Integration](/docs/integrations/home-assistant) — person and vehicle detection as native HA sensors for automating lights, alarms, and notifications
- [Perimeter Security & Line Crossing](/docs/applications/perimeter-security-line-crossing-api) — tripwire detection and region entry/exit
- [Real-Time Object Tracking](/docs/applications/real-time-object-tracking-api) — continuous target position data via traject
- [Relay Control & IoT Automation](/docs/applications/relay-control-iot-automation-api) — trigger relays based on human detection
- [Webhook Event Notification](/docs/applications/webhook-event-notification-api) — complete webhook setup and format reference
- [Viewtron Python SDK](/docs/getting-started/python-sdk) — parse intrusion events in Python with typed accessors

## Related Products

- [Viewtron AI Security Cameras](https://www.cctvcamerapros.com/AI-security-cameras-s/1512.htm) — IP cameras with built-in human detection
- [Viewtron IP Camera NVRs](https://www.cctvcamerapros.com/IP-Camera-NVRs-s/1472.htm) — NVRs with HTTP POST event forwarding

For a walkthrough of human detection events in action, including zone configuration and live webhook output, see the [AI Security Camera System video guide](https://videos.cctvcamerapros.com/v/ai-security-camera-system.html).

## Questions & Development Inquiries

- **Email:** mike@viewtron.com
- **Phone:** 561-433-8488
- **Forum:** [NVR Webhook Setup Guide](https://videos.cctvcamerapros.com/support/topic/setup-nvr-api-webhooks)

Mike Haldas is available for questions, consultation, and custom software development for Viewtron API related projects. Email details about your project to mike@viewtron.com.
