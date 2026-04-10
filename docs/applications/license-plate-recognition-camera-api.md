---
title: "License Plate Recognition Camera API (LPR/ALPR)"
sidebar_label: "License Plate Recognition"
description: "Integrate Viewtron LPR cameras with your software using the HTTP API. Read license plates, manage plate databases (whitelist/blacklist), trigger gate access control, and receive plate images via webhook."
keywords:
  - lpr camera api
  - alpr api integration
  - license plate recognition camera api
  - anpr camera api
  - camera that reads plates
sidebar_position: 2
---

# License Plate Recognition Camera API (LPR/ALPR)

Viewtron AI security cameras include built-in license plate recognition (LPR/ALPR) that runs entirely on the camera hardware — no cloud service, external software, or third-party LPR engine required. When a vehicle passes through the camera's detection zone, the camera reads the license plate and sends an HTTP POST webhook to your server with the plate number, a cropped plate image, and (on NVR v2.0) detailed vehicle attributes including type, color, brand, and model.

The API also supports managing an on-camera plate database with whitelist and blacklist entries, enabling automated gate access control without any middleware. Plates can be added with date ranges and owner information. The camera includes a Wiegand output for direct integration with gate controllers and access control panels. All Viewtron IP cameras and NVRs are NDAA compliant.

## What You Can Build

- **Automated gate access control** — open gates and barriers when whitelisted plates are detected, using Wiegand output or webhook-triggered relay
- **Vehicle access logs** — record every plate read with timestamp, plate image, and authorization status for parking garages, gated communities, or corporate campuses
- **Visitor management systems** — pre-register expected visitor plates with date ranges using AddLicensePlates, automatically grant access on arrival
- **Blacklist alerting** — receive instant notifications when a blacklisted plate is detected on property
- **Fleet tracking** — monitor arrival/departure times for company vehicles across multiple camera locations
- **Law enforcement integration** — feed plate reads into stolen vehicle databases or BOLO systems in real time
- **Parking enforcement** — detect unauthorized vehicles and trigger alerts or record violations with plate crop images

## How It Works

1. **Install an LPR camera** at the vehicle entry point — position the camera to capture plates at the correct angle and distance
2. **Configure LPR detection** on the camera — set the plate region (U.S.A, Canada, Europe, etc.), sensitivity, and detection zone
3. **Enable HTTP POST webhooks** — point the camera or NVR at your server's IP and port
4. **Manage the plate database** (optional) — add plates to the whitelist or blacklist using the AddLicensePlates API with owner info
5. **Your server receives XML** when a plate is read — the POST includes the plate number, authorization status, plate crop image, and vehicle attributes
6. **Parse the event** using the [Viewtron Python SDK](/docs/getting-started/python-sdk) (`pip install viewtron`) or raw XML parsing
7. **Take action** — log the plate read, trigger a gate relay, send alerts, or update your database

## Event Data Included

Each LPR webhook POST contains:

| Field | Description |
|-------|-------------|
| `smartType` | `VEHICE` (IPC) or `vehicle` (NVR) |
| `plateNumber` / `licensePlateNumber` | Detected plate text (e.g., `JP116D`) |
| `vehicleListType` | `whiteList`, `blackList`, `temporaryList`, or absent if not in database (IPC v1.x). Temporary plates outside their valid date range also have this field absent. |
| `licensePlateAttribute/color` | Plate color (NVR v2.0) |
| `carAttribute/carType` | Vehicle type: `sedan`, `suv`, `mpv`, `truck`, etc. (NVR v2.0) |
| `carAttribute/color` | Vehicle color (NVR v2.0) |
| `carAttribute/brand` | Vehicle brand: `GMC`, `Ford`, `Toyota`, etc. (NVR v2.0) |
| `carAttribute/model` | Vehicle model: `GMC_SAVANA`, etc. (NVR v2.0) |
| `rect` | Plate bounding box coordinates (x1, y1, x2, y2) |
| `targetBase64Data` | Cropped plate JPEG image (base64 encoded, ~10-20 KB) |
| `sourceBase64Data` | Full-frame overview JPEG image (base64 encoded, ~400-500 KB) |
| `currentTime` | Detection timestamp |

