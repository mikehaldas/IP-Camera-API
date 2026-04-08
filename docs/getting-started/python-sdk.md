---
title: "Viewtron Python SDK"
sidebar_label: "Python SDK"
description: "Python SDK for Viewtron IP cameras. Parse inbound AI detection events (LPR, face, intrusion) and control cameras programmatically. Install with pip install viewtron."
keywords:
  - viewtron python sdk
  - ip camera python library
  - ip camera python sdk
  - security camera python api
  - camera api python
  - lpr python library
  - license plate recognition python
  - face detection python sdk
  - ip camera sdk
  - viewtron sdk
  - pip install viewtron
sidebar_position: 6
---

# Viewtron Python SDK

The Viewtron Python SDK (`pip install viewtron`) is the recommended way to work with the Viewtron IP Camera API. It handles two things:

1. **Inbound events** — parse XML alarm events from cameras into Python objects (LPR, face detection, intrusion, counting)
2. **Outbound API** — control cameras and manage plate databases programmatically

The SDK handles all XML formatting, API version differences (IPC v1.x vs NVR v2.0), and authentication automatically.

## Install

```bash
pip install viewtron
```

Requires Python 3.7+. Dependencies: `requests`, `xmltodict`.

Source code: [github.com/mikehaldas/viewtron-python-sdk](https://github.com/mikehaldas/viewtron-python-sdk)

## Inbound Events — Parse Camera Alarm Data

Viewtron cameras send AI detection events as HTTP POST requests with XML payloads. The SDK parses these into Python objects with typed accessors for every field.

### Quick Example

```python
from viewtron import LPR, VehicleLPR

# In your HTTP POST handler, pass the raw request body:
event = LPR(request_body)

print(event.get_plate_number())       # "ABC1234"
print(event.is_plate_authorized())    # True
print(event.get_vehicle_list_type())  # "whiteList"

# Images are included as base64 JPEG
if event.source_image_exists():
    overview = event.get_source_image()    # full scene image
if event.target_image_exists():
    plate_crop = event.get_target_image()  # plate closeup
```

### Event Classes

The SDK provides separate classes for each detection type and API version. Version detection is automatic — IPC v1.x and NVR v2.0 use different XML structures, but the classes share common methods.

#### IPC v1.x (Direct from Camera)

| Class | smartType | Detection | Application Guide |
|-------|-----------|-----------|-------------------|
| `LPR` | `VEHICE` | License plate recognition with whitelist/blacklist | [LPR](/docs/applications/license-plate-recognition-camera-api) |
| `FaceDetection` | `FACE` | Face detection with crop image | [Face Detection](/docs/applications/face-detection-recognition-api) |
| `IntrusionDetection` | `PEA` | Perimeter intrusion (person/vehicle/motorcycle) | [Human Detection](/docs/applications/human-detection-intrusion-api) |
| `IntrusionEntry` | `AVD` | Zone entry detection | [Perimeter Security](/docs/applications/perimeter-security-line-crossing-api) |
| `IntrusionExit` | `AVD` | Zone exit detection | [Perimeter Security](/docs/applications/perimeter-security-line-crossing-api) |
| `LoiteringDetection` | `LOITERING` | Loitering in a zone | [Loitering](/docs/applications/loitering-detection-api) |
| `IllegalParking` | `PVD` | Parking violation | [Vehicle/Parking](/docs/applications/vehicle-detection-parking-management-api) |
| `VideoMetadata` | `VIDEO_METADATA` | Continuous object detection | [Real-Time Tracking](/docs/applications/real-time-object-tracking-api) |

#### NVR v2.0 (Forwarded via NVR)

| Class | smartType | Detection | Application Guide |
|-------|-----------|-----------|-------------------|
| `VehicleLPR` | `vehicle` | LPR with vehicle brand, color, type, model | [LPR](/docs/applications/license-plate-recognition-camera-api) |
| `FaceDetectionV2` | `faceDetection` | Face detection with age, sex, glasses, mask | [Face Detection](/docs/applications/face-detection-recognition-api) |
| `RegionIntrusion` | `regionIntrusion` | Perimeter intrusion | [Human Detection](/docs/applications/human-detection-intrusion-api) |
| `LineCrossing` | `lineCrossing` | Tripwire line crossing | [Perimeter Security](/docs/applications/perimeter-security-line-crossing-api) |
| `TargetCountingByLine` | `targetCountingByLine` | People/vehicle counting by line | [People Counting](/docs/applications/people-counting-traffic-analytics-api) |
| `TargetCountingByArea` | `targetCountingByArea` | People/vehicle counting by area | [People Counting](/docs/applications/people-counting-traffic-analytics-api) |
| `VideoMetadataV2` | `videoMetadata` | Continuous object detection | [Real-Time Tracking](/docs/applications/real-time-object-tracking-api) |

### Common Methods

All event classes share these methods:

| Method | Returns | Description |
|--------|---------|-------------|
| `get_ip_cam()` | `str` | Camera IP address or device name |
| `get_alarm_type()` | `str` | Detection type identifier (e.g., `PEA`, `VEHICE`) |
| `get_alarm_description()` | `str` | Human-readable description |
| `get_time_stamp()` | `str` | Raw timestamp from event |
| `get_time_stamp_formatted()` | `str` | Formatted date/time string |
| `source_image_exists()` | `bool` | Whether a full-frame image is included |
| `get_source_image()` | `str` | Base64 JPEG of the full scene |
| `target_image_exists()` | `bool` | Whether a target crop image is included |
| `get_target_image()` | `str` | Base64 JPEG of the detected target |

### Version Routing

Your HTTP server receives events from both IPC and NVR sources. Route to the correct class based on the XML version:

```python
import xmltodict
from viewtron import (
    LPR, VehicleLPR,
    IntrusionDetection, RegionIntrusion,
    FaceDetection, FaceDetectionV2,
)

def handle_post(body):
    data = xmltodict.parse(body)
    config = data.get('config', {})
    version = config.get('@version', '')

    if version.startswith('2'):
        # NVR v2.0 format
        smart_type = str(config.get('smartType', ''))
        if smart_type == 'vehicle':
            event = VehicleLPR(body)
        elif smart_type == 'regionIntrusion':
            event = RegionIntrusion(body)
        elif smart_type == 'faceDetection':
            event = FaceDetectionV2(body)
    else:
        # IPC v1.x format
        st = config.get('smartType', {})
        alarm = (st.get('#text') or str(st)).strip() if isinstance(st, dict) else str(st).strip()
        if alarm == 'VEHICE':
            event = LPR(body)
        elif alarm == 'PEA':
            event = IntrusionDetection(body)
        elif alarm == 'FACE':
            event = FaceDetection(body)
```

See each [application guide](/docs/category/applications) for complete working examples with image saving and CSV logging.

## Outbound API — Control the Camera

The `ViewtronCamera` class sends commands to cameras using Basic HTTP authentication.

### Quick Example

```python
from viewtron import ViewtronCamera

camera = ViewtronCamera("192.168.0.20", "admin", "password")

# Device info
info = camera.get_device_info()
print(info["model"])  # "LPR-IP4"

# Manage the license plate database
camera.add_plate("ABC1234", owner="Mike", list_type="whiteList")
plates = camera.get_plates()
camera.modify_plate("ABC1234", owner="Mike H.", telephone="555-1234")
camera.delete_plate("ABC1234")
```

Or use as a context manager:

```python
with ViewtronCamera("192.168.0.20", "admin", "password") as cam:
    plates = cam.get_plates()
    for plate in plates:
        print(plate)
```

### Camera Client Methods

| Method | Description |
|--------|-------------|
| `get_device_info()` | Get camera model, firmware version, device name |
| `add_plate(plate, owner, list_type, group_id)` | Add a plate to the camera database |
| `get_plates(group_id, max_results, offset)` | Query plates with pagination |
| `modify_plate(plate, owner, telephone, group_id)` | Update plate details |
| `delete_plate(plate, group_id)` | Remove a plate from the database |

See the [LPR Config API reference](/docs/api-reference/smart-detection/license-plate-recognition-config) for the underlying XML endpoints.

## Projects Built with This SDK

| Project | Description |
|---------|-------------|
| [Viewtron Home Assistant Integration](/docs/integrations/home-assistant) | Camera AI events as native HA sensors via MQTT auto-discovery |
| [IP Camera API Server](https://github.com/mikehaldas/IP-Camera-API) | Alarm server with CSV logging and image saving |
| [ESP8266 Relay Controller](/docs/applications/relay-control-iot-automation-api) | IoT relay triggered by camera detection events |

## Related Documentation

- [Authentication](/docs/getting-started/authentication) — Basic auth for all API requests
- [HTTP POST Setup](/docs/getting-started/http-post-setup) — configure cameras to send webhook events
- [API Versions](/docs/getting-started/api-versions) — IPC v1.x vs NVR v2.0 format differences
- [Webhook Event Formats](/docs/api-reference/events/ipc-event-format) — raw XML event structure reference
- [Home Assistant Integration](/docs/integrations/home-assistant) — connect cameras to Home Assistant

## Supported Cameras

The SDK works with any [Viewtron AI security camera](https://www.cctvcamerapros.com/AI-security-cameras-s/1512.htm) or [NVR](https://www.cctvcamerapros.com/IP-Camera-NVRs-s/1472.htm) that supports HTTP POST webhooks. For license plate recognition, use the [Viewtron LPR cameras](https://www.cctvcamerapros.com/License-Plate-Recognition-Systems-s/1518.htm). All Viewtron products are NDAA compliant.

## Video Guides

- [LPR Camera API Setup and Demo](https://videos.cctvcamerapros.com/v/lpr-camera-api.html) — video walkthrough of configuring webhooks and receiving events with the SDK
- [AI Security Camera System Overview](https://videos.cctvcamerapros.com/v/ai-security-camera-system.html) — human detection, vehicle detection, and AI event types

## Questions & Development Inquiries

- **Email:** mike@viewtron.com
- **Phone:** 561-433-8488
- **PyPI:** [pypi.org/project/viewtron](https://pypi.org/project/viewtron/)
- **GitHub:** [github.com/mikehaldas/viewtron-python-sdk](https://github.com/mikehaldas/viewtron-python-sdk)

Mike Haldas is available for questions, consultation, and custom software development for Viewtron API related projects. Email details about your project to mike@viewtron.com.
