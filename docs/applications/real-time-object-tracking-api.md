---
title: "Real-Time Object Tracking API (traject)"
sidebar_label: "Real-Time Tracking"
description: "Receive continuous real-time target position updates from Viewtron IP cameras — track people and vehicles with position, speed, and trajectory data using the traject HTTP POST stream."
keywords:
  - ip camera tracking api
  - real-time object tracking
  - camera traject api
  - continuous object position data
  - camera target tracking api
  - presence detection camera api
sidebar_position: 9
---

# Real-Time Object Tracking API (traject)

Viewtron AI cameras support a unique real-time tracking mode called **traject** that continuously streams target position data to your server via HTTP POST. Unlike alarm-based detection events that fire once per event, traject sends **continuous updates at approximately 7 posts per second** for the entire duration a target is being tracked. Each post is only ~1.7 KB of XML data containing the target ID, target type (person, car, or motorcycle), and bounding box coordinates — no images are included.

This makes traject fundamentally different from every other detection type in the Viewtron API. Alarm-based methods like human detection or line crossing send a single event with images when something happens. Traject gives you a continuous stream of position data that lets you know exactly where a target is, how long it has been there, and when it leaves. The stream starts within ~140ms of a target being detected and stops within ~1 second of the target leaving the camera's view.

**Important:** Traject is only available from IPC cameras directly — NVRs do not forward traject data. The camera must be subscribed to the `traject` data type via httpPostV2 configuration.

## What You Can Build

