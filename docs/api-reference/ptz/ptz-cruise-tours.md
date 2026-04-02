---
title: "PTZ Cruise Tours — Automated Patrol"
description: "API reference for PTZ Cruise Tours — configure and run automated patrol routes on Viewtron PTZ IP cameras and NVRs."
keywords: [ptz cruise tour api, viewtron api, camera automated patrol]
sidebar_label: "Cruise Tours"
sidebar_position: 4
---

# PTZ Cruise Tours

:::tip Application Guide
For a complete walkthrough of PTZ camera control with code examples, see the [PTZ Camera Control](/docs/applications/ptz-camera-control-api) application guide.
:::

Manage PTZ cruise tours (automated patrol routes). A cruise tour moves the camera through a sequence of saved presets with configurable speed and dwell time at each position. This page covers three related endpoints:

- **PtzGetCruises** -- list configured cruise tours
- **PtzRunCruise** -- start a cruise tour
- **PtzStopCruise** -- stop a running cruise tour

---

## Endpoint Summary

| Command | Endpoint | Method | Request Body |
|---------|----------|--------|-------------|
| **PtzGetCruises** | `/PtzGetCruises[/channelId]` | `POST` or `GET` | None |
| **PtzRunCruise** | `/PtzRunCruise[/channelId]` | `POST` | Cruise ID |
| **PtzStopCruise** | `/PtzStopCruise[/channelId]` | `POST` | None |

**Products:** IPC, NVR
**Channel ID:** Optional (default `1`)

---

## PtzGetCruises

Returns the list of configured cruise tours and their preset sequences.

No request body required.

---

## PtzRunCruise

Starts a cruise tour by ID. The camera will cycle through the tour's preset positions at the configured speed and dwell time.

### Request Example

```xml
<?xml version="1.0" encoding="utf-8"?>
<cruiseInfo version="1.0" xmlns="http://www.ipc.com/ver10">
  <id>1</id>
</cruiseInfo>
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | uint32 | The cruise tour ID to start |

---

## PtzStopCruise

Stops the currently running cruise tour on the specified channel.

No request body required.

---

## Notes

- Use [PtzGetCaps](ptz-get-capabilities.md) to check cruise tour limits for your device:
  - `cruiseMaxCount` -- maximum number of cruise tours (typically 8)
  - `cruisePresetMaxCount` -- maximum presets per cruise tour (typically 16)
  - `cruisePresetMinSpeed` / `cruisePresetMaxSpeed` -- valid speed range for transitions
  - `cruisePresetMaxHoldTime` -- maximum dwell time per preset (typically 240 seconds)
- Cruise tours are configured through the camera's web interface or NVR GUI. The API provides read and run/stop control.
- Presets must be created with [PtzAddPreset](ptz-presets.md) before they can be added to a cruise tour.
