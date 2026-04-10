---
title: "Perimeter Security & Line Crossing Detection API"
sidebar_label: "Perimeter & Line Crossing"
description: "Configure tripwire line crossing detection and region entry/exit alerts on Viewtron IP cameras via HTTP API. Receive webhook notifications when objects cross a defined line or enter/exit a zone."
keywords:
  - perimeter security camera api
  - line crossing detection api
  - tripwire camera api
  - region entry exit camera api
  - directional crossing detection
  - ndaa compliant tripwire camera
sidebar_position: 6
---

# Perimeter Security & Line Crossing Detection API

Viewtron AI security cameras support tripwire line crossing detection and region entry/exit detection that runs entirely on the camera hardware — no cloud service or external AI software required. When a person, vehicle, or motorcycle crosses a defined line or enters/exits a defined region, the camera sends an HTTP POST webhook to your server with the detection event data, including a full-frame overview image, a cropped image of the detected target, bounding box coordinates, and the line or region boundary.

Line crossing detection uses a start point and end point to define a tripwire. You can configure direction filtering to detect only objects crossing in a specific direction (left-to-right, right-to-left, or both). Region entry and exit detection uses a polygon zone and triggers when an object enters or leaves that area. All Viewtron IP cameras and NVRs are NDAA compliant.

The key difference from [intrusion detection](/docs/applications/human-detection-intrusion-api) is that line crossing detects movement across a boundary line rather than presence within a polygon zone. Region entry/exit detects the transition into or out of a zone, rather than continuous presence.

## What You Can Build

- **Boundary crossing alerts** — detect when people or vehicles cross a property line, fence line, or restricted area boundary
- **Directional traffic monitoring** — filter by crossing direction to track one-way traffic flow at gates, driveways, or corridors
- **Doorway and entry counting** — combine with [people counting](/docs/applications/people-counting-traffic-analytics-api) for occupancy tracking
- **Loading dock monitoring** — alert when vehicles enter or exit loading zones
- **Parking lot entry/exit** — detect vehicles crossing gate lines for access logging
- **Zone transition tracking** — trigger different actions when objects enter vs leave a defined region

## How It Works

1. **Configure a tripwire line** on the camera — define a start point and end point, set the crossing direction filter (both, left/right, or top/bottom)
2. **Or configure a region entry/exit zone** — define a polygon region for AOI (Area of Interest) entry or exit detection
3. **Enable HTTP POST webhooks** — point the camera or NVR at your server's IP and port
4. **Your server receives XML** when a detection occurs — the POST includes alarm type, line coordinates, target bounding box, and base64 images
5. **Parse the event** using the [Viewtron Python SDK](/docs/getting-started/python-sdk) (`pip install viewtron`) or raw XML parsing
6. **Take action** — save images, log to CSV, send alerts, trigger relays

## Event Data Included

Each line crossing or region entry/exit webhook POST contains:

| Field | Description |
|-------|-------------|
| `smartType` | `PEA` (IPC line cross), `lineCrossing` (NVR), `AOIENTRY` (IPC entry), `AOILEAVE` (IPC exit) |
| `boundary` | `tripwire` (line crossing) or zone polygon (region entry/exit) |
| `directionLine` | Start and end point of the tripwire line (NVR format) |
| `startPoint` / `endPoint` | Line coordinates defining the tripwire (IPC format uses `lineInfo`) |
| `rect` | Bounding box of the detected target (x1, y1, x2, y2) |
| `eventId` / `targetId` | Unique IDs for the event and tracked target |
| `status` | `SMART_START`, `SMART_PROCEDURE`, or `SMART_STOP` |
| `sourceBase64Data` | Full-frame JPEG image (base64 encoded) |
| `targetBase64Data` | Cropped target JPEG image (base64 encoded) |
| `currentTime` | Detection timestamp |

## Tripwire Direction Options

The IPC tripwire configuration supports directional filtering:

| Direction | Description |
|-----------|-------------|
| `none` | Detect crossing in both directions |
| `rightortop` | Detect crossing from left-to-right or bottom-to-top only |
| `leftorbotton` | Detect crossing from right-to-left or top-to-bottom only |

:::note
The NVR v2.0 `lineCrossing` event does not include crossing direction in the webhook POST data. The direction line coordinates are included, but not which direction the object crossed.
:::

## Webhook XML Examples

