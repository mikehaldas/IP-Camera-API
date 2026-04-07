---
title: "People Counting & Traffic Analytics API"
sidebar_label: "People Counting"
description: "Count people crossing lines or entering areas using the Viewtron IP camera API. Track entrance/exit statistics, monitor occupancy, and build retail analytics with real-time webhook data."
keywords:
  - people counting camera api
  - traffic counting camera api
  - occupancy counting api
  - footfall counter camera
  - entrance exit counter camera
  - retail foot traffic camera api
sidebar_position: 5
---

# People Counting & Traffic Analytics API

Viewtron AI cameras include built-in people counting that runs entirely on the camera hardware — no cloud service or external software required. When a person, vehicle, or motorcycle crosses a virtual counting line or enters a defined counting area, the camera sends an HTTP POST webhook to your server with the event data, including a full-frame overview image, a cropped image of the counted target, and the boundary or line coordinates that were crossed.

There are two counting methods available, each suited to different use cases. **Line counting** tracks objects crossing a virtual line and classifies each crossing as an entrance or exit. **Area counting** tracks objects entering a defined polygon region. Both methods include images with every event, and line counting also supports a polling endpoint to query cumulative entrance/exit statistics without webhooks.

## What You Can Build

- **Retail foot traffic analytics** — count customers entering and exiting a store entrance, track hourly and daily patterns
- **Building occupancy monitoring** — maintain a real-time occupancy count by tracking entrances minus exits
- **Parking lot capacity** — count vehicles entering and exiting a lot, display available spaces
- **Queue monitoring** — count people entering a service area and detect when queue length exceeds a threshold
- **Bi-directional traffic analysis** — use the line counting direction to separate inbound vs outbound foot traffic
- **Multi-zone analytics** — deploy area counting across different store sections to identify high-traffic areas

## How It Works

