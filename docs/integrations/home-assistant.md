---
title: "Home Assistant Security Camera Integration"
sidebar_label: "Home Assistant"
description: "Integrate Viewtron AI security cameras with Home Assistant via MQTT. License plate recognition, person detection, face detection, and vehicle detection as native HA sensors — no cloud, no Frigate, no Coral TPU required."
keywords:
  - home assistant camera integration
  - home assistant security camera
  - home assistant lpr
  - home assistant license plate
  - home assistant ai camera
  - home assistant camera motion detection
  - home assistant person detection camera
  - home assistant onvif
  - home assistant ptz
  - home assistant ptz camera
  - home assistant cctv
  - home assistant ip cam
  - home assistant compatible cameras
  - home assistant camera
  - home assistant doorbell camera
  - security camera home assistant
  - best security camera for home assistant
  - cameras that work with home assistant
  - home assistant camera compatible
  - home assistant video camera
  - home assistant security camera system
  - home assistant outdoor camera
  - home assistant indoor camera
  - best poe cameras for home assistant
  - best camera for home assistant
  - mqtt camera home assistant
  - ip camera home assistant
  - poe cameras that work with home assistant
sidebar_position: 1
---

# Home Assistant Security Camera Integration

Viewtron AI security cameras integrate with Home Assistant via MQTT auto-discovery. The camera runs all AI processing on-device — license plate recognition, human detection, vehicle detection, and face detection — then sends events to a lightweight bridge that publishes them as native Home Assistant sensors. No Frigate, no Coral TPU, no cloud API, no subscription.

```
Viewtron IP Camera → HTTP POST (XML) → Viewtron Bridge → MQTT → Home Assistant
```

The bridge is built on the [Viewtron Python SDK](/docs/getting-started/python-sdk) and handles both IPC (v1.x) and NVR (v2.0) event formats automatically.

## What Home Assistant Receives