- **Real-time position dashboards** — display target locations on a map or floor plan that updates in real time
- **Presence-based relay control** — turn on lights, activate alarms, or control relays while a person is present (see the [ESP8266 relay controller project](https://github.com/mikehaldas/IP-Camera-API))
- **Dwell time analysis** — calculate exactly how long each target stays in view, down to sub-second precision
- **Speed and direction estimation** — track bounding box movement between frames to estimate velocity
- **Occupancy counting** — monitor how many targets are simultaneously active in the camera's field of view
- **Custom alarm logic** — build your own detection rules based on target position, duration, or movement patterns

## How It Works

1. **Enable traject on the camera** — subscribe to the `traject` data type in the httpPostV2 configuration and enable "Smart track data" in the camera's HTTP Post V2 web interface
2. **Your server receives continuous XML posts** while any target is being tracked — approximately 7 posts per second per target
3. **Parse the position data** — each post contains one or more targets with targetId, targetType, and bounding rect coordinates
4. **Track targets over time** — use the targetId to correlate posts for the same target, calculate dwell time and movement
5. **Detect departure** — when posts stop arriving for a targetId, the target has left the camera's view

## Comparison with Other Methods

| Method | Signal Type | Posts While Present | Gaps While Present | Data per Post |
|--------|------------|--------------------|--------------------|--------------|
| `GetAlarmStatus` polling | `perimeterAlarm=true` | Periodic (your poll rate) | Yes (5-20 seconds) | ~660 bytes |
| Alarm server push | One POST per event | 1-2 per entry | Yes (20-60 seconds) | ~510-530 KB (with images) |
| **httpPostV2 `traject`** | **Continuous POSTs** | **6-12 per second** | **None** | **~1.7 KB (no images)** |

The key advantage of traject is **zero gaps**. Alarm-based methods have significant blind periods where a target is present but no data is being sent. Traject provides continuous confirmation that a target is still there.

## Traject Data Fields

Each traject POST contains one or more tracked targets:

| Field | Type | Description |
|-------|------|-------------|
| `targetId` | uint32 | Unique ID for the tracked target — new ID assigned per entry |
| `targetType` | string | `person`, `car`, or `motor` |
| `rect` | x1, y1, x2, y2 | Bounding box in normalized coordinates (0-10000) |
| `point` | x, y | Target center point (may be 0,0) |
| `velocity` | uint32 | Target velocity (may be 0) |
| `direction` | uint32 | Target direction (may be 0) |
| `trajectlength` | list | Trajectory path points (may be empty) |
| `currentTime` | tint64 | Timestamp in microseconds |
| `mac` | string | Camera MAC address |
| `deviceName` | string | Camera name |

:::note
The `velocity`, `direction`, and `trajectlength` fields are included in the XML but are typically reported as zero in current firmware. You can calculate speed and direction yourself by tracking bounding box position changes between consecutive posts.
:::

## Webhook XML Example

### IPC Format — traject

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<config version="1.7" xmlns="http://www.ipc.com/ver10">
  <types>
    <openAlramObj>
      <enum>MOTION</enum><enum>SENSOR</enum><enum>PEA</enum>
    </openAlramObj>
    <subscribeRelation>
      <enum>ALARM</enum>
      <enum>FEATURE_RESULT</enum>
      <enum>ALARM_FEATURE</enum>
    </subscribeRelation>
    <targetType>
      <enum>person</enum>
      <enum>car</enum>
      <enum>motor</enum>
    </targetType>
  </types>
  <subscribeOption type="subscribeRelation">FEATURE_RESULT</subscribeOption>
  <currentTime type="tint64">1774646121524166</currentTime>
  <mac type="string"><![CDATA[58:5b:69:5f:42:1b]]></mac>
  <sn type="string"><![CDATA[I421B0Z1173Q]]></sn>
  <deviceName type="string"><![CDATA[FaceCam]]></deviceName>
  <traject type="list" count="1">
    <item>
      <targetId type="uint32">434</targetId>
      <point>
        <x type="uint32">0</x>
        <y type="uint32">0</y>
      </point>
      <rect>
        <x1 type="uint32">6534</x1>
        <y1 type="uint32">2708</y1>
        <x2 type="uint32">7585</x2>
        <y2 type="uint32">6388</y2>
      </rect>
      <velocity type="uint32">0</velocity>
      <direction type="uint32">0</direction>
      <targetType type="targetType">person</targetType>
      <trajectlength type="list" count="0"/>
    </item>
  </traject>
</config>
```

Multiple targets can be tracked simultaneously — each appears as a separate `<item>` in the `<traject>` list with a unique `targetId`. The `count` attribute reflects the number of targets in that post.

## Configuration

Enable traject on an IPC camera by sending this XML to `SetHttpPostConfig`:

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
      <port>80</port>
      <path><![CDATA[/API]]></path>
      <authentication>none</authentication>
    </url>
    <heatBeatSwitch>true</heatBeatSwitch>
    <keepaliveTimeval>90</keepaliveTimeval>
    <subscribeDateType type="list" count="1">
      <item>traject</item>
    </subscribeDateType>
    <subscriptionEvents type="list" count="1">
      <item>PERIMETER</item>
    </subscriptionEvents>
  </item></urlList>
</postUrlConf></httpPostV2>
</config>
```

:::warning
The **"Smart track data" checkbox must also be enabled** in the camera's HTTP Post V2 web interface (Edit HTTP POST dialog). The camera will not send traject data even if configured via API unless this checkbox is checked.
:::

## Important Notes

- **Traject is IPC-only.** NVRs do not forward traject data and do not expose the smart track data subscription.
- **Works through NVR PoE.** When an IPC is connected to an NVR via PoE, the camera still sends traject directly to your server. The XML format is identical — the source IP will be the NVR's PoE interface.
- **No images included.** Traject posts contain only position data (~1.7 KB). For images, use a parallel alarm-based subscription.
- **Recommended dual setup:** Configure the NVR's HTTP POST for alarm events with images, and configure the IPC's httpPostV2 for traject tracking. This gives you both event snapshots and continuous position data.
- **New targetId per entry.** Each time a target enters the camera's view, it receives a new unique targetId. The same physical person will get different IDs if they leave and return.

## Quick Start Example

This standalone script listens for traject posts and displays a live updating console showing active targets, post rate, and dwell time. Since traject is not wrapped in a viewtron.py class, this example parses the XML directly with xmltodict:

```python
#!/usr/bin/env python3
"""Real-Time Traject Tracker — Viewtron IP Camera API"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime as dt
import xmltodict
import time
import sys

# pip install xmltodict

PORT = 5002

# Active targets: {targetId: {type, first_seen, last_seen, post_count, last_rect}}
active_targets = {}
total_posts = 0
start_time = time.time()

# Expire targets after this many seconds without a post
TARGET_TIMEOUT = 2.0

class TrajectHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        global total_posts

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

            # Check for traject data
            traject = config.get('traject', {})
            if not traject:
                return

            now = time.time()
            total_posts += 1

            # Parse target items
            items = traject.get('item', [])
            if not isinstance(items, list):
                items = [items] if items else []

            for item in items:
                if not isinstance(item, dict):
                    continue

                target_id_raw = item.get('targetId', {})
                target_id = (target_id_raw.get('#text') if isinstance(target_id_raw, dict)
                             else str(target_id_raw))

                target_type_raw = item.get('targetType', {})
                target_type = (target_type_raw.get('#text') if isinstance(target_type_raw, dict)
                               else str(target_type_raw))

                rect = item.get('rect', {})
                rect_str = "({},{}) ({},{})".format(
                    rect.get('x1', {}).get('#text', '0') if isinstance(rect.get('x1'), dict) else rect.get('x1', '0'),
                    rect.get('y1', {}).get('#text', '0') if isinstance(rect.get('y1'), dict) else rect.get('y1', '0'),
                    rect.get('x2', {}).get('#text', '0') if isinstance(rect.get('x2'), dict) else rect.get('x2', '0'),
                    rect.get('y2', {}).get('#text', '0') if isinstance(rect.get('y2'), dict) else rect.get('y2', '0'),
                )

                if target_id in active_targets:
                    active_targets[target_id]['last_seen'] = now
                    active_targets[target_id]['post_count'] += 1
                    active_targets[target_id]['last_rect'] = rect_str
                else:
                    active_targets[target_id] = {
                        'type': target_type,
                        'first_seen': now,
                        'last_seen': now,
                        'post_count': 1,
                        'last_rect': rect_str,
                    }

            # Expire old targets
            expired = [tid for tid, t in active_targets.items()
                       if now - t['last_seen'] > TARGET_TIMEOUT]
            for tid in expired:
                t = active_targets.pop(tid)
                dwell = t['last_seen'] - t['first_seen']
                print(f"\n  [DEPARTED] Target {tid} ({t['type']}) — "
                      f"dwell: {dwell:.1f}s, posts: {t['post_count']}")

            # Display live status
            elapsed = now - start_time
            rate = total_posts / elapsed if elapsed > 0 else 0
            active_list = ", ".join(
                f"{tid}:{t['type']}({t['post_count']})"
                for tid, t in active_targets.items()
            )
            status = (f"\r  Active: [{active_list or 'none'}]  "
                      f"Total posts: {total_posts}  Rate: {rate:.1f}/sec  ")
            sys.stdout.write(status)
            sys.stdout.flush()

        except Exception as e:
            print(f"\nError: {e}")

    def log_message(self, format, *args):
        pass  # Suppress default HTTP log output

if __name__ == '__main__':
    print(f"Traject Tracker running on port {PORT}")
    print(f"Waiting for traject data...\n")
    print(f"  Targets will show as targetId:type(post_count)")
    print(f"  Departed targets will show dwell time and total posts\n")
    HTTPServer(('', PORT), TrajectHandler).serve_forever()
```

**To run:**

```bash
pip install xmltodict
python3 traject_tracker.py
```

Then configure your IPC camera to send httpPostV2 traject data to `http://<your-server-ip>:5002/`.

**For a working automation example**, see the [ESP8266 Relay Controller](https://github.com/mikehaldas/IP-Camera-API) project, which uses traject data to control a relay for continuous human presence detection — keeping a relay energized for the entire duration a person is in view with zero gaps.

## Relevant API Endpoints

| Endpoint | Purpose | Reference |
|----------|---------|-----------|
| SetHttpPostConfig | Configure httpPostV2 with traject subscription | [Webhook Config](/docs/api-reference/alarm/http-post-webhook-config) |
| GetHttpPostConfig | Read current httpPostV2 configuration | [Webhook Config](/docs/api-reference/alarm/http-post-webhook-config) |
| GetSmartPerimeterConfig | Configure the perimeter detection zone that triggers tracking | [Intrusion Detection Config](/docs/api-reference/smart-detection/intrusion-perimeter-detection-config) |

## Related Applications

- [Human Detection & Intrusion Detection](/docs/applications/human-detection-intrusion-api) — event-based detection with images (complements traject)
- [Relay Control & IoT Automation](/docs/applications/relay-control-iot-automation-api) — trigger relays based on traject presence data
- [People Counting & Traffic Analytics](/docs/applications/people-counting-traffic-analytics-api) — count targets crossing lines or entering areas
- [Webhook Event Notification](/docs/applications/webhook-event-notification-api) — complete webhook setup and format reference

## Related Products

- [Viewtron AI Security Cameras](https://www.cctvcamerapros.com/AI-security-cameras-s/1512.htm) — IP cameras with built-in traject tracking
- [Viewtron IP Camera NVRs](https://www.cctvcamerapros.com/IP-Camera-NVRs-s/1472.htm) — NVRs for centralized camera management (traject requires direct IPC connection)

## Questions & Development Inquiries

- **Email:** mike@viewtron.com
- **Phone:** 561-433-8488
- **Forum:** [NVR Webhook Setup Guide](https://videos.cctvcamerapros.com/support/topic/setup-nvr-api-webhooks)

Mike Haldas is available for questions, consultation, and custom software development for Viewtron API related projects. Email details about your project to mike@viewtron.com.
