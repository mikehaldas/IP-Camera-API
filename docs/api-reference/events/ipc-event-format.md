---
title: "IPC Event Format (v1.x)"
description: "XML format reference for IPC v1.x alarm events — keepalive, alarm status, and detection data from Viewtron IP cameras."
keywords: [ip camera event format, viewtron api xml, ipc alarm data format]
sidebar_label: "IPC Format"
sidebar_position: 3
---

# IPC Event Format (v1.x)

IP cameras send alarm data directly to your HTTP server using config version `1.0` or `1.7` with `Content-Type: application/xml; charset=utf-8` and `Connection: keep-alive`.

The IPC sends three types of messages: keepalive heartbeats, alarm status changes, and full alarm data with detection details and images.

## Keepalive

Periodic heartbeat. Uses a `<DeviceInfo>` root element (not `<config>`).

```xml
<?xml version="1.0" encoding="UTF-8"?>
<DeviceInfo>
    <DeviceName>Device Name</DeviceName>
    <DeviceNo.>1</DeviceNo.>
    <SN><![CDATA[NF40D099BCM0]]></SN>
    <ipAddress>192.168.1.192</ipAddress>
    <macAddress>58:5B:69:40:F4:0D</macAddress>
</DeviceInfo>
```

## Alarm Status (alarmStatusInfo)

Sent when an alarm state changes. Small post (~660 bytes), no images.

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<config version="1.7" xmlns="http://www.ipc.com/ver10">
<alarmStatusInfo>
<perimeterAlarm type="boolean" id="1">true</perimeterAlarm>
</alarmStatusInfo>
<dataTime><![CDATA[2026-03-29 09:58:21]]></dataTime>
<deviceInfo>
<deviceName><![CDATA[FaceCam]]></deviceName>
<deviceNo.><![CDATA[1]]></deviceNo.>
<sn><![CDATA[I421B0Z1173Q]]></sn>
<ipAddress><![CDATA[192.168.0.52]]></ipAddress>
<macAddress><![CDATA[58:5b:69:5f:42:1b]]></macAddress>
</deviceInfo>
</config>
```

**Key behavior:**
- `true` arrives shortly after first detection
- `false` arrives after `alarmHoldTime` expires -- NOT when the person leaves
- Only one true/false cycle per alarm period

## Alarm Data (smartData with images)

Full detection event with coordinates, zone boundary, and optionally images.

### PEA -- Perimeter Intrusion

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
  <smartType type="openAlramObj">PEA</smartType>
  <subscribeOption type="subscribeRelation">FEATURE_RESULT</subscribeOption>
  <currentTime type="tint64">1774792701902505</currentTime>
  <mac type="string"><![CDATA[58:5b:69:5f:42:1b]]></mac>
  <sn type="string"><![CDATA[I421B0Z1173Q]]></sn>
  <deviceName type="string"><![CDATA[FaceCam]]></deviceName>
  <perimeter>
    <perInfo type="list" count="1">
      <item>
        <eventId type="uint32">2357</eventId>
        <targetId type="uint32">2157</targetId>
        <status type="perStatus">SMART_START</status>
        <boundary type="list" count="5">
          <item><point><x type="uint32">450</x><y type="uint32">466</y></point></item>
          <item><point><x type="uint32">9775</x><y type="uint32">400</y></point></item>
          <item><point><x type="uint32">9675</x><y type="uint32">9466</y></point></item>
          <item><point><x type="uint32">425</x><y type="uint32">9700</y></point></item>
          <item><point><x type="uint32">400</x><y type="uint32">500</y></point></item>
        </boundary>
        <rect>
          <x1 type="uint32">4403</x1><y1 type="uint32">694</y1>
          <x2 type="uint32">5909</x2><y2 type="uint32">8125</y2>
        </rect>
      </item>
    </perInfo>
  </perimeter>
  <relativeTime type="tint64">167998902412</relativeTime>
  <sourceDataInfo>
    <dataType type="uint32">0</dataType>
    <width type="uint32">1280</width>
    <height type="uint32">720</height>
    <sourceBase64Length type="uint32">474378</sourceBase64Length>
    <sourceBase64Data type="string"><![CDATA[... (base64 JPEG) ...]]></sourceBase64Data>
  </sourceDataInfo>
</config>
```

### PEA with Target Crop

When both source and target images are subscribed, the post includes a `<listInfo>` block with cropped target image data:

