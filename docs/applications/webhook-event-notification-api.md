---
title: "Webhook Event Notification API"
sidebar_label: "Webhook Events"
description: "Set up HTTP POST webhooks on Viewtron IP cameras and NVRs to receive real-time AI detection events with images, bounding boxes, and target classification."
keywords:
  - security camera webhook
  - camera event notification api
  - ip camera http post events
  - camera that sends data to my server
  - security camera event notification api
sidebar_position: 13
---

# Webhook Event Notification API

Viewtron IP cameras and NVRs can push real-time AI detection events to your HTTP server as webhooks. When a camera detects a person, vehicle, face, or license plate, it sends an HTTP POST to your server with XML data containing the event details, bounding box coordinates, and optionally base64-encoded JPEG images of the scene and detected target.

No polling required — your server receives events the moment they happen. No cloud service, no monthly fees, no third-party dependencies. The camera posts directly to your server on your local network or over the internet.

## What You Can Build

- Real-time alert systems — push notifications when AI detections occur
- Event logging and analytics — record all detections with timestamps, images, and metadata
- Custom automation — trigger actions (lights, relays, gates, alarms) based on detection events
- Integration with VMS, SIEM, or building management systems
- Multi-camera event aggregation and dashboards

## Two Sources of Webhook Data

| Source | Format | Supports traject | Setup |
|--------|--------|-----------------|-------|
| **IP Camera (direct)** | IPC v1.x XML | Yes | Configure on camera via API or web interface |
| **NVR (forwarded)** | NVR v2.0 XML | No | Configure on NVR web interface |

**Recommended setup:** Configure the NVR to forward alarm events (images included), and configure individual cameras to send `traject` real-time tracking data directly. Your server receives both streams simultaneously.

## How It Works

1. **Configure the webhook destination** on the camera or NVR — your server's IP, port, and URL path
2. **Enable detection types** you want to receive (perimeter, face, LPR, etc.)
3. **Start your HTTP server** listening for POST requests
4. **Parse the XML** when events arrive — extract alarm type, target info, and images
5. **Respond with success XML** to keep the connection alive

## Supported Detection Types

| IPC smartType | NVR smartType | Detection |
|---|---|---|
| `PEA` (intrusion) | `regionIntrusion` | [Human Detection / Intrusion](/docs/applications/human-detection-intrusion-api) |
| `PEA` (line cross) | `lineCrossing` | [Perimeter / Line Crossing](/docs/applications/perimeter-security-line-crossing-api) |
| `VEHICE` | `vehicle` | [License Plate Recognition](/docs/applications/license-plate-recognition-camera-api) |
| `VFD` | `videoFaceDetect` | [Face Detection](/docs/applications/face-detection-recognition-api) |
| `PASSLINECOUNT` | `targetCountingByLine` | [People Counting](/docs/applications/people-counting-traffic-analytics-api) |
| `TRAFFIC` | `targetCountingByArea` | [People Counting](/docs/applications/people-counting-traffic-analytics-api) |
| `VSD` | `videoMetadata` | Video Metadata (full-frame detection) |
| `VFD_MATCH` | Not supported | Face Recognition Match (IPC only) |

## Webhook Message Types

Every webhook POST is one of three message types:

| Type | Purpose | Size | Frequency |
|------|---------|------|-----------|
| **keepalive** | Heartbeat — confirms connection is active | ~300 bytes | Every 30-120 seconds |
| **alarmStatus** | Alarm state change (on/off) | ~660 bytes | One per state change |
| **alarmData** | Full detection event with coordinates and images | 2 KB - 530 KB | One per detection |

## Configuring Webhooks via API

Use [SetHttpPostConfig](/docs/api-reference/alarm/http-post-webhook-config) to configure the webhook destination on IP cameras. The httpPostV2 system supports up to 3 URLs with independent event filtering:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="1.0" xmlns="http://www.ipc.com/ver10">
<httpPostV2><postUrlConf>
  <urlList type="list" count="1"><item>
    <urlId>1</urlId>
    <switch>true</switch>
    <url>
      <protocol>http</protocol>
      <domain><![CDATA[192.168.0.53]]></domain>
      <port>5002</port>
      <path><![CDATA[/API]]></path>
      <authentication>none</authentication>
    </url>
    <heatBeatSwitch>true</heatBeatSwitch>
    <keepaliveTimeval>90</keepaliveTimeval>
    <subscribeDateType type="list" count="5">
      <item>alarmStatus</item>
      <item>traject</item>
      <item>smartData</item>
      <item>sourceImage</item>
      <item>targetImage</item>
    </subscribeDateType>
    <subscriptionEvents type="list" count="1">
      <item>PERIMETER</item>
    </subscriptionEvents>
  </item></urlList>
</postUrlConf></httpPostV2>
</config>
```

## Data Type Subscriptions (httpPostV2)

Control what data each webhook URL receives:

| Data Type | Description | Post Size |
|-----------|-------------|-----------|
| `alarmStatus` | Alarm on/off state changes | ~660 bytes |
| `traject` | Continuous real-time target tracking | ~1.7 KB at ~7/sec |
| `smartData` | Detection event with coordinates | ~2-3 KB |
| `sourceImage` | Full-frame JPEG (base64 in XML) | ~500 KB |
| `targetImage` | Cropped target JPEG (base64 in XML) | Included with smartData |

:::tip
Subscribe to `smartData` + `sourceImage` + `targetImage` to receive complete detection events with both overview and cropped target images in a single POST.
:::

## Server Response

Your server must respond with this XML to keep the connection alive:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="1.0" xmlns="http://www.ipc.com/ver10">
  <status>success</status>
</config>
```

