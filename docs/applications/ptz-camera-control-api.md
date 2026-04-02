---
title: "PTZ Camera Control API (Pan Tilt Zoom)"
sidebar_label: "PTZ Control"
description: "Control Viewtron PTZ cameras via HTTP API — pan, tilt, zoom, focus, presets, cruise tours, and AI auto-tracking. Send commands from any language to move cameras programmatically."
keywords:
  - ptz camera api
  - pan tilt zoom camera control api
  - auto tracking ptz camera api
  - camera I can control from my phone
sidebar_position: 4
---

# PTZ Camera Control API (Pan Tilt Zoom)

Viewtron PTZ cameras can be controlled programmatically via HTTP API — pan, tilt, zoom, focus, iris, presets, and cruise tours. Unlike the webhook-based detection features, PTZ control uses outbound HTTP requests that you send to the camera. Any programming language or tool that can make HTTP requests (Python, JavaScript, curl, mobile apps) can control PTZ movement in real time.

The API supports continuous movement commands with adjustable speed (1-8), preset positions for instant recall, and cruise tours that cycle through multiple presets automatically. Viewtron PTZ cameras also include AI auto-tracking, which can be combined with the [real-time traject data](/docs/applications/real-time-object-tracking-api) for intelligent tracking applications.

## What You Can Build

- **Remote camera control apps** — build a web or mobile interface to pan, tilt, and zoom cameras from anywhere
- **Automated patrol routes** — program cruise tours that cycle through preset positions on a schedule
- **Event-driven camera positioning** — move the PTZ to a preset position when an alarm triggers on another camera
- **Integration with VMS software** — add PTZ control to custom video management systems
- **Auto-tracking override** — programmatically interrupt or redirect auto-tracking when needed
- **Multi-camera coordination** — move multiple PTZ cameras to coordinated positions simultaneously
- **Tour guide systems** — create scripted camera movements for demonstrations or presentations

## How It Works

1. **Install a PTZ camera** — Viewtron PTZ cameras connect via standard IP networking
2. **Query capabilities** — use `PtzGetCaps` to discover speed range, preset count, and cruise limits
3. **Send movement commands** — POST to `PtzControl` with the desired direction and speed
4. **Use presets** — save positions with `PtzAddPreset` and recall them instantly with `PtzGotoPreset`
5. **Run cruise tours** — configure tours in the camera UI, then start/stop them via API with `PtzRunCruise` and `PtzStopCruise`
6. **Stop movement** — send the `Stop` action to halt any current movement

## PTZ Control Commands

### Movement Actions

All movement commands use the same URL pattern: `POST http://<host>/PtzControl[/channelId]/<action>`

| Action | Description |
|--------|-------------|
| `Up` | Tilt up |
| `Down` | Tilt down |
| `Left` | Pan left |
| `Right` | Pan right |
| `LeftUp` | Pan left and tilt up simultaneously |
| `LeftDown` | Pan left and tilt down simultaneously |
| `RightUp` | Pan right and tilt up simultaneously |
| `RightDown` | Pan right and tilt down simultaneously |
| `ZoomIn` | Zoom in (telephoto) |
| `ZoomOut` | Zoom out (wide angle) |
| `Near` | Focus near |
| `Far` | Focus far |
| `IrisOpen` | Open iris (brighter) |
| `IrisClose` | Close iris (darker) |
| `Stop` | Stop all current movement |

### Preset Commands

| Command | URL | Method | Description |
|---------|-----|--------|-------------|
| PtzGotoPreset | `/PtzGotoPreset[/channelId]` | POST | Move to a saved preset position |
| PtzGetPresets | `/PtzGetPresets[/channelId]` | POST/GET | List all saved presets |
| PtzAddPreset | `/PtzAddPreset[/channelId]` | POST | Save the current position as a preset |
| PtzDeletePreset | `/PtzDeletePreset[/channelId]` | POST | Delete a saved preset |

### Cruise Tour Commands

