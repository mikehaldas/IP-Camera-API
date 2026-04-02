---
title: "GetImageOsdConfig — On-Screen Display"
description: "API reference for GetImageOsdConfig — configure on-screen display text overlays for timestamp and channel name on Viewtron IP cameras."
keywords: [ip camera osd config api, viewtron api, camera text overlay]
sidebar_label: "OSD Config"
sidebar_position: 6
---

# GetImageOsdConfig / SetImageOsdConfig

Get or set OSD (On-Screen Display) text overlay configuration for timestamp and channel name.

## Endpoint

| Field | Value |
|-------|-------|
| **Method** | `POST` or `GET` (Get) / `POST` (Set) |
| **URL (Get)** | `http://<host>[:port]/GetImageOsdConfig[/channelId]` |
| **URL (Set)** | `http://<host>[:port]/SetImageOsdConfig[/channelId]` |
| **Products** | IPC |
| **Channel ID** | Optional (default 1) |

:::caution v1.9 Only
This command is available on v1.9 firmware only.
:::

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `time.switch` | boolean | Enable/disable timestamp overlay |
| `time.X` | uint32 | Timestamp X position (0--10000) |
| `time.Y` | uint32 | Timestamp Y position (0--10000) |
| `time.dateFormat` | dateFormat | Date display format |
| `channelName.switch` | boolean | Enable/disable channel name overlay |
| `channelName.X` | uint32 | Channel name X position (0--10000) |
| `channelName.Y` | uint32 | Channel name Y position (0--10000) |
| `channelName.name` | string | Channel name text (max 19 chars) |

### Date Format Values

| Value | Example |
|-------|---------|
| `year-month-day` | 2024-08-21 |
| `month-day-year` | 08-21-2024 |
| `day-month-year` | 21-08-2024 |

## Response

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="1.0" xmlns="http://www.ipc.com/ver10">
  <types>
    <dateFormat>
      <enum>year-month-day</enum>
      <enum>month-day-year</enum>
      <enum>day-month-year</enum>
    </dateFormat>
  </types>
  <imageOsd>
    <time>
      <switch type="boolean">true</switch>
      <X type="uint32">0</X>
      <Y type="uint32">0</Y>
      <dateFormat type="dateFormat">year-month-day</dateFormat>
    </time>
    <channelName>
      <switch type="boolean">false</switch>
      <X type="uint32">0</X>
      <Y type="uint32">0</Y>
      <name type="string" maxLen="19"><![CDATA[name]]></name>
    </channelName>
  </imageOsd>
</config>
```

## Notes

- X and Y coordinates use a **10000x10000 normalized grid**. Position `(0, 0)` is the top-left corner, `(10000, 10000)` is the bottom-right.
- The channel name text is limited to 19 characters.
- Both the timestamp and channel name overlays can be independently enabled/disabled and positioned.
