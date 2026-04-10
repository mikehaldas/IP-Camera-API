---
title: "Face Detection & Recognition Camera API"
sidebar_label: "Face Detection"
description: "Use the Viewtron IP camera HTTP API to detect faces, extract face attributes (age, sex, glasses, mask), receive face crop images via webhook, and match faces against a stored library for recognition alerts."
keywords:
  - face detection camera api
  - face recognition camera api
  - facial recognition ip camera
  - face detection webhook
sidebar_position: 3
---

# Face Detection & Recognition Camera API

Viewtron AI security cameras include built-in face detection that runs entirely on the camera hardware — no cloud service or external AI software required. When a face is detected in the camera's field of view, the camera sends an HTTP POST webhook to your server with a cropped face image, the full scene image, and face attributes including estimated age, sex, glasses, and mask status.

The camera also supports face recognition (matching) through an on-camera face sample library. When a detected face matches a stored sample, the camera sends a `VFD_MATCH` event with the match result. Face recognition matching is available on IPC cameras directly — the NVR forwards face detection events (`videoFaceDetect`) but does not forward match data. 8-channel NVRs support both face detection and face database/recognition, while 4-channel NVRs support face detection only.

## What You Can Build

- **VIP arrival alerts** — detect known faces from a stored library and notify staff when important guests or employees arrive
- **Access control integration** — grant or deny entry based on face recognition match results
- **Demographic analytics** — aggregate age and sex attributes across face detections to understand visitor demographics
- **Mask compliance monitoring** — detect whether people are wearing masks in healthcare or clean room environments
- **Face crop archives** — save every detected face crop image with timestamp for after-the-fact review
- **Multi-camera face tracking** — correlate face detections across camera locations by storing and comparing face crops
- **Attendance systems** — log employee arrivals and departures using face recognition matching

## How It Works

1. **Configure face detection** on the camera — enable VFD (Video Face Detection) and set sensitivity and detection zones
2. **Enable HTTP POST webhooks** — point the camera or NVR at your server's IP and port
3. **Upload face samples** (optional) — add face images to the on-camera library for face recognition matching
4. **Your server receives XML** when a face is detected — the POST includes a full scene image, cropped face image, and face attributes
5. **Parse the event** using the [Viewtron Python SDK](/docs/getting-started/python-sdk) (`pip install viewtron`) or raw XML parsing
6. **Take action** — save face crops, log attributes to a database, send alerts on recognition matches

## Event Data Included

Each face detection webhook POST contains:

| Field | Description |
|-------|-------------|
| `smartType` | `VFD` (IPC) or `videoFaceDetect` (NVR) |
| `targetId` | Detection tracking ID |
| `rect` | Face bounding box coordinates (x1, y1, x2, y2) |
| `age` | Age classification: `child`, `young`, `middleAged`, `old` (NVR v2.0) |
| `sex` | Gender classification: `male`, `female` (NVR v2.0) |
| `glasses` | Glasses detection: `yes`, `no`, `unknown` (NVR v2.0) |
| `mask` | Mask detection: `yes`, `no`, `unknown` (NVR v2.0) |
| `sourceBase64Data` | Full scene JPEG image (base64 encoded, ~400-500 KB) |
| `targetBase64Data` | Square face crop JPEG image (base64 encoded, ~10-20 KB, typically 184x184) |
| `currentTime` | Detection timestamp |

### Face Recognition (VFD_MATCH) — IPC Only

When a detected face matches a sample in the on-camera library, the IPC sends a `VFD_MATCH` event with the match result. This event type is IPC only — the NVR does not forward match data.

## Face Attribute Values

| Attribute | Possible Values |
|-----------|----------------|
| `age` | `child`, `young`, `middleAged`, `old` |
| `sex` | `male`, `female` |
| `glasses` | `yes`, `no`, `unknown` |
| `mask` | `yes`, `no`, `unknown` |

## Webhook XML Examples

### NVR Format (v2.0) — videoFaceDetect

