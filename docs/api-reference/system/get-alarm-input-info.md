---
title: "GetAlarmInInfo — Alarm Input Configuration"
description: "API reference for GetAlarmInInfo — retrieve alarm input sensor list and configuration on Viewtron IP cameras and NVRs."
keywords: [ip camera alarm input api, viewtron api, nvr alarm sensor config]
sidebar_label: "Alarm Inputs"
sidebar_position: 5
---

# GetAlarmInList / GetAlarmInInfo

Retrieves the alarm input list. The endpoint name changed between API versions.

## Endpoint

| Field | Value |
|-------|-------|
| **Method** | `POST` or `GET` |
| **URL (v1.9)** | `http://<host>[:port]/GetAlarmInList` |
| **URL (v2.0)** | `http://<host>[:port]/GetAlarmInInfo` |
| **Products** | NVR (v1.9), IPC + NVR (v2.0) |
| **Channel ID** | N/A |

## Response Fields (v2.0)

| Field | Type | Description |
|-------|------|-------------|
| `id` | uint32 | Alarm input identifier |
| `alarmInType` | alarmType | Type of alarm input |

### Alarm Type Values (v2.0)

| Type | Description |
|------|-------------|
| `local` | Physical alarm input on the device |
| `virtual` | Software-defined alarm (used by NVRs for `TriggerVirtualAlarm`) |
| `remote` | Alarm input from a remote/connected device |

## Response (v2.0 -- GetAlarmInInfo)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="2.0.0" xmlns="http://www.ipc.com/ver10">
  <types>
    <alarmType>
      <enum>local</enum>
      <enum>virtual</enum>
      <enum>remote</enum>
    </alarmType>
  </types>
  <alarmInInfoList type="list" count="1">
    <item>
      <id type="uint32">1</id>
      <alarmInType type="alarmType">local</alarmInType>
    </item>
  </alarmInInfoList>
</config>
```

## Response (v1.9 -- GetAlarmInList, NVR only)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="1.0" xmlns="http://www.ipc.com/ver10">
  <alarmInIDList type="list" count="8"></alarmInIDList>
  <itemType type="string" maxLen="20"/>
  <item>1</item>
  <item>2</item>
  <!-- ... up to 8 items ... -->
</config>
```

## Notes

- v1.9 `GetAlarmInList` is NVR only and returns a simple list of alarm input IDs.
- The number of alarm inputs can also be checked via `alarmInCount` in `GetDeviceInfo`.

:::info v2.0 Changes
v2.0 adds alarm type classification (local, virtual, remote). Virtual alarms are used by NVRs for `TriggerVirtualAlarm`. The endpoint was renamed from `GetAlarmInList` to `GetAlarmInInfo`.
:::
