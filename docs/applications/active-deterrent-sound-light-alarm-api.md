---
title: "Active Deterrent Sound & Light Alarm API"
sidebar_label: "Active Deterrent"
description: "Control active deterrent features on Viewtron cameras — trigger sirens, strobe lights, and speaker warnings via HTTP API. Combine with AI detection webhooks for automated deterrence."
keywords:
  - active deterrent camera api
  - security camera siren api
  - camera alarm api
  - strobe light camera api
  - automated deterrence system
  - ndaa compliant active deterrent camera
sidebar_position: 7
---

# Active Deterrent Sound & Light Alarm API

Viewtron AI security cameras with active deterrent features include built-in sirens, red and blue strobe lights, and two-way audio speakers that can be controlled via the HTTP API. Unlike webhook-based detections where the camera pushes events to your server, active deterrent control uses outbound API calls — your application sends HTTP requests to the camera to trigger or configure audio and light alarms.

The real power of active deterrent API control comes from combining it with AI detection webhooks. You can build a fully automated deterrence system: receive a human detection or intrusion webhook, verify the event in your application logic, then immediately trigger the camera's siren and strobe lights via API call — all running on local hardware with no cloud dependency. All Viewtron IP cameras and NVRs are NDAA compliant.

## What You Can Build

- **Automated intruder deterrence** — detect a person via [intrusion detection](/docs/applications/human-detection-intrusion-api) webhook, then trigger siren and strobe lights on the same camera
- **Scheduled siren tests** — periodically test active deterrent hardware via API to confirm operation
- **Multi-camera deterrence chain** — detect intrusion on one camera, trigger alarms on multiple cameras in the area
- **Alarm panel integration** — connect camera deterrent features to existing alarm and building management systems
- **Progressive response** — start with white light, escalate to red/blue strobe, then activate siren based on dwell time
- **Two-way audio warnings** — combine with audio alarm configuration for speaker-based verbal warnings

## How It Works

1. **Verify camera supports active deterrent** — not all models have sirens and strobe lights (check product specs)
2. **Read current configuration** — use `GetAudioAlarmOutConfig` and `GetWhiteLightAlarmOutConfig` to see available settings
3. **Receive a detection webhook** — your server receives an intrusion, line crossing, or other AI detection event
4. **Evaluate the event** — check target type, confidence, time of day, or other criteria in your application logic
5. **Trigger deterrent via API** — send HTTP requests to the camera to activate siren, strobe, or both
6. **Reset after timeout** — deactivate the deterrent after a configurable period

## Active Deterrent Endpoints

| Endpoint | Purpose | Version |
|----------|---------|---------|
| `GetAudioAlarmOutConfig` | Read siren/audio alarm configuration | v2.0 only |
| `GetWhiteLightAlarmOutConfig` | Read white light/strobe alarm configuration | v2.0 only |

:::note
These endpoints are read-only configuration commands documented in API v2.0. Direct triggering of siren and strobe outputs works through the alarm output relay system or by combining detection rules with alarm actions configured on the camera. The `ManualAlarmOut` endpoint can also be used to trigger the relay output which may be wired to external sirens or lights.
:::

## Combining Detection Webhooks with Deterrent API Calls

The most common use case is an event-driven pipeline:

```
Camera detects person → Webhook POST to your server → Your logic decides →
API call back to camera → Siren/strobe activates
```

This requires two types of API interaction:
1. **Inbound webhooks** (camera pushes to your server) — detection events with images
2. **Outbound API calls** (your server sends to camera) — trigger alarm outputs

## Quick Start Example

This standalone script receives intrusion detection webhooks and triggers the alarm output relay on the camera when a person is detected:

```python
#!/usr/bin/env python3
"""Active Deterrent Controller — Viewtron IP Camera API

Receives intrusion webhooks and triggers alarm output on the camera.
Combines webhook receiving with outbound API calls.
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime as dt
import xmltodict
import requests
import base64
import csv
import os
import threading

# pip install xmltodict requests
# pip install viewtron
from viewtron import (IntrusionDetection, RegionIntrusion)

PORT = 5002
IMG_DIR = "images"
CSV_FILE = "deterrent_events.csv"
os.makedirs(IMG_DIR, exist_ok=True)

# Camera credentials for outbound API calls
CAMERA_USER = "admin"
CAMERA_PASS = "password123"

# How long to keep the alarm active (seconds)
ALARM_DURATION = 10


def trigger_alarm(camera_ip, activate=True):
    """Send ManualAlarmOut to the camera to trigger or release the relay."""
    status = "true" if activate else "false"
    xml_body = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<config version="1.0" xmlns="http://www.ipc.com/ver10">\n'
        f'  <action><status>{status}</status></action>\n'
        '</config>'
    )
    try:
        url = f"http://{camera_ip}/ManualAlarmOut"
        r = requests.post(url, data=xml_body,
                          auth=(CAMERA_USER, CAMERA_PASS),
                          headers={'Content-Type': 'application/xml'},
                          timeout=5)
        action = "ACTIVATED" if activate else "DEACTIVATED"
        print(f"  Alarm {action} on {camera_ip} (HTTP {r.status_code})")
    except Exception as e:
        print(f"  Alarm trigger failed on {camera_ip}: {e}")


def trigger_alarm_with_timeout(camera_ip, duration):
    """Activate alarm, wait, then deactivate."""
    trigger_alarm(camera_ip, activate=True)

    def deactivate():
        trigger_alarm(camera_ip, activate=False)

    threading.Timer(duration, deactivate).start()


class DeterrentHandler(BaseHTTPRequestHandler):
    def do_POST(self):
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
            version = config.get('@version', '')

            # Route to the correct SDK class based on API version
            if version.startswith('2'):
                msg_type = str(config.get('messageType', ''))
                smart_type = str(config.get('smartType', ''))
                if msg_type != 'alarmData' or smart_type != 'regionIntrusion':
                    return
                event = RegionIntrusion(body)
                camera_ip = str(config.get('deviceInfo', {}).get('ip', ''))
            else:
                st = config.get('smartType', {})
                alarm_type = (st.get('#text') or str(st)).strip() if isinstance(st, dict) else str(st).strip()
                if alarm_type != 'PEA':
                    return
                event = IntrusionDetection(body)
                camera_ip = self.client_address[0]

            client_ip = self.client_address[0]

            # Print event details
            print(f"\n{'='*60}")
            print(f"[{dt.now():%Y-%m-%d %H:%M:%S}] INTRUSION — TRIGGERING DETERRENT")
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
                    path = os.path.join(IMG_DIR, f"{ts}-deterrent-{suffix}.jpg")
                    with open(path, "wb") as f:
                        f.write(base64.b64decode(get_img()))
                    saved_files.append(path)
                    print(f"  Image: {path}")

            # Trigger alarm on the camera
            if camera_ip:
                trigger_alarm_with_timeout(camera_ip, ALARM_DURATION)

            # Log to CSV
            with open(CSV_FILE, 'a', newline='') as f:
                csv.writer(f).writerow([
                    event.get_time_stamp_formatted(),
                    event.get_ip_cam(),
                    event.get_alarm_type(),
                    event.get_alarm_description(),
                    camera_ip,
                    "ALARM_TRIGGERED",
                    "|".join(saved_files),
                ])
            print(f"  Logged to {CSV_FILE}")

        except Exception as e:
            print(f"Error: {e}")

    def log_message(self, format, *args):
        pass  # Suppress default HTTP log output

if __name__ == '__main__':
    print(f"Active Deterrent Controller running on port {PORT}")
    print(f"Images will be saved to {IMG_DIR}/")
    print(f"Events will be logged to {CSV_FILE}")
    print(f"Alarm duration: {ALARM_DURATION} seconds")
    print(f"Waiting for intrusion events...\n")
    HTTPServer(('', PORT), DeterrentHandler).serve_forever()
```

**To run:**

```bash
pip install xmltodict requests
# pip install viewtron
python3 deterrent_controller.py
```

Then configure your camera or NVR to send HTTP POST events to `http://<your-server-ip>:5002/`.

:::caution Known Firmware Bug
On IPC cameras, the firmware forcibly resets the alarm output when a perimeter alarm cycle ends, even when alarm output mode is set to `manual_alarm` and `triggerAlarmOut` is unchecked. This makes `ManualAlarmOut` unreliable for automation while perimeter detection is active on the same camera. NVR alarm outputs are not affected by this bug.
:::

## Relevant API Endpoints

| Endpoint | Purpose | Reference |
|----------|---------|-----------|
| GetAudioAlarmOutConfig | Read audio/siren alarm configuration (v2.0) | [Sound & Light Config](/docs/api-reference/alarm/sound-light-alarm-config) |
| GetWhiteLightAlarmOutConfig | Read white light/strobe alarm configuration (v2.0) | [Sound & Light Config](/docs/api-reference/alarm/sound-light-alarm-config) |
| ManualAlarmOut | Trigger or release alarm relay output | [Alarm Input/Output Config](/docs/api-reference/alarm/alarm-input-output-config) |
| GetAlarmOutConfig | Read alarm output relay configuration | [Alarm Input/Output Config](/docs/api-reference/alarm/alarm-input-output-config) |
| SetHttpPostConfig | Configure webhook destination for detection events | [Webhook Config](/docs/api-reference/alarm/http-post-webhook-config) |

## Related Applications

- [Human Detection & Intrusion](/docs/applications/human-detection-intrusion-api) — intrusion detection events that trigger deterrence
- [Perimeter Security & Line Crossing](/docs/applications/perimeter-security-line-crossing-api) — line crossing events for boundary-based deterrence
- [Relay Control & IoT Automation](/docs/applications/relay-control-iot-automation-api) — relay output control for external siren and lighting systems
- [Loitering Detection](/docs/applications/loitering-detection-api) — escalated deterrence for prolonged presence

## Related Products

- [Viewtron AI Security Cameras](https://www.cctvcamerapros.com/AI-security-cameras-s/1512.htm) — IP cameras with built-in active deterrent features (red/blue strobe, siren, two-way audio)
- [Viewtron IP Camera NVRs](https://www.cctvcamerapros.com/IP-Camera-NVRs-s/1472.htm) — NVRs with alarm relay outputs and HTTP POST event forwarding

## Questions & Development Inquiries

- **Email:** mike@viewtron.com
- **Phone:** 561-433-8488
- **Forum:** [NVR Webhook Setup Guide](https://videos.cctvcamerapros.com/support/topic/setup-nvr-api-webhooks)

Mike Haldas is available for questions, consultation, and custom software development for Viewtron API related projects. Email details about your project to mike@viewtron.com.