1. **Configure a counting line or area** on the camera — draw a virtual line with a direction arrow, or define a polygon region
2. **Enable HTTP POST webhooks** — point the camera or NVR at your server's IP and port
3. **Your server receives XML** when a count event occurs — the POST includes the counting method, target coordinates, boundary geometry, and base64 images
4. **Parse the event** using the [viewtron.py](https://github.com/mikehaldas/IP-Camera-API) library or raw XML parsing
5. **Track counts and take action** — maintain running entrance/exit totals, save images, log to CSV, trigger alerts at thresholds

## Counting Methods

### Line Counting (targetCountingByLine / PASSLINECOUNT)

Objects are counted when they cross a virtual line drawn on the camera view. The line has a direction arrow — crossings in the direction of the arrow are counted as **entrances**, and crossings against it are counted as **exits**. This is the most common method for doorways, hallways, and gates.

| Field | Description |
|-------|-------------|
| `smartType` | `PASSLINECOUNT` (IPC) or `targetCountingByLine` (NVR) |
| `targetType` | `person`, `car`, or `motor` |
| `boundary` | `tripwire` — indicates a line crossing event |
| `directionLine` | Start and end point coordinates of the counting line |
| `rect` | Bounding box of the target (may be all zeros for line counting) |
| `eventId` / `targetId` | Unique IDs for the event and tracked target |
| `sourceBase64Data` | Full-frame JPEG image (base64 encoded) |
| `targetBase64Data` | Cropped target JPEG image (base64 encoded) |
| `currentTime` | Detection timestamp |

### Area Counting (targetCountingByArea / TRAFFIC)

Objects are counted when they enter a defined polygon region. This is useful for open areas, intersections, or zones where a single line crossing is not practical.

| Field | Description |
|-------|-------------|
| `smartType` | `TRAFFIC` (IPC) or `targetCountingByArea` (NVR) |
| `targetType` | `person`, `car`, or `motor` |
| `boundary` | `area` — indicates an area entry event |
| `pointGroup` | Polygon coordinates defining the counting area |
| `rect` | Bounding box of the detected target (x1, y1, x2, y2) |
| `eventId` / `targetId` | Unique IDs for the event and tracked target |
| `sourceBase64Data` | Full-frame JPEG image (base64 encoded) |
| `targetBase64Data` | Cropped target JPEG image (base64 encoded) |
| `currentTime` | Detection timestamp |

## Webhook XML Examples

### NVR Format (v2.0) — targetCountingByLine

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="2.0.0" xmlns="http://www.ipc.com/ver10">
    <messageType>alarmData</messageType>
    <deviceInfo>
        <deviceName><![CDATA[Device Name]]></deviceName>
        <ip><![CDATA[192.168.0.60]]></ip>
        <mac><![CDATA[58:5B:69:40:F4:0D]]></mac>
        <channelId>1</channelId>
    </deviceInfo>
    <smartType>targetCountingByLine</smartType>
    <currentTime>1772140991308000</currentTime>
    <eventInfo>
        <item>
            <eventId>1080</eventId>
            <targetId>480</targetId>
            <boundary>tripwire</boundary>
            <directionLine>
                <startPoint><x>3977</x><y>2146</y></startPoint>
                <endPoint><x>3977</x><y>9974</y></endPoint>
            </directionLine>
            <rect><x1>0</x1><y1>0</y1><x2>0</x2><y2>0</y2></rect>
        </item>
    </eventInfo>
    <sourceDataInfo>
        <dataType>0</dataType>
        <width>1280</width>
        <height>720</height>
        <sourceBase64Length>441256</sourceBase64Length>
        <sourceBase64Data>... (base64 JPEG) ...</sourceBase64Data>
    </sourceDataInfo>
    <targetListInfo>
        <item>
            <targetId>480</targetId>
            <targetType>person</targetType>
            <targetImageData>
                <dataType>0</dataType>
                <width>336</width>
                <height>448</height>
                <targetBase64Length>72896</targetBase64Length>
                <targetBase64Data>... (base64 JPEG) ...</targetBase64Data>
            </targetImageData>
        </item>
    </targetListInfo>
</config>
```

:::note
The `rect` in `eventInfo` is all zeros for line counting. The target crop in `targetListInfo` still captures the person.
:::

### NVR Format (v2.0) — targetCountingByArea

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="2.0.0" xmlns="http://www.ipc.com/ver10">
    <messageType>alarmData</messageType>
    <deviceInfo>
        <deviceName><![CDATA[Device Name]]></deviceName>
        <ip><![CDATA[192.168.0.60]]></ip>
        <mac><![CDATA[58:5B:69:40:F4:0D]]></mac>
        <channelId>1</channelId>
    </deviceInfo>
    <smartType>targetCountingByArea</smartType>
    <currentTime>1772145352968000</currentTime>
    <eventInfo>
        <item>
            <eventId>2904</eventId>
            <targetId>2204</targetId>
            <boundary>area</boundary>
            <pointGroup>
                <item><x>4450</x><y>4292</y></item>
                <item><x>4469</x><y>9015</y></item>
                <item><x>1079</x><y>8510</y></item>
                <item><x>1344</x><y>4166</y></item>
            </pointGroup>
            <rect><x1>4431</x1><y1>4409</y1><x2>4971</x2><y2>9791</y2></rect>
        </item>
    </eventInfo>
    <sourceDataInfo>
        <dataType>0</dataType>
        <width>1280</width>
        <height>720</height>
        <sourceBase64Length>414832</sourceBase64Length>
        <sourceBase64Data>... (base64 JPEG) ...</sourceBase64Data>
    </sourceDataInfo>
    <targetListInfo>
        <item>
            <targetId>2204</targetId>
            <targetType>person</targetType>
            <targetImageData>
                <dataType>0</dataType>
                <width>336</width>
                <height>448</height>
                <targetBase64Length>72136</targetBase64Length>
                <targetBase64Data>... (base64 JPEG) ...</targetBase64Data>
            </targetImageData>
        </item>
    </targetListInfo>
</config>
```

## Polling Statistics (v2.0 IPC Only)

For line counting, you can query the camera's cumulative entrance/exit counts directly without webhooks using the `GetPassLineCountStatistics` endpoint. This is useful for periodic polling or dashboard displays.

**Request:**

```
GET http://<camera-ip>/GetPassLineCountStatistics
```

**Response:**

```xml
<?xml version="1.0" encoding="utf-8"?>
<config xmlns="http://www.ipc.com/ver10" version="2.0.0">
  <entranceCount>
    <person type="uint32">0</person>
    <car type="uint32">0</car>
    <bike type="uint32">0</bike>
  </entranceCount>
  <exitCount>
    <person type="uint32">0</person>
    <car type="uint32">0</car>
    <bike type="uint32">0</bike>
  </exitCount>
</config>
```

This returns separate entrance and exit counts for each object type (person, car, bike). The counts are cumulative since the camera was last reset.

:::tip
Use `GetPassLineCountStatistics` for simple dashboard displays where you only need current totals. Use webhook events when you need per-event images, timestamps, and real-time processing.
:::

## Quick Start Example

This standalone script listens for both line counting and area counting events, maintains running entrance/exit totals, saves images, and logs to CSV:

```python
#!/usr/bin/env python3
"""People Counting Event Receiver — Viewtron IP Camera API"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime as dt
import xmltodict
import base64
import csv
import os

# pip install xmltodict
# Download viewtron.py from https://github.com/mikehaldas/IP-Camera-API
from viewtron import (TargetCountingByLine, TargetCountingByArea)

PORT = 5002
IMG_DIR = "images"
CSV_FILE = "counting_events.csv"
os.makedirs(IMG_DIR, exist_ok=True)

# Running counts
entrance_count = 0
exit_count = 0
area_count = 0

class CountingHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        global entrance_count, exit_count, area_count

        # Respond with success XML
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
            smart_type = str(config.get('smartType', '')).strip()

            if smart_type == 'targetCountingByLine':
                event = TargetCountingByLine(body)
                # Line counting — increment entrance count
                # (direction logic depends on your line configuration)
                entrance_count += 1
                count_type = "LINE"
                print(f"\n{'='*60}")
                print(f"[{dt.now():%Y-%m-%d %H:%M:%S}] LINE COUNT EVENT")
                print(f"  Camera: {event.get_ip_cam()}")
                print(f"  Type: {event.get_alarm_description()}")
                print(f"  Running Total — Entrances: {entrance_count}  Exits: {exit_count}")

            elif smart_type == 'targetCountingByArea':
                event = TargetCountingByArea(body)
                area_count += 1
                count_type = "AREA"
                print(f"\n{'='*60}")
                print(f"[{dt.now():%Y-%m-%d %H:%M:%S}] AREA COUNT EVENT")
                print(f"  Camera: {event.get_ip_cam()}")
                print(f"  Type: {event.get_alarm_description()}")
                print(f"  Running Total — Area Entries: {area_count}")

            else:
                return  # Not a counting event

            client_ip = self.client_address[0]
            print(f"  Source: {client_ip}")
            print(f"  Time: {event.get_time_stamp_formatted()}")

            # Save images
            ts = event.get_time_stamp()
            saved_files = []
            for get_img, exists, suffix in [
                (event.get_source_image, event.source_image_exists, "overview"),
                (event.get_target_image, event.target_image_exists, "target"),
            ]:
                if exists() and get_img():
                    path = os.path.join(IMG_DIR, f"{ts}-{count_type.lower()}-{suffix}.jpg")
                    with open(path, "wb") as f:
                        f.write(base64.b64decode(get_img()))
                    saved_files.append(path)
                    print(f"  Image: {path}")

            # Log to CSV with entrance/exit counts
            with open(CSV_FILE, 'a', newline='') as f:
                csv.writer(f).writerow([
                    event.get_time_stamp_formatted(),
                    event.get_ip_cam(),
                    count_type,
                    event.get_alarm_type(),
                    entrance_count,
                    exit_count,
                    area_count,
                    client_ip,
                    "|".join(saved_files),
                ])
            print(f"  Logged to {CSV_FILE}")

        except Exception as e:
            print(f"Error: {e}")

    def log_message(self, format, *args):
        pass  # Suppress default HTTP log output

if __name__ == '__main__':
    print(f"People Counting Receiver running on port {PORT}")
    print(f"Images will be saved to {IMG_DIR}/")
    print(f"Events will be logged to {CSV_FILE}")
    print(f"Waiting for counting events...\n")
    HTTPServer(('', PORT), CountingHandler).serve_forever()
```

**To run:**

```bash
pip install xmltodict
# Place viewtron.py in the same directory
python3 counting_receiver.py
```

Then configure your camera or NVR to send HTTP POST events to `http://<your-server-ip>:5002/`.

## Relevant API Endpoints

| Endpoint | Purpose | Reference |
|----------|---------|-----------|
| GetSmartPassLineCountConfig | Read line counting zone configuration | [Pass Line Count Config](/docs/api-reference/smart-detection/line-counting-config) |
| GetPassLineCountStatistics | Query current entrance/exit counts (v2.0 IPC) | [Pass Line Count Config](/docs/api-reference/smart-detection/line-counting-config) |
| SetHttpPostConfig | Configure webhook destination | [Webhook Config](/docs/api-reference/alarm/http-post-webhook-config) |
| GetAlarmStatus | Poll current alarm state | [Alarm Status](/docs/api-reference/alarm/alarm-status) |

## Related Applications

- [Home Assistant Integration](/docs/integrations/home-assistant) — people/vehicle counting as native HA sensors for occupancy tracking
- [Human Detection & Intrusion Detection](/docs/applications/human-detection-intrusion-api) — detect people entering defined zones with images
- [Perimeter Security & Line Crossing](/docs/applications/perimeter-security-line-crossing-api) — tripwire detection and region entry/exit
- [Real-Time Object Tracking](/docs/applications/real-time-object-tracking-api) — continuous target position data via traject
- [Webhook Event Notification](/docs/applications/webhook-event-notification-api) — complete webhook setup and format reference
- [Viewtron Python SDK](/docs/getting-started/python-sdk) — parse counting events in Python

## Related Products

- [Viewtron AI Security Cameras](https://www.cctvcamerapros.com/AI-security-cameras-s/1512.htm) — IP cameras with built-in people counting
- [Viewtron IP Camera NVRs](https://www.cctvcamerapros.com/IP-Camera-NVRs-s/1472.htm) — NVRs with HTTP POST event forwarding

## Questions & Development Inquiries

- **Email:** mike@viewtron.com
- **Phone:** 561-433-8488
- **Forum:** [NVR Webhook Setup Guide](https://videos.cctvcamerapros.com/support/topic/setup-nvr-api-webhooks)

Mike Haldas is available for questions, consultation, and custom software development for Viewtron API related projects. Email details about your project to mike@viewtron.com.
