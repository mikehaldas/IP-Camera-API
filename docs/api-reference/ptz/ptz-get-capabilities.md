---
title: "PtzGetCaps — PTZ Capabilities"
description: "API reference for PtzGetCaps — query PTZ speed ranges, preset count, and cruise tour limits on Viewtron IP cameras and NVRs."
keywords: [ptz camera capabilities api, viewtron api, ptz speed range presets]
sidebar_label: "PTZ Capabilities"
sidebar_position: 1
---

# PtzGetCaps

:::tip Application Guide
For a complete walkthrough of PTZ camera control with code examples, see the [PTZ Camera Control](/docs/applications/ptz-camera-control-api) application guide.
:::

Retrieves the PTZ capabilities of a camera, including speed ranges, preset count, and cruise tour limits. Use this endpoint to discover the valid parameter ranges for other PTZ commands before sending control requests.

| Field | Value |
|-------|-------|
| **Endpoint** | `/PtzGetCaps[/channelId]` |
| **Method** | `POST` or `GET` |
| **Products** | IPC, NVR |
| **Channel ID** | Optional (default `1`) |

---

## Response Example

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="2.0.0" xmlns="http://www.ipc.com/ver10">
  <caps>
    <controlMinSpeed type="uint32">1</controlMinSpeed>
    <controlMaxSpeed type="uint32">8</controlMaxSpeed>
    <presetMaxCount type="uint32">255</presetMaxCount>
    <cruiseMaxCount type="uint32">8</cruiseMaxCount>
    <cruisePresetMinSpeed type="uint32">1</cruisePresetMinSpeed>
    <cruisePresetMaxSpeed type="uint32">8</cruisePresetMaxSpeed>
    <cruisePresetMaxHoldTime type="uint32">240</cruisePresetMaxHoldTime>
    <cruisePresetMaxCount type="uint32">16</cruisePresetMaxCount>
  </caps>
</config>
```

---

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `controlMinSpeed` | uint32 | Minimum speed value for `PtzControl` movement commands |
| `controlMaxSpeed` | uint32 | Maximum speed value for `PtzControl` movement commands |
| `presetMaxCount` | uint32 | Maximum number of saved preset positions |
| `cruiseMaxCount` | uint32 | Maximum number of cruise tours that can be configured |
| `cruisePresetMinSpeed` | uint32 | Minimum speed for cruise tour preset transitions |
| `cruisePresetMaxSpeed` | uint32 | Maximum speed for cruise tour preset transitions |
| `cruisePresetMaxHoldTime` | uint32 | Maximum dwell time (seconds) at each preset in a cruise tour |
| `cruisePresetMaxCount` | uint32 | Maximum number of presets per cruise tour |

---

## Notes

- Always query capabilities before building PTZ control logic. The speed range and preset limits may vary by camera model and firmware version.
- On NVR systems, include the `channelId` to query capabilities for a specific camera channel.