## Webhook XML Examples

### NVR Format (v2.0) — vehicle

The NVR v2.0 format uses `licensePlateListInfo` instead of `eventInfo` + `targetListInfo`, with detailed vehicle attributes including type, color, brand, and model.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="2.0.0" xmlns="http://www.ipc.com/ver10">
    <messageType>alarmData</messageType>
    <deviceInfo>
        <deviceName><![CDATA[Parking Entrance]]></deviceName>
        <ip><![CDATA[192.168.0.60]]></ip>
        <mac><![CDATA[58:5B:69:40:F4:0D]]></mac>
        <channelId>2</channelId>
    </deviceInfo>
    <smartType>vehicle</smartType>
    <currentTime>18445822972087551616</currentTime>
    <sourceDataInfo>
        <dataType>0</dataType>
        <width>0</width>
        <height>0</height>
    </sourceDataInfo>
    <licensePlateListInfo>
        <item>
            <targetId>104</targetId>
            <rect>
                <x1>1104</x1><y1>546</y1>
                <x2>1232</x2><y2>610</y2>
            </rect>
            <licensePlateAttribute>
                <licensePlateNumber><![CDATA[JP116D]]></licensePlateNumber>
                <color>white</color>
            </licensePlateAttribute>
            <carRect>
                <x1>1</x1><y1>0</y1>
                <x2>1</x2><y2>0</y2>
            </carRect>
            <carAttribute>
                <carType><![CDATA[mpv]]></carType>
                <color><![CDATA[white]]></color>
                <brand><![CDATA[GMC]]></brand>
                <model><![CDATA[GMC_SAVANA]]></model>
            </carAttribute>
            <targetImageData>
                <dataType>0</dataType>
                <width>128</width>
                <height>64</height>
                <targetBase64Length>...</targetBase64Length>
                <targetBase64Data>... (base64 JPEG of plate crop) ...</targetBase64Data>
            </targetImageData>
        </item>
    </licensePlateListInfo>
</config>
```

### IPC Format (v1.x) — VEHICE

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<config version="1.7" xmlns="http://www.ipc.com/ver10">
  <smartType type="openAlramObj">VEHICE</smartType>
  <deviceName type="string"><![CDATA[LPR Camera]]></deviceName>
  <currentTime type="tint64">1774792701902505</currentTime>
  <sourceDataInfo>
    <sourceBase64Length type="uint32">418200</sourceBase64Length>
    <sourceBase64Data type="jpegBase64">... (base64 JPEG overview) ...</sourceBase64Data>
  </sourceDataInfo>
  <listInfo type="list" count="2">
    <item>
      <targetImageData>
        <targetBase64Length type="uint32">52480</targetBase64Length>
        <targetBase64Data type="jpegBase64">... (base64 JPEG overview crop) ...</targetBase64Data>
      </targetImageData>
    </item>
    <item>
      <plateNumber type="string"><![CDATA[ABC1234]]></plateNumber>
      <vehicleListType type="string">whiteList</vehicleListType>
      <targetImageData>
        <targetBase64Length type="uint32">8640</targetBase64Length>
        <targetBase64Data type="jpegBase64">... (base64 JPEG plate crop) ...</targetBase64Data>
      </targetImageData>
    </item>
  </listInfo>
</config>
```

:::note
The IPC smartType uses `VEHICE` (note the typo in the firmware — not `VEHICLE`). The NVR uses `vehicle`.
:::

## Quick Start Example

This standalone script listens for LPR events from both IPC (v1.x) and NVR (v2.0) formats. It prints the plate number, authorization status, and vehicle attributes, saves both the overview image and plate crop, and logs everything to CSV:

