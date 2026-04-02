---
title: "PTZ Presets — Save and Recall Positions"
description: "API reference for PTZ Presets — save, list, recall, and delete camera positions on Viewtron PTZ IP cameras via HTTP API."
keywords: [ptz preset api, viewtron api, camera preset positions]
sidebar_label: "Presets"
sidebar_position: 3
---

# PTZ Presets

:::tip Application Guide
For a complete walkthrough of PTZ camera control with code examples, see the [PTZ Camera Control](/docs/applications/ptz-camera-control-api) application guide.
:::

Manage PTZ preset positions -- save, list, recall, and delete named camera positions. This page covers four related endpoints:

- **PtzGotoPreset** -- move the camera to a saved preset
- **PtzGetPresets** -- list all saved presets
- **PtzAddPreset** -- save the current position as a new preset
- **PtzDeletePreset** -- remove a saved preset

---

## Endpoint Summary

| Command | Endpoint | Method | Request Body |
|---------|----------|--------|-------------|
| **PtzGotoPreset** | `/PtzGotoPreset[/channelId]` | `POST` | Preset ID |
| **PtzGetPresets** | `/PtzGetPresets[/channelId]` | `POST` or `GET` | None |
| **PtzAddPreset** | `/PtzAddPreset[/channelId]` | `POST` | Preset name |
| **PtzDeletePreset** | `/PtzDeletePreset[/channelId]` | `POST` | Preset ID |

**Products:** IPC, NVR
**Channel ID:** Optional (default `1`)

---

## PtzGotoPreset

Moves the camera to a saved preset position by ID.

### Request Example

```xml
<?xml version="1.0" encoding="utf-8"?>
<presetInfo version="1.0" xmlns="http://www.ipc.com/ver10">
  <id>2</id>
</presetInfo>
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | uint32 | The preset ID to navigate to (as returned by `PtzGetPresets`) |

---

## PtzGetPresets

Returns a list of all saved preset positions with their IDs and names.

### Response Example

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="1.0" xmlns="http://www.ipc.com/ver10">
  <presetInfo type="list" maxCount="360">
    <itemType type="string" maxLen="10"></itemType>
    <item id="1"><![CDATA[DDD]]></item>
  </presetInfo>
</config>
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `maxCount` | uint32 | Maximum number of presets supported by this device |
| `item` (attribute: `id`) | uint32 | Preset ID number |
| `item` (value) | string | Preset name (max 10 characters) |

---

## PtzAddPreset

Saves the camera's current position as a new named preset. First move the camera to the desired position using [PtzControl](ptz-control-movement.md), then call this endpoint.

### Request Example

```xml
<?xml version="1.0" encoding="utf-8"?>
<presetInfo version="1.0" xmlns="http://www.ipc.com/ver10">
  <name><![CDATA[preset1]]></name>
</presetInfo>
```

| Parameter | Type | Range | Description |
|-----------|------|-------|-------------|
| `name` | string | Max 10 characters | Name for the preset position |

---

## PtzDeletePreset

Deletes a saved preset by ID.

### Request Example

```xml
<?xml version="1.0" encoding="utf-8"?>
<presetInfo version="1.0" xmlns="http://www.ipc.com/ver10">
  <id>2</id>
</presetInfo>
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | uint32 | The preset ID to delete |

---

## Notes

- Use [PtzGetCaps](ptz-get-capabilities.md) to check `presetMaxCount` for the maximum number of presets your device supports (typically 255 or 360).
- Preset names are limited to 10 characters and should be wrapped in `CDATA` tags.
- Presets are stored on the device and persist across reboots.
