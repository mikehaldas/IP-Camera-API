---
title: "GetVideoStreamConfig — Video Stream Settings"
description: "API reference for GetVideoStreamConfig — configure resolution, encoding, bitrate, and GOP on Viewtron IP cameras and NVRs."
keywords: [ip camera video stream api, viewtron api, camera resolution bitrate config]
sidebar_label: "Video Streams"
sidebar_position: 3
---

# GetVideoStreamConfig / SetVideoStreamConfig

Get or set video stream parameters (resolution, encoding, bitrate, GOP).

## Endpoint

| Field | Value |
|-------|-------|
| **Method** | `POST` or `GET` (Get) / `POST` (Set) |
| **URL (Get)** | `http://<host>[:port]/GetVideoStreamConfig[/channelId]` |
| **URL (Set)** | `http://<host>[:port]/SetVideoStreamConfig[/channelId]` |
| **Products** | IPC, NVR |
| **Channel ID** | Optional (default 1) |

## Stream Parameters

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Stream profile name (max 32 chars) |
| `resolution` | string | Video resolution (e.g., `1920x1080`) |
| `frameRate` | uint32 | Frame rate in fps |
| `bitRateType` | enum | `VBR` (variable) or `CBR` (constant) |
| `maxBitRate` | uint32 | Maximum bitrate in kbps (64--12288) |
| `encodeType` | enum | `h264`, `h265`, or `mjpeg` |
| `encodeLevel` | enum | `baseLine`, `mainProfile`, or `highProfile` |
| `quality` | enum | `lowest`, `lower`, `medium`, `higher`, `highest` |
| `GOP` | uint32 | Group of Pictures interval (30--200) |

## Response

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="1.0" xmlns="http://www.ipc.com/ver10">
  <types>
    <bitRateType>
      <enum>VBR</enum>
      <enum>CBR</enum>
    </bitRateType>
    <quality>
      <enum>lowest</enum>
      <enum>lower</enum>
      <enum>medium</enum>
      <enum>higher</enum>
      <enum>highest</enum>
    </quality>
    <encodeType>
      <enum>h264</enum>
      <enum>h265</enum>
      <enum>mjpeg</enum>
    </encodeType>
  </types>
  <streams type="list" count="4">
    <item id="1">
      <name type="string" maxLen="32"><![CDATA[profile1]]></name>
      <resolution>1920x1080</resolution>
      <frameRate type="uint32">25</frameRate>
      <bitRateType type="bitRateType">CBR</bitRateType>
      <maxBitRate type="uint32" min="64" max="12288">4096</maxBitRate>
      <encodeType>h264</encodeType>
      <encodeLevel>baseLine</encodeLevel>
      <quality type="quality">highest</quality>
      <GOP type="uint32" min="30" max="200">100</GOP>
    </item>
  </streams>
</config>
```

## Notes

- `id="1"` is the main stream, `id="2"` is the sub stream.
- `maxBitRate` is in kbps.
- RTSP stream URL for NVR: `rtsp://<host>[:port]?chID=<channelId>&streamType=<main|sub>`
- RTSP stream URL for IPC: `rtsp://<host>[:port]/<streamName>`