```python
#!/usr/bin/env python3
"""License Plate Recognition Event Receiver — Viewtron IP Camera API"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime as dt
import xmltodict
import base64
import csv
import os

# pip install xmltodict
# pip install viewtron
from viewtron import (LPR, VehicleLPR)

PORT = 5002
IMG_DIR = "images"
CSV_FILE = "lpr_events.csv"
os.makedirs(IMG_DIR, exist_ok=True)

class LPRHandler(BaseHTTPRequestHandler):
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

            plate_number = ''
            authorized = ''
            car_type = car_color = car_brand = car_model = ''

            # Route to the correct SDK class based on API version
            if version.startswith('2'):
                msg_type = str(config.get('messageType', ''))
                smart_type = str(config.get('smartType', ''))
                if msg_type != 'alarmData' or smart_type != 'vehicle':
                    return
                event = VehicleLPR(body)
                plate_number = event.get_plate_number()
                authorized = 'N/A'  # NVR v2.0 does not include list type
                car_type = event.get_car_type()
                car_color = event.get_car_color()
                car_brand = event.get_car_brand()
                car_model = event.get_car_model()
            else:
                st = config.get('smartType', {})
                alarm_type = (st.get('#text') or str(st)).strip() if isinstance(st, dict) else str(st).strip()
                if alarm_type != 'VEHICE':
                    return
                event = LPR(body)
                plate_number = event.get_plate_number()
                plate_group = event.get_plate_group()
                authorized = plate_group if plate_group else 'Unknown'

            client_ip = self.client_address[0]

            # Print event details
            print(f"\n{'='*60}")
            print(f"[{dt.now():%Y-%m-%d %H:%M:%S}] LICENSE PLATE DETECTED")
            print(f"  Camera: {event.get_ip_cam()}")
            print(f"  Source: {client_ip}")
            print(f"  Plate: {plate_number}")
            print(f"  Authorized: {authorized}")
            if car_type:
                print(f"  Vehicle: {car_type} | {car_color} | {car_brand} {car_model}")

            # Save images
            ts = event.get_time_stamp()
            saved_files = []

            # Overview image
            if event.has_source_image and event.source_image:
                path = os.path.join(IMG_DIR, f"{ts}-lpr-overview.jpg")
                with open(path, "wb") as f:
                    f.write(base64.b64decode(event.source_image))
                saved_files.append(path)
                print(f"  Overview: {path}")

            # Plate crop image
            if event.has_target_image and event.target_image:
                path = os.path.join(IMG_DIR, f"{ts}-lpr-plate.jpg")
                with open(path, "wb") as f:
                    f.write(base64.b64decode(event.target_image))
                saved_files.append(path)
                print(f"  Plate crop: {path}")

            # Log to CSV
            with open(CSV_FILE, 'a', newline='') as f:
                csv.writer(f).writerow([
                    event.get_time_stamp_formatted(),
                    event.get_ip_cam(),
                    plate_number,
                    authorized,
                    car_type,
                    car_color,
                    car_brand,
                    car_model,
                    client_ip,
                    "|".join(saved_files),
                ])
            print(f"  Logged to {CSV_FILE}")

        except Exception as e:
            print(f"Error: {e}")

    def log_message(self, format, *args):
        pass  # Suppress default HTTP log output

if __name__ == '__main__':
    print(f"LPR Event Receiver running on port {PORT}")
    print(f"Images will be saved to {IMG_DIR}/")
    print(f"Events will be logged to {CSV_FILE}")
    print(f"Waiting for license plate events...\n")
    HTTPServer(('', PORT), LPRHandler).serve_forever()
```

**To run:**

```bash
pip install xmltodict
# pip install viewtron
python3 lpr_receiver.py
```

Then configure your camera or NVR to send HTTP POST events to `http://<your-server-ip>:5002/`.

## Relevant API Endpoints

