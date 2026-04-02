---
title: "PtzControl — Pan, Tilt, Zoom Movement"
description: "API reference for PtzControl — send pan, tilt, zoom, focus, and iris commands to Viewtron PTZ IP cameras and NVRs."
keywords: [ptz camera control api, viewtron api, pan tilt zoom commands]
sidebar_label: "PTZ Movement"
sidebar_position: 2
---

# PtzControl

:::tip Application Guide
For a complete walkthrough of PTZ camera control with code examples, see the [PTZ Camera Control](/docs/applications/ptz-camera-control-api) application guide.
:::

Controls PTZ camera movement including pan, tilt, zoom, focus, and iris adjustments. The movement action is specified in the URL path, and the speed is provided in the request body.

| Field | Value |
|-------|-------|
| **Endpoint** | `/PtzControl[/channelId]/<action>` |
| **Method** | `POST` |
| **Products** | IPC, NVR |
| **Channel ID** | Optional (default `1`) |
| **Action** | Movement command in URL path (see table below) |

---

## Available Actions

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
| `IrisOpen` | Open iris |
| `IrisClose` | Close iris |
| `Stop` | Stop all current PTZ movement |

---

## Request Example

Send this XML body with the desired movement speed:

```xml
<?xml version="1.0" encoding="utf-8"?>
<actionInfo version="1.0" xmlns="http://www.ipc.com/ver10">
  <speed>4</speed>
</actionInfo>
```

---

## Parameters

| Parameter | Type | Range | Description |
|-----------|------|-------|-------------|
| `speed` | uint32 | `1` - `8` | Movement speed. Use [PtzGetCaps](ptz-get-capabilities.md) to confirm the valid range for your device. |

---

## URL Examples

```
# Pan left at speed 4
POST http://192.168.1.100/PtzControl/Left

# Zoom in on NVR channel 3
POST http://192.168.1.100/PtzControl/3/ZoomIn

# Stop all movement
POST http://192.168.1.100/PtzControl/Stop
```

---

## Notes

- Always send a `Stop` command to halt continuous movement. Pan and tilt actions continue until stopped.
- The `speed` value must fall within the range returned by `PtzGetCaps` (`controlMinSpeed` to `controlMaxSpeed`). The typical range is 1-8.
- On NVR systems, place the channel ID between `PtzControl` and the action: `/PtzControl/3/Left`.