## Quick Start Example

This standalone script receives webhook events from any Viewtron camera or NVR, prints event details, saves images, and logs to CSV:

```python
#!/usr/bin/env python3
"""Viewtron Webhook Event Receiver — receives all detection types."""

from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime as dt
import xmltodict
import base64
import csv
import os

# pip install xmltodict
# Download viewtron.py from https://github.com/mikehaldas/IP-Camera-API
from viewtron import *

PORT = 5002
IMG_DIR = "images"
CSV_FILE = "events.csv"
os.makedirs(IMG_DIR, exist_ok=True)

# Route alarm types to the correct viewtron.py class
IPC_CLASSES = {
    'PEA': IntrusionDetection, 'VFD': FaceDetection,
    'VEHICE': LPR, 'VEHICLE': LPR, 'VSD': VideoMetadata,
    'AOIENTRY': IntrusionEntry, 'AOILEAVE': IntrusionExit,
}
NVR_CLASSES = {
    'regionIntrusion': RegionIntrusion, 'lineCrossing': LineCrossing,
    'vehicle': VehicleLPR, 'videoFaceDetect': FaceDetectionV2,
    'videoMetadata': VideoMetadataV2,
    'targetCountingByLine': TargetCountingByLine,
    'targetCountingByArea': TargetCountingByArea,
}

class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Respond immediately to keep the connection alive
        response = '<?xml version="1.0" encoding="UTF-8"?>\n'
        response += '<config version="1.0" xmlns="http://www.ipc.com/ver10">\n'
        response += '  <status>success</status>\n</config>'
        self.send_response(200)
        self.send_header('Content-Type', 'application/xml')
        self.send_header('Content-Length', str(len(response)))
        self.end_headers()
        self.wfile.write(response.encode())

        # Read and parse the POST body
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

            # Detect v2.0 (NVR) vs v1.x (IPC)
            if version.startswith('2'):
                msg_type = str(config.get('messageType', ''))
                if msg_type != 'alarmData':
                    return
                smart_type = str(config.get('smartType', ''))
                if smart_type not in NVR_CLASSES:
                    return
                event = NVR_CLASSES[smart_type](body)
            else:
                st = config.get('smartType', {})
                alarm_type = (st.get('#text') or st.get('value') or
                              str(st)).strip() if isinstance(st, dict) else str(st).strip()
                if alarm_type not in IPC_CLASSES:
                    return
                event = IPC_CLASSES[alarm_type](body)

            # Print event info
            client_ip = self.client_address[0]
            print(f"\n[{dt.now():%H:%M:%S}] {event.get_alarm_description()} from {client_ip}")
            print(f"  Camera: {event.get_ip_cam()}")
            print(f"  Type: {event.get_alarm_type()}")

            # Save images if present
            ts = event.get_time_stamp()
            for get_img, exists, suffix in [
                (event.get_source_image, event.source_image_exists, "overview"),
                (event.get_target_image, event.target_image_exists, "target"),
            ]:
                if exists() and get_img():
                    path = os.path.join(IMG_DIR, f"{ts}-{suffix}.jpg")
                    with open(path, "wb") as f:
                        f.write(base64.b64decode(get_img()))
                    print(f"  Saved: {path}")

            # Log to CSV
            with open(CSV_FILE, 'a', newline='') as f:
                csv.writer(f).writerow([
                    event.get_time_stamp_formatted(), event.get_ip_cam(),
                    event.get_alarm_type(), event.get_alarm_description(),
                    event.get_plate_number(), client_ip,
                ])

        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    print(f"Listening for webhooks on port {PORT}...")
    HTTPServer(('', PORT), WebhookHandler).serve_forever()
```

## Relevant API Endpoints

| Endpoint | Purpose | Reference |
|----------|---------|-----------|
| SetHttpPostConfig | Configure webhook destination and subscriptions | [Webhook Config](/docs/api-reference/alarm/http-post-webhook-config) |
| GetHttpPostConfig | Read current webhook configuration | [Webhook Config](/docs/api-reference/alarm/http-post-webhook-config) |
| GetAlarmStatus | Poll current alarm state | [Alarm Status](/docs/api-reference/alarm/alarm-status) |

## Related Resources

- **Python API Server** — [github.com/mikehaldas/IP-Camera-API](https://github.com/mikehaldas/IP-Camera-API) — full-featured server handling all detection types
- **Webhook format details** — [IPC Event Format](/docs/api-reference/events/ipc-event-format) and [NVR Event Format](/docs/api-reference/events/nvr-event-format)
- **Detection types reference** — [All Detection Types](/docs/api-reference/events/detection-types-reference)

## Related Products

- [Viewtron AI Security Cameras](https://www.cctvcamerapros.com/AI-security-cameras-s/1512.htm) — IP cameras with built-in AI detection
- [Viewtron IP Camera NVRs](https://www.cctvcamerapros.com/IP-Camera-NVRs-s/1472.htm) — NVRs with HTTP POST event forwarding

## Questions & Development Inquiries

- **Email:** mike@viewtron.com
- **Phone:** 561-433-8488
- **Forum:** [NVR Webhook Setup Guide](https://videos.cctvcamerapros.com/support/topic/setup-nvr-api-webhooks)

Mike Haldas is available for questions, consultation, and custom software development for Viewtron API related projects. Email details about your project to mike@viewtron.com.
