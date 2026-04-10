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

The Viewtron Python SDK (`pip install viewtron`) is the recommended way to work with the Viewtron IP Camera API. It handles three things:

1. **Event server** — built-in HTTP server that receives camera webhook events, handles persistent connections and keepalives
2. **Event parsing** — automatically detects IPC v1.x vs NVR v2.0 format and returns typed Python objects
3. **Camera control** — send commands to cameras and manage plate databases programmatically

The SDK handles all XML formatting, API version differences, HTTP connection management, and authentication automatically.

## Install

```bash
pip install viewtron
```

Requires Python 3.8+. Dependencies: `requests`, `xmltodict`.

Source code: [github.com/mikehaldas/viewtron-python-sdk](https://github.com/mikehaldas/viewtron-python-sdk) | Full API reference: [Python SDK Reference](/docs/category/python-sdk-reference)

## Receiving Events — ViewtronServer

The `ViewtronServer` class is a complete HTTP server that receives webhook events from Viewtron cameras. It handles HTTP/1.1 persistent connections, keepalive messages, multi-threaded request handling, and XML response — you just write the callback.

```python
from viewtron import ViewtronServer

def on_event(event, client_ip):
    print(f"[{event.category}] from {client_ip}")

    if event.category == "lpr":
        print(f"  Plate: {event.get_plate_number()}")
        print(f"  Group: {event.get_plate_group()}")

    # Save images
    overview = event.get_source_image_bytes()   # decoded JPEG bytes
    if overview:
        with open("overview.jpg", "wb") as f:
            f.write(overview)

server = ViewtronServer(port=5002, on_event=on_event)
server.serve_forever()
```

Point your camera's HTTP POST at `<your-server-ip>:5002` and events start flowing. No XML parsing, no base64 decoding, no keepalive handling — the SDK does it all.

### Server Options

| Parameter | Default | Description |
|-----------|---------|-------------|
| `port` | `5002` | HTTP listener port |
| `on_event` | required | Callback for alarm events — receives `(event, client_ip)` |
| `on_traject` | `None` | Callback for real-time tracking data — receives `(traject, client_ip)` |

### ViewtronEvent — Parse Any Event

If you're building your own HTTP server or processing saved XML, use `ViewtronEvent` directly:

```python
from viewtron import ViewtronEvent

event = ViewtronEvent(xml_body)
if event is None:
    return  # keepalive, alarm status, or unrecognized

print(event.category)                 # "lpr", "intrusion", "face", "counting", "metadata"
print(event.get_plate_number())       # "ABC1234"
print(event.get_plate_group())        # "whiteList" (IPC) or NVR group name

# Images as decoded JPEG bytes — ready for saving, MQTT, notifications
overview = event.get_source_image_bytes()    # full scene
plate_crop = event.get_target_image_bytes()  # plate closeup
```

`ViewtronEvent` automatically detects the API version (IPC v1.x vs NVR v2.0), identifies the event type from the `smartType` field, and returns the correct typed object. Returns `None` for keepalives, alarm status messages, and unrecognized event types.

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
| `category` | `str` | Event category: `"lpr"`, `"intrusion"`, `"face"`, `"counting"`, `"metadata"` |
| `get_ip_cam()` | `str` | Camera IP address or device name |
| `get_alarm_type()` | `str` | Raw detection type from camera (e.g., `VEHICE`, `PEA`, `vehicle`) |
| `get_alarm_description()` | `str` | Human-readable description |
| `get_time_stamp_formatted()` | `str` | Formatted date/time string |
| `source_image_exists()` | `bool` | Whether a full-frame image is included |
| `get_source_image_bytes()` | `bytes` | Decoded JPEG of the full scene (ready to save or send) |
| `target_image_exists()` | `bool` | Whether a target crop image is included |
| `get_target_image_bytes()` | `bytes` | Decoded JPEG of the detected target |
| `get_source_image()` | `str` | Base64-encoded full scene (use `_bytes()` for most cases) |
| `get_target_image()` | `str` | Base64-encoded target crop |

### LPR-Specific Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `get_plate_number()` | `str` | Detected plate text |
| `get_plate_group()` | `str` | Plate database group: `"whiteList"`, `"blackList"`, `"temporaryList"` (IPC), or user-defined group name (NVR). Empty string if plate is not in the database. |
| `get_car_brand()` | `str` | Vehicle brand (NVR v2.0 only) |
| `get_car_model()` | `str` | Vehicle model (NVR v2.0 only) |
| `get_car_type()` | `str` | Vehicle type: sedan, suv, mpv, etc. (NVR v2.0 only) |
| `get_car_color()` | `str` | Vehicle color (NVR v2.0 only) |

### Face Detection Methods (NVR v2.0)

| Method | Returns | Description |
|--------|---------|-------------|
| `get_face_age()` | `str` | Age range: young, youth, middleAged, elderly, unknown |
| `get_face_sex()` | `str` | male, female, unknown |
| `get_face_glasses()` | `str` | yes, no, unknown |
| `get_face_mask()` | `str` | yes, no, unknown |

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
camera.add_plate("ABC1234")
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
| `add_plate(plate_number, group_id="1")` | Add a plate to the camera database |
| `add_plates(plate_numbers, group_id="1")` | Add multiple plates in one request |
| `get_plates(max_results=50, offset=1, group_id="1")` | Query plates with pagination (offset is 1-based) |
| `modify_plate(plate_number, group_id="1", owner=None, telephone=None)` | Update plate details |
| `delete_plate(plate_number, group_id="1")` | Remove a plate from the database |

See the [LPR Config API reference](/docs/api-reference/smart-detection/license-plate-recognition-config) for the underlying XML endpoints.

## Projects Built with This SDK

| Project | Description |
|---------|-------------|
| [Viewtron Home Assistant Integration](/docs/integrations/home-assistant) | Camera AI events as native HA sensors and images via MQTT auto-discovery |
| [IP Camera API Server](https://github.com/mikehaldas/IP-Camera-API) | Alarm server with CSV logging and image saving — uses `ViewtronServer` |
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
