---
title: "Webhook Events Overview"
description: "Overview of webhook event delivery from Viewtron IP cameras and NVRs — IPC direct posts vs NVR forwarded events and setup guidance."
keywords: [ip camera webhook events, viewtron api, camera http post overview]
sidebar_label: "Overview"
sidebar_position: 1
---

# Webhook Events Overview

Viewtron devices can push real-time AI detection events to your HTTP server as webhooks. There are two sources of HTTP POST data:

1. **IP Camera (direct)** -- The camera sends posts directly to your server using the IPC v1.x XML format (config version `1.0` or `1.7`). Supports the full httpPostV2 subscription system including real-time `traject` tracking.

2. **NVR (forwarded)** -- The NVR receives events from cameras on its PoE ports and forwards them to your server using the NVR v2.0 XML format (config version `2.0.0`). Does **not** support `traject`.

## Recommended Setup

For full coverage, configure both sources simultaneously:

1. Configure the **NVR** HTTP Post to send to your server (alarm events with images, v2.0 format)
2. Configure the **IPC** httpPostV2 to send to your server with `traject` subscribed (real-time tracking, v1.x format)
3. Your server receives both streams simultaneously

This dual-source approach gives you alarm events with images from the NVR and continuous real-time tracking from the camera.

## Working Python Server

A complete working implementation is available at [github.com/mikehaldas/IP-Camera-API](https://github.com/mikehaldas/IP-Camera-API). It handles both IPC and NVR formats, extracts images, logs events to CSV, and supports traject-based relay control.

## Event Flow

When a detection event occurs, you receive these message types:

| Message Type | Description | Source |
|-------------|-------------|--------|
| **keepalive** | Periodic heartbeat | IPC and NVR |
| **alarmStatus** | Alarm state change (true/false) | IPC and NVR |
| **alarmData / smartData** | Full detection event with coordinates and images | IPC and NVR |
| **traject** | Continuous real-time target position tracking | IPC only |

## Format Differences

The two sources use different XML formats. See the dedicated pages for each:

- [IPC Event Format (v1.x)](./ipc-event-format.md) -- Direct camera posts
- [NVR Event Format (v2.0)](./nvr-event-format.md) -- NVR-forwarded posts

## Section Guide

| Page | What You'll Find |
|------|-----------------|
| [Detection Types](./detection-types-reference.md) | Complete table of all detection types with IPC and NVR codes |
| [IPC Format](./ipc-event-format.md) | XML structure for direct camera posts (v1.x) |
| [NVR Format](./nvr-event-format.md) | XML structure for NVR-forwarded posts (v2.0) |
| [Data Types](./httppostv2-data-types.md) | How httpPostV2 subscription types interact |
| [traject Tracking](./real-time-target-tracking-traject.md) | Continuous real-time target position data |
| [Image Data](./image-data-handling.md) | Base64 image encoding, source vs target images |
| [Timestamps](./timestamp-handling.md) | Timestamp formats across IPC and NVR |

:::tip Application Guides
For step-by-step setup instructions, see [Webhook Event Notification API](/docs/applications/webhook-event-notification-api) in the Applications section.
:::
