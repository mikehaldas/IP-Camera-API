---
title: "Node-RED IP Camera / AI Security Camera Integration"
sidebar_label: "Node-RED"
description: "Receive AI detection events from Viewtron IP cameras in Node-RED, including License plate recognition (LPR/ALPR), human detection, vehicle detection, face detection, and people counting events. Node-RED recieved real time messages directly from Viewtron AI security cameras to flow with no middleware."
keywords:
  - node-red ip camera
  - node-red security camera
  - node-red lpr
  - node-red license plate
  - node-red alpr
  - node-red anpr
  - node-red camera
  - node-red cctv
  - node-red surveillance
  - node-red viewtron
  - node-red human detection
  - node-red person detection
  - node-red face detection
  - node-red vehicle detection
  - node-red people counting
  - node-red gate access
  - node-red access control
  - node-red ip camera api
  - node-red mqtt camera
  - node-red automation camera
  - node-red industrial camera
  - node-red iot camera
  - ip camera node-red
  - security camera node-red
  - lpr camera node-red
  - camera ai node-red
sidebar_position: 2
---

# Node-RED IP Camera Integration

The **Viewtron AI Camera** node for Node-RED receives AI detection events directly from Viewtron AI security cameras and outputs structured JSON messages. License plate recognition, human detection, vehicle detection, face detection, and people counting — all processed on the camera with no cloud service, no middleware, and no bridge required. The camera posts events directly to your Node-RED flow.

```
Viewtron IP Camera --> HTTP POST (XML) --> Viewtron AI Camera node --> JSON --> Your Flow
```

