---
title: "GetMotionConfig — Motion Detection Settings"
description: "API reference for GetMotionConfig — configure motion detection sensitivity, grid zones, and alarm triggers on Viewtron IP cameras."
keywords: [ip camera motion detection api, viewtron api, camera motion config]
sidebar_label: "Motion Detection"
sidebar_position: 1
---

# GetMotionConfig / SetMotionConfig

:::tip Application Guide
For motion detection integration with webhooks, see the [Webhook Event Notification](/docs/applications/webhook-event-notification-api) application guide.
:::

Get or set motion detection configuration, including sensitivity, detection grid, alarm hold time, and alarm output triggers.

| Field | Value |
|-------|-------|
| **Endpoint (Get)** | `/GetMotionConfig[/channelId]` |
| **Endpoint (Set)** | `/SetMotionConfig[/channelId]` |
| **Method (Get)** | `POST` or `GET` |
| **Method (Set)** | `POST` |
| **Products** | IPC, NVR |
| **Channel ID** | Optional (default `1`) |

:::caution Version Note
`SetMotionConfig` is documented for v1.9 only. On v2.0 devices, motion configuration may need to be set through the web interface.
:::

---

## Response Example

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="1.0" xmlns="http://www.ipc.com/ver10">
  <motion>
    <switch type="boolean">false</switch>
    <sensitivity type="int32" min="0" max="8">4</sensitivity>
    <alarmHoldTime type="uint32">20</alarmHoldTime>
    <area type="list" count="18">
      <itemType type="string" minLen="22" maxLen="22"></itemType>
      <item><![CDATA[1111111111111111111111]]></item>
      <item><![CDATA[1111111111111111111111]]></item>
      <!-- ... 18 items total ... -->
    </area>
    <triggerAlarmOut type="list" count="1">
      <itemType type="boolean"></itemType>
      <item id="1">false</item>
    </triggerAlarmOut>
  </motion>
</config>
```

---

## Parameters

| Parameter | Type | Range | Description |
|-----------|------|-------|-------------|
| `switch` | boolean | `true` / `false` | Enable or disable motion detection |
| `sensitivity` | int32 | `0` - `8` | Detection sensitivity (higher = more sensitive) |
| `alarmHoldTime` | uint32 | seconds | Duration the alarm stays active after motion stops |
| `area` | list | 18 items of 22 characters | Detection grid (see below) |
| `triggerAlarmOut` | list | boolean items | Whether to trigger each alarm output relay on detection |

---

## Detection Grid

The `area` element defines a 22x18 grid overlaid on the camera's field of view. Each of the 18 items is a string of 22 characters:

- `1` = motion detection enabled in this cell
- `0` = motion detection disabled in this cell

The grid covers the full frame. To detect motion only in a specific region, set the corresponding cells to `1` and the rest to `0`.

---

## Notes

- The grid resolution (22x18) is fixed and cannot be changed.
- On NVR systems, include the `channelId` to configure motion detection for a specific camera channel.
- For AI-based detection (human/vehicle filtering), use the [Smart Detection](/docs/api-reference/smart-detection/intrusion-perimeter-detection-config) endpoints instead, which provide more accurate results than basic motion detection.
