---
title: Viewtron IP Camera HTTP API
sidebar_label: Overview
sidebar_position: 0
description: "Complete HTTP API documentation for Viewtron AI security cameras and NVRs. Control PTZ, configure AI detection, receive real-time webhooks — no cloud required."
keywords:
  - ip camera api
  - security camera api
  - viewtron api
  - camera HTTP API
  - ndaa compliant camera with api
  - open api security camera
  - ip camera sdk
slug: /
---

# Viewtron IP Camera HTTP API

Viewtron IP cameras and NVRs expose an HTTP API for programmatic access to device configuration, live video, PTZ control, AI detection settings, alarm management, and real-time event webhooks. The API uses XML payloads over HTTP POST requests with Basic Authentication.

All AI inference runs on the camera hardware — no cloud service, external software, or per-device licensing required. All Viewtron products are NDAA compliant.

## What You Can Do

- **Receive real-time AI detection webhooks** — HTTP POST events when cameras detect humans, vehicles, faces, or license plates, with snapshot images and bounding box coordinates
- **Control PTZ cameras** — pan, tilt, zoom, focus, presets, cruise tours
- **Track objects continuously** — real-time target position data via `traject` streaming at ~7 updates/sec
- **Read and capture license plates** — LPR with plate database management and gate access control via Wiegand
- **Detect and recognize faces** — face detection with attributes (age, sex, glasses, mask) and face matching
- **Count people and vehicles** — entrance/exit counting by line or area with statistics
- **Configure AI detection zones** — intrusion zones, line crossing, region entry/exit, loitering, parking violations
- **Capture snapshots** — live JPEG snapshots and time-based recording search via RTSP
- **Control alarm outputs** — trigger relays, sirens, and strobe lights programmatically
- **Query device status** — model info, firmware version, disk capacity, channel configuration

## Documentation Layers

This documentation is organized in four layers, from low-level protocol to ready-made integrations:

### 1. API Reference — Raw HTTP Endpoints

The [API Reference](/docs/category/api-reference) documents every HTTP endpoint exposed by Viewtron cameras and NVRs. All requests use HTTP POST with XML payloads and Basic Authentication. This is language-agnostic — any HTTP client in any language can use it directly.

### 2. SDK Reference — Python & Node.js Libraries

The SDKs wrap the raw API with typed objects, built-in HTTP servers for receiving webhook events, and automatic IPC/NVR version handling.

- **[Python SDK Reference](/docs/category/python-sdk-reference)** — `pip install viewtron` — ViewtronServer receives events, ViewtronEvent parses them, ViewtronCamera manages plate databases
- **[Node.js SDK Reference](/docs/category/nodejs-sdk-reference)** — `npm install viewtron-sdk` — EventEmitter-based server with the same event model

Developers who don't use our SDKs need to build their own HTTP servers and XML parsing.

### 3. Applications — Solution Guides

[Application guides](/docs/category/applications) show how to build real solutions using the API and SDKs — human detection, LPR gate access, face detection, PTZ control, people counting, and more. Each guide includes working code in both Python and Node.js.

### 4. Integrations — Home Assistant & Node-RED

Pre-built integrations for [Home Assistant](/docs/integrations/home-assistant) (MQTT auto-discovery) and [Node-RED](/docs/integrations/node-red) (direct HTTP POST) — no coding required.

## Quick Example

```python
import requests
from requests.auth import HTTPBasicAuth

# Query camera info
response = requests.get(
    "http://192.168.0.50/GetDeviceInfo",
    auth=HTTPBasicAuth("admin", "password123")
)
print(response.text)

# Move a PTZ camera
requests.get(
    "http://192.168.0.50/PtzControl/1/ZoomIn",
    auth=HTTPBasicAuth("admin", "password123")
)
```

## Applicable Products

All [Viewtron IP cameras](https://www.cctvcamerapros.com/AI-security-cameras-s/1512.htm) and [Viewtron NVRs](https://www.cctvcamerapros.com/IP-Camera-NVRs-s/1472.htm) support this API. See [Supported Products](/docs/supported-products) for a complete list with per-product API capabilities.

## Quick Start

1. **Authenticate** — all requests use [Basic Authentication](/docs/getting-started/authentication)
2. **Install an SDK** — `pip install viewtron` ([Python](/docs/category/python-sdk-reference)) or `npm install viewtron-sdk` ([Node.js](/docs/category/nodejs-sdk-reference))
3. **Test connectivity** — send a `GetDeviceInfo` request to verify access
4. **Explore Applications** — browse [solution guides](/docs/category/applications) to see what you can build
5. **Connect to Home Assistant** — set up the [Home Assistant integration](/docs/integrations/home-assistant) for smart home automations
6. **Reference endpoints** — find detailed request/response docs in the [API Reference](/docs/category/api-reference)

## Resources

- **Python SDK** — [`pip install viewtron`](/docs/category/python-sdk-reference) — receive AI detection events and manage plate databases from Python
- **Node.js SDK** — [`npm install viewtron-sdk`](/docs/category/nodejs-sdk-reference) — EventEmitter-based server for receiving camera events in Node.js
- **Home Assistant Integration** — [connect Viewtron cameras to Home Assistant](/docs/integrations/home-assistant) via MQTT auto-discovery
- **API Server & Examples** — [github.com/mikehaldas/IP-Camera-API](https://github.com/mikehaldas/IP-Camera-API) — working webhook receiver examples
- **Markdown Documentation** — all documentation pages are available as Markdown files in the [GitHub docs directory](https://github.com/mikehaldas/IP-Camera-API/tree/main/docs) for easy integration with AI coding assistants and automated tools
- **Single-File Reference** — the complete API documentation in [one searchable file](https://github.com/mikehaldas/IP-Camera-API/blob/main/docs/viewtron-api-guide.md) for quick reference and AI assistant ingestion
- **Support Forum** — [NVR Webhook Setup Guide](https://videos.cctvcamerapros.com/support/topic/setup-nvr-api-webhooks)

## Video Guides & Tutorials

These blog posts and video walkthroughs cover camera setup, installation best practices, and live demos of the API in action.

- [LPR Camera API Setup and Live Demo](https://videos.cctvcamerapros.com/v/lpr-camera-api.html) — configuring webhooks, receiving plate reads, and viewing event data in real time
- [AI Security Camera System Overview](https://videos.cctvcamerapros.com/v/ai-security-camera-system.html) — human detection, vehicle detection, and the different AI event types
- [ANPR / LPR Camera System](https://videos.cctvcamerapros.com/v/lpr-camera-system-anpr.html) — installation, plate capture zones, and system design for license plate recognition
- [Best License Plate Recognition Cameras](https://videos.cctvcamerapros.com/surveillance-systems/best-license-plate-recognition-cameras.html) — buyer's guide comparing Viewtron LPR cameras
- [IP Camera Alarm Relay Control](https://videos.cctvcamerapros.com/v/ip-camera-alarm-relay.html) — triggering relays and alarm outputs via the API

## Questions & Development Inquiries

- **Email:** mike@viewtron.com
- **Phone:** 561-433-8488

Mike Haldas is available for questions, consultation, and custom software development for Viewtron API related projects. Email details about your project to mike@viewtron.com.
