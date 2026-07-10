---
title: "Viewtron Node.js SDK"
sidebar_label: "Node.js SDK"
description: "Node.js SDK for Viewtron IP cameras. Receive and parse inbound AI detection events (LPR, face, intrusion) using the EventEmitter pattern. Install with npm install viewtron-sdk."
keywords:
  - viewtron node.js sdk
  - ip camera node.js library
  - ip camera nodejs sdk
  - security camera node api
  - camera api node.js
  - lpr node.js library
  - license plate recognition node.js
  - face detection node.js sdk
  - ip camera sdk
  - viewtron sdk
  - npm install viewtron-sdk
sidebar_position: 7
---

# Viewtron Node.js SDK

The Viewtron Node.js SDK (`npm install viewtron-sdk`) is the recommended way to receive AI detection events from Viewtron cameras and NVRs in a Node.js application. It provides one main component:

- **ViewtronServer** — an HTTP server, built on the Node.js `EventEmitter` pattern, that receives camera webhook events, handles persistent connections and keepalives, and parses each payload into a typed event object.

Both IPC (IP camera, v1.x API) and NVR (network video recorder, v2.0 API) formats are handled transparently — your code receives the same `event.category` values regardless of which device sent the event. The SDK handles all XML parsing, API version differences, HTTP connection management, and keepalive responses automatically.

The Node.js SDK is **receive-only**. For outbound camera control (device info, plate database CRUD), use the [Python SDK](/docs/getting-started/python-sdk).

## Install

```bash
npm install viewtron-sdk
```

Requires Node.js 18.0.0+. Installs one dependency: `fast-xml-parser`.