### NVR Format (v2.0) — lineCrossing

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="2.0.0" xmlns="http://www.ipc.com/ver10">
    <messageType>alarmData</messageType>
    <deviceInfo>
        <deviceName><![CDATA[Driveway]]></deviceName>
        <ip><![CDATA[192.168.0.55]]></ip>
        <mac><![CDATA[58:5B:69:40:F4:0D]]></mac>
        <channelId>2</channelId>
    </deviceInfo>
    <smartType>lineCrossing</smartType>
    <currentTime>1772056914604000</currentTime>
    <eventInfo>
        <item>
            <eventId>1409</eventId>
            <targetId>1309</targetId>
            <boundary>tripwire</boundary>
            <directionLine>
                <startPoint><x>3579</x><y>2550</y></startPoint>
                <endPoint><x>3655</x><y>9797</y></endPoint>
            </directionLine>
            <rect><x1>3494</x1><y1>4409</y1><x2>4261</x2><y2>9791</y2></rect>
        </item>
    </eventInfo>
    <sourceDataInfo>
        <sourceBase64Length>400924</sourceBase64Length>
        <sourceBase64Data>... (base64 JPEG) ...</sourceBase64Data>
    </sourceDataInfo>
    <targetListInfo>
        <item>
            <targetId>1309</targetId>
            <targetType>person</targetType>
            <targetImageData>
                <targetBase64Length>78796</targetBase64Length>
                <targetBase64Data>... (base64 JPEG) ...</targetBase64Data>
            </targetImageData>
        </item>
    </targetListInfo>
</config>
```

### IPC Format (v1.x) — PEA (line cross)

IPC uses the same `PEA` smartType for both intrusion and line crossing. Line crossing events contain a `<tripwire>` block instead of `<perimeter>`:

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<config version="1.7" xmlns="http://www.ipc.com/ver10">
  <smartType type="openAlramObj">PEA</smartType>
  <deviceName type="string"><![CDATA[FrontGate]]></deviceName>
  <currentTime type="tint64">1774792701902505</currentTime>
  <tripwire>
    <tripInfo type="list" count="1">
      <item>
        <eventId type="uint32">3410</eventId>
        <targetId type="uint32">3210</targetId>
        <status type="perStatus">SMART_START</status>
        <startPoint>
          <x type="uint32">3579</x>
          <y type="uint32">2550</y>
        </startPoint>
        <endPoint>
          <x type="uint32">3655</x>
          <y type="uint32">9797</y>
        </endPoint>
        <rect>
          <x1 type="uint32">3494</x1><y1 type="uint32">4409</y1>
          <x2 type="uint32">4261</x2><y2 type="uint32">9791</y2>
        </rect>
      </item>
    </tripInfo>
  </tripwire>
  <!-- sourceDataInfo and listInfo with base64 images -->
</config>
```

## Quick Start Example

This standalone script listens for line crossing and region entry/exit events, prints details to the console, saves images, and logs to CSV:

