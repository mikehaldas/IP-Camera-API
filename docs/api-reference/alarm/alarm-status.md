---
title: "GetAlarmStatus — Current Alarm State"
description: "API reference for GetAlarmStatus — poll current alarm trigger states for all detection types on Viewtron IP cameras and NVRs."
keywords: [ip camera alarm status api, viewtron api, camera alarm polling]
sidebar_label: "Alarm Status"
sidebar_position: 3
---

# GetAlarmStatus

:::tip Application Guide
For webhook-based alarm monitoring, see the [Webhook Event Notification](/docs/applications/webhook-event-notification-api) application guide. For continuous presence tracking, see [Real-Time Object Tracking](/docs/applications/real-time-object-tracking-api).
:::

Retrieves the current alarm trigger status for all detection types. Use this endpoint to poll the device and check which alarms are currently active.

| Field | Value |
|-------|-------|
| **Endpoint** | `/GetAlarmStatus` |
| **Method** | `POST` or `GET` |
| **Products** | IPC, NVR |
| **Request Body** | None |

> Tested: IPC v1.9 (firmware 5.1.4.0)

---

## Response Example

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="1.0" xmlns="http://www.ipc.com/ver10">
  <alarmStatusInfo>
    <motionAlarm type="boolean" id="1">false</motionAlarm>
    <motionAlarm type="boolean" id="2">true</motionAlarm>
    <sensorAlarmIn type="list" count="4">
      <itemType type="boolean"/>
      <item id="1">false</item>
      <item id="2">false</item>
      <item id="3">false</item>
      <item id="4">false</item>
    </sensorAlarmIn>
    <perimeterAlarm type="boolean">false</perimeterAlarm>
    <tripwireAlarm type="boolean">false</tripwireAlarm>
    <vfdAlarm type="boolean">false</vfdAlarm>
    <vehicleAlarm type="boolean" id="1">false</vehicleAlarm>
    <aoiEntryAlarm type="boolean" id="1">false</aoiEntryAlarm>
    <aoiLeaveAlarm type="boolean" id="1">false</aoiLeaveAlarm>
  </alarmStatusInfo>
</config>
```

---

## Alarm Types

| Field | Description |
|-------|-------------|
| `motionAlarm` | Basic motion detection (per channel, identified by `id`) |
| `sensorAlarmIn` | Physical alarm input sensors |
| `perimeterAlarm` | AI perimeter / intrusion zone detection |
| `tripwireAlarm` | AI line crossing / tripwire detection |
| `vfdAlarm` | Video face detection |
| `vehicleAlarm` | License plate recognition |
| `aoiEntryAlarm` | Region entry detection |
| `aoiLeaveAlarm` | Region exit detection |

Each alarm field returns `true` when actively triggered and `false` when inactive.

---

## Notes

- **Alarm hold time behavior:** `perimeterAlarm` goes `true` when detection triggers, stays `true` for the configured `alarmHoldTime`, then drops to `false` even if the target is still present. There will be 5-20 second gaps between alarm cycles. This makes polling `GetAlarmStatus` unsuitable for continuous presence tracking.
- **For continuous presence tracking:** Use `traject` data via [httpPostV2](http-post-webhook-config.md) instead. The traject stream provides approximately 7 updates per second with real-time target coordinates as long as targets are visible. See the [traject documentation](/docs/api-reference/events/real-time-target-tracking-traject) for details.
- This endpoint returns all alarm types in a single response. You do not need separate requests per detection type.
