---
title: "GetAudioStreamConfig — Audio Settings"
description: "API reference for GetAudioStreamConfig — retrieve audio encoding, input source, and volume settings on Viewtron IP cameras."
keywords: [ip camera audio config api, viewtron api, camera audio stream settings]
sidebar_label: "Audio Config"
sidebar_position: 5
---

# GetAudioStreamConfig

Retrieves audio stream configuration including encoding, input source, and volume levels.

## Endpoint

| Field | Value |
|-------|-------|
| **Method** | `POST` or `GET` |
| **URL** | `http://<host>[:port]/GetAudioStreamConfig[/channelId]` |
| **Products** | IPC, NVR |
| **Channel ID** | Optional (default 1) |

:::caution v2.0 Only
This command does not exist on v1.9 firmware.
:::

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `audioInSwitch` | boolean | Audio input enabled/disabled |
| `audioEncode` | audioEncodeE | Audio encoding format |
| `audioInput` | audioInputE | Audio input source type |
| `linInVolume` | uint32 | Line-in volume (0--100) |
| `micInVolume` | uint32 | Microphone volume (0--100) |
| `audioOutVolume` | uint32 | Audio output volume (0--100) |
| `audioOutput` | audioOutputE | Audio output mode |

### Audio Encode Types

| Type | Description |
|------|-------------|
| `G711A` | G.711 A-law (8kHz, 64kbps) |
| `G711U` | G.711 mu-law (8kHz, 64kbps) |

### Audio Input Types

| Type | Description |
|------|-------------|
| `MIC` | Microphone input |
| `LIN` | Line-in input |

### Audio Output Types

| Type | Description |
|------|-------------|
| `TALKBACK` | Two-way audio talkback |
| `ALARM_AUDIO` | Alarm audio output |
| `AUTO` | Automatic selection |

## Response

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="2.0.0" xmlns="http://www.ipc.com/ver10">
  <types>
    <audioEncodeE>
      <enum>G711A</enum>
      <enum>G711U</enum>
    </audioEncodeE>
    <audioInputE>
      <enum>MIC</enum>
      <enum>LIN</enum>
    </audioInputE>
    <audioOutputE>
      <enum>TALKBACK</enum>
      <enum>ALARM_AUDIO</enum>
      <enum>AUTO</enum>
    </audioOutputE>
  </types>
  <audioInSwitch type="boolean">true</audioInSwitch>
  <audioEncode type="audioEncodeE">G711U</audioEncode>
  <audioInput type="audioInputE">MIC</audioInput>
  <volume>
    <linInVolume type="uint32" min="0" max="100">75</linInVolume>
    <micInVolume type="uint32" min="0" max="100">75</micInVolume>
    <audioOutVolume type="uint32" min="0" max="100">75</audioOutVolume>
  </volume>
  <audioOutput type="audioOutputE">ALARM_AUDIO</audioOutput>
</config>
```

## Notes

- Check `audioInCount` and `audioOutCount` from `GetDeviceInfo` to confirm audio hardware availability before using this endpoint.
- Volume levels for all three channels (line-in, microphone, output) are independently configurable from 0 to 100.
