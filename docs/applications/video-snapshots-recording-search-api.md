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

After identifying a recording segment, use the RTSP playback URL to stream or export it:

```
rtsp://<user>:<pass>@<host>[:554]/chID=<channel>&date=YYYY-MM-DD&time=HH:MM:SS&timelen=<seconds>&streamType=main&action=playback
```

| Parameter | Description |
|-----------|-------------|
| `chID` | Channel number (1-based) |
| `date` | Recording date (`YYYY-MM-DD`) |
| `time` | Start time (`HH:MM:SS`) |
| `timelen` | Duration in seconds |
| `streamType` | `main` or `sub` (NVR may only serve main for playback) |
| `action` | Must be `playback` |

:::note
The parameter order matters — some NVR firmware versions will hang if the parameters are reordered. Use the exact order shown above: `chID`, `date`, `time`, `timelen`, `streamType`, `action`.
:::

### Exporting Recorded Video Clips

Use FFmpeg with the RTSP playback URL to export recorded video segments to MP4 files. The `-c:v copy` flag copies the H.264/H.265 stream as-is with no re-encoding — fast and lossless:

```bash
ffmpeg -rtsp_transport tcp -stimeout 5000000 \
  -i "rtsp://admin:password@192.168.0.50:554/chID=1&date=2026-04-02&time=11:00:00&timelen=10&streamType=main&action=playback" \
  -c:v copy -an -t 10 -y ch1_2026-04-02_11-00-00_10s.mp4
```

| Flag | Purpose |
|------|---------|
| `-rtsp_transport tcp` | Use TCP for reliable transport |
| `-stimeout 5000000` | Auto-stop after 5 seconds of no data (prevents hanging) |
| `-c:v copy` | Copy video stream as-is — no re-encoding |
| `-an` | Drop audio (NVR audio is PCM mu-law which is incompatible with MP4) |
| `-t 10` | Stop after 10 seconds of output |
| `-y` | Overwrite output file without prompting |

## Quick Start Examples

### Example 1: Snapshot Capture & Recording Search

This script captures a live snapshot and searches for recordings:

```python
#!/usr/bin/env python3
"""Snapshot Capture & Recording Search — Viewtron IP Camera API"""

import requests
import xmltodict
import base64
import os
from datetime import datetime as dt, timedelta

# pip install requests xmltodict

HOST = "192.168.0.50"
USER = "admin"
PASS = "password123"
CHANNEL = 1
IMG_DIR = "snapshots"
os.makedirs(IMG_DIR, exist_ok=True)


def capture_live_snapshot(channel=1):
    """Capture a live JPEG snapshot from the camera."""
    url = f"http://{HOST}/GetSnapshot/{channel}"
    r = requests.get(url, auth=(USER, PASS), timeout=10)
    if r.status_code != 200:
        print(f"Snapshot failed: HTTP {r.status_code}")
        return None

    ts = dt.now().strftime('%Y%m%d_%H%M%S')
    content_type = r.headers.get('Content-Type', '')

    if 'image/jpeg' in content_type:
        # v1.9: raw JPEG response
        path = os.path.join(IMG_DIR, f"snapshot_ch{channel}_{ts}.jpg")
        with open(path, 'wb') as f:
            f.write(r.content)
    elif 'xml' in content_type:
        # v2.0: base64 in XML
        data = xmltodict.parse(r.text)
        b64 = data.get('config', {}).get('downloadOneImage', {}).get('sourceBase64Data', '')
        if not b64:
            print("No image data in response")
            return None
        path = os.path.join(IMG_DIR, f"snapshot_ch{channel}_{ts}.jpg")
        with open(path, 'wb') as f:
            f.write(base64.b64decode(b64))

    print(f"Snapshot saved: {path}")
    return path


def search_recordings(channel=1, start="2026-04-02 00:00:00", end="2026-04-02 23:59:59"):
    """Search for recorded video segments in a time range."""
    url = f"http://{HOST}/SearchByTime/{channel}"
    xml_body = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<config version="1.0" xmlns="http://www.ipc.com/ver10">\n'
        '  <search>\n'
        '    <recTypes type="list">\n'
        '      <itemType type="recType"></itemType>\n'
        '      <item>manual</item><item>schedule</item>\n'
        '      <item>motion</item><item>intel detection</item>\n'
        '    </recTypes>\n'
        f'    <starttime type="string"><![CDATA[{start}]]></starttime>\n'
        f'    <endtime type="string"><![CDATA[{end}]]></endtime>\n'
        '  </search>\n'
        '</config>'
    )
    r = requests.post(url, data=xml_body, auth=(USER, PASS),
                      headers={'Content-Type': 'application/xml'}, timeout=10)
    if r.status_code == 200:
        print(f"Recording search results ({start} to {end}):")
        print(r.text[:2000])
    else:
        print(f"Search failed: HTTP {r.status_code}")


if __name__ == '__main__':
    print(f"Target: {HOST} (Channel {CHANNEL})\n")

    print("Capturing live snapshot...")
    capture_live_snapshot(CHANNEL)

    print("\nSearching recordings (last 24 hours)...")
    now = dt.now()
    search_recordings(
        channel=CHANNEL,
        start=(now - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S'),
        end=now.strftime('%Y-%m-%d %H:%M:%S'),
    )
```

