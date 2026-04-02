---
title: "Video Snapshots & Recording Search API"
sidebar_label: "Snapshots & Recording"
description: "Capture JPEG snapshots and search recorded video on Viewtron IP cameras and NVRs via HTTP API. Build timelapse systems, evidence retrieval tools, and remote monitoring dashboards."
keywords:
  - ip camera snapshot api
  - security camera recording api
  - camera image capture api
  - nvr recording search api
  - camera timelapse api
  - ndaa compliant camera snapshot
sidebar_position: 12
---

# Video Snapshots & Recording Search API

Viewtron IP cameras and NVRs provide HTTP API endpoints for capturing live JPEG snapshots and searching recorded video segments by time range. Unlike webhook-based detections where the camera pushes events to your server, snapshot and recording search are outbound API calls — your application sends HTTP requests to the camera or NVR on demand.

These endpoints enable periodic snapshot capture for timelapse projects, on-demand image retrieval for remote monitoring dashboards, and evidence retrieval by searching recorded video for specific time ranges. All requests use standard HTTP with Basic authentication and return either raw JPEG data (v1.9) or base64-encoded images in XML (v2.0). No cloud services or additional software licenses are required. All Viewtron IP cameras and NVRs are NDAA compliant.

## What You Can Build

- **Timelapse photography** — capture snapshots at regular intervals from one or more cameras for construction monitoring, weather tracking, or event documentation
- **Remote monitoring dashboard** — display live snapshots from multiple cameras on a web page or mobile app
- **Evidence retrieval** — search for recorded video segments by time range when investigating incidents
- **Thumbnail generation** — capture preview images from each camera for a multi-camera overview grid
- **Periodic health checks** — verify cameras are online and producing images by capturing test snapshots
- **Snapshot-on-event** — combine with webhook events to capture additional snapshots from nearby cameras when a detection occurs

## How It Works

1. **Capture a live snapshot** — send a `GetSnapshot` request to receive a JPEG image directly from the camera's current live view
2. **Capture by time** — send a `GetSnapshotByTime` request to retrieve a stored image from a specific date and time
3. **Search recordings** — send a `SearchByTime` request with a time range and recording type to find available video segments
4. **Play back recordings** — use the RTSP playback URL format to stream recorded video for a specific time range

## Snapshot Endpoints

### GetSnapshot

Captures a live JPEG snapshot from the camera's current view.

| Field | Value |
|-------|-------|
| **URL** | `GET http://<host>[:port]/GetSnapshot[/channelId]` |
| **Products** | IPC, NVR |
| **Auth** | HTTP Basic (admin credentials) |
| **Response** | Raw JPEG image data (check `Content-Type: image/jpeg` header) |

The channel ID is optional and defaults to 1. For NVRs, specify the channel to capture from a specific camera (e.g., `/GetSnapshot/3` for channel 3).

### GetSnapshotByTime

Retrieves a stored image from a specific date and time.

| Field | Value |
|-------|-------|
| **URL** | `POST http://<host>[:port]/GetSnapshotByTime[/channelId]` |
| **Products** | IPC, NVR |
| **Auth** | HTTP Basic (admin credentials) |

**Request body:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="2.0.0" xmlns="http://www.ipc.com/ver10">
  <search>
    <time><![CDATA[2024-08-23 15:07:28]]></time>
    <length>10</length>
  </search>
</config>
```

:::note Version Difference
In v1.9, `GetSnapshot` returns a raw JPEG image directly. In v2.0, `GetSnapshotByTime` returns a base64-encoded image wrapped in XML (`downloadOneImage/sourceBase64Data`). Always check the `Content-Type` response header to determine the format.
:::

## Recording Search Endpoints

### SearchByTime

Searches for recorded video segments within a time range, filtered by recording type.

| Field | Value |
|-------|-------|
| **URL** | `POST http://<host>[:port]/SearchByTime[/channelId]` |
| **Products** | IPC, NVR |
| **Auth** | HTTP Basic (admin credentials) |

**Request body:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="1.0" xmlns="http://www.ipc.com/ver10">
  <search>
    <recTypes type="list">
      <itemType type="recType"></itemType>
      <item>manual</item>
      <item>schedule</item>
      <item>motion</item>
    </recTypes>
    <starttime type="string"><![CDATA[2024-08-23 00:00:00]]></starttime>
    <endtime type="string"><![CDATA[2024-08-23 23:59:59]]></endtime>
  </search>
</config>
```

### GetRecordType

Retrieves the list of supported recording types for use in `SearchByTime` queries.

| Field | Value |
|-------|-------|
| **URL** | `GET http://<host>[:port]/GetRecordType` |
| **Products** | IPC, NVR |
| **Auth** | HTTP Basic (admin credentials) |