| Endpoint | Purpose | Reference |
|----------|---------|-----------|
| GetSmartVehicleConfig | Read LPR detection settings (sensitivity, region, dedup mode) | [LPR Config](/docs/api-reference/smart-detection/license-plate-recognition-config) |
| AddLicensePlates | Add plates to the database | [LPR Config](/docs/api-reference/smart-detection/license-plate-recognition-config#addlicenseplates) |
| GetLicensePlates | Query the plate database with pagination | [LPR Config](/docs/api-reference/smart-detection/license-plate-recognition-config#getlicenseplates) |
| ModifyLicensePlate | Update plate details (owner, phone) | [LPR Config](/docs/api-reference/smart-detection/license-plate-recognition-config#modifylicenseplate) |
| DeleteLicensePlate | Remove a plate from the database | [LPR Config](/docs/api-reference/smart-detection/license-plate-recognition-config#deletelicenseplate) |
| SetHttpPostConfig | Configure webhook destination | [Webhook Config](/docs/api-reference/alarm/http-post-webhook-config) |
| GetAlarmStatus | Poll current alarm state | [Alarm Status](/docs/api-reference/alarm/alarm-status) |

:::tip Wiegand Output for Gate Access
Viewtron LPR cameras include a Wiegand output that sends the plate number directly to gate controllers and access control panels. This works independently of the HTTP API — the camera can simultaneously send Wiegand signals to a gate controller and HTTP POST webhooks to your software.
:::

## Related Applications

- [Home Assistant Integration](/docs/integrations/home-assistant) — automate gates, lights, and alerts based on plate reads using native HA sensors
- [Vehicle Detection & Parking Management](/docs/applications/vehicle-detection-parking-management-api) — detect vehicles without reading plates
- [Relay Control & IoT Automation](/docs/applications/relay-control-iot-automation-api) — trigger gate relays based on plate authorization
- [Webhook Event Notification](/docs/applications/webhook-event-notification-api) — complete webhook setup and format reference
- [Human Detection & Intrusion Detection](/docs/applications/human-detection-intrusion-api) — detect people in the same zones
- [Viewtron Python SDK](/docs/getting-started/python-sdk) — parse LPR events and manage the plate database programmatically

## Related Products

- [Viewtron LPR Cameras](https://www.cctvcamerapros.com/License-Plate-Capture-Cameras-s/189.htm) — IP cameras with built-in license plate recognition
- [Viewtron LPR Gate Access Camera Systems](https://www.cctvcamerapros.com/LPR-Camera-Systems-Gate-Security-s/1405.htm) — complete LPR systems for gated communities and commercial facilities
- [Viewtron IP Camera NVRs](https://www.cctvcamerapros.com/IP-Camera-NVRs-s/1472.htm) — NVRs with HTTP POST event forwarding
- [Best License Plate Recognition Cameras](https://videos.cctvcamerapros.com/surveillance-systems/best-license-plate-recognition-cameras.html) — buyer's guide comparing LPR camera options

## Video Guides

- [LPR Camera API Setup and Demo](https://videos.cctvcamerapros.com/v/lpr-camera-api.html) — video walkthrough of configuring LPR webhooks and viewing live plate reads
- [ANPR / LPR Camera System Overview](https://videos.cctvcamerapros.com/v/lpr-camera-system-anpr.html) — camera installation, plate capture zones, and system design
- [LPR Camera Installation Best Practices](https://videos.cctvcamerapros.com/v/anpr-lpr-camera-installation.html) — mounting angles, distances, and IR illumination

## Questions & Development Inquiries

- **Email:** mike@viewtron.com
- **Phone:** 561-433-8488
- **Forum:** [NVR Webhook Setup Guide](https://videos.cctvcamerapros.com/support/topic/setup-nvr-api-webhooks)

Mike Haldas is available for questions, consultation, and custom software development for Viewtron API related projects. Email details about your project to mike@viewtron.com.
