---
title: "Relay Control & IoT Automation API"
sidebar_label: "Relay & IoT Control"
description: "Trigger alarm relay outputs and virtual alarms on Viewtron cameras and NVRs via HTTP API. Build IoT automation with ESP8266 integration and event-driven relay control."
keywords:
  - security camera relay control
  - camera automation api
  - ip camera iot integration
  - nvr relay trigger api
  - virtual alarm api
  - esp8266 camera relay
sidebar_position: 8
---

# Relay Control & IoT Automation API

Viewtron IP cameras and NVRs include hardware alarm relay outputs that can be triggered via HTTP API calls. This enables IoT automation workflows where AI detection events from the camera drive physical actions in the real world — opening gates, activating lights, triggering external alarm panels, or controlling any device connected to the relay output. All processing runs on local hardware with no cloud dependency.

The API provides two relay control mechanisms: `ManualAlarmOut` for directly triggering a physical relay output on the camera or NVR, and `TriggerVirtualAlarm` (NVR v2.0 only) for triggering virtual alarm inputs that can activate NVR recording, push notifications, and relay outputs on specific channels. Both endpoints accept standard HTTP requests with Basic authentication. All Viewtron IP cameras and NVRs are NDAA compliant.

A working real-world example of this API is the [ESP8266 relay controller project](https://github.com/mikehaldas/IP-Camera-API) on GitHub, which uses Viewtron camera traject data for continuous human detection to control an ESP8266-based relay module.

## What You Can Build

- **Gate access control** — combine with [license plate recognition](/docs/applications/license-plate-recognition-camera-api) to open gates for authorized vehicles
- **Lighting automation** — activate lights when a person is detected at night, deactivate after a timeout
- **Alarm panel integration** — trigger wired alarm panel zones from camera AI detection events
- **Home automation** — connect camera events to smart home relays for HVAC, locks, or irrigation
- **Industrial automation** — trigger conveyor belts, safety shutoffs, or indicators based on human/vehicle detection
- **ESP8266/Arduino control** — use microcontrollers as intermediary relay controllers driven by camera webhook events

## How It Works

1. **Camera detects an event** — human detection, LPR, line crossing, or other AI detection triggers a webhook POST to your server
2. **Your server processes the event** — verify target type, check authorization lists, evaluate time-based rules
3. **Send relay command** — call `ManualAlarmOut` on the camera/NVR to trigger the physical relay output
4. **Or trigger a virtual alarm** — call `TriggerVirtualAlarm` on the NVR to activate recording and notifications on a specific channel
5. **Reset after timeout** — send a follow-up API call to release the relay after the desired duration

## Relay Control Endpoints

### ManualAlarmOut

Directly triggers or releases a physical alarm relay output.

| Field | Value |
|-------|-------|
| **URL** | `POST http://<host>[:port]/ManualAlarmOut[/channelId]` |
| **Products** | IPC, NVR |
| **Auth** | HTTP Basic (admin credentials) |

**Trigger relay (activate):**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="1.0" xmlns="http://www.ipc.com/ver10">
  <action>
    <status>true</status>
  </action>
</config>
```

**Release relay (deactivate):**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="1.0" xmlns="http://www.ipc.com/ver10">
  <action>
    <status>false</status>
  </action>
</config>
```

:::caution Known Firmware Bug
On IPC cameras, the firmware forcibly resets the alarm output when a perimeter alarm cycle ends, even when alarm output mode is set to `manual_alarm` and `triggerAlarmOut` is unchecked. This makes `ManualAlarmOut` unreliable for automation while perimeter detection is active on the same camera. NVR alarm outputs are not affected by this bug.
:::

### TriggerVirtualAlarm (NVR v2.0 Only)

Triggers a virtual alarm input on the NVR, which can activate recording, push notifications, and relay outputs on specific channels.

| Field | Value |
|-------|-------|
| **URL** | `GET http://<host>[:port]/TriggerVirtualAlarm/{virtualAlarmId}` |
| **Products** | NVR only |
| **Auth** | HTTP Basic (admin credentials) |

**Virtual alarm ID calculation:** IDs start after physical alarm inputs. If the NVR has 16 physical alarms, virtual alarm 1 = ID 17, virtual alarm 2 = ID 18, etc. Use `GetAlarmInInfo` to see the full list.

```bash
curl -u admin:password "http://192.168.0.147/TriggerVirtualAlarm/17"
```

## Quick Start Example

This standalone script receives human detection webhook events and triggers the alarm relay output on the NVR when a person is detected:

```python
#!/usr/bin/env python3
"""Relay Control via Human Detection — Viewtron IP Camera API

Receives human detection webhooks and triggers ManualAlarmOut
on the NVR to control a physical relay output.
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
# Download viewtron.py from https://github.com/mikehaldas/IP-Camera-API
from viewtron import (IntrusionDetection, RegionIntrusion)

PORT = 5002
IMG_DIR = "images"
CSV_FILE = "relay_events.csv"
os.makedirs(IMG_DIR, exist_ok=True)

# NVR/camera credentials for relay control
NVR_IP = "192.168.0.147"
NVR_USER = "admin"
NVR_PASS = "password123"

# How long to keep the relay active (seconds)
RELAY_DURATION = 15


def set_relay(activate=True):
    """Send ManualAlarmOut to the NVR to trigger or release the relay."""
    status = "true" if activate else "false"
    xml_body = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<config version="1.0" xmlns="http://www.ipc.com/ver10">\n'
        f'  <action><status>{status}</status></action>\n'
        '</config>'
    )
    try:
        url = f"http://{NVR_IP}/ManualAlarmOut"
        r = requests.post(url, data=xml_body,
                          auth=(NVR_USER, NVR_PASS),
                          headers={'Content-Type': 'application/xml'},
                          timeout=5)
        state = "ON" if activate else "OFF"
        print(f"  Relay {state} on {NVR_IP} (HTTP {r.status_code})")
    except Exception as e:
        print(f"  Relay control failed: {e}")


def relay_with_timeout(duration):
    """Activate relay, wait, then deactivate."""
    set_relay(activate=True)

    def deactivate():
        set_relay(activate=False)

    threading.Timer(duration, deactivate).start()


class RelayHandler(BaseHTTPRequestHandler):
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
            print(f"[{dt.now():%Y-%m-%d %H:%M:%S}] PERSON DETECTED — TRIGGERING RELAY")
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
                    path = os.path.join(IMG_DIR, f"{ts}-relay-{suffix}.jpg")
                    with open(path, "wb") as f:
                        f.write(base64.b64decode(get_img()))
                    saved_files.append(path)
                    print(f"  Image: {path}")

            # Trigger relay
            relay_with_timeout(RELAY_DURATION)

            # Log to CSV
            with open(CSV_FILE, 'a', newline='') as f:
                csv.writer(f).writerow([
                    event.get_time_stamp_formatted(),
                    event.get_ip_cam(),
                    event.get_alarm_type(),
                    event.get_alarm_description(),
                    client_ip,
                    NVR_IP,
                    "RELAY_TRIGGERED",
                    "|".join(saved_files),
                ])
            print(f"  Logged to {CSV_FILE}")

        except Exception as e:
            print(f"Error: {e}")

    def log_message(self, format, *args):
        pass  # Suppress default HTTP log output

if __name__ == '__main__':
    print(f"Relay Controller running on port {PORT}")
    print(f"NVR relay target: {NVR_IP}")
    print(f"Images will be saved to {IMG_DIR}/")
    print(f"Events will be logged to {CSV_FILE}")
    print(f"Relay duration: {RELAY_DURATION} seconds")
    print(f"Waiting for detection events...\n")
    HTTPServer(('', PORT), RelayHandler).serve_forever()
```

**To run:**

```bash
pip install xmltodict requests
# Place viewtron.py in the same directory
python3 relay_controller.py
```

Then configure your camera or NVR to send HTTP POST events to `http://<your-server-ip>:5002/`.

## ESP8266 Relay Controller Project

A complete real-world example using an ESP8266 microcontroller as a relay controller is available in the [IP-Camera-API GitHub repository](https://github.com/mikehaldas/IP-Camera-API). This project uses Viewtron camera `httpPostV2` traject data for continuous human detection to keep a relay active as long as a person is present in the camera's field of view. When the person leaves and traject data stops, the relay deactivates after a configurable timeout.

This approach solves the limitation of `perimeterAlarm` — which drops to false during the 5-20 second gaps between alarm cycles even if the person is still present — by using continuous traject position data instead.

## Relevant API Endpoints

| Endpoint | Purpose | Reference |
|----------|---------|-----------|
| ManualAlarmOut | Trigger or release alarm relay output | [Alarm Input/Output Config](/docs/api-reference/alarm/alarm-input-output-config) |
| GetAlarmOutConfig | Read alarm output relay configuration | [Alarm Input/Output Config](/docs/api-reference/alarm/alarm-input-output-config) |
| TriggerVirtualAlarm | Trigger virtual alarm on NVR (v2.0) | [Virtual Alarm](/docs/api-reference/alarm/trigger-virtual-alarm) |
| GetAlarmStatus | Poll current alarm state | [Alarm Status](/docs/api-reference/alarm/alarm-status) |
| SetHttpPostConfig | Configure webhook destination for detection events | [Webhook Config](/docs/api-reference/alarm/http-post-webhook-config) |

## Related Applications

- [Human Detection & Intrusion](/docs/applications/human-detection-intrusion-api) — detection events that trigger relay actions
- [License Plate Recognition](/docs/applications/license-plate-recognition-camera-api) — LPR events for gate access control
- [Active Deterrent](/docs/applications/active-deterrent-sound-light-alarm-api) — siren and strobe control via alarm outputs
- [Real-Time Object Tracking](/docs/applications/real-time-object-tracking-api) — continuous traject data for presence-based relay control

## Related Products

- [Viewtron AI Security Cameras](https://www.cctvcamerapros.com/AI-security-cameras-s/1512.htm) — IP cameras with alarm relay outputs and AI detection
- [Viewtron IP Camera NVRs](https://www.cctvcamerapros.com/IP-Camera-NVRs-s/1472.htm) — NVRs with multiple alarm relay outputs and virtual alarm support

## Questions & Development Inquiries

- **Email:** mike@viewtron.com
- **Phone:** 561-433-8488
- **Forum:** [NVR Webhook Setup Guide](https://videos.cctvcamerapros.com/support/topic/setup-nvr-api-webhooks)

Mike Haldas is available for questions, consultation, and custom software development for Viewtron API related projects. Email details about your project to mike@viewtron.com.
