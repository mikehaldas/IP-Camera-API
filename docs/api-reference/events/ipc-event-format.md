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

Several details depend on camera firmware. See [Firmware Differences](#firmware-differences) before you hard-code a field name or value.

## Keepalive

Periodic heartbeat. **The interval is configurable** in the camera's HTTP POST settings (`keepaliveTimeval`, 30-120 seconds; see [Webhook Configuration](/docs/api-reference/alarm/http-post-webhook-config)). Base any "connection lost" timeout on the value you configured, not on a fixed number. For example, an LPR-IP4 on firmware 5.3.1 with the setting at 90 seconds sent a keepalive every 90 seconds over one persistent connection. 90 seconds is an example setting, not a fixed value.

The body depends on firmware, so accept every form below.

### Firmware 5.3.1

Observed on LPR-IP4 firmware 5.3.1. A `<config>` document (version `1.7`) with `messageType` `keepalive` and a `deviceInfo` block. There is no XML declaration.

```xml
<config version="1.7" xmlns="http://www.ipc.com/ver10">
<messageType>keepalive</messageType>
<deviceInfo>
<deviceName><![CDATA[LPR Camera]]></deviceName>
<ip><![CDATA[192.0.2.100]]></ip>
<mac><![CDATA[00:00:00:00:00:00]]></mac>
</deviceInfo>
</config>
```

### Older firmware

Older firmware uses a `<DeviceInfo>` root element (not `<config>`) and includes the serial number.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<DeviceInfo>
    <DeviceName>Device Name</DeviceName>
    <DeviceNo.>1</DeviceNo.>
    <SN><![CDATA[SERIALNUMBER]]></SN>
    <ipAddress>192.0.2.100</ipAddress>
    <macAddress>00:00:00:00:00:00</macAddress>
</DeviceInfo>
```

Some cameras send keepalive posts with an empty body (see the [httpPostV2 Data Types](./httppostv2-data-types.md) timeline).

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

`dataTime` follows the camera's date and time display format. The sample above uses `YYYY-MM-DD HH:MM:SS`. LPR-IP4 firmware 5.3.1 sent `MM-DD-YYYY hh:mm:ss AM/PM` (for example `09-21-2026 02:15:30 PM`). Parse both, or use `currentTime` on alarm data posts. License plate alarms use `vehiceAlarm` (firmware spelling).

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
    <subscribeOption type="subscribeRelation">FEATURE_RESULT</subscribeOption>
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
| `listInfo/targetImageData` | Cropped target JPEG. `targetType` is numeric (1=person, 2=car, 4=bike) in the samples above. LPR-IP4 firmware 5.3.1 sends a string (`car`) on plate posts, so accept both. |

The `type` attributes are type names, and their spelling varies by firmware. The samples above show `openAlramObj` and `subscribeRelation`. LPR-IP4 firmware 5.3.1 sends `openAlarmObj` and `subscribeRelationV1`. Match on element names (`smartType`, `subscribeOption`), not on `type` attribute values.

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
| `VEHICE` / `VEHICLE` | License plate (spelling depends on firmware, see [Firmware Differences](#firmware-differences)) | `listInfo` | `vehiceAlarm` | Yes |
| `AOIENTRY` | Region entry | `AOIENTRY` | (undocumented) | Yes |
| `AOILEAVE` | Region exit | `AOILEAVE` | (undocumented) | Yes |
| `PASSLINECOUNT` | Line counting | `PASSLINECOUNT` | (undocumented) | Yes |
| `TRAFFIC` | Area counting | `TRAFFIC` | (undocumented) | Yes |

### LPR Event (VEHICE / VEHICLE)

A plate read arrives as one `FEATURE_RESULT` post. There is no `sourceDataInfo` block. `listInfo` has two items:

- **Item 0** is the overview image (`image` 0, empty `plateNumber`, `width`/`height` 0, empty `targetType`).
- **Item 1** is the plate read and the plate crop (`image` 1, `targetType` `car`).

Shape observed on LPR-IP4 firmware 5.3.1 (HTTP POST V1 layout). Device identity, the timestamp, image data, and vehicle attribute values are placeholders. `IB36NL` is a test plate. The full file is [examples/ipc-v1x/lpr.xml](https://github.com/mikehaldas/IP-Camera-API/blob/main/examples/ipc-v1x/lpr.xml).

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<config version="1.7" xmlns="http://www.ipc.com/ver10">
<types><!-- ... enum lists ... --></types>
<smartType type="openAlarmObj">VEHICE</smartType>
<subscribeOption type="subscribeRelationV1">FEATURE_RESULT</subscribeOption>
<currentTime type="tint64">1785000000123456</currentTime>
<mac type="string"><![CDATA[00:00:00:00:00:00]]></mac>
<sn type="string"><![CDATA[SERIALNUMBER]]></sn>
<deviceName type="string"><![CDATA[LPR Camera]]></deviceName>
<channelId type="uint32">1</channelId>
<plateCount type="uint32">1</plateCount>
<listInfo type="list" count="2">
    <item>
        <image type="uint32">0</image>
        <plateNumber type="string"><![CDATA[]]></plateNumber>
        <!-- ... same fields as item 1, all zero ... -->
        <targetImageData>
            <dataType type="uint32">0</dataType>
            <targetType type="targetType"></targetType>
            <width type="uint32">0</width>
            <height type="uint32">0</height>
            <targetBase64Length type="uint32">770384</targetBase64Length>
            <targetBase64Data type="string"><![CDATA[... (base64 JPEG overview) ...]]></targetBase64Data>
        </targetImageData>
    </item>
    <item>
        <image type="uint32">1</image>
        <vehiceId type="uint32">1</vehiceId>
        <plateNumber type="string"><![CDATA[IB36NL]]></plateNumber>
        <plateCharCount type="uint32">6</plateCharCount>
        <vehicleDirect type="vehicleDirectType">approach</vehicleDirect>
        <vehicleListType type="vehileMatchAlarmList">whiteList</vehicleListType>
        <PlateWidth type="uint32">176</PlateWidth>
        <PlateHeight type="uint32">100</PlateHeight>
        <SourceImageWidth type="uint32">2688</SourceImageWidth>
        <SourceImageHeight type="uint32">1776</SourceImageHeight>
        <leftTop><x type="uint32">7559</x><y type="uint32">2072</y></leftTop>
        <rightTop><x type="uint32">8214</x><y type="uint32">2072</y></rightTop>
        <leftBottom><x type="uint32">7559</x><y type="uint32">2635</y></leftBottom>
        <rightBottom><x type="uint32">8214</x><y type="uint32">2635</y></rightBottom>
        <PlateConfidence type="uint32" count="9900"/>
        <plateColor type="uint32" count="3"/>
        <plateColorRate type="uint32" count="0"/>
        <plateStyle type="uint32" count="1"/>
        <vehiceColor type="uint32" count="0"/>
        <plateAngleH type="uint32" count="0"/>
        <plateAngleV type="uint32" count="0"/>
        <province type="string"></province>
        <carAttr>
            <color type="vsdCarAttrColorType">white</color>
            <type type="vsdCarAttrTypeType">saloon car</type>
            <brand type="vsdCarAttrBrandType">Toyota</brand>
            <model type="vsdCarAttrModelType">Toyota_Camry</model>
        </carAttr>
        <carRect>
            <x type="uint32">1242</x><y type="uint32"/>
            <width type="uint32">586</width><height type="uint32">446</height>
        </carRect>
        <targetImageData>
            <dataType type="uint32">0</dataType>
            <targetType type="targetType">car</targetType>
            <width type="uint32">176</width>
            <height type="uint32">100</height>
            <targetBase64Length type="uint32">19520</targetBase64Length>
            <targetBase64Data type="string"><![CDATA[... (base64 JPEG plate crop) ...]]></targetBase64Data>
        </targetImageData>
    </item>
</listInfo>
</config>
```

#### LPR Fields

"Confirmed on" names the firmware where the field was seen in a captured post.

| Field | Description | Confirmed on |
|-------|-------------|--------------|
| `smartType` | `VEHICE` or `VEHICLE`, depending on firmware | 5.1.1, 5.3.1 |
| `currentTime` | Event time from the camera clock, Unix microseconds (16 digits). Check the camera clock before comparing it with arrival time. | 5.3.1 |
| `plateCount` | Number of plates in the post | 5.3.1 |
| `listInfo/item[0]/targetImageData` | Overview JPEG (base64). About 760 KB of base64 text in an LPR-IP4 post. | 5.1.1, 5.3.1 |
| `plateNumber` | Plate text (CDATA). Empty on item 0. | 5.1.1, 5.3.1 |
| `plateCharCount` | Number of characters in the plate text | 5.3.1 |
| `vehicleDirect` | `approach` or `away`. Earlier versions of this page listed `leave`, which has not been seen in a captured post. Treat `leave` like `away` if it appears. | 5.1.1 (`approach`), 5.3.1 (both) |
| `vehicleListType` | Plate list the plate matched (table below). Not sent at all on 5.1.x. | 5.3.1 |
| `PlateConfidence` | Value is in the `count` attribute, on a 0-10000 scale (`count="9900"` = 99%). The element has no text. | 5.3.1 |
| `plateColor` | Numeric code in the `count` attribute (for example `count="3"`), not a color name. The code-to-color mapping is not documented. | 5.3.1 |
| `plateColorRate`, `plateStyle`, `vehiceColor`, `plateAngleH`, `plateAngleV` | Numeric values in the `count` attribute. Meaning not documented. | 5.3.1 |
| `leftTop`, `rightTop`, `leftBottom`, `rightBottom` | Plate corner points, normalized 0-10000. There is no `rect` on IPC plate posts. | 5.3.1 |
| `PlateWidth`, `PlateHeight` | Plate crop size in pixels | 5.3.1 |
| `SourceImageWidth`, `SourceImageHeight` | Full-frame size in pixels | 5.3.1 |
| `province` | Plate region text. Empty in U.S. reads. | 5.3.1 |
| `carAttr/color`, `carAttr/type`, `carAttr/brand`, `carAttr/model` | Vehicle color, type (for example `saloon car`), brand, and model (`Brand_Model` form) | 5.3.1 |
| `carRect` | Vehicle box: `x`, `y`, `width`, `height`. `y` was an empty element. Units not confirmed. | 5.3.1 |
| `listInfo/item[1]/targetImageData` | Plate crop JPEG (base64), `targetType` `car`. About 19 KB of base64 text. | 5.1.1, 5.3.1 |

The post carries no plate group number. Map list names yourself.

**Plate database status (`vehicleListType`):**

| Value | Meaning | Confirmed on |
|-------|---------|--------------|
| `whiteList` | Plate is on the allow list | 5.3.1 |
| `blackList` | Plate is on the block list | 5.3.1 |
| `temporaryList` | Plate is on the temporary list | Not yet confirmed in a captured post |
| *(field absent)* | Plate is on no list. On 5.1.x the field is always absent, even for listed plates. | 5.1.1, 5.3.1 |

Not yet confirmed: plates whose valid date range has expired (allow, block, or temporary) are expected to have `vehicleListType` omitted, so the camera checks date ranges for every list type. Test this on your firmware before you rely on it.

#### Image data

Decode the actual base64 text, and don't size buffers from `targetBase64Length`. On LPR-IP4 firmware 5.3.1 the declared length didn't match the text: the overview declared 770,384 characters and carried about 760,500, and the plate crop declared 19,520 and carried 19,270.

## Firmware Differences

Observed on LPR-IP4 cameras. Behaviour on other models may differ.

| Behaviour | 5.1.1.0 (build 52592) | 5.1.1.0 (build 66800) | 5.3.1 |
|-----------|-----------------------|-----------------------|-------|
| Public API version (`GetDeviceInfo`) | 1.7 | 1.7 | 2.1.0 |
| Plate post layout | V1, config `1.7` | V1, config `1.7` | V1, config `1.7` (also when a V2 row is saved; see [IPC Format (v2.1)](./ipc-http-post-format-v21.md)) |
| `smartType` | `VEHICE` | `VEHICLE` | `VEHICE` |
| `vehicleListType` | Never sent | Never sent | Sent for listed plates (`whiteList`, `blackList`); absent for unlisted plates |
| `vehicleDirect` | `approach` seen on 5.1.1 (build not recorded) | `approach` seen on 5.1.1 (build not recorded) | `approach` and `away` seen |
| `carAttr` vehicle attributes | Not confirmed | Not confirmed | Sent |
| Keepalive body | Not confirmed | Not confirmed | `config` 1.7 + `messageType` `keepalive` + `deviceInfo` |
| `type` attribute names | Not confirmed | Not confirmed | `openAlarmObj`, `subscribeRelationV1` |

Accept both `VEHICE` and `VEHICLE`. The spelling doesn't follow firmware age: 5.3.1 is newer than build 66800 and still sends `VEHICE`.

:::tip Application Guides
For step-by-step setup of IPC webhook events, see [Webhook Event Notification API](/docs/applications/webhook-event-notification-api). For traject-based real-time tracking from IPC, see [Real-Time Object Tracking](/docs/applications/real-time-object-tracking-api). For LPR plate database management, see [LPR Configuration](/docs/api-reference/smart-detection/license-plate-recognition-config).
:::