### Example 2: NVR Clip Export Tool

This script exports recorded video clips from the NVR using the RTSP playback URL and FFmpeg. It copies the video stream as-is with no re-encoding.

```python
#!/usr/bin/env python3
"""
NVR Clip Export Tool — Viewtron IP Camera API

Exports a recorded video clip from the NVR via RTSP playback.
Uses FFmpeg with -c:v copy for fast, lossless export.

Usage:
    python3 clip_export.py -c 1 -s "2026-04-02 11:00:00" -d 10
    python3 clip_export.py -c 1 -s "2026-04-02 11:00:00" -d 30 -o /tmp/clips/
"""

import argparse
import os
import subprocess
import sys
import time
from datetime import datetime

# NVR connection settings
NVR_IP = "192.168.0.50"
NVR_USER = "admin"
NVR_PASS = "password123"
RTSP_PORT = 554


def build_playback_url(channel_id, date_str, time_str, duration):
    """Build the RTSP playback URL for recorded footage."""
    return (
        f"rtsp://{NVR_USER}:{NVR_PASS}"
        f"@{NVR_IP}:{RTSP_PORT}"
        f"/chID={channel_id}"
        f"&date={date_str}"
        f"&time={time_str}"
        f"&timelen={duration}"
        f"&streamType=main"
        f"&action=playback"
    )


def export_clip(channel_id, start_dt, duration, output_dir):
    """Pull a recorded clip from the NVR and save to MP4."""
    date_str = start_dt.strftime('%Y-%m-%d')
    time_str = start_dt.strftime('%H:%M:%S')
    rtsp_url = build_playback_url(channel_id, date_str, time_str, duration)

    # Build output filename
    ts_slug = start_dt.strftime('%Y-%m-%d_%H-%M-%S')
    filename = f"ch{channel_id}_{ts_slug}_{duration}s.mp4"
    output_path = os.path.join(output_dir, filename)

    # FFmpeg command — copy video as-is, no audio, auto-stop
    cmd = [
        'ffmpeg',
        '-rtsp_transport', 'tcp',
        '-stimeout', '5000000',
        '-i', rtsp_url,
        '-t', str(duration),
        '-c:v', 'copy',
        '-an',
        '-y',
        output_path,
    ]

    print(f"Exporting: channel {channel_id}, {date_str} {time_str}, {duration}s")
    print(f"Output: {output_path}")

    t0 = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True)
    elapsed = time.time() - t0

    if result.returncode != 0:
        print(f"FFmpeg failed (exit {result.returncode}):")
        print(result.stderr[-500:] if len(result.stderr) > 500 else result.stderr)
        sys.exit(1)

    # Verify output with ffprobe
    probe = subprocess.run(
        ['ffprobe', '-v', 'error', '-select_streams', 'v:0',
         '-show_entries', 'stream=width,height,r_frame_rate,codec_name',
         '-of', 'default=noprint_wrappers=1', output_path],
        capture_output=True, text=True
    )
    size_mb = os.path.getsize(output_path) / (1024 * 1024)

    print(f"\nExport complete in {elapsed:.1f}s")
    print(probe.stdout.strip())
    print(f"File size: {size_mb:.2f} MB")

    return output_path


def main():
    parser = argparse.ArgumentParser(
        description='Export recorded video clips from Viewtron NVR',
        epilog='Example: python3 clip_export.py -c 1 -s "2026-04-02 11:00:00" -d 10'
    )
    parser.add_argument('-c', '--channel', type=int, required=True,
                        help='NVR channel ID (1-based)')
    parser.add_argument('-s', '--start', required=True,
                        help='Start datetime: "YYYY-MM-DD HH:MM:SS"')
    parser.add_argument('-d', '--duration', type=int, default=10,
                        help='Clip duration in seconds (default: 10, max: 300)')
    parser.add_argument('-o', '--output-dir', default='.',
                        help='Output directory (default: current directory)')

    args = parser.parse_args()

    try:
        start_dt = datetime.strptime(args.start, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        print('Error: Use format "YYYY-MM-DD HH:MM:SS"')
        sys.exit(1)

    if args.duration < 1 or args.duration > 300:
        print('Error: Duration must be between 1 and 300 seconds')
        sys.exit(1)

    os.makedirs(args.output_dir, exist_ok=True)
    export_clip(args.channel, start_dt, args.duration, args.output_dir)


if __name__ == '__main__':
    main()
```

**To run:**

```bash
# Export a 10-second clip from channel 1
python3 clip_export.py -c 1 -s "2026-04-02 11:00:00" -d 10

# Export to a specific directory
python3 clip_export.py -c 1 -s "2026-04-02 11:00:00" -d 30 -o /tmp/clips/
```

:::tip Advanced: Downscaling During Export
If you need the exported clip at a different resolution (e.g., to match a substream for AI processing), replace `-c:v copy` with re-encoding flags:

```bash
ffmpeg -rtsp_transport tcp -stimeout 5000000 \
  -i "rtsp://..." \
  -t 10 -vf scale=1280:720 -r 15 -c:v libx265 -crf 18 -an -y output.mp4
```

This re-encodes the video and is slower, but gives you full control over resolution, frame rate, and codec.
:::

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
