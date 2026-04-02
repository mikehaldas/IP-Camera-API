---
title: "GetStreamCaps — Stream Capabilities"
description: "API reference for GetStreamCaps — discover supported resolutions, encoding types, and frame rates on Viewtron IP cameras."
keywords: [ip camera stream capabilities api, viewtron api, camera resolution support]
sidebar_label: "Stream Capabilities"
sidebar_position: 4
---

# GetStreamCaps

Retrieves stream capabilities including supported resolutions, encoding types, and frame rates.

## Endpoint

| Field | Value |
|-------|-------|
| **Method** | `POST` or `GET` |
| **URL** | `http://<host>[:port]/GetStreamCaps[/channelId]` |
| **Products** | IPC, NVR |
| **Channel ID** | Optional (default 1) |

:::caution v1.9 Only
On v2.0 devices, stream capabilities are embedded in `GetVideoStreamConfig` response attributes.
:::

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `rtspPort` | uint16 | RTSP streaming port |
| `streamName` | string | Stream profile name |
| `resolutionCaps` | list | Supported resolutions with max frame rates |
| `encodeTypeCaps` | list | Supported encoding formats |
| `encodeLevelCaps` | list | Supported encoding profiles |

### Supported Encode Types

| Type | Description |
|------|-------------|
| `h264` | H.264 / AVC |
| `mpeg4` | MPEG-4 |
| `mjpeg` | Motion JPEG |
| `h264plus` | H.264+ (smart codec) |
| `h265plus` | H.265+ (smart codec) |
| `h264smart` | H.264 Smart |
| `h265smart` | H.265 Smart |

### Supported Encode Levels

| Level | Description |
|-------|-------------|
| `baseLine` | Baseline profile |
| `mainProfile` | Main profile |
| `highProfile` | High profile |

## Response

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="1.0" xmlns="http://www.ipc.com/ver10">
  <types>
    <resolution>
      <enum>1920x1080</enum>
      <enum>1280x720</enum>
      <enum>704x576</enum>
      <enum>352x288</enum>
    </resolution>
    <encodeType>
      <enum>h264</enum>
      <enum>mpeg4</enum>
      <enum>mjpeg</enum>
      <enum>h264plus</enum>
      <enum>h265plus</enum>
      <enum>h264smart</enum>
      <enum>h265smart</enum>
    </encodeType>
    <encodeLevel>
      <enum>baseLine</enum>
      <enum>mainProfile</enum>
      <enum>highProfile</enum>
    </encodeLevel>
  </types>
  <rtspPort type="uint16">554</rtspPort>
  <streamList type="list" count="4">
    <item id="1">
      <streamName type="string"><![CDATA[profile1]]></streamName>
      <resolutionCaps type="list" count="1">
        <itemType type="resolution"/>
        <item maxFrameRate="25">1920x1080</item>
      </resolutionCaps>
      <encodeTypeCaps type="list" count="1">
        <itemType type="encodeType"/>
        <item>h264</item>
      </encodeTypeCaps>
      <encodeLevelCaps type="list" count="3">
        <itemType type="encodeLevel"/>
        <item>baseLine</item>
        <item>mainProfile</item>
        <item>highProfile</item>
      </encodeLevelCaps>
    </item>
  </streamList>
</config>
```

## Notes

- Each stream profile lists its own supported resolutions, encode types, and encode levels.
- The `maxFrameRate` attribute on resolution items indicates the maximum fps for that resolution.
- Use this information to validate parameters before calling `SetVideoStreamConfig`.