```python
#!/usr/bin/env python3
"""Line Crossing & Region Entry/Exit Event Receiver — Viewtron IP Camera API"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime as dt
import xmltodict
import base64
import csv
import os

# pip install xmltodict
# pip install viewtron
from viewtron import (IntrusionDetection, IntrusionEntry, IntrusionExit, LineCrossing)

PORT = 5002
IMG_DIR = "images"
CSV_FILE = "line_crossing_events.csv"
os.makedirs(IMG_DIR, exist_ok=True)

# IPC smartTypes handled by this script
IPC_TYPES = {
    'PEA': 'line_crossing',
    'AOIENTRY': 'region_entry',
    'AOILEAVE': 'region_exit',
}

class LineCrossingHandler(BaseHTTPRequestHandler):
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

            # Route to the correct SDK class based on API version
            if version.startswith('2'):
                msg_type = str(config.get('messageType', ''))
                smart_type = str(config.get('smartType', ''))
                if msg_type != 'alarmData' or smart_type != 'lineCrossing':
                    return
                event = LineCrossing(body)
                event_label = "LINE CROSSING"
            else:
                st = config.get('smartType', {})
                alarm_type = (st.get('#text') or str(st)).strip() if isinstance(st, dict) else str(st).strip()
                if alarm_type == 'PEA':
                    # Check for tripwire block (line crossing) vs perimeter (intrusion)
                    if 'tripwire' not in body:
                        return  # This is an intrusion event, not line crossing
                    event = IntrusionDetection(body)
                    event_label = "LINE CROSSING"
                elif alarm_type == 'AOIENTRY':
                    event = IntrusionEntry(body)
                    event_label = "REGION ENTRY"
                elif alarm_type == 'AOILEAVE':
                    event = IntrusionExit(body)
                    event_label = "REGION EXIT"
                else:
                    return

            client_ip = self.client_address[0]

            # Print event details
            print(f"\n{'='*60}")
            print(f"[{dt.now():%Y-%m-%d %H:%M:%S}] {event_label} DETECTED")
            print(f"  Camera: {event.get_ip_cam()}")
            print(f"  Source: {client_ip}")
            print(f"  Type: {event.get_alarm_description()}")
            print(f"  Time: {event.get_time_stamp_formatted()}")

            # Save images
            ts = event.get_time_stamp()
            saved_files = []
            suffix_base = event_label.lower().replace(' ', '-')
            for get_img, exists, suffix in [
                (event.get_source_image, event.source_image_exists, "overview"),
                (event.get_target_image, event.target_image_exists, "target"),
            ]:
                if exists() and get_img():
                    path = os.path.join(IMG_DIR, f"{ts}-{suffix_base}-{suffix}.jpg")
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
                    event_label,
                    client_ip,
                    "|".join(saved_files),
                ])
            print(f"  Logged to {CSV_FILE}")

        except Exception as e:
            print(f"Error: {e}")

    def log_message(self, format, *args):
        pass  # Suppress default HTTP log output

if __name__ == '__main__':
    print(f"Line Crossing & Region Entry/Exit Receiver running on port {PORT}")
    print(f"Images will be saved to {IMG_DIR}/")
    print(f"Events will be logged to {CSV_FILE}")
    print(f"Waiting for events...\n")
    HTTPServer(('', PORT), LineCrossingHandler).serve_forever()
```

**To run:**

```bash
pip install xmltodict
# pip install viewtron
python3 line_crossing_receiver.py
```

Then configure your camera or NVR to send HTTP POST events to `http://<your-server-ip>:5002/`.

## Relevant API Endpoints

| Endpoint | Purpose | Reference |
|----------|---------|-----------|
| GetSmartTripwireConfig | Read tripwire line crossing configuration | [Line Crossing Config](/docs/api-reference/smart-detection/line-crossing-tripwire-config) |
| GetSmartAoiEntryConfig | Read region entry detection configuration | [Region Entry/Exit Config](/docs/api-reference/smart-detection/region-entry-exit-config) |
| GetSmartAoiLeaveConfig | Read region exit detection configuration | [Region Entry/Exit Config](/docs/api-reference/smart-detection/region-entry-exit-config) |
| SetHttpPostConfig | Configure webhook destination | [Webhook Config](/docs/api-reference/alarm/http-post-webhook-config) |
| GetAlarmStatus | Poll current alarm state (tripwireAlarm, aoiEntryAlarm, aoiLeaveAlarm) | [Alarm Status](/docs/api-reference/alarm/alarm-status) |

## Related Applications

- [Human Detection & Intrusion](/docs/applications/human-detection-intrusion-api) — polygon zone intrusion detection (vs line crossing)
- [People Counting & Traffic Analytics](/docs/applications/people-counting-traffic-analytics-api) — count objects crossing a line with running totals
- [Relay Control & IoT Automation](/docs/applications/relay-control-iot-automation-api) — trigger relays based on line crossing events
- [Webhook Event Notification](/docs/applications/webhook-event-notification-api) — complete webhook setup and format reference

## Related Products

- [Viewtron AI Security Cameras](https://www.cctvcamerapros.com/AI-security-cameras-s/1512.htm) — IP cameras with built-in line crossing and region entry/exit detection
- [Viewtron IP Camera NVRs](https://www.cctvcamerapros.com/IP-Camera-NVRs-s/1472.htm) — NVRs with HTTP POST event forwarding

## Questions & Development Inquiries

- **Email:** mike@viewtron.com
- **Phone:** 561-433-8488
- **Forum:** [NVR Webhook Setup Guide](https://videos.cctvcamerapros.com/support/topic/setup-nvr-api-webhooks)

Mike Haldas is available for questions, consultation, and custom software development for Viewtron API related projects. Email details about your project to mike@viewtron.com.