![Viewtron LPR camera in Home Assistant](https://videos.cctvcamerapros.com/wp-content/files/home-assistant-LPR-camera.jpg)

When a license plate is detected, two sensors appear on the Viewtron device in Home Assistant:

| Sensor | What It Shows | Example |
|--------|---------------|---------|
| **License Plate** | The plate number that was read | `ABC1234` |
| **Plate Status** | Whether the plate is in the camera's database | `Authorized` |

The **Plate Status** sensor has four possible values:

| Status | Meaning |
|--------|---------|
| **Authorized** | Plate is on the camera's allow list |
| **Blacklisted** | Plate is on the camera's block list |
| **Temporary** | Plate is on the temporary list and within its valid date range |
| **Unknown** | Plate is not in the camera's database, or a listed plate with an expired date range |

:::note Date Range Validation
Date range validation applies to all list types — not just temporary plates. An allow list or block list plate with an expired end date will also come through as Unknown. The camera validates dates internally and simply omits the `vehicleListType` field when a plate is outside its valid range.
:::

## Supported Detection Types

| Detection | HA Entity | Status |
|-----------|-----------|--------|
| **[License Plate Recognition (LPR)](/docs/applications/license-plate-recognition-camera-api)** | `sensor.viewtron_*_plate` + `sensor.viewtron_*_plate_status` | Tested and supported |
| **[Human / Vehicle Detection](/docs/applications/human-detection-intrusion-api)** | `binary_sensor.viewtron_*_intrusion` | Coming soon |
| **[Face Detection](/docs/applications/face-detection-recognition-api)** | `binary_sensor.viewtron_*_face` | Coming soon |
| **[Object Counting](/docs/applications/people-counting-traffic-analytics-api)** | `sensor.viewtron_*_counting` | Coming soon |

All detection types use the same bridge architecture. Entities auto-discover via MQTT — no manual YAML configuration in Home Assistant.

## What You Can Automate

- **Gate and garage access** — open gates and garage doors when an authorized license plate is recognized
- **Unknown vehicle alerts** — send a phone notification with the plate number when an unrecognized vehicle arrives
- **Person detection lighting** — turn on driveway or porch lights when a person is detected at night
- **Intrusion alarms** — trigger sirens or alarm panels when someone enters a restricted zone after hours
- **Face-based access control** — unlock doors when a recognized face is detected
- **Vehicle counting** — track how many vehicles enter and exit a parking area throughout the day
- **PTZ camera presets** — move a [PTZ camera](/docs/applications/ptz-camera-control-api) to a preset position when an event triggers

## Installation

### Docker (Recommended)

```bash
docker run -d --name viewtron-bridge --restart unless-stopped \
  --network host \
  -e BRIDGE_PORT=5002 \
  -e MQTT_BROKER=localhost \
  ghcr.io/mikehaldas/viewtron-bridge
```

| Variable | Default | Description |
|----------|---------|-------------|
| `BRIDGE_PORT` | `5002` | Port the bridge listens on for camera HTTP POST events |
| `MQTT_BROKER` | `localhost` | MQTT broker hostname or IP |
| `MQTT_PORT` | `1883` | MQTT broker port |
| `MQTT_USERNAME` | *(empty)* | MQTT username (if broker requires auth) |
| `MQTT_PASSWORD` | *(empty)* | MQTT password |
| `SAVE_IMAGES` | `false` | Save event images to disk |

### Manual Install

```bash
git clone https://github.com/mikehaldas/viewtron-home-assistant.git
cd viewtron-home-assistant
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp config.yaml.example config.yaml
# Edit config.yaml with your MQTT broker address
python3 viewtron_bridge.py
```

For boot persistence, create a systemd service — see the [full setup guide](https://github.com/mikehaldas/viewtron-home-assistant#option-b-manual-install) on GitHub.

### MQTT Broker

The bridge requires an MQTT broker. Most Home Assistant users already have Mosquitto running.

**Home Assistant OS:** Settings > Add-ons > Add-on Store > search "Mosquitto broker" > Install > Start.

**Docker / Linux:** Run Mosquitto in Docker:

```bash
docker run -d --name mosquitto --restart unless-stopped \
  -p 1883:1883 eclipse-mosquitto:2 \
  sh -c 'echo -e "listener 1883\nallow_anonymous true" > /mosquitto/config/mosquitto.conf && exec mosquitto -c /mosquitto/config/mosquitto.conf'
```

Then add the MQTT integration in Home Assistant: Settings > Devices & Services > Add Integration > MQTT.

## Camera Setup

### 1. Configure AI Detection

Enable the detection type you want on your camera. For LPR cameras, enable License Plate Detection and draw the detection zone. For AI cameras, configure intrusion zones with person/vehicle filters.

See the [application guides](/docs/category/applications) for detection-specific setup instructions, or the [HTTP POST Setup guide](/docs/getting-started/http-post-setup) for webhook configuration.

### 2. Point HTTP POST at the Bridge

In the camera's web interface, go to **Network > HTTP POST > Edit > Add**:

- **Server IP:** the machine running the Viewtron bridge
- **Port:** `5002` (or your configured `BRIDGE_PORT`)
- **Path:** `/API`

Select the detection types you want forwarded to Home Assistant and click Save.

### 3. Verify in Home Assistant

The first time a camera sends an event, a **Viewtron** device appears automatically in Home Assistant under **Settings > Devices & Services > MQTT**. No restart required.

## Example Automations

**Open garage door for authorized plates:**

```yaml
- alias: "Open garage for authorized plates"
  trigger:
    - platform: state
      entity_id: sensor.viewtron_ipc_plate_status
      to: "Authorized"
  action:
    - service: cover.open_cover
      target:
        entity_id: cover.garage_door
```

**Send phone notification for unknown vehicles:**

```yaml
- alias: "Alert on unknown vehicle"
  trigger:
    - platform: state
      entity_id: sensor.viewtron_ipc_plate_status
      to: "Unknown"
  action:
    - service: notify.mobile_app_phone
      data:
        title: "Unknown vehicle detected"
        message: "Plate {{ states('sensor.viewtron_ipc_plate') }} detected"
```

**Turn on lights when person detected at night:**

```yaml
- alias: "Driveway lights on person detection"
  trigger:
    - platform: state
      entity_id: binary_sensor.viewtron_ipc_intrusion
      to: "on"
  condition:
    - condition: sun
      after: sunset
  action:
    - service: light.turn_on
      target:
        entity_id: light.driveway
```

## How the Bridge Works

The Viewtron bridge is built on the [Viewtron Python SDK](/docs/getting-started/python-sdk) (`pip install viewtron`). The SDK parses the camera's XML events into Python objects, and the bridge translates those into MQTT messages with Home Assistant auto-discovery payloads.

1. Camera detects an event (plate read, person, face) and sends an HTTP POST with XML data
2. Bridge receives the XML and parses it using the `viewtron` SDK — version detection is automatic
3. Bridge publishes the event to MQTT with HA discovery config
4. Home Assistant creates/updates sensors automatically
5. Your automations trigger based on sensor state changes

The bridge handles both **IPC direct (v1.x)** and **NVR forwarded (v2.0)** event formats. You can connect cameras directly to the bridge, or have an NVR forward events from all connected cameras.

## Viewtron vs. ONVIF in Home Assistant

Home Assistant's built-in [ONVIF integration](https://www.home-assistant.io/integrations/onvif/) provides video streaming and basic motion detection. Viewtron cameras support ONVIF for video streams, but the Viewtron integration goes further:

| Capability | ONVIF | Viewtron Integration |
|-----------|-------|---------------------|
| Live video stream | Yes | Use ONVIF for video |
| Basic motion detection | Yes | Yes |
| License plate recognition | No | Yes — plate number, authorization status, plate image |
| Human vs. vehicle classification | No | Yes — AI classifies person, car, motorcycle |
| Face detection | No | Yes — with attributes (age, sex, glasses, mask on NVR) |
| Vehicle attributes | No | Yes — brand, color, type, model (NVR v2.0) |
| Object counting | No | Yes — entrance/exit counts by line or area |
| Plate database management | No | Yes — via [Python SDK](/docs/getting-started/python-sdk) |

Use both: ONVIF for video streaming in your HA dashboard, and the Viewtron integration for AI detection events and automations.

## Managing the Plate Database

The LPR camera maintains an on-camera plate database with allow list, block list, and temporary entries. You can manage plates through:

1. **Camera web interface** — add plates manually or bulk import from CSV
2. **Viewtron Python SDK** — manage plates programmatically:

```python
from viewtron import ViewtronCamera

camera = ViewtronCamera("192.168.0.20", "admin", "password")

# Add an authorized plate
camera.add_plate("ABC1234", owner="Mike", list_type="whiteList")

# Query the database
plates = camera.get_plates()

# Remove a plate
camera.delete_plate("ABC1234")
```

See the [LPR Config API reference](/docs/api-reference/smart-detection/license-plate-recognition-config) for the full plate database API.

## Compatible Cameras

Any [Viewtron IP camera](https://www.cctvcamerapros.com/AI-security-cameras-s/1512.htm) or [NVR](https://www.cctvcamerapros.com/IP-Camera-NVRs-s/1472.htm) with HTTP POST support works with this integration. Recommended models:

| Model | Detection Types | Best For |
|-------|----------------|----------|
| [LPR-IP4](https://www.cctvcamerapros.com/LPR-Camera-p/lpr-ip4.htm) | License plate recognition | Driveways, gates, parking entrances |
| [AI security cameras](https://www.cctvcamerapros.com/AI-security-cameras-s/1512.htm) | Human, vehicle, face detection | Perimeter security, access control |
| [NVRs](https://www.cctvcamerapros.com/IP-Camera-NVRs-s/1472.htm) | All types (forwarded from cameras) | Multi-camera systems |

All Viewtron products are NDAA compliant.

## Resources

- **GitHub:** [viewtron-home-assistant](https://github.com/mikehaldas/viewtron-home-assistant) — bridge source code, Docker image, example automations
- **Python SDK:** [viewtron on PyPI](https://pypi.org/project/viewtron/) — `pip install viewtron`
- **Docker Image:** `ghcr.io/mikehaldas/viewtron-bridge`

## Related Documentation

- [Viewtron Python SDK](/docs/getting-started/python-sdk) — the SDK that powers this integration
- [License Plate Recognition](/docs/applications/license-plate-recognition-camera-api) — LPR application guide with webhook format details
- [Human Detection](/docs/applications/human-detection-intrusion-api) — person and vehicle detection events
- [Face Detection](/docs/applications/face-detection-recognition-api) — face detection and recognition
- [Webhook Event Notification](/docs/applications/webhook-event-notification-api) — complete webhook setup reference
- [HTTP POST Setup](/docs/getting-started/http-post-setup) — camera webhook configuration

## Video Guides & Blog Posts

- [LPR Camera API Setup and Demo](https://videos.cctvcamerapros.com/v/lpr-camera-api.html) — video walkthrough of configuring LPR webhooks and viewing live plate reads
- [ANPR / LPR Camera System Overview](https://videos.cctvcamerapros.com/v/lpr-camera-system-anpr.html) — camera installation, plate capture zones, and system design
- [LPR Camera for Home Use](https://videos.cctvcamerapros.com/v/lpr-camera-for-home.html) — residential driveway and garage setup with the LPR-IP4
- [LPR Camera Installation Best Practices](https://videos.cctvcamerapros.com/v/anpr-lpr-camera-installation.html) — mounting angles, distances, and IR illumination for reliable plate capture

## Questions & Development Inquiries

- **Email:** mike@viewtron.com
- **Phone:** 561-433-8488
- **Forum:** [NVR Webhook Setup Guide](https://videos.cctvcamerapros.com/support/topic/setup-nvr-api-webhooks)

Mike Haldas is available for questions, consultation, and custom software development for Viewtron API related projects. Email details about your project to mike@viewtron.com.