| Command | URL | Method | Description |
|---------|-----|--------|-------------|
| PtzGetCruises | `/PtzGetCruises[/channelId]` | POST/GET | List configured cruise tours |
| PtzRunCruise | `/PtzRunCruise[/channelId]` | POST | Start a cruise tour |
| PtzStopCruise | `/PtzStopCruise[/channelId]` | POST | Stop the running cruise tour |

## PTZ Capabilities

Use `PtzGetCaps` to query the camera's PTZ limits before sending commands:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="2.0.0" xmlns="http://www.ipc.com/ver10">
  <caps>
    <controlMinSpeed type="uint32">1</controlMinSpeed>
    <controlMaxSpeed type="uint32">8</controlMaxSpeed>
    <presetMaxCount type="uint32">255</presetMaxCount>
    <cruiseMaxCount type="uint32">8</cruiseMaxCount>
    <cruisePresetMinSpeed type="uint32">1</cruisePresetMinSpeed>
    <cruisePresetMaxSpeed type="uint32">8</cruisePresetMaxSpeed>
    <cruisePresetMaxHoldTime type="uint32">240</cruisePresetMaxHoldTime>
    <cruisePresetMaxCount type="uint32">16</cruisePresetMaxCount>
  </caps>
</config>
```

| Field | Description | Typical Value |
|-------|-------------|---------------|
| `controlMinSpeed` / `controlMaxSpeed` | Movement speed range | 1 - 8 |
| `presetMaxCount` | Maximum saved presets | 255 |
| `cruiseMaxCount` | Maximum cruise tours | 8 |
| `cruisePresetMaxCount` | Maximum presets per cruise tour | 16 |
| `cruisePresetMaxHoldTime` | Maximum seconds at each preset | 240 |

## XML Request/Response Examples

### PtzControl — Move Camera

```xml
<!-- POST http://<host>/PtzControl/1/Right -->
<?xml version="1.0" encoding="utf-8"?>
<actionInfo version="1.0" xmlns="http://www.ipc.com/ver10">
  <speed>4</speed>
</actionInfo>
```

### PtzGotoPreset — Go to Preset

```xml
<!-- POST http://<host>/PtzGotoPreset/1 -->
<?xml version="1.0" encoding="utf-8"?>
<presetInfo version="1.0" xmlns="http://www.ipc.com/ver10">
  <id>2</id>
</presetInfo>
```

### PtzAddPreset — Save Current Position

```xml
<!-- POST http://<host>/PtzAddPreset/1 -->
<?xml version="1.0" encoding="utf-8"?>
<presetInfo version="1.0" xmlns="http://www.ipc.com/ver10">
  <name><![CDATA[Front Gate]]></name>
</presetInfo>
```

### PtzGetPresets — List Saved Presets

```xml
<!-- Response from GET http://<host>/PtzGetPresets/1 -->
<?xml version="1.0" encoding="UTF-8"?>
<config version="1.0" xmlns="http://www.ipc.com/ver10">
  <presetInfo type="list" maxCount="360">
    <itemType type="string" maxLen="10"></itemType>
    <item id="1"><![CDATA[Front Gate]]></item>
    <item id="2"><![CDATA[Parking Lot]]></item>
    <item id="3"><![CDATA[Loading Dock]]></item>
  </presetInfo>
</config>
```

## Quick Start Example

This standalone script demonstrates PTZ camera control using Python and the `requests` library with Basic Auth:

```python
#!/usr/bin/env python3
"""PTZ Camera Controller — Viewtron IP Camera API"""

import requests
from requests.auth import HTTPDigestAuth
import xml.etree.ElementTree as ET
import time

# pip install requests

# Camera connection settings
CAMERA_IP = "192.168.1.108"
CAMERA_PORT = 80
USERNAME = "admin"
PASSWORD = "your_password"
CHANNEL = 1

BASE_URL = f"http://{CAMERA_IP}:{CAMERA_PORT}"
AUTH = HTTPDigestAuth(USERNAME, PASSWORD)


def ptz_get_caps():
    """Get PTZ capabilities (speed range, preset count, cruise limits)."""
    url = f"{BASE_URL}/PtzGetCaps/{CHANNEL}"
    resp = requests.get(url, auth=AUTH, timeout=5)
    resp.raise_for_status()
    print("PTZ Capabilities:")
    print(resp.text)
    return resp.text


