---
title: "GetChannelInfo — Channel Configuration"
description: "API reference for GetChannelInfo — list camera channels, connection status, and channel types on Viewtron NVRs and IP cameras."
keywords: [nvr channel list api, viewtron api, ip camera channel info]
sidebar_label: "Channel Info"
sidebar_position: 4
---

# GetChannelList / GetChannelInfo

Retrieves the channel list from the device. The endpoint name changed between API versions.

## Endpoint

| Field | Value |
|-------|-------|
| **Method** | `POST` or `GET` |
| **URL (v1.9)** | `http://<host>[:port]/GetChannelList` |
| **URL (v2.0)** | `http://<host>[:port]/GetChannelInfo` |
| **Products** | NVR (v1.9), IPC + NVR (v2.0) |
| **Channel ID** | N/A |

## Response Fields (v2.0)

| Field | Type | Description |
|-------|------|-------------|
| `channelId` | uint32 | Channel number (starts from 1) |
| `name` | string | User-assigned channel name |
| `status` | channelStatus | Current channel status |
| `attribute` | channelType | Channel type classification |

### Channel Status Values

| Status | Description |
|--------|-------------|
| `online` | Channel is connected and active |
| `offline` | Channel is disconnected |
| `videoOn` | Video feed is active |
| `videoLoss` | Video signal lost |

### Channel Type Values (v2.0)

| Type | Description |
|------|-------------|
| `Normal` | Standard camera channel |
| `Thermal` | Thermal imaging channel |
| `Fisheye` | Fisheye lens channel |
| `Panoramic` | Panoramic camera channel |
| `PTZ` | Pan-tilt-zoom channel |
| `4PTZFusion` | 4-channel PTZ fusion |

## Response (v2.0 -- GetChannelInfo)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="2.0.0" xmlns="http://www.ipc.com/ver10">
  <types>
    <channelStatus>
      <enum>online</enum>
      <enum>offline</enum>
      <enum>videoOn</enum>
      <enum>videoLoss</enum>
    </channelStatus>
    <channelType>
      <enum>Normal</enum>
      <enum>Thermal</enum>
      <enum>Fisheye</enum>
      <enum>Panoramic</enum>
      <enum>PTZ</enum>
      <enum>4PTZFusion</enum>
    </channelType>
  </types>
  <channelList type="list" count="1">
    <item>
      <channelId type="uint32">1</channelId>
      <name type="string"><![CDATA[channel1]]></name>
      <status type="channelStatus">online</status>
      <attribute type="channelType">Normal</attribute>
    </item>
  </channelList>
</config>
```

## Response (v1.9 -- GetChannelList, NVR only)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="1.0" xmlns="http://www.ipc.com/ver10">
  <types>
    <channelStatus>
      <enum>online</enum>
      <enum>offline</enum>
      <enum>videoOn</enum>
      <enum>videoLoss</enum>
    </channelStatus>
  </types>
  <channelIDList type="list" count="4"/>
  <itemType type="string" maxLen="20"/>
  <item channelStatus="online">1</item>
  <item channelStatus="online">2</item>
  <item channelStatus="online">3</item>
  <item channelStatus="online">4</item>
</config>
```

## Notes

- v1.9 `GetChannelList` is NVR only. If `deviceDescription` equals `IPCamera`, do not send this command.
- Channel ID starts from 1.

:::info v2.0 Changes
v2.0 adds channel names, channel types (Normal, Thermal, Fisheye, etc.), and works on both IPC and NVR. The endpoint was renamed from `GetChannelList` to `GetChannelInfo`.
:::