Supported recording types include: `manual`, `schedule`, `motion`, `sensor`, `intel detection`, and `nic broken` (IPC only).

### RTSP Playback URL

After identifying a recording segment, use the RTSP playback URL to stream it:

```
rtsp://<host>[:rtspPort]/chID=0&date=2024-08-23&time=15:07:28&timelen=200&streamType=main&action=playback
```

## Quick Start Example

This standalone script captures a live snapshot, saves it, and searches for recordings in a time range:

```python
#!/usr/bin/env python3
"""Snapshot Capture & Recording Search — Viewtron IP Camera API

Demonstrates:
1. Capturing a live JPEG snapshot via GetSnapshot
2. Capturing a snapshot by time via GetSnapshotByTime
3. Searching for recorded video segments via SearchByTime
"""

import requests
import xmltodict
import base64
import os
from datetime import datetime as dt

# pip install requests xmltodict

# Camera/NVR connection settings
HOST = "192.168.0.147"
USER = "admin"
PASS = "password123"
CHANNEL = 1

IMG_DIR = "snapshots"
os.makedirs(IMG_DIR, exist_ok=True)


def capture_live_snapshot(channel=1):
    """Capture a live JPEG snapshot from the camera."""
    url = f"http://{HOST}/GetSnapshot/{channel}"
    try:
        r = requests.get(url, auth=(USER, PASS), timeout=10)
        if r.status_code == 200:
            content_type = r.headers.get('Content-Type', '')
            ts = dt.now().strftime('%Y%m%d_%H%M%S')

            if 'image/jpeg' in content_type:
                # v1.9: raw JPEG response
                path = os.path.join(IMG_DIR, f"snapshot_ch{channel}_{ts}.jpg")
                with open(path, 'wb') as f:
                    f.write(r.content)
                print(f"Snapshot saved: {path} ({len(r.content):,} bytes)")
                return path

            elif 'xml' in content_type:
                # v2.0: base64 in XML
                data = xmltodict.parse(r.text)
                config = data.get('config', {})
                img_data = config.get('downloadOneImage', {})
                b64 = img_data.get('sourceBase64Data', '')
                if b64:
                    path = os.path.join(IMG_DIR, f"snapshot_ch{channel}_{ts}.jpg")
                    with open(path, 'wb') as f:
                        f.write(base64.b64decode(b64))
                    print(f"Snapshot saved: {path}")
                    return path

        print(f"Snapshot failed: HTTP {r.status_code}")
    except Exception as e:
        print(f"Snapshot error: {e}")
    return None


def capture_snapshot_by_time(channel=1, time_str="2024-08-23 15:07:28"):
    """Retrieve a stored snapshot for a specific date and time."""
    url = f"http://{HOST}/GetSnapshotByTime/{channel}"
    xml_body = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<config version="2.0.0" xmlns="http://www.ipc.com/ver10">\n'
        f'  <search><time><![CDATA[{time_str}]]></time><length>10</length></search>\n'
        '</config>'
    )
    try:
        r = requests.post(url, data=xml_body, auth=(USER, PASS),
                          headers={'Content-Type': 'application/xml'},
                          timeout=10)
        if r.status_code == 200:
            content_type = r.headers.get('Content-Type', '')
            safe_time = time_str.replace(' ', '_').replace(':', '-')

            if 'image/jpeg' in content_type:
                path = os.path.join(IMG_DIR, f"snapshot_by_time_{safe_time}.jpg")
                with open(path, 'wb') as f:
                    f.write(r.content)
                print(f"Snapshot by time saved: {path} ({len(r.content):,} bytes)")
                return path

            elif 'xml' in content_type:
                data = xmltodict.parse(r.text)
                config = data.get('config', {})
                img_data = config.get('downloadOneImage', {})
                b64 = img_data.get('sourceBase64Data', '')
                if b64:
                    path = os.path.join(IMG_DIR, f"snapshot_by_time_{safe_time}.jpg")
                    with open(path, 'wb') as f:
                        f.write(base64.b64decode(b64))
                    print(f"Snapshot by time saved: {path}")
                    return path

        print(f"Snapshot by time failed: HTTP {r.status_code}")
    except Exception as e:
        print(f"Snapshot by time error: {e}")
    return None


def search_recordings(channel=1, start="2024-08-23 00:00:00", end="2024-08-23 23:59:59"):
    """Search for recorded video segments in a time range."""
    url = f"http://{HOST}/SearchByTime/{channel}"
    xml_body = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<config version="1.0" xmlns="http://www.ipc.com/ver10">\n'
        '  <search>\n'
        '    <recTypes type="list">\n'
        '      <itemType type="recType"></itemType>\n'
        '      <item>manual</item>\n'
        '      <item>schedule</item>\n'
        '      <item>motion</item>\n'
        '      <item>sensor</item>\n'
        '      <item>intel detection</item>\n'
        '    </recTypes>\n'
        f'    <starttime type="string"><![CDATA[{start}]]></starttime>\n'
        f'    <endtime type="string"><![CDATA[{end}]]></endtime>\n'
        '  </search>\n'
        '</config>'
    )
    try:
        r = requests.post(url, data=xml_body, auth=(USER, PASS),
                          headers={'Content-Type': 'application/xml'},
                          timeout=10)
        if r.status_code == 200:
            print(f"\nRecording search results ({start} to {end}):")
            print(r.text[:2000])  # Print first 2000 chars of response
        else:
            print(f"Search failed: HTTP {r.status_code}")
    except Exception as e:
        print(f"Search error: {e}")


def get_record_types():
    """Get supported recording types."""
    url = f"http://{HOST}/GetRecordType"
    try:
        r = requests.get(url, auth=(USER, PASS), timeout=10)
        if r.status_code == 200:
            data = xmltodict.parse(r.text)
            config = data.get('config', {})
            caps = config.get('recTypeCaps', {})
            items = caps.get('item', [])
            if not isinstance(items, list):
                items = [items]
            print(f"Supported recording types: {', '.join(items)}")
            return items
        print(f"GetRecordType failed: HTTP {r.status_code}")
    except Exception as e:
        print(f"GetRecordType error: {e}")
    return []


if __name__ == '__main__':
    print(f"Viewtron Snapshot & Recording Tool")
    print(f"Target: {HOST} (Channel {CHANNEL})")
    print(f"Snapshots will be saved to {IMG_DIR}/\n")

    # 1. Get supported recording types
    print("=" * 50)
    print("Step 1: Get supported recording types")
    get_record_types()

    # 2. Capture a live snapshot
    print("\n" + "=" * 50)
    print("Step 2: Capture live snapshot")
    capture_live_snapshot(CHANNEL)

    # 3. Search for recordings in the last 24 hours
    print("\n" + "=" * 50)
    print("Step 3: Search recordings")
    from datetime import timedelta
    now = dt.now()
    yesterday = now - timedelta(days=1)
    search_recordings(
        channel=CHANNEL,
        start=yesterday.strftime('%Y-%m-%d %H:%M:%S'),
        end=now.strftime('%Y-%m-%d %H:%M:%S'),
    )
```