The NVR v2.0 format uses `faceListInfo` instead of `eventInfo` + `targetListInfo`, with face attributes (age, sex, glasses, mask) directly in each item.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="2.0.0" xmlns="http://www.ipc.com/ver10">
    <messageType>alarmData</messageType>
    <deviceInfo>
        <deviceName><![CDATA[Front Entrance]]></deviceName>
        <ip><![CDATA[192.168.0.60]]></ip>
        <mac><![CDATA[58:5B:69:40:F4:0D]]></mac>
        <channelId>1</channelId>
    </deviceInfo>
    <smartType>videoFaceDetect</smartType>
    <currentTime>1772212642929000</currentTime>
    <sourceDataInfo>
        <dataType>0</dataType>
        <width>1280</width>
        <height>720</height>
        <sourceBase64Length>440072</sourceBase64Length>
        <sourceBase64Data>... (base64 JPEG overview) ...</sourceBase64Data>
    </sourceDataInfo>
    <faceListInfo>
        <item>
            <targetId>50</targetId>
            <rect>
                <x1>854</x1><y1>176</y1>
                <x2>978</x2><y2>300</y2>
            </rect>
            <age>middleAged</age>
            <sex>male</sex>
            <glasses>unknown</glasses>
            <mask>unknown</mask>
            <targetImageData>
                <dataType>0</dataType>
                <width>184</width>
                <height>184</height>
                <targetBase64Length>14860</targetBase64Length>
                <targetBase64Data>... (base64 JPEG face crop) ...</targetBase64Data>
            </targetImageData>
        </item>
    </faceListInfo>
</config>
```

### IPC Format (v1.x) — VFD

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<config version="1.7" xmlns="http://www.ipc.com/ver10">
  <smartType type="openAlramObj">VFD</smartType>
  <deviceName type="string"><![CDATA[FaceCam]]></deviceName>
  <currentTime type="tint64">1774792701902505</currentTime>
  <sourceDataInfo>
    <sourceBase64Length type="uint32">440072</sourceBase64Length>
    <sourceBase64Data type="jpegBase64">... (base64 JPEG scene) ...</sourceBase64Data>
  </sourceDataInfo>
  <listInfo type="list" count="1">
    <item>
      <targetImageData>
        <targetBase64Length type="uint32">14860</targetBase64Length>
        <targetBase64Data type="jpegBase64">... (base64 JPEG face crop) ...</targetBase64Data>
      </targetImageData>
    </item>
  </listInfo>
</config>
```

:::note
Face attributes (age, sex, glasses, mask) are only available in the NVR v2.0 format. The IPC v1.x format includes the face crop image but not the attribute analysis. `VFD_MATCH` (face recognition) is IPC only — the NVR does not forward match data.
:::

## Quick Start Example

This standalone script listens for face detection events from both IPC (v1.x) and NVR (v2.0) formats. It prints face attributes, saves the scene image and face crop, and logs everything to CSV:

```python
#!/usr/bin/env python3
"""Face Detection Event Receiver — Viewtron IP Camera API"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime as dt
import xmltodict
import base64
import csv
import os

# pip install xmltodict
# pip install viewtron
from viewtron import (FaceDetection, FaceDetectionV2)

PORT = 5002
IMG_DIR = "images"
CSV_FILE = "face_events.csv"
os.makedirs(IMG_DIR, exist_ok=True)

class FaceHandler(BaseHTTPRequestHandler):
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

            age = sex = glasses = mask = ''

            # Route to the correct SDK class based on API version
            if version.startswith('2'):
                msg_type = str(config.get('messageType', ''))
                smart_type = str(config.get('smartType', ''))
                if msg_type != 'alarmData' or smart_type != 'videoFaceDetect':
                    return
                event = FaceDetectionV2(body)
                age = event.get_face_age()
                sex = event.get_face_sex()
                glasses = event.get_face_glasses()
                mask = event.get_face_mask()
            else:
                st = config.get('smartType', {})
                alarm_type = (st.get('#text') or str(st)).strip() if isinstance(st, dict) else str(st).strip()
                if alarm_type != 'VFD':
                    return
                event = FaceDetection(body)

            client_ip = self.client_address[0]

            # Print event details
            print(f"\n{'='*60}")
            print(f"[{dt.now():%Y-%m-%d %H:%M:%S}] FACE DETECTED")
            print(f"  Camera: {event.get_ip_cam()}")
            print(f"  Source: {client_ip}")
            if age:
                print(f"  Age: {age}")
                print(f"  Sex: {sex}")
                print(f"  Glasses: {glasses}")
                print(f"  Mask: {mask}")

            # Save images
            ts = event.get_time_stamp()
            saved_files = []

            # Scene image (source)
            if event.has_source_image and event.source_image:
                path = os.path.join(IMG_DIR, f"{ts}-face-scene.jpg")
                with open(path, "wb") as f:
                    f.write(base64.b64decode(event.source_image))
                saved_files.append(path)
                print(f"  Scene: {path}")

            # Face crop image (target)
            if event.has_target_image and event.target_image:
                path = os.path.join(IMG_DIR, f"{ts}-face-crop.jpg")
                with open(path, "wb") as f:
                    f.write(base64.b64decode(event.target_image))
                saved_files.append(path)
                print(f"  Face crop: {path}")

            # Log to CSV
            with open(CSV_FILE, 'a', newline='') as f:
                csv.writer(f).writerow([
                    event.get_time_stamp_formatted(),
                    event.get_ip_cam(),
                    age,
                    sex,
                    glasses,
                    mask,
                    client_ip,
                    "|".join(saved_files),
                ])
            print(f"  Logged to {CSV_FILE}")

        except Exception as e:
            print(f"Error: {e}")

    def log_message(self, format, *args):
        pass  # Suppress default HTTP log output

if __name__ == '__main__':
    print(f"Face Detection Receiver running on port {PORT}")
    print(f"Images will be saved to {IMG_DIR}/")
    print(f"Events will be logged to {CSV_FILE}")
    print(f"Waiting for face detection events...\n")
    HTTPServer(('', PORT), FaceHandler).serve_forever()
```

