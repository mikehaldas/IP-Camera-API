---
title: "GetPrivacyMaskConfig — Privacy Zones"
description: "API reference for GetPrivacyMaskConfig — configure privacy mask zones to obscure regions in the Viewtron IP camera view."
keywords: [ip camera privacy mask api, viewtron api, camera privacy zone config]
sidebar_label: "Privacy Masks"
sidebar_position: 7
---

# GetPrivacyMaskConfig

Retrieves privacy mask configuration for defining obscured regions in the camera view.

## Endpoint

| Field | Value |
|-------|-------|
| **Method** | `POST` or `GET` |
| **URL** | `http://<host>[:port]/GetPrivacyMaskConfig[/channelId]` |
| **Products** | IPC |
| **Channel ID** | Optional (default 1) |

:::caution v1.9 Only
This command is available on v1.9 firmware only.
:::

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `switch` | boolean | Enable/disable this privacy mask zone |
| `rectangle.X` | uint32 | Zone X position (0--640) |
| `rectangle.Y` | uint32 | Zone Y position (0--480) |
| `rectangle.width` | uint32 | Zone width (0--640) |
| `rectangle.height` | uint32 | Zone height (0--480) |
| `color` | color | Mask fill color |

### Color Values

| Color | Description |
|-------|-------------|
| `black` | Black mask overlay |
| `white` | White mask overlay |
| `gray` | Gray mask overlay |

## Response

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="1.0" xmlns="http://www.ipc.com/ver10">
  <types>
    <color>
      <enum>black</enum>
      <enum>white</enum>
      <enum>gray</enum>
    </color>
  </types>
  <privacyMask type="list" count="4">
    <itemType>
      <switch type="boolean"/>
      <rectangle>
        <X type="uint32"/>
        <Y type="uint32"/>
        <width type="uint32"/>
        <height type="uint32"/>
      </rectangle>
      <color type="color"/>
    </itemType>
    <item>
      <switch>false</switch>
      <rectangle>
        <X>0</X>
        <Y>0</Y>
        <width>0</width>
        <height>0</height>
      </rectangle>
      <color>black</color>
    </item>
  </privacyMask>
</config>
```

## Notes

- X and Y coordinates use a **640x480 grid** (not the 10000x10000 grid used by OSD positioning).
- Up to 4 privacy mask zones can be configured (see `count="4"` in the response).
- Each zone can be independently enabled/disabled with the `switch` field.
- Privacy masks are applied to both the live view and recorded video -- they cannot be removed after recording.
- Check `supportPrivateMask` in `GetDeviceDetail` to confirm the device supports this feature.