def ptz_move(action, speed=4, duration=1.0):
    """Move the camera in a direction for a specified duration.

    Actions: Up, Down, Left, Right, LeftUp, LeftDown, RightUp, RightDown,
             ZoomIn, ZoomOut, Near, Far, IrisOpen, IrisClose, Stop
    Speed: 1 (slowest) to 8 (fastest)
    """
    url = f"{BASE_URL}/PtzControl/{CHANNEL}/{action}"
    xml_body = (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<actionInfo version="1.0" xmlns="http://www.ipc.com/ver10">\n'
        f'  <speed>{speed}</speed>\n'
        '</actionInfo>'
    )
    resp = requests.post(url, data=xml_body, auth=AUTH,
                         headers={'Content-Type': 'application/xml'}, timeout=5)
    resp.raise_for_status()
    print(f"Moving: {action} (speed {speed})")

    if action != "Stop" and duration > 0:
        time.sleep(duration)
        ptz_stop()


def ptz_stop():
    """Stop all PTZ movement."""
    url = f"{BASE_URL}/PtzControl/{CHANNEL}/Stop"
    xml_body = (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<actionInfo version="1.0" xmlns="http://www.ipc.com/ver10">\n'
        '  <speed>1</speed>\n'
        '</actionInfo>'
    )
    requests.post(url, data=xml_body, auth=AUTH,
                  headers={'Content-Type': 'application/xml'}, timeout=5)
    print("Stopped.")


def ptz_goto_preset(preset_id):
    """Move the camera to a saved preset position."""
    url = f"{BASE_URL}/PtzGotoPreset/{CHANNEL}"
    xml_body = (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<presetInfo version="1.0" xmlns="http://www.ipc.com/ver10">\n'
        f'  <id>{preset_id}</id>\n'
        '</presetInfo>'
    )
    resp = requests.post(url, data=xml_body, auth=AUTH,
                         headers={'Content-Type': 'application/xml'}, timeout=5)
    resp.raise_for_status()
    print(f"Going to preset {preset_id}")


def ptz_add_preset(name):
    """Save the current camera position as a named preset."""
    url = f"{BASE_URL}/PtzAddPreset/{CHANNEL}"
    xml_body = (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<presetInfo version="1.0" xmlns="http://www.ipc.com/ver10">\n'
        f'  <name><![CDATA[{name}]]></name>\n'
        '</presetInfo>'
    )
    resp = requests.post(url, data=xml_body, auth=AUTH,
                         headers={'Content-Type': 'application/xml'}, timeout=5)
    resp.raise_for_status()
    print(f"Saved preset: {name}")


def ptz_get_presets():
    """List all saved preset positions."""
    url = f"{BASE_URL}/PtzGetPresets/{CHANNEL}"
    resp = requests.get(url, auth=AUTH, timeout=5)
    resp.raise_for_status()
    print("Saved Presets:")

    root = ET.fromstring(resp.text)
    ns = {'ns': 'http://www.ipc.com/ver10'}
    for item in root.findall('.//ns:presetInfo/ns:item', ns):
        preset_id = item.get('id')
        name = item.text or '(unnamed)'
        print(f"  Preset {preset_id}: {name}")
    return resp.text


def ptz_run_cruise(cruise_id):
    """Start a cruise tour."""
    url = f"{BASE_URL}/PtzRunCruise/{CHANNEL}"
    xml_body = (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<cruiseInfo version="1.0" xmlns="http://www.ipc.com/ver10">\n'
        f'  <id>{cruise_id}</id>\n'
        '</cruiseInfo>'
    )
    resp = requests.post(url, data=xml_body, auth=AUTH,
                         headers={'Content-Type': 'application/xml'}, timeout=5)
    resp.raise_for_status()
    print(f"Started cruise tour {cruise_id}")


def ptz_stop_cruise():
    """Stop the running cruise tour."""
    url = f"{BASE_URL}/PtzStopCruise/{CHANNEL}"
    resp = requests.post(url, data=b'', auth=AUTH, timeout=5)
    resp.raise_for_status()
    print("Stopped cruise tour")