**To run:**

```bash
pip install xmltodict
# pip install viewtron
python3 face_receiver.py
```

Then configure your camera or NVR to send HTTP POST events to `http://<your-server-ip>:5002/`.

## Face Sample Library

For face recognition (matching), upload face samples to the camera's on-device library. The camera compares detected faces against stored samples and sends `VFD_MATCH` events when a match is found.

**Face library error codes:**

| Code | Description |
|------|-------------|
| 150 | Face library full |
| 151 | Face sample already exists |
| 152 | Face sample not found |
| 153 | Invalid face image format |
| 154 | Face not detected in sample image |
| 155 | Multiple faces in sample image |
| 156 | Face image too small |
| 157 | Face image too blurry |
| 158 | Face library database error |
| 159 | Face library operation timeout |

:::note
Face recognition (VFD_MATCH) requires an 8-channel NVR or direct IPC connection. 4-channel NVRs support face detection but not face database/recognition. Even with a face database configured on the NVR, only `videoFaceDetect` events are forwarded via HTTP Post — match data is not included.
:::

## Relevant API Endpoints

| Endpoint | Purpose | Reference |
|----------|---------|-----------|
| GetSmartVfdConfig | Read face detection configuration | [Face Detection Config](/docs/api-reference/smart-detection/face-detection-config) |
| SetHttpPostConfig | Configure webhook destination | [Webhook Config](/docs/api-reference/alarm/http-post-webhook-config) |
| GetAlarmStatus | Poll current alarm state (`vfdAlarm`) | [Alarm Status](/docs/api-reference/alarm/alarm-status) |

## Related Applications

- [Home Assistant Integration](/docs/integrations/home-assistant) — face detection events as native HA sensors for access control automations
- [Human Detection & Intrusion Detection](/docs/applications/human-detection-intrusion-api) — detect people entering zones (body detection, not face)
- [People Counting & Traffic Analytics](/docs/applications/people-counting-traffic-analytics-api) — count people crossing lines or entering areas
- [Webhook Event Notification](/docs/applications/webhook-event-notification-api) — complete webhook setup and format reference
- [Real-Time Object Tracking](/docs/applications/real-time-object-tracking-api) — continuous target position data via traject
- [Viewtron Python SDK](/docs/getting-started/python-sdk) — parse face detection events with typed accessors for attributes

## Related Products

- [Viewtron Face Recognition Cameras](https://www.cctvcamerapros.com/face-recognition-cameras-s/1761.htm) — AI camera models with built-in face detection and facial recognition
- [Viewtron AI Security Cameras](https://www.cctvcamerapros.com/AI-security-cameras-s/1512.htm) — full AI camera lineup
- [Viewtron IP Camera NVRs](https://www.cctvcamerapros.com/IP-Camera-NVRs-s/1472.htm) — NVRs with HTTP POST event forwarding

All face detection processing runs on the camera hardware. There is no cloud API dependency, which is important for deployments that need to comply with facial recognition regulations. The NVR v2.0 format includes face attributes (age, sex, glasses, mask) that the IPC v1.x format does not — see the [face detection video demo](https://videos.cctvcamerapros.com/v/ai-face-recognition.html) for a walkthrough of both formats.

## Questions & Development Inquiries

- **Email:** mike@viewtron.com
- **Phone:** 561-433-8488
- **Forum:** [NVR Webhook Setup Guide](https://videos.cctvcamerapros.com/support/topic/setup-nvr-api-webhooks)

Mike Haldas is available for questions, consultation, and custom software development for Viewtron API related projects. Email details about your project to mike@viewtron.com.