Source code: [github.com/mikehaldas/viewtron-nodejs-sdk](https://github.com/mikehaldas/viewtron-nodejs-sdk) | Full API reference: [Node.js SDK Reference](/docs/category/nodejs-sdk-reference)

## Receiving Events — ViewtronServer

`ViewtronServer` is a complete HTTP server that receives webhook events from Viewtron cameras. It handles HTTP/1.1 persistent connections, keepalive messages, and XML responses — you just listen for the `'event'` events.

```javascript
const { ViewtronServer } = require('viewtron-sdk');

const server = new ViewtronServer({ port: 5050 });

server.on('event', (event, clientIP) => {
  console.log(`[${event.category}] from ${clientIP}`);

  if (event.category === 'lpr') {
    console.log(`  Plate: ${event.plateNumber}`);
    console.log(`  Group: ${event.plateGroup}`);
  }

  // Save the full-scene image
  if (event.sourceImage) {
    require('fs').writeFileSync('overview.jpg', event.sourceImageBytes);
  }
});

server.start().then(({ port, ip }) => {
  console.log(`Listening on ${ip}:${port}`);
});
```

Point your camera's HTTP POST at `http://<your-server-ip>:5050` and events start flowing. No XML parsing, no base64 decoding, no keepalive handling — the SDK does it all.

### ES Module syntax

```javascript
import { ViewtronServer } from 'viewtron-sdk';

const server = new ViewtronServer({ port: 5050 });

server.on('event', (event, clientIP) => {
  console.log(`${event.category} from ${clientIP}`);
});

const { port, ip } = await server.start();
console.log(`Listening on ${ip}:${port}`);
```

### Callback-style options

If you prefer passing callbacks in the constructor instead of using `.on()`:

```javascript
const server = new ViewtronServer({
  port: 5050,
  onEvent: (event, clientIP) => {
    console.log(event.category, event.plateNumber);
  },
  onConnect: (clientIP) => {
    console.log(`Camera connected: ${clientIP}`);
  },
});

server.start();
```

### EventEmitter events

`ViewtronServer` extends Node.js `EventEmitter` and emits five event types. Only `'event'` fires for real detections — keepalives, alarm status, and traject data are filtered out.

| Event | Arguments | When |
|-------|-----------|------|
| `'event'` | `(event, clientIP)` | Parsed `ViewtronEvent` from a real detection |
| `'connect'` | `(clientIP)` | First message from a new camera IP |
| `'raw'` | `(xml, clientIP)` | Raw XML string before parsing (excludes traject) |
| `'listening'` | `({ port, ip })` | Server started successfully |
| `'error'` | `(err)` | Server or parsing error |

### ViewtronEvent — Parse Any Event

If you're building your own HTTP server or processing saved XML, use `ViewtronEvent` directly. It parses the raw XML, detects IPC v1.x vs NVR v2.0 automatically, and returns a `ViewtronEvent` object — or `null` for keepalives, alarm status messages, and unrecognized payloads.

```javascript
const { ViewtronEvent } = require('viewtron-sdk');

const event = ViewtronEvent(xmlString);
if (event === null) {
  return; // keepalive, alarm status, or unrecognized
}

console.log(event.source);            // "IPC" or "NVR"
console.log(event.category);          // "lpr", "intrusion", "face", "counting", "metadata"
console.log(event.plateNumber);       // "ABC1234"
console.log(event.plateGroup);        // "whiteList" (IPC) or NVR group name

// Images as decoded JPEG Buffers — ready for saving, MQTT, notifications
const overview = event.sourceImageBytes;   // Buffer or null (full scene)
const plateCrop = event.targetImageBytes;  // Buffer or null (target closeup)
```

### Routing by category

Every event has a `.category` string. Route on it:

```javascript
server.on('event', (event, clientIP) => {
  switch (event.category) {
    case 'lpr':
      console.log(`Plate: ${event.plateNumber} (group: ${event.plateGroup})`);
      break;
    case 'intrusion':
      console.log(`Intrusion: ${event.eventDescription}, target: ${event.targetType}`);
      break;
    case 'face':
      console.log(`Face: ${event.face ? event.face.sex : 'no attributes'}`);
      break;
  }
});
```

| Category | Description | Application Guide |
|----------|-------------|-------------------|
| `lpr` | License plate recognition with plate group / vehicle attributes | [LPR](/docs/applications/license-plate-recognition-camera-api) |
| `face` | Face detection (with age/sex/glasses/mask on NVR) | [Face Detection](/docs/applications/face-detection-recognition-api) |
| `intrusion` | Line crossing, region intrusion, zone entry/exit, loitering | [Human Detection](/docs/applications/human-detection-intrusion-api) · [Perimeter Security](/docs/applications/perimeter-security-line-crossing-api) |
| `counting` | People/vehicle counting by line or area | [People Counting](/docs/applications/people-counting-traffic-analytics-api) |
| `metadata` | Continuous object detection | [Real-Time Tracking](/docs/applications/real-time-object-tracking-api) |

## Event Properties

Unlike the Python SDK (which returns a different class per event type), the Node.js SDK always returns a single `ViewtronEvent` object with the relevant fields populated.

### Common Fields

| Property | Type | Description |
|----------|------|-------------|
| `source` | string | `"IPC"` for cameras, `"NVR"` for NVRs |
| `category` | string | `"lpr"`, `"face"`, `"intrusion"`, `"counting"`, `"metadata"`, `"traject"` |
| `eventType` | string | Raw smartType code (IPC uppercase e.g. `VEHICE`, NVR camelCase e.g. `vehicle`) |
| `eventDescription` | string | Human-readable description (e.g. `"License Plate Detection"`) |
| `cameraName` | string | Device or camera name |
| `cameraIp` | string | Camera IP address (NVR events only; empty for IPC) |
| `channelId` | string | NVR channel number (NVR only; empty for IPC) |
| `timestamp` | string | Event timestamp from the XML |

### LPR Fields (`category === "lpr"`)

| Property | Type | Description |
|----------|------|-------------|
| `plateNumber` | string | Detected plate text |
| `plateGroup` | string | **IPC:** `"whiteList"`, `"blackList"`, `"temporaryList"`. **NVR:** user-defined group name. Empty if not in the database. |
| `plateColor` | string | Plate color (NVR only) |
| `carOwner` | string | Owner name from an NVR plate-database match (NVR only) |
| `vehicle` | object \| null | `{ type, color, brand, model }` when available (NVR only), else `null` |

### Face Fields (`category === "face"`)

| Property | Type | Description |
|----------|------|-------------|
| `face` | object \| null | `{ age, sex, glasses, mask }` when available (NVR only), else `null` |

### Detection Fields (`intrusion` / `counting`)

| Property | Type | Description |
|----------|------|-------------|
| `eventId` | string | Event identifier from the detection zone |
| `targetId` | string | Target identifier for tracking across frames |
| `targetType` | string | `"person"`, `"car"`, `"motorcycle"` |
| `status` | string | IPC detection status (`SMART_START`, `SMART_PROCEDURE`, `SMART_STOP`); empty for NVR |

See each [application guide](/docs/category/applications) for complete working examples.

## Images

Most events include JPEG snapshots embedded as base64. The SDK exposes both the raw base64 strings and lazy-decoded `Buffer` objects.

| Property | Type | Description |
|----------|------|-------------|
| `sourceImage` | string | Base64 full scene, or `''` if absent |
| `targetImage` | string | Base64 target crop, or `''` if absent |
| `sourceImageBytes` | Buffer \| null | Decoded full scene (lazy, cached), or `null` |
| `targetImageBytes` | Buffer \| null | Decoded target crop (lazy, cached), or `null` |
| `hasImages` | boolean | `true` if either image is present |

```javascript
const fs = require('fs');

server.on('event', (event) => {
  if (event.hasImages) {
    if (event.sourceImage) fs.writeFileSync(`${event.timestamp}_source.jpg`, event.sourceImageBytes);
    if (event.targetImage) fs.writeFileSync(`${event.timestamp}_target.jpg`, event.targetImageBytes);
  }
});
```

Use the base64 strings (`sourceImage` / `targetImage`) directly for a JSON API or an HTML `<img>` tag; use the `Bytes` Buffers for writing to disk or sending over a socket. Buffers are decoded once on first access, then cached.

## No Outbound Camera Control

The Node.js SDK is receive-only. Unlike the Python SDK's `ViewtronCamera` class, it does not send commands to cameras or manage plate databases. For outbound control from Node.js, call the camera's HTTP API directly (see the [API Reference](/docs/category/api-reference)) or use the [Python SDK](/docs/getting-started/python-sdk).

## Projects Built with This SDK

| Project | Description |
|---------|-------------|
| [Node-RED Integration](/docs/integrations/node-red) | `node-red-contrib-viewtron` — receive camera AI events as Node-RED flow messages using this SDK |

## Related Documentation

- [Python SDK](/docs/getting-started/python-sdk) — the receive + outbound-control SDK for Python
- [HTTP POST Setup](/docs/getting-started/http-post-setup) — configure cameras to send webhook events
- [API Versions](/docs/getting-started/api-versions) — IPC v1.x vs NVR v2.0 format differences
- [Webhook Event Formats](/docs/api-reference/events/ipc-event-format) — raw XML event structure reference

## Supported Cameras

The SDK works with any [Viewtron AI security camera](https://www.cctvcamerapros.com/AI-security-cameras-s/1512.htm) or [NVR](https://www.cctvcamerapros.com/IP-Camera-NVRs-s/1472.htm) that supports HTTP POST webhooks. For license plate recognition, use the [Viewtron LPR cameras](https://www.cctvcamerapros.com/License-Plate-Recognition-Systems-s/1518.htm). All Viewtron products are NDAA compliant.

## Questions & Development Inquiries

- **Email:** mike@viewtron.com
- **Phone:** 561-433-8488
- **npm:** [npmjs.com/package/viewtron-sdk](https://www.npmjs.com/package/viewtron-sdk)
- **GitHub:** [github.com/mikehaldas/viewtron-nodejs-sdk](https://github.com/mikehaldas/viewtron-nodejs-sdk)

Mike Haldas is available for questions, consultation, and custom software development for Viewtron API related projects. Email details about your project to mike@viewtron.com.