if __name__ == '__main__':
    # 1. Check PTZ capabilities
    ptz_get_caps()
    print()

    # 2. List saved presets
    ptz_get_presets()
    print()

    # 3. Pan right for 2 seconds at speed 4, then stop
    ptz_move("Right", speed=4, duration=2.0)
    print()

    # 4. Zoom in for 1 second
    ptz_move("ZoomIn", speed=3, duration=1.0)
    print()

    # 5. Go to preset 1
    ptz_goto_preset(1)
    print()

    # 6. Save current position as a new preset
    # ptz_add_preset("API Test Position")

    # 7. Run cruise tour 1
    # ptz_run_cruise(1)
    # time.sleep(30)
    # ptz_stop_cruise()
```

**To run:**

```bash
pip install requests
python3 ptz_controller.py
```

Update the `CAMERA_IP`, `USERNAME`, and `PASSWORD` variables with your camera's credentials.

## Relevant API Endpoints

| Endpoint | Purpose | Reference |
|----------|---------|-----------|
| PtzGetCaps | Query speed range, preset count, cruise limits | [PTZ Commands](/docs/api-reference/ptz/ptz-control-movement) |
| PtzControl | Move camera (pan, tilt, zoom, focus, iris, stop) | [PTZ Commands](/docs/api-reference/ptz/ptz-control-movement) |
| PtzGotoPreset | Move to a saved preset position | [PTZ Presets](/docs/api-reference/ptz/ptz-presets) |
| PtzGetPresets | List all saved presets | [PTZ Presets](/docs/api-reference/ptz/ptz-presets) |
| PtzAddPreset | Save current position as a named preset | [PTZ Presets](/docs/api-reference/ptz/ptz-presets) |
| PtzDeletePreset | Delete a saved preset | [PTZ Presets](/docs/api-reference/ptz/ptz-presets) |
| PtzGetCruises | List configured cruise tours | [PTZ Cruise Tours](/docs/api-reference/ptz/ptz-cruise-tours) |
| PtzRunCruise | Start a cruise tour | [PTZ Cruise Tours](/docs/api-reference/ptz/ptz-cruise-tours) |
| PtzStopCruise | Stop the running cruise tour | [PTZ Cruise Tours](/docs/api-reference/ptz/ptz-cruise-tours) |

:::tip Auto-Tracking PTZ
Viewtron PTZ cameras include AI auto-tracking that automatically follows detected targets. When auto-tracking is active, the camera moves to keep the target centered in the frame. You can combine PTZ API control with [real-time traject data](/docs/applications/real-time-object-tracking-api) to build intelligent tracking applications that coordinate multiple cameras or override tracking behavior programmatically.
:::

## Related Applications

- [Real-Time Object Tracking](/docs/applications/real-time-object-tracking-api) — continuous target position data for auto-tracking coordination
- [Human Detection & Intrusion Detection](/docs/applications/human-detection-intrusion-api) — trigger PTZ presets when intrusion is detected
- [License Plate Recognition](/docs/applications/license-plate-recognition-camera-api) — combine PTZ positioning with LPR for gate monitoring
- [Video Snapshots & Recording](/docs/applications/video-snapshots-recording-search-api) — capture snapshots at preset positions

## Related Products

- [Viewtron PTZ Security Cameras](https://www.cctvcamerapros.com/PTZ-Security-Cameras-s/45.htm) — PTZ cameras with HTTP API control and AI auto-tracking
- [Viewtron IP Camera NVRs](https://www.cctvcamerapros.com/IP-Camera-NVRs-s/1472.htm) — NVRs with PTZ pass-through control

## Questions & Development Inquiries

- **Email:** mike@viewtron.com
- **Phone:** 561-433-8488
- **Forum:** [NVR Webhook Setup Guide](https://videos.cctvcamerapros.com/support/topic/setup-nvr-api-webhooks)

Mike Haldas is available for questions, consultation, and custom software development for Viewtron API related projects. Email details about your project to mike@viewtron.com.
