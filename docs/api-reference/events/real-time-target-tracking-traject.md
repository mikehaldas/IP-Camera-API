---
title: "Real-Time Target Tracking (traject)"
description: "Reference for traject real-time tracking — continuous HTTP POST target data from Viewtron IP cameras for presence detection."
keywords: [ip camera traject tracking, viewtron api real-time, camera object tracking data]
sidebar_label: "traject Tracking"
sidebar_position: 6
---

# Real-Time Target Tracking (traject)

When subscribed to `traject` via httpPostV2, the camera sends **continuous HTTP Posts** for the entire duration a target is being tracked. This is fundamentally different from alarm-based approaches.

> Tested: IPC v1.9 (firmware 5.1.4.0), March 27-29, 2026

## Comparison vs Polling and Alarm Methods

| Method | Signal | Gaps While Present | Gap Duration |
|--------|--------|-------------------|--------------|
| `GetAlarmStatus` polling | `perimeterAlarm=true` | Yes (frequent) | 5-20 seconds |
| Alarm server push (legacy) | One POST per event | Yes (large) | 20-60 seconds |
| **httpPostV2 `traject`** | **Continuous POSTs** | **None** | **N/A** |

**Key characteristics:**
- 6-12 posts per second for the entire tracking duration
- Zero gaps while target is in zone
- Posts stop within ~1 second of target leaving
- Each post includes target ID, type, bounding box, velocity, direction
- Multiple targets tracked simultaneously

## traject Post Format

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<config version="1.7" xmlns="http://www.ipc.com/ver10">
  <types>
    <openAlramObj>
      <enum>MOTION</enum><enum>SENSOR</enum><enum>PEA</enum>
      <!-- ... all alarm types ... -->
    </openAlramObj>
    <subscribeRelation>
      <enum>ALARM</enum>
      <enum>FEATURE_RESULT</enum>
      <enum>ALARM_FEATURE</enum>
    </subscribeRelation>
    <perStatus>
      <enum>SMART_NONE</enum>
      <enum>SMART_START</enum>
      <enum>SMART_STOP</enum>
      <enum>SMART_PROCEDURE</enum>
    </perStatus>
    <targetType>
      <enum>person</enum>
      <enum>car</enum>
      <enum>motor</enum>
    </targetType>
  </types>
  <subscribeOption type="subscribeRelation">FEATURE_RESULT</subscribeOption>
  <currentTime type="tint64">1774646121524166</currentTime>
  <mac type="string"><![CDATA[58:5b:69:5f:42:1b]]></mac>
  <sn type="string"><![CDATA[I421B0Z1173Q]]></sn>
  <deviceName type="string"><![CDATA[FaceCam]]></deviceName>
  <traject type="list" count="1">
    <item>
      <targetId type="uint32">434</targetId>
      <point>
        <x type="uint32">0</x>
        <y type="uint32">0</y>
      </point>
      <rect>
        <x1 type="uint32">6534</x1>
        <y1 type="uint32">2708</y1>
        <x2 type="uint32">7585</x2>
        <y2 type="uint32">6388</y2>
      </rect>
      <velocity type="uint32">0</velocity>
      <direction type="uint32">0</direction>
      <targetType type="targetType">person</targetType>
      <trajectlength type="list" count="0"/>
    </item>
  </traject>
</config>
```

## traject Fields

| Field | Type | Description |
|-------|------|-------------|
| `targetId` | uint32 | Unique ID for the tracked target. New ID per entry. |
| `point` | x, y | Target point (observed as 0,0 -- possibly unused) |
| `rect` | x1, y1, x2, y2 | Bounding box (normalized 0-10000 coordinates) |
| `velocity` | uint32 | Target velocity (observed as 0) |
| `direction` | uint32 | Target direction (observed as 0) |
| `targetType` | string | `person`, `car`, or `motor` |
| `trajectlength` | list | Trajectory path points (observed as empty) |

## Test Results

**Test: Person standing in zone for 60 seconds (IPC standalone)**
- 6-8 posts per second, zero gaps
- Posts stopped within ~1 second of leaving

**Test: Two entries with gap (IPC standalone)**
- 104 traject posts total (50 + 54)
- Clean start/stop, new targetId per entry

**Test: IPC connected to NVR PoE (March 29, 2026)**
- 72 traject posts (39 + 33), post rate 9-12/sec
- XML format identical to standalone
- Source IP was the NVR's PoE interface

### Post Sizes by Data Type

| Data Type | Size | Frequency |
|-----------|------|-----------|
| `traject` | ~1.7 KB | ~7/sec continuous |
| `alarmStatus` | ~660 bytes | 1 per alarm cycle |
| `smartData` + images | ~510-530 KB | 1-2 per entry |
| keepalive | 0 bytes (empty body) | every ~90 sec |

## Configuration

Enable traject on an IPC via `SetHttpPostConfig`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="1.0" xmlns="http://www.ipc.com/ver10">
<httpPostV2><postUrlConf>
  <urlList type="list" count="1"><item>
    <urlId>1</urlId>
    <switch>true</switch>
    <url>
      <protocol>http</protocol>
      <domain><![CDATA[192.168.0.53]]></domain>
      <port>80</port>
      <path><![CDATA[/API]]></path>
      <authentication>none</authentication>
    </url>
    <heatBeatSwitch>true</heatBeatSwitch>
    <keepaliveTimeval>90</keepaliveTimeval>
    <subscribeDateType type="list" count="1">
      <item>traject</item>
    </subscribeDateType>
    <subscriptionEvents type="list" count="1">
      <item>PERIMETER</item>
    </subscriptionEvents>
  </item></urlList>
</postUrlConf></httpPostV2>
</config>
```

## Important Notes

- **traject is IPC-only.** NVRs do not forward traject data and do not expose the smart track data subscription.
- **The "Smart track data" checkbox must be enabled** in the camera's HTTP Post V2 web interface (Edit HTTP POST dialog). The camera will not send traject even if configured via API unless this checkbox is also checked.
- **Works through NVR PoE.** The camera sends traject directly to your server, independent of the NVR. Format is identical.
- **Recommended dual setup:** NVR HTTP Post for alarm events + IPC httpPostV2 for traject tracking.

## Use Cases

- Real-time presence detection (relay control, lighting automation)
- People/vehicle counting with continuous position tracking
- Dwell time analysis
- Custom alarm logic based on target position and movement
- Occupancy monitoring

**Example implementation:** See the [Raspberry Pi Human Detection Relay Controller](https://github.com/mikehaldas/IP-Camera-API) for a working implementation using traject data.

:::tip Application Guides
For a complete traject-based automation project, see [Real-Time Object Tracking](/docs/applications/real-time-object-tracking-api) and [Relay Control & IoT Automation](/docs/applications/relay-control-iot-automation-api).
:::
