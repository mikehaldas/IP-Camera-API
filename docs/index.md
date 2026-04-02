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
slug: /
---

# Viewtron IP Camera HTTP API

Viewtron IP cameras and NVRs expose an HTTP API for programmatic access to device configuration, live video, PTZ control, AI detection settings, alarm management, and real-time event webhooks. The API uses XML payloads over HTTP POST requests with Basic Authentication.

All AI inference runs on the camera hardware — no cloud service, external software, or per-device licensing required. All Viewtron products are NDAA compliant.

## What You Can Do

- **Query device status** — model info, firmware version, disk capacity, channel configuration
- **Capture snapshots** — live JPEG snapshots and time-based recording search
- **Control PTZ cameras** — pan, tilt, zoom, focus, presets, cruise tours
- **Configure AI detection** — intrusion zones, line crossing, face detection, LPR, people counting
- **Receive real-time webhooks** — HTTP POST events when AI detections occur, with images and bounding boxes
- **Track objects continuously** — real-time target position data via `traject` streaming
- **Control alarm outputs** — trigger relays, sirens, and strobe lights programmatically

## Applicable Products

| Product Line | Description |
|-------------|-------------|
| [Viewtron AI Security Cameras](https://www.cctvcamerapros.com/AI-security-cameras-s/1512.htm) | IP cameras with built-in AI — human detection, vehicle detection, face recognition, LPR, auto-tracking PTZ |
| [Viewtron IP Camera NVRs](https://www.cctvcamerapros.com/IP-Camera-NVRs-s/1472.htm) | Network video recorders with built-in PoE, AI detection management, and HTTP POST event forwarding |

## Quick Start

1. **Authenticate** — all requests use [Basic Authentication](/docs/getting-started/authentication)
2. **Test connectivity** — send a `GetDeviceInfo` request to verify access
3. **Explore Applications** — browse [solution guides](/docs/category/applications) to see what you can build
4. **Reference endpoints** — find detailed request/response docs in the [API Reference](/docs/category/api-reference)

## Resources

- **Python API Server** — [github.com/mikehaldas/IP-Camera-API](https://github.com/mikehaldas/IP-Camera-API)
- **Support Forum** — [NVR Webhook Setup Guide](https://videos.cctvcamerapros.com/support/topic/setup-nvr-api-webhooks)
- **Questions & Development Inquiries** — mike@viewtron.com | 561-433-8488