```xml
<config version="1.7" xmlns="http://www.ipc.com/ver10">
    <smartType type="openAlramObj">PEA</smartType>
    <subscribeRelation type="subscribeOption">FEATURE_RESULT</subscribeRelation>
    <currentTime type="tint64">1563528106584193</currentTime>
    <perimeter>
        <perInfo type="list" count="1">
            <item>
                <eventId type="uint32">220</eventId>
                <targetId type="uint32">20</targetId>
                <status type="smartStatus">SMART_START</status>
                <boundary type="list" count="4">
                    <item><point><x type="uint32">1625</x><y type="uint32">2133</y></point></item>
                    <item><point><x type="uint32">1725</x><y type="uint32">8800</y></point></item>
                    <!-- ... additional points ... -->
                </boundary>
                <rect>
                    <x1 type="uint32">113</x1><y1 type="uint32">0</y1>
                    <x2 type="uint32">5511</x2><y2 type="uint32">8472</y2>
                </rect>
            </item>
        </perInfo>
    </perimeter>
    <sourceDataInfo>
        <dataType type="uint32">0</dataType>
        <width type="uint32">1920</width>
        <height type="uint32">1080</height>
        <sourceBase64Length type="uint32">161438</sourceBase64Length>
        <sourceBase64Data type="string"><![CDATA[... (base64 JPEG) ...]]></sourceBase64Data>
    </sourceDataInfo>
    <listInfo type="list" count="1">
        <item>
            <targetId type="tuint32">20</targetId>
            <rect>...</rect>
            <targetImageData>
                <dataType type="uint32">0</dataType>
                <targetType type="uint32">1</targetType>
                <Width type="tuint32">1276</Width>
                <Height type="tuint32">1080</Height>
                <targetBase64Length type="uint32">100774</targetBase64Length>
                <targetBase64Data type="string"><![CDATA[... (base64 JPEG) ...]]></targetBase64Data>
            </targetImageData>
        </item>
    </listInfo>
</config>
```

## IPC smartData Fields

| Field | Description |
|-------|-------------|
| `smartType` | Detection type: `PEA`, `VEHICE`/`VEHICLE`, `VFD`, `VSD`, etc. |
| `perimeter/perInfo` | Perimeter data (for PEA intrusion). Line crossing uses `tripwire/tripInfo`. |
| `eventId` | Unique event ID |
| `targetId` | Target ID (matches `targetId` in concurrent traject posts) |
| `status` | `SMART_START`, `SMART_STOP`, or `SMART_PROCEDURE` |
| `boundary` | Zone polygon coordinates (normalized 0-10000) |
| `rect` | Target bounding box (normalized 0-10000) |
| `sourceDataInfo` | Full frame JPEG (when `sourceImage` subscribed) |
| `listInfo/targetImageData` | Cropped target JPEG. `targetType` is numeric: 1=person, 2=car, 4=bike |

## IPC smartType Codes (Complete)

| smartType | Description | AlarmData Field | AlarmStatus Field | Images |
|-----------|-------------|-----------------|-------------------|--------|
| `MOTION` | Motion detection | `motion` (grid) | `motionAlarm` | Yes |
| `SENSOR` | Sensor alarm | None | `sensorAlarm` | No |
| `PEA` (intrusion) | Perimeter intrusion | `perimeter/perInfo` | `perimeterAlarm` | Yes |
| `PEA` (line cross) | Line crossing | `tripwire/tripInfo` | `tripwireAlarm` | Yes |
| `AVD` (blur) | Video blur | None | `clarityAbnormal` | No |
| `AVD` (cast) | Video cast | None | `colorAbnormal` | No |
| `AVD` (scene) | Scene change | None | `sceneChange` | No |
| `OSC` | Object removal | `smartType: OSC` | `oscAlarm` | Yes |
| `CPC` | People counting | `CPC` | `CPCAlarm` | Yes |
| `CDD` | Crowd density | `CDD` | `CDDAlarm` | Yes |
| `IPD` | People intrusion | `IPD` | `IPDAlarm` | Yes |
| `VFD` | Face detection | `VFD` | `VFDAlarm` | Yes |
| `VFD_MATCH` | Face recognition | `VFD_MATCH` | `VFDAlarm` | Yes |
| `VEHICE` | License plate | `VEHICE` | `vehiceAlarm` | Yes |
| `AOIENTRY` | Region entry | `AOIENTRY` | (undocumented) | Yes |
| `AOILEAVE` | Region exit | `AOILEAVE` | (undocumented) | Yes |
| `PASSLINECOUNT` | Line counting | `PASSLINECOUNT` | (undocumented) | Yes |
| `TRAFFIC` | Area counting | `TRAFFIC` | (undocumented) | Yes |

### LPR Event Fields (VEHICE)

License plate events include plate data in the second `<item>` of `<listInfo>`. The first item contains the overview image, the second contains the plate number, authorization status, and plate crop image.

| Field | Description |
|-------|-------------|
| `plateNumber` | Detected plate text |
| `vehicleListType` | Plate database status (see table below) |
| `PlateConfidence` | Detection confidence score |
| `plateColor` | Plate color |
| `vehicleDirect` | Vehicle direction (`approach` or `leave`) |
| `targetImageData/targetBase64Data` | Base64 JPEG plate crop image |

**Plate database status (`vehicleListType`):**

| Value | Meaning |
|-------|---------|
| `whiteList` | Plate is on the allow list |
| `blackList` | Plate is on the block list |
| `temporaryList` | Plate is on the temporary list and within its valid date range |
| *(field absent)* | Plate is not in the database, or a temporary plate outside its valid date range |

The camera validates temporary plate date ranges internally. Expired temporary plates have `vehicleListType` omitted entirely — they are indistinguishable from unknown plates in the HTTP POST event.

:::tip Application Guides
For step-by-step setup of IPC webhook events, see [Webhook Event Notification API](/docs/applications/webhook-event-notification-api). For traject-based real-time tracking from IPC, see [Real-Time Object Tracking](/docs/applications/real-time-object-tracking-api). For LPR plate database management, see [LPR Configuration](/docs/api-reference/smart-detection/license-plate-recognition-config).
:::
