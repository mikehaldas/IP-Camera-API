---
title: "GetAlarmOutList — Alarm Output List"
description: "API reference for GetAlarmOutList — retrieve alarm output relay list on Viewtron NVRs for relay control and automation."
keywords: [nvr alarm output api, viewtron api, ip camera relay list]
sidebar_label: "Alarm Outputs"
sidebar_position: 6
---

# GetAlarmOutList

Retrieves the alarm output list. **NVR only.**

## Endpoint

| Field | Value |
|-------|-------|
| **Method** | `POST` or `GET` |
| **URL** | `http://<host>[:port]/GetAlarmOutList` |
| **Products** | NVR |
| **Channel ID** | N/A |

:::caution v1.9 Only
On v2.0 devices, use `GetAlarmInInfo` which returns both input and output information, or check `alarmOutCount` in `GetDeviceInfo`.
:::

## Response

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="1.0" xmlns="http://www.ipc.com/ver10">
  <alarmOutIDList type="list" count="4"></alarmOutIDList>
  <itemType type="string" maxLen="20"/>
  <item>1</item>
  <item>2</item>
  <item>3</item>
  <item>4</item>
</config>
```

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `alarmOutIDList` | list | List of alarm output identifiers |
| `count` | attribute | Total number of alarm outputs |
| `item` | string | Individual alarm output ID |

## Notes

- Each `<item>` contains an alarm output ID number.
- The number of alarm outputs can also be checked via `alarmOutCount` in `GetDeviceInfo`.
- This endpoint is only available on NVR devices running v1.9 firmware.