**To run:**

```bash
pip install requests xmltodict
python3 snapshot_tool.py
```

Update `HOST`, `USER`, and `PASS` with your camera or NVR's IP address and credentials.

## Relevant API Endpoints

| Endpoint | Purpose | Reference |
|----------|---------|-----------|
| GetSnapshot | Capture a live JPEG snapshot | [Snapshot](/docs/api-reference/image/get-snapshot) |
| GetSnapshotByTime | Retrieve a stored image by date/time | [Snapshot](/docs/api-reference/image/get-snapshot) |
| SearchByTime | Search for recorded video by time range | [Recording Search](/docs/api-reference/playback/search-recordings-by-time) |
| GetRecordType | List supported recording types | [Record Types](/docs/api-reference/playback/get-record-types) |

## Related Applications

- [Human Detection & Intrusion](/docs/applications/human-detection-intrusion-api) — webhook events that include snapshot images automatically
- [Webhook Event Notification](/docs/applications/webhook-event-notification-api) — automatic image delivery with detection events
- [Real-Time Object Tracking](/docs/applications/real-time-object-tracking-api) — continuous tracking data (complements periodic snapshots)

## Related Products

- [Viewtron AI Security Cameras](https://www.cctvcamerapros.com/AI-security-cameras-s/1512.htm) — IP cameras with built-in snapshot and recording capabilities
- [Viewtron IP Camera NVRs](https://www.cctvcamerapros.com/IP-Camera-NVRs-s/1472.htm) — NVRs with multi-channel snapshot capture and recording search

## Questions & Development Inquiries

- **Email:** mike@viewtron.com
- **Phone:** 561-433-8488
- **Forum:** [NVR Webhook Setup Guide](https://videos.cctvcamerapros.com/support/topic/setup-nvr-api-webhooks)

Mike Haldas is available for questions, consultation, and custom software development for Viewtron API related projects. Email details about your project to mike@viewtron.com.
