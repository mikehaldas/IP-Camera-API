---
title: "GetRecordType — Recording Mode Configuration"
description: "API reference for GetRecordType — query supported recording trigger modes on Viewtron IP cameras and NVRs."
keywords: [ip camera recording types api, viewtron api, nvr record mode config]
sidebar_label: "Record Types"
sidebar_position: 1
---

# GetRecordType

:::tip Application Guide
For video snapshot and recording search examples, see the [Video Snapshots & Recording Search](/docs/applications/video-snapshots-recording-search-api) application guide.
:::

Retrieves the list of supported recording types (trigger modes) for the device. Use this to discover which recording modes are available before searching for recorded video with [SearchByTime](search-recordings-by-time.md).

| Field | Value |
|-------|-------|
| **Endpoint** | `/GetRecordType` |
| **Method** | `POST` or `GET` |
| **Products** | IPC, NVR |
| **Request Body** | None |

---

## Response Example

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="1.0" xmlns="http://www.ipc.com/ver10">
  <recTypeCaps type="list" count="6">
    <itemType type="string" maxLen="20"/>
    <item>manual</item>
    <item>schedule</item>
    <item>motion</item>
    <item>sensor</item>
    <item>intel detection</item>
    <item>nic broken</item>
  </recTypeCaps>
</config>
```

---

## Recording Types

| Type | Description |
|------|-------------|
| `manual` | Manually triggered recording |
| `schedule` | Time-based scheduled recording |
| `motion` | Recording triggered by motion detection |
| `sensor` | Recording triggered by alarm input sensor |
| `intel detection` | Recording triggered by AI/smart detection (perimeter, tripwire, face, LPR, etc.) |
| `nic broken` | Recording triggered by network disconnection (**IPC only**) |

---

## Notes

- The `nic broken` recording type is only available on IP cameras (IPC), not on NVRs.
- Use the recording type values returned here as filter parameters in [SearchByTime](search-recordings-by-time.md) requests.
- The available recording types may vary by device model and firmware version.
