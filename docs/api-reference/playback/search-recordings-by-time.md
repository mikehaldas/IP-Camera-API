---
title: "SearchByTime — Video Recording Search"
description: "API reference for SearchByTime — find recorded video segments by time range and recording type on Viewtron IP cameras and NVRs."
keywords: [ip camera recording search api, viewtron api, nvr video playback search]
sidebar_label: "Search Recordings"
sidebar_position: 2
---

# SearchByTime

:::tip Application Guide
For video snapshot and recording search examples, see the [Video Snapshots & Recording Search](/docs/applications/video-snapshots-recording-search-api) application guide.
:::

Searches for recorded video segments within a specified time range and recording type filter. Use this to find available recordings before constructing RTSP playback URLs.

| Field | Value |
|-------|-------|
| **Endpoint** | `/SearchByTime[/channelId]` |
| **Method** | `POST` or `GET` |
| **Products** | IPC, NVR |
| **Channel ID** | Optional (default `1`) |

---

## Request Example

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="1.0" xmlns="http://www.ipc.com/ver10">
  <search>
    <recTypes type="list">
      <itemType type="recType"></itemType>
      <item>manual</item>
      <item>schedule</item>
      <item>motion</item>
    </recTypes>
    <starttime type="string"><![CDATA[2017-06-30 00:00:00]]></starttime>
    <endtime type="string"><![CDATA[2017-06-30 23:59:59]]></endtime>
  </search>
</config>
```

---

## Parameters

| Parameter | Type | Format | Description |
|-----------|------|--------|-------------|
| `recTypes` | list | string items | Recording types to search for. Use values from [GetRecordType](get-record-types.md). |
| `starttime` | string | `YYYY-MM-DD HH:MM:SS` | Start of the search time range |
| `endtime` | string | `YYYY-MM-DD HH:MM:SS` | End of the search time range |

---

## RTSP Playback URL

Once you have identified a recording segment, construct an RTSP URL to play it back:

```
rtsp://<host>[:rtspPort]/chID=0&date=2014-01-09&time=15:07:28&timelen=200&streamType=main&action=playback
```

| Parameter | Description |
|-----------|-------------|
| `chID` | Channel ID (0-based) |
| `date` | Recording date (`YYYY-MM-DD`) |
| `time` | Recording start time (`HH:MM:SS`) |
| `timelen` | Playback duration in seconds |
| `streamType` | `main` (full resolution) or `sub` (lower resolution) |
| `action` | `playback` |

---

## Notes

- The time range format uses `YYYY-MM-DD HH:MM:SS` wrapped in CDATA tags.
- You can include multiple recording types in the `recTypes` list to search across different trigger types simultaneously.
- On NVR systems, include the `channelId` in the URL to search recordings for a specific camera channel.
- The RTSP playback URL uses 0-based channel indexing (`chID=0` for channel 1).
