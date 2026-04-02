---
title: "GetSnapshot / GetSnapshotByTime — JPEG Capture"
description: "API reference for GetSnapshot — capture live JPEG snapshots or retrieve stored images by time from Viewtron IP cameras and NVRs."
keywords: [ip camera snapshot api, viewtron api, camera jpeg capture]
sidebar_label: "Snapshots"
sidebar_position: 2
---

# GetSnapshot / GetSnapshotByTime

Capture a live snapshot or retrieve a stored image by time.

## Endpoint

| Field | Value |
|-------|-------|
| **Method** | `POST` or `GET` (GetSnapshot) / `POST` (GetSnapshotByTime) |
| **URL** | `http://<host>[:port]/GetSnapshot[/channelId]` |
| **URL** | `http://<host>[:port]/GetSnapshotByTime[/channelId]` |
| **Products** | IPC, NVR |
| **Channel ID** | Optional (default 1) |

## GetSnapshot

Returns a JPEG-encoded image directly. Check the `Content-Type` response header to confirm the format.

### Usage

```
GET http://192.168.1.100/GetSnapshot
GET http://192.168.1.100/GetSnapshot/2
```

## GetSnapshotByTime

Retrieves a stored image captured at or near the specified time.

### Request

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="2.0.0" xmlns="http://www.ipc.com/ver10">
  <search>
    <time><![CDATA[2024-08-23 15:07:28]]></time>
    <length>10</length>
  </search>
</config>
```

### Request Fields

| Field | Type | Description |
|-------|------|-------------|
| `time` | string | Target timestamp (`YYYY-MM-DD HH:MM:SS`) |
| `length` | uint32 | Search window length in seconds |

## Notes

- `GetSnapshot` returns a live capture from the camera's current view.
- `GetSnapshotByTime` searches stored recordings for an image near the specified time.
- The response body is binary JPEG data (v1.9) -- save it directly to a `.jpg` file.

:::info v2.0 Changes
v2.0 returns base64-encoded image data in XML (`downloadOneImage/sourceBase64Data`) instead of raw JPEG. v1.9 may return raw JPEG or H.264/H.265 key frame data.
:::