![Viewtron AI Camera node in Node-RED with live LPR events](https://videos.cctvcamerapros.com/wp-content/files/Node-RED-LPR-camera-integration.jpg)

## Install

Install from the Node-RED palette manager or the command line:

**Palette Manager:** Menu > Manage palette > Install > search `node-red-contrib-viewtron`

**Command line:**

```bash
cd ~/.node-red
npm install node-red-contrib-viewtron
```

**npm:** [node-red-contrib-viewtron](https://www.npmjs.com/package/node-red-contrib-viewtron)

## How It Works

Viewtron AI cameras run all detection on-device and push HTTP POST events when they detect a license plate, person, vehicle, or face. The **Viewtron AI Camera** node creates an HTTP listener on a configurable port. When the camera sends an event, the node parses the XML payload and outputs a structured JSON message to the appropriate output.

No middleware, no bridge, no cloud API — the camera connects directly to the Node-RED node over your local network.

## Outputs

The node has 5 outputs, one per detection category:

| Output | Category | Key Fields |
|--------|----------|------------|
| 1 | **LPR** | `plate_number`, `plate_status` (Authorized / Blacklisted / Temporary / Unknown), `vehicle` (brand, color, type) |
| 2 | **Intrusion** | `target_type` (person, car, motorcycle), `event_id`, `status` |
| 3 | **Face** | `face.age`, `face.sex`, `face.glasses`, `face.mask` |
| 4 | **Counting** | `target_type`, `boundary` |
| 5 | **Other** | Video metadata and unclassified events |

Wire each output to the flow logic you need — separate handling for plates vs. people vs. faces.

### Common Fields

Every event message includes:

| Field | Description |
|-------|-------------|
| `msg.payload.event_type` | Raw alarm type from camera (e.g., `VEHICE`, `PEA`) |
| `msg.payload.category` | Normalized category: `lpr`, `intrusion`, `face`, `counting`, `metadata` |
| `msg.payload.camera_ip` | IP address of the camera that sent the event |
| `msg.payload.timestamp` | Event timestamp from the camera |
| `msg.topic` | Set to `viewtron/{category}` for easy MQTT republishing |

### Images

When **Original picture** and **Target picture** are enabled on the camera, `msg.payload.source_image` (full scene) and `msg.payload.target_image` (cropped detection target) are included as base64 JPEG strings. These payloads can be large (300KB+) — leave the camera image options unchecked if you only need the detection data.

The **Include images** checkbox on the node controls whether images are passed through to the output or stripped.

## What You Can Build

- **Gate and garage access** — read license plates and trigger relay nodes to open gates for authorized vehicles
- **Unknown vehicle alerts** — send Telegram, email, or push notifications when an unrecognized plate is detected
- **Person detection lighting** — trigger smart lighting when a person is detected in a zone
- **Intrusion alarms** — wire to siren or alarm panel nodes when someone enters a restricted area
- **Vehicle counting dashboards** — feed counting data to InfluxDB + Grafana for parking or traffic analytics
- **MQTT republishing** — forward structured events to an MQTT broker for consumption by Home Assistant, AWS IoT, or other subscribers
- **Multi-camera routing** — use Switch nodes to route events by camera IP, detection type, or plate status

## Camera Setup

### 1. Add the Node to Your Flow

Drag the **Viewtron AI Camera** node from the palette onto the canvas and set the listen port (default: 5002).

### 2. Configure HTTP POST on the Camera

Open your camera's web interface and navigate to **Network > Advanced > HTTP Notification**.

![Viewtron camera HTTP POST settings](https://videos.cctvcamerapros.com/wp-content/files/IP-camera-HTTP-Post-Settings.jpg)

Set the **Push Protocol Version** to **V1**, then click **Add** to create a server entry.

:::warning Push Protocol Version
The camera's HTTP POST settings have a **Push Protocol Version** dropdown. You must select **V1**. The V2 protocol sends alarm status events but images don't come through reliably.
:::

### 3. Configure the Server Connection

![HTTP POST server configuration](https://videos.cctvcamerapros.com/wp-content/files/IP-camera-HTTP-Post-Server.jpg)

| Setting | Value |
|---------|-------|
| **Enable** | Checked |
| **Domain/IP** | Your Node-RED machine's IP address |
| **Server Port** | Port configured in the node (default: 5002) |
| **Path** | `/API` |
| **Connection Type** | Persistent connection |
| **Send Heartbeat** | Checked |
| **Heartbeat Interval** | 30 seconds |
| **Smart Alarm Data** | Check **Smart event data** |
| **Original picture** | Optional — include full scene image in events |
| **Target picture** | Optional — include cropped target image in events |
| **Smart Alarm Type** | Select the detection types you want (e.g., License Plate Detection) |

Click **Save**, then deploy your flow in Node-RED. The camera must be rebooted after initial HTTP POST configuration changes.

### Connection Status

The camera maintains a persistent HTTP connection and sends heartbeats to confirm the server is reachable. The node status shows a green dot when listening and updates with the latest event data (e.g., plate number and status).

## Plate Status

The LPR camera maintains an on-device plate database. Each detected plate is matched against the database and assigned a status:

| Status | Meaning |
|--------|---------|
| **Authorized** | Plate is on the camera's allow list |
| **Blacklisted** | Plate is on the camera's block list |
| **Temporary** | Plate is on a temporary list with a valid date range |
| **Unknown** | Plate is not in the database, or a listed plate with an expired date range |

:::note Date Range Validation
Date range validation applies to all list types — not just temporary plates. An allow list or block list plate with an expired end date will also come through as Unknown. The camera validates dates internally and simply omits the `vehicleListType` field when a plate is outside its valid range.
:::

Plates are added to the camera's database through its web interface or via the [Viewtron API](/docs/api-reference/smart-detection/license-plate-recognition-config).

## Example: LPR Gate Access

Import this flow to get started with license plate gate access control. The Viewtron AI Camera node reads plates, and a Switch node routes authorized vehicles to one action and unknown vehicles to another.

```json
[
    {
        "id": "viewtron1",
        "type": "viewtron-camera",
        "name": "Gate Camera",
        "port": "5002",
        "includeImages": false,
        "wires": [["switch1"], [], [], [], []]
    },
    {
        "id": "switch1",
        "type": "switch",
        "name": "Authorized?",
        "property": "payload.plate_status",
        "rules": [
            {"t": "eq", "v": "Authorized"},
            {"t": "eq", "v": "Unknown"}
        ],
        "outputs": 2,
        "wires": [["gate_open"], ["notify"]]
    },
    {
        "id": "gate_open",
        "type": "debug",
        "name": "Open Gate"
    },
    {
        "id": "notify",
        "type": "debug",
        "name": "Alert: Unknown Vehicle"
    }
]
```

Replace the debug nodes with your actual gate control and notification nodes. The `msg.payload.plate_number` field is available in both outputs for logging or display.

## Supported Event Types

### IPC v1.x (Direct from Camera)

| Alarm Type | Category | Detection |
|-----------|----------|-----------|
| `VEHICE` / `VEHICLE` | lpr | License plate recognition |
| `VFD` | face | Face detection |
| `PEA` | intrusion | Perimeter intrusion |
| `AOIENTRY` | zone_entry | Zone entry |
| `AOILEAVE` | zone_exit | Zone exit |
| `LOITER` | loitering | Loitering detection |
| `PASSLINECOUNT` | counting | People/vehicle counting |

### NVR v2.0 (Forwarded via NVR)

| Alarm Type | Category | Detection |
|-----------|----------|-----------|
| `vehicle` | lpr | LPR with vehicle brand, color, type, model |
| `videoFaceDetect` | face | Face with age, sex, glasses, mask attributes |
| `regionIntrusion` | intrusion | Perimeter intrusion |
| `lineCrossing` | line_crossing | Tripwire line crossing |
| `targetCountingByLine` | counting | Counting by line |
| `targetCountingByArea` | counting | Counting by area |

Version detection is automatic — the node handles both IPC and NVR formats transparently.

## Node Settings

| Setting | Default | Description |
|---------|---------|-------------|
| **Port** | 5002 | HTTP listener port for camera events |
| **Include images** | Off | Pass base64 JPEG images through to output (`source_image`, `target_image`) |

## Node-RED vs. Home Assistant

Both integrations receive the same camera events. Choose based on your use case:

| | Node-RED | [Home Assistant](/docs/integrations/home-assistant) |
|---|---------|------|
| **Architecture** | Camera → Node-RED (direct) | Camera → Bridge → MQTT → HA |
| **Best for** | Custom logic, industrial automation, dashboards, multi-system integration | Smart home automations, mobile notifications, device control |
| **Setup** | `npm install`, drag node | Docker container + MQTT broker |
| **Programming** | Visual flow editor | YAML automations or HA UI |
| **MQTT** | Optional (can republish) | Required |

You can run both — point the camera's HTTP POST at Node-RED, then use Node-RED's MQTT output to also feed events into Home Assistant.

## Compatible Cameras

Any [Viewtron IP camera](https://www.cctvcamerapros.com/AI-security-cameras-s/1512.htm) or [NVR](https://www.cctvcamerapros.com/IP-Camera-NVRs-s/1472.htm) with HTTP POST support works with this node. Recommended models:

| Model | Detection Types | Best For |
|-------|----------------|----------|
| [LPR-IP4](https://www.cctvcamerapros.com/LPR-Camera-p/lpr-ip4.htm) | License plate recognition | Driveways, gates, parking entrances |
| [AI security cameras](https://www.cctvcamerapros.com/AI-security-cameras-s/1512.htm) | Human, vehicle, face detection | Perimeter security, access control |
| [NVRs](https://www.cctvcamerapros.com/IP-Camera-NVRs-s/1472.htm) | All types (forwarded from cameras) | Multi-camera systems |

All Viewtron products are NDAA compliant.

## Resources

- **npm:** [node-red-contrib-viewtron](https://www.npmjs.com/package/node-red-contrib-viewtron)
- **GitHub:** [node-red-contrib-viewtron](https://github.com/mikehaldas/node-red-contrib-viewtron) — source code, example flows, issue tracker
- **Python SDK:** [viewtron on PyPI](https://pypi.org/project/viewtron/) — `pip install viewtron` for Python projects
- **Home Assistant:** [viewtron-home-assistant](https://github.com/mikehaldas/viewtron-home-assistant) — MQTT bridge for Home Assistant

## Related Documentation

- [Home Assistant Integration](/docs/integrations/home-assistant) — MQTT-based integration for smart home automations
- [Viewtron Python SDK](/docs/getting-started/python-sdk) — Python SDK for direct camera API access
- [License Plate Recognition](/docs/applications/license-plate-recognition-camera-api) — LPR application guide
- [Human Detection](/docs/applications/human-detection-intrusion-api) — person and vehicle detection events
- [Face Detection](/docs/applications/face-detection-recognition-api) — face detection and recognition
- [HTTP POST Setup](/docs/getting-started/http-post-setup) — camera webhook configuration guide

## Video Guides & Blog Posts

- [LPR Camera API Setup and Demo](https://videos.cctvcamerapros.com/v/lpr-camera-api.html) — video walkthrough of configuring LPR webhooks and viewing live plate reads
- [ANPR / LPR Camera System Overview](https://videos.cctvcamerapros.com/v/lpr-camera-system-anpr.html) — camera installation, plate capture zones, and system design
- [LPR Camera for Home Use](https://videos.cctvcamerapros.com/v/lpr-camera-for-home.html) — residential driveway and garage setup with the LPR-IP4

## Questions & Development Inquiries

- **Email:** mike@viewtron.com
- **Phone:** 561-433-8488
- **Forum:** [IP Camera API Webhooks Setup](https://videos.cctvcamerapros.com/support/topic/ip-camera-api-webbooks)

Mike Haldas is available for questions, consultation, and custom software development for Viewtron API related projects. Email details about your project to mike@viewtron.com.
