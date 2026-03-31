# Viewtron NVR and IP Camera API Guide / Security Camera HTTP Post Webhook Guide

> **Published by CCTV Camera Pros**
> https://www.cctvcamerapros.com
>
> **Technical Contact:** Mike Haldas, Co-Founder CCTV Camera Pros
> 
> **Development & Consultation** mike@viewtron.com | 561-433-8488 ext. 86
> 
> **Python API Server:** https://github.com/mikehaldas/IP-Camera-API
>
> **Support Forum:**
> - [NVR Webhook Setup Guide](https://videos.cctvcamerapros.com/support/topic/setup-nvr-api-webhooks)
> - [NVR API Events Reference](https://videos.cctvcamerapros.com/support/topic/nvr-webhook-api-ai-events)
> - [IP Camera Webhook Setup Guide](https://videos.cctvcamerapros.com/support/topic/ip-camera-api-webbooks)
> - [IP Camera API Events Reference](https://videos.cctvcamerapros.com/support/topic/ai-security-camera-api)

---

## Applicable Products

This API applies to all **Viewtron IP cameras** and **Viewtron NVRs** sold by CCTV Camera Pros. These products have built-in HTTP API support — no additional software licenses or cloud services are required.

| Product Line | Description | Link |
|-------------|-------------|------|
| **Viewtron AI Security Cameras** | IP cameras with built-in AI (human detection, vehicle detection, face detection / facial recognition, license plate recognition, auto-tracking PTZ). All AI inference runs on the camera. | https://www.cctvcamerapros.com/AI-security-cameras-s/1512.htm |
| **Viewtron IP Camera NVRs** | Network video recorders with built-in PoE ports. Record IP cameras, manage AI detection, forward alarm events via HTTP POST, alarm panel input / output. | https://www.cctvcamerapros.com/IP-Camera-NVRs-s/1472.htm |

All Viewtron IP cameras and NVRs are NDAA compliant (safe for US government and federal contractor use).

---

## Table of Contents

- [1. Overview](#1-overview)
  - [1.1 What This API Does](#11-what-this-api-does)
  - [1.2 API Versions](#12-api-versions)
  - [1.3 Authentication](#13-authentication)
  - [1.4 Request Format](#14-request-format)
  - [1.5 Response Format](#15-response-format)
  - [1.6 XML Conventions](#16-xml-conventions)
  - [1.7 Error Codes](#17-error-codes)
- [2. System Commands](#2-system-commands)
  - [GetDeviceInfo](#getdeviceinfo)
  - [GetSupportedAPIs](#getsupportedapis)
  - [GetDiskInfo](#getdiskinfo)
  - [GetChannelList / GetChannelInfo](#getchannellist--getchannelinfo)
  - [GetAlarmInList / GetAlarmInInfo](#getalarminlist--getalarmininfo)
  - [GetAlarmOutList](#getalarmoutlist)
  - [GetDeviceDetail](#getdevicedetail)
  - [GetDateAndTime / SetDateAndTime](#getdateandtime--setdateandtime)
- [3. Image Commands](#3-image-commands)
  - [GetImageConfig / SetImageConfig](#getimageconfig--setimageconfig)
  - [GetSnapshot / GetSnapshotByTime](#getsnapshot--getsnapshotbytime)
  - [GetVideoStreamConfig / SetVideoStreamConfig](#getvideostreamconfig--setvideostreamconfig)
  - [GetStreamCaps](#getstreamcaps)
  - [GetAudioStreamConfig](#getaudiostreamconfig)
  - [GetImageOsdConfig / SetImageOsdConfig](#getimageosdconfig--setimageosdconfig)
  - [GetPrivacyMaskConfig](#getprivacymaskconfig)
- [4. PTZ Commands](#4-ptz-commands)
  - [PtzGetCaps](#ptzgetcaps)
  - [PtzControl](#ptzcontrol)
  - [PtzGotoPreset / PtzGetPresets / PtzAddPreset / PtzDeletePreset](#ptzgotopreset--ptzgetpresets--ptzaddpreset--ptzdeletepreset)
  - [PtzGetCruises / PtzRunCruise / PtzStopCruise](#ptzgetcruises--ptzstopcruise)
- [5. Alarm Commands](#5-alarm-commands)
  - [5.1 Motion Detection](#51-motion-detection)
  - [5.2 Alarm Input/Output](#52-alarm-inputoutput)
  - [5.3 Alarm Status](#53-alarm-status)
  - [5.4 Legacy Alarm Server](#54-legacy-alarm-server)
  - [5.5 HTTP Post Configuration](#55-http-post-configuration)
  - [5.6 Sound-Light Alarm](#56-sound-light-alarm)
- [6. Receiving HTTP POST Events](#6-receiving-http-post-events)
  - [6.1 Overview](#61-overview)
  - [6.2 Quick Reference -- All Detection Types](#62-quick-reference----all-detection-types)
  - [6.3 IPC Format (v1.x)](#63-ipc-format-v1x)
  - [6.4 NVR Format (v2.0)](#64-nvr-format-v20)
  - [6.5 httpPostV2 Data Types](#65-httppostv2-data-types)
  - [6.6 traject -- Real-Time Target Tracking](#66-traject----real-time-target-tracking)
  - [6.7 Image Data Handling](#67-image-data-handling)
  - [6.8 Timestamp Handling](#68-timestamp-handling)
- [7. Playback Commands](#7-playback-commands)
  - [GetRecordType](#getrecordtype)
  - [SearchByTime](#searchbytime)
- [8. Network Commands](#8-network-commands)
  - [GetNetBasicConfig](#getnetbasicconfig)
  - [GetPortConfig](#getportconfig)
- [9. Security Commands](#9-security-commands)
  - [ModifyPassword](#modifypassword)
- [10. Smart Detection Commands](#10-smart-detection-commands)
  - [GetSmartPerimeterConfig](#getsmartperimeterconfig)
  - [GetSmartTripwireConfig](#getsmarttripwireconfig)
  - [GetSmartVfdConfig](#getsmartvfdconfig)
  - [GetSmartVehicleConfig / AddVehiclePlate / GetVehiclePlate](#getsmartvehicleconfig--addvehicleplate--getvehicleplate)
  - [GetSmartAoiEntryConfig / GetSmartAoiLeaveConfig](#getsmartaoientryconfig--getsmartaoileaveconfig)
  - [GetSmartPassLineCountConfig / GetPassLineCountStatistics](#getsmartpasslinecountconfig--getpasslinecountstatistics)
  - [GetSmartVsdConfig](#getsmartvsdconfig)
  - [GetSmartLoiteringConfig](#getsmartloiteringconfig)
  - [GetSmartPvdConfig](#getsmartpvdconfig)
  - [GetMeasureTemperatureConfig](#getmeasuretemperatureconfig)

---

## 1. Overview

### 1.1 What This API Does

Viewtron IP cameras and NVRs expose an HTTP API for programmatic access to device configuration, live video, PTZ control, AI detection settings, alarm management, alarm input / alarm output triggers, and real-time alarm / event webhooks. The API uses XML payloads over HTTP POST requests with Basic Authentication. Used for security camera integrations and applications development.

You can use this API to:

- Query device status and configuration
- Capture snapshots and search recorded video
- Control PTZ cameras (pan, tilt, zoom, presets, cruises)
- Configure AI security camera detection (human detection, car detection, intrusion, line crossing, face detection, LPR, object counting)
- Receive real-time HTTP POST webhooks when AI detections occur (with images)
- Receive continuous real-time target tracking data (`traject`)
- Control alarm outputs (relays)
- Virtial alarm access

### 1.2 API Versions

Viewtron devices ship with one of two firmware generations. The HTTP API protocol is approximately 95% identical between them. This guide documents both versions as a single unified reference, with inline callouts where they differ.

**How to check your version:** Send a `GetDeviceInfo` request. The response includes an `apiVersion` field:

```xml
<apiVersion type="string"><![CDATA[2.0.0]]></apiVersion>
```

If there is no `apiVersion` field, use `GetDeviceDetail` -- the `apiVersion` appears in the `property` block. Devices without either field are running the v1.x protocol.

**Firmware-to-protocol mapping:**

| Firmware | API Protocol | Config Version in XML |
|----------|-------------|----------------------|
| IPC 5.2 or earlier | v1.9 (v1.0 / v1.7) | `1.0` or `1.7` |
| IPC 5.3 or later | v2.0.0 | `2.0.0` |
| NVR 1.4.12 or earlier | v1.9 | `1.0` or `1.7` |
| NVR 1.4.13 or later | v2.0.0 | `2.0.0` |

**What changed in v2.0:**

- `GetDeviceInfo` now includes `apiVersion` and `httpPostVersion` fields directly
- New command: `GetSupportedAPIs` lists all available API endpoints
- `GetChannelList` renamed to `GetChannelInfo` with richer response (channel types, names)
- `GetAlarmInList` renamed to `GetAlarmInInfo` with alarm type classification (local/virtual/remote)
- `GetImageConfig` adds `sharpen`, `denoise`, `backlightCompensation`, `infraredMode` fields
- `GetSnapshotByTime` returns base64 image data in XML (v1.9 returns raw JPEG)
- `GetDiskInfo` adds `storageType` (SD/HDD) and `locked` status
- New command: `TriggerVirtualAlarm` (NVR only)
- New command: `GetAudioStreamConfig`
- New command: `GetPassLineCountStatistics`
- New command: `GetMeasureTemperatureConfig` (thermal cameras)
- New command: `GetVehiclePlate` (query plate database)
- Error codes expanded from 5 to 50+ with descriptive `errorDesc` attribute
- v2.0 responses include `Applicable Products` metadata (IPC, NVR, or both)

After this section, you should not need to think about versions unless you encounter a specific callout.

### 1.3 Authentication

All requests must be authenticated using **Basic Access Authentication** (RFC 2617). Include the `Authorization` header with every request.

```http
POST http://192.168.0.50/GetDeviceInfo HTTP/1.1
Authorization: Basic YWRtaW46MTIzNDU2
```

The value `YWRtaW46MTIzNDU2` is the Base64-encoded string `admin:123456` (username:password).

An unauthenticated request returns:

```http
401 Unauthorized
WWW-Authenticate: Basic realm="XXXXXX"
```

> **v2.0 note:** Some v2.0 devices also support Digest Authentication. Basic Auth works on all versions.

### 1.4 Request Format

All API requests use the **HTTP POST method**. GET also works for read-only commands on most firmware versions, but POST is the documented and recommended method.

**URL format:**

```
http://<host>[:port]/<command>[/channelId][/action]
```

| Component | Description |
|-----------|-------------|
| `host` | IP address or hostname of the device |
| `port` | HTTP port (default 80) |
| `command` | API command name (e.g., `GetDeviceInfo`, `PtzControl`) |
| `channelId` | Channel number (optional, default is `1`). For IPC, can be omitted. |
| `action` | Sub-operation for some commands (e.g., `PtzControl/1/Up`) |

**Request with XML body:**

```http
POST http://192.168.0.50/SetImageConfig HTTP/1.1
Authorization: Basic YWRtaW46MTIzNDU2
Content-Type: application/xml; charset="UTF-8"

<?xml version="1.0" encoding="UTF-8"?>
<config version="1.0" xmlns="http://www.ipc.com/ver10">
  <image>
    <bright>60</bright>
  </image>
</config>
```

For persistent connections, include `Connection: Keep-Alive`.

### 1.5 Response Format

**Successful response with data:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="2.0.0" xmlns="http://www.ipc.com/ver10">
  <deviceInfo>
    <supportTalk type="boolean">true</supportTalk>
  </deviceInfo>
</config>
```

**Successful response (no data):**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config status="success"/>
```

**Error response:**

```xml
<?xml version="1.0" encoding="utf-8" ?>
<config status="failed" errorCode="1" errorDesc="Invalid Request"/>
```

> **v2.0 adds:** The `errorDesc` attribute with human-readable error descriptions. v1.9 returns only the numeric `errorCode`.

### 1.6 XML Conventions

**Element naming:** camelCase (e.g., `deviceName`, `alarmHoldTime`).

**Type attributes:** Each element has a `type` attribute defining its data type:

| Type | Description |
|------|-------------|
| `boolean` | `true` or `false` |
| `int8` / `uint8` | 8-bit signed/unsigned integer |
| `int16` / `uint16` | 16-bit signed/unsigned integer |
| `int32` / `uint32` | 32-bit signed/unsigned integer |
| `int64` / `uint64` | 64-bit signed/unsigned integer |
| `string` | Character string (value wrapped in CDATA) |
| `list` | List of items |

**Numeric elements** may include `min`, `max`, and `default` attributes:

```xml
<bright type="uint8" min="0" max="100" default="50">50</bright>
```

**String elements** may include `minLen`, `maxLen`, `minCharNum`, `maxCharNum` attributes. Values are wrapped in CDATA:

```xml
<ntpServer type="string" minLen="0" maxLen="127">
  <![CDATA[time.windows.com]]>
</ntpServer>
```

**List elements** use `maxCount` for variable-length lists and `count` for the current number of items:

```xml
<content type="list" count="2" maxCount="6">
  <itemType type="string" minLen="0" maxLen="32"/>
  <item><![CDATA[111111]]></item>
  <item><![CDATA[222222]]></item>
</content>
```

**The `types` element:** When basic data types are insufficient, the response defines enum types:

```xml
<types>
  <userType>
    <enum>administrator</enum>
    <enum>advance</enum>
    <enum>normal</enum>
  </userType>
</types>
```

These enums are defined by the device and used as type references elsewhere in the response. Client applications cannot define their own types -- learn them from responses.

> **v2.0 adds:** The `Annotation` convention in documentation: `<!--Required-->`, `<!--Optional-->`, `<!--Dependent-->` comments in XML blocks indicate whether fields are mandatory.

### 1.7 Error Codes

**v1.9 error codes (5 codes):**

| Code | Description |
|------|-------------|
| 1 | **Invalid Request** -- Command name, channel ID, or action name not recognized |
| 2 | **Invalid XML Format** -- XML cannot be parsed |
| 3 | **Invalid XML Content** -- Incomplete message or out-of-range parameters |
| 4 | **Permission Denied** -- User lacks permission |
| 5 | **Network Port Error** -- Network port number error |

**v2.0 error codes (all of the above, plus):**

| Code | Description |
|------|-------------|
| 0 | Successful |
| 5 | **Network Limit** -- Client restricted by blacklist/whitelist |
| 6 | **Sensor ID Error** -- Invalid sensor ID |
| 7 | **System Busy** -- System upgrading or importing config |
| 8 | **Password Expired** -- Change password and retry |
| 9 | **Unauthorized** -- Incorrect username or password |
| 10 | **User Locked** -- User account locked |
| 11 | **Unsupported Function** -- Function not supported |
| 12 | **Channel Error** -- Invalid channel ID |
| 13 | **SD Error** -- SD card status error |
| 14 | **Action Error** -- Invalid action name in URL |
| 15 | **Missing Required Parameters** |
| 16 | **Range Error** -- Parameter value out of range |
| 17 | **Service Not Enabled** -- API service not enabled |
| 18 | **Modification Not Allowed** -- Change would cause system restart |
| 19 | **Over Specifications** -- Exceeding system limits |
| 79 | **Internal Error** -- Device processing error |
| 80 | **Upgrade Error** |
| 81 | **Upgrade Version Same** |
| 82 | **Upgrade Package Error** -- Package doesn't match device |
| 83 | **Upgrade Signature Error** |
| 84 | **Upgrade Incompatible** |

**Audio error codes (v2.0, 101-111):**

| Code | Description |
|------|-------------|
| 101 | Audio Not Working |
| 102 | Audio Param Error |
| 103 | Audio Not PCM |
| 104 | Audio Not Wave |
| 105 | Audio Sampling Rate Error |
| 106 | Audio Save Fail |
| 107 | Audio File Over Limit |
| 108 | Audio File Too Large |
| 109 | Audio File Not Exist |
| 110 | Audio Alarming |
| 111 | Audio File Occupied |

**Face processing error codes (v2.0, 150-159):**

| Code | Description |
|------|-------------|
| 150 | General face processing error |
| 151 | Exceeding maximum face sample library limit |
| 152 | Face picture format not supported |
| 153 | No face or more than one face in the picture |
| 154 | Picture is too large |
| 155 | Same face already exists in face sample library |
| 156 | Face does not exist |
| 157 | Face group already exists |
| 158 | Exceeding maximum face groups limit |
| 159 | Face group does not exist |

**License plate processing error codes (v2.0, 201-207):**

| Code | Description |
|------|-------------|
| 201 | General license plate processing error |
| 202 | Exceeding maximum license plate library limit |
| 203 | Same license plate already exists |
| 204 | License plate not exist |
| 205 | License plate group already exists |
| 206 | Exceeding maximum license plate groups limit |
| 207 | License plate does not exist |

---

## 2. System Commands

### GetDeviceInfo

Retrieves basic information about the device including model, firmware version, MAC address, capabilities, and API version.

| Field | Value |
|-------|-------|
| **URL** | `POST` or `GET http://<host>[:port]/GetDeviceInfo` |
| **Products** | IPC, NVR |
| **Entity Data** | None |

> Tested: IPC v1.9 (firmware 5.1.4.0), NVR v2.0 (firmware 1.4.13)

**Response (v2.0 IPC):**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="2.0.0" xmlns="http://www.ipc.com/ver10">
  <deviceInfo>
    <deviceName type="string"><![CDATA[IPC]]></deviceName>
    <deviceDescription type="string"><![CDATA[E4_4MP_]]></deviceDescription>
    <apiVersion type="string"><![CDATA[2.0.0]]></apiVersion>
    <softwareVersion type="string">
      <![CDATA[5.3.0.12288B240820.IG1.U1(08A10).beta]]>
    </softwareVersion>
    <softwareBuildDate type="string"><![CDATA[2024-10-31]]></softwareBuildDate>
    <kernelVersion type="string"><![CDATA[20241010]]></kernelVersion>
    <hardwareVersion type="string"><![CDATA[1.5]]></hardwareVersion>
    <model type="string"><![CDATA[E4_4MP_]]></model>
    <brand type="string"><![CDATA[Customer]]></brand>
    <mac type="string"><![CDATA[70:ab:c8:1b:5d:dc]]></mac>
    <sn type="string"><![CDATA[2E323D9463D5]]></sn>
    <chlMaxCount type="uint32">1</chlMaxCount>
    <audioInCount type="uint32">2</audioInCount>
    <audioOutCount type="uint32">1</audioOutCount>
    <alarmInCount type="uint32">1</alarmInCount>
    <alarmOutCount type="uint32">1</alarmOutCount>
    <integratedPtz type="boolean">false</integratedPtz>
    <supportRS485Ptz type="boolean">false</supportRS485Ptz>
    <supportSDCard type="boolean">true</supportSDCard>
  </deviceInfo>
</config>
```

**Response (v2.0 NVR):**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="2.0.0" xmlns="http://www.ipc.com/ver10">
  <deviceInfo>
    <deviceName type="string"><![CDATA[Device Name]]></deviceName>
    <apiVersion type="string"><![CDATA[2.0.0]]></apiVersion>
    <model type="string"><![CDATA[TD-3308H1-8P-B1]]></model>
    <brand type="string"><![CDATA[IP CAM]]></brand>
    <deviceDescription type="string"><![CDATA[TD-3308H1-8P-B1]]></deviceDescription>
    <audioInCount type="uint32">0</audioInCount>
    <audioOutCount type="uint32">1</audioOutCount>
    <integratedPtz type="boolean">true</integratedPtz>
    <supportRS485Ptz type="boolean">true</supportRS485Ptz>
    <supportSDCard type="boolean">false</supportSDCard>
    <alarmInCount type="uint32">16</alarmInCount>
    <alarmOutCount type="uint32">4</alarmOutCount>
    <softwareVersion type="string">
      <![CDATA[1.4.12.71946B240815.N0W.U1(8A418).beta]]>
    </softwareVersion>
    <softwareBuildDate type="string">
      <![CDATA[1.4.12.69452B240510.N2P.U1(16A840).beta]]>
    </softwareBuildDate>
    <kernelVersion type="string"><![CDATA[N8G8-N38C-O5A5]]></kernelVersion>
    <hardwareVersion type="string"><![CDATA[300112-V1]]></hardwareVersion>
    <mac type="string"><![CDATA[00:18:ae:00:88:15]]></mac>
    <sn type="string"><![CDATA[N018AEA8A9C2]]></sn>
    <chlMaxCount type="uint32">8</chlMaxCount>
  </deviceInfo>
</config>
```

**Response (v1.9 IPC):**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="1.0" xmlns="http://www.ipc.com/ver10">
  <deviceInfo>
    <deviceName type="string"><![CDATA[212]]></deviceName>
    <model type="string"><![CDATA[TD-9421M]]></model>
    <brand type="string"><![CDATA[IPC]]></brand>
    <deviceDescription type="string"><![CDATA[IPCamera]]></deviceDescription>
    <audioInCount type="uint32">1</audioInCount>
    <audioOutCount type="uint32">1</audioOutCount>
    <integratedPtz type="boolean">true</integratedPtz>
    <supportRS485Ptz type="boolean">false</supportRS485Ptz>
    <supportSDCard type="boolean">true</supportSDCard>
    <alarmInCount type="uint32">1</alarmInCount>
    <alarmOutCount type="uint32">1</alarmOutCount>
    <softwareVersion type="string"><![CDATA[4.0.0 beta1]]></softwareVersion>
    <softwareBuildDate type="string"><![CDATA[2013-12-24]]></softwareBuildDate>
    <kernelVersion type="string"><![CDATA[20111010]]></kernelVersion>
    <hardwareVersion type="string"><![CDATA[1.3]]></hardwareVersion>
    <mac type="string"><![CDATA[00:18:ae:98:38:fd]]></mac>
    <sn type="string"><![CDATA[2E323D9463D5]]></sn>
    <chlMaxCount type="uint32">9</chlMaxCount>
  </deviceInfo>
</config>
```

**Notes:**
- Use `apiVersion` to determine which protocol version the device supports.
- For fixed-channel devices (IPC, DVR): `audioInCount`, `audioOutCount`, `alarmInCount`, `alarmOutCount` are always included.
- For variable-channel devices (NVR): These may be optional. Use `GetChannelInfo`/`GetAlarmInInfo` for details.

> **v2.0 adds:** `apiVersion`, `httpPostVersion` fields directly in the response.

---

### GetSupportedAPIs

Retrieves the list of all API endpoints supported by the device.

| Field | Value |
|-------|-------|
| **URL** | `POST` or `GET http://<host>[:port]/GetSupportedAPIs` |
| **Products** | IPC, NVR |
| **Entity Data** | None |

> **v2.0 only.** This command does not exist on v1.9 firmware.

**Response:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="2.0.0" xmlns="http://www.ipc.com/ver10">
  <applicationInterfaces type="list" count="99">
    <itemType type="string" maxLen="63"/>
    <item><![CDATA[GetSupportedAPIs]]></item>
    <item><![CDATA[GetAlarmInInfo]]></item>
    <item><![CDATA[GetAlarmOutList]]></item>
    <item><![CDATA[GetAlarmStatus]]></item>
    <item><![CDATA[GetChannelInfo]]></item>
    <item><![CDATA[GetDeviceDetail]]></item>
    <item><![CDATA[GetDeviceInfo]]></item>
    <item><![CDATA[GetDiskInfo]]></item>
    <!-- ... additional APIs ... -->
  </applicationInterfaces>
</config>
```

**Notes:**
- Use the API names in each `<item>` to look up commands in this document.

---

### GetDiskInfo

Retrieves disk/storage information.

| Field | Value |
|-------|-------|
| **URL** | `POST` or `GET http://<host>[:port]/GetDiskInfo` |
| **Products** | IPC, NVR |
| **Entity Data** | None |

**Response (v2.0 IPC):**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="2.0.0" xmlns="http://www.ipc.com/ver10">
  <types>
    <diskStatus>
      <enum>read</enum>
      <enum>read/write</enum>
      <enum>unformat</enum>
      <enum>formatting</enum>
      <enum>exception</enum>
      <enum>locked</enum>
    </diskStatus>
  </types>
  <diskInfo type="list" count="1">
    <item>
      <id type="string"><![CDATA[disk1]]></id>
      <totalSpace type="uint32">30371</totalSpace>
      <freeSpace type="uint32">0</freeSpace>
      <imageFreeSpace type="uint32">2985</imageFreeSpace>
      <status type="diskStatus">read/write</status>
      <storageType type="diskType">SD</storageType>
    </item>
  </diskInfo>
</config>
```

**Response (v1.9):**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="1.0" xmlns="http://www.ipc.com/ver10">
  <types>
    <diskStatus>
      <enum>read</enum>
      <enum>read/write</enum>
      <enum>unformat</enum>
      <enum>formatting</enum>
      <enum>exception</enum>
    </diskStatus>
  </types>
  <diskInfo type="list" count="1">
    <item>
      <id type="string"><![CDATA[{5B457B2A-D467-834E-B1E8-22F3450DA873}]]></id>
      <totalSpace type="uint32">953869</totalSpace>
      <freeSpace type="uint32">847872</freeSpace>
      <imageFreeSpace type="uint32">847872</imageFreeSpace>
      <diskStatus type="diskStatus">read/write</diskStatus>
    </item>
  </diskInfo>
</config>
```

**Notes:**
- `totalSpace` and `freeSpace` are in megabytes (MB).
- If no disk is present, the `diskInfo` node will be empty.
- `imageFreeSpace` is IPC only.

> **v2.0 adds:** `storageType` (SD/HDD) and `locked` disk status.

---

### GetChannelList / GetChannelInfo

Retrieves the channel list from the device.

| Field | Value |
|-------|-------|
| **URL (v1.9)** | `POST` or `GET http://<host>[:port]/GetChannelList` |
| **URL (v2.0)** | `POST` or `GET http://<host>[:port]/GetChannelInfo` |
| **Products** | NVR (v1.9), IPC + NVR (v2.0) |
| **Entity Data** | None |

**Response (v2.0 -- GetChannelInfo):**

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

**Response (v1.9 -- GetChannelList, NVR only):**

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

**Notes:**
- v1.9 `GetChannelList` is NVR only. If `deviceDescription` equals `IPCamera`, do not send this command.
- Channel ID starts from 1.

> **v2.0 adds:** Channel names, channel types (Normal, Thermal, Fisheye, etc.), and works on both IPC and NVR.

---

### GetAlarmInList / GetAlarmInInfo

Retrieves the alarm input list.

| Field | Value |
|-------|-------|
| **URL (v1.9)** | `POST` or `GET http://<host>[:port]/GetAlarmInList` |
| **URL (v2.0)** | `POST` or `GET http://<host>[:port]/GetAlarmInInfo` |
| **Products** | NVR (v1.9), IPC + NVR (v2.0) |
| **Entity Data** | None |

**Response (v2.0 -- GetAlarmInInfo):**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="2.0.0" xmlns="http://www.ipc.com/ver10">
  <types>
    <alarmType>
      <enum>local</enum>
      <enum>virtual</enum>
      <enum>remote</enum>
    </alarmType>
  </types>
  <alarmInInfoList type="list" count="1">
    <item>
      <id type="uint32">1</id>
      <alarmInType type="alarmType">local</alarmInType>
    </item>
  </alarmInInfoList>
</config>
```

**Response (v1.9 -- GetAlarmInList, NVR only):**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="1.0" xmlns="http://www.ipc.com/ver10">
  <alarmInIDList type="list" count="8"></alarmInIDList>
  <itemType type="string" maxLen="20"/>
  <item>1</item>
  <item>2</item>
  <!-- ... up to 8 items ... -->
</config>
```

> **v2.0 adds:** Alarm type classification (local, virtual, remote). Virtual alarms are used by NVRs for `TriggerVirtualAlarm`.

---

### GetAlarmOutList

Retrieves the alarm output list. **NVR only.**

| Field | Value |
|-------|-------|
| **URL** | `POST` or `GET http://<host>[:port]/GetAlarmOutList` |
| **Products** | NVR |
| **Entity Data** | None |

> **v1.9 only.** On v2.0 devices, use `GetAlarmInInfo` which returns both input and output information, or check `alarmOutCount` in `GetDeviceInfo`.

**Response:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="1.0" xmlns="http://www.ipc.com/ver10">
  <alarmOutIDList type="list" count="4"></alarmOutIDList>
  <itemType type="string" maxLen="20"/>
  <item>1</item>
  <item>2</item>
  <item>3</item>
  <item>4</item>
</config>
```

---

### GetDeviceDetail

Retrieves detailed device information including smart feature support flags. **IPC only.**

| Field | Value |
|-------|-------|
| **URL** | `POST` or `GET http://<host>[:port]/GetDeviceDetail` |
| **Products** | IPC |
| **Entity Data** | None |

**Response:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="1.0" xmlns="http://www.ipc.com/ver10">
  <detail>
    <property>
      <deviceName type="string"><![CDATA[IPC]]></deviceName>
      <deviceDescription type="string"><![CDATA[IPCamera]]></deviceDescription>
      <model type="string"><![CDATA[TD-9421M]]></model>
      <brand type="string"><![CDATA[IPC]]></brand>
      <sn type="string"><![CDATA[2E323D9463D5]]></sn>
      <mac type="string"><![CDATA[00:18:ae:98:38:fd]]></mac>
      <softwareVersion type="string"><![CDATA[4.0.0 beta1]]></softwareVersion>
      <softwareBuildDate type="string"><![CDATA[2013-12-24]]></softwareBuildDate>
      <kernelVersion type="string"><![CDATA[20111010]]></kernelVersion>
      <hardwareVersion type="string"><![CDATA[1.3]]></hardwareVersion>
      <apiVersion type="string"><![CDATA[1.7]]></apiVersion>
    </property>
    <smart>
      <supportTripwire type="boolean">false</supportTripwire>
      <supportPerimeter type="boolean">false</supportPerimeter>
      <supportOsc type="boolean">false</supportOsc>
      <supportAvd type="boolean">false</supportAvd>
      <supportVfd type="boolean">false</supportVfd>
      <supportCpc type="boolean">false</supportCpc>
      <supportCdd type="boolean">false</supportCdd>
      <supportIpd type="boolean">false</supportIpd>
      <supportVfdMatch type="boolean">false</supportVfdMatch>
      <supportvehicle type="boolean">false</supportvehicle>
      <supportAoiEntry type="boolean">false</supportAoiEntry>
      <supportAoiLeave type="boolean">false</supportAoiLeave>
      <supportPassLineCount type="boolean">false</supportPassLineCount>
      <supportThermal type="boolean">false</supportThermal>
      <supportTraffic type="boolean">false</supportTraffic>
      <supportHeatMap type="boolean">false</supportHeatMap>
      <supportVsd type="boolean">false</supportVsd>
      <supportAsd type="boolean">false</supportAsd>
      <supportPvd type="boolean">false</supportPvd>
      <supportLoitering type="boolean">false</supportLoitering>
    </smart>
    <image>
      <supportAZ type="boolean">true</supportAZ>
      <supportROI type="boolean">true</supportROI>
      <supportInfraredLamp type="boolean">false</supportInfraredLamp>
      <supportWatermark type="boolean">true</supportWatermark>
      <supportPrivateMask type="boolean">true</supportPrivateMask>
    </image>
    <alarm>
      <supportMultiMotionSensitivity type="boolean">false</supportMultiMotionSensitivity>
      <supportAlarmServer type="boolean">false</supportAlarmServer>
      <alarmInCount type="uint32">1</alarmInCount>
      <alarmOutCount type="uint32">1</alarmOutCount>
      <supportAudioAlarmOut type="boolean">false</supportAudioAlarmOut>
      <supportWhiteLightAlarmOut type="boolean">false</supportWhiteLightAlarmOut>
    </alarm>
    <system>
      <supportSnmp type="boolean">true</supportSnmp>
      <audioInCount type="uint32">1</audioInCount>
      <audioOutCount type="uint32">1</audioOutCount>
      <integratedPtz type="boolean">true</integratedPtz>
      <supportRS485Ptz type="boolean">false</supportRS485Ptz>
      <supportSDCard type="boolean">true</supportSDCard>
      <chlMaxCount type="uint32">9</chlMaxCount>
    </system>
  </detail>
</config>
```

**Smart feature abbreviations:**

| Abbreviation | Feature |
|--------------|---------|
| `tripwire` | Line Crossing Detection |
| `perimeter` | Intrusion / Perimeter Detection |
| `osc` | Object Status Change (left/missing) |
| `avd` | Audio/Video Diagnostics |
| `vfd` | Face Detection |
| `vfdMatch` | Face Recognition / Match |
| `vehicle` | License Plate Recognition |
| `aoiEntry` / `aoiLeave` | Region Entry/Exit |
| `passLineCount` | Object Counting by Line |
| `traffic` | Object Counting by Area |
| `vsd` | Video Metadata Detection |
| `pvd` | Illegal Parking Detection |
| `loitering` | Loitering Detection |
| `thermal` | Thermal Temperature Measurement |
| `heatMap` | Heat Map |
| `asd` | Audio Abnormal Detection |
| `cpc` | People Counting |
| `cdd` | Crowd Density Detection |

---

### GetDateAndTime / SetDateAndTime

Get or set the system date, time, timezone, and NTP configuration.

| Field | Value |
|-------|-------|
| **URL** | `POST` or `GET http://<host>[:port]/GetDateAndTime` |
| **URL** | `POST http://<host>[:port]/SetDateAndTime` |
| **Products** | IPC, NVR |
| **Entity Data** | None (Get) / `time` element (Set) |

**GetDateAndTime Response (v2.0):**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="2.0.0" xmlns="http://www.ipc.com/ver10">
  <types>
    <timeFormatModeType>
      <enum>12h</enum>
      <enum>24h</enum>
    </timeFormatModeType>
  </types>
  <time>
    <timezoneInfo>
      <timeZone type="string"><![CDATA[CST-8]]></timeZone>
    </timezoneInfo>
    <synchronizeInfo>
      <type type="timeFormatModeType">NTP</type>
      <ntpServer type="string" maxLen="127"><![CDATA[time.windows.com]]></ntpServer>
      <ntpSyncInterval type="uint32" min="30" max="10080">1440</ntpSyncInterval>
      <currentTime type="string"><![CDATA[2024-08-21 15:05:31]]></currentTime>
    </synchronizeInfo>
  </time>
</config>
```

**GetDateAndTime Response (v1.9):**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="1.7" xmlns="http://www.ipc.com/ver10">
  <types>
    <synchronizeType>
      <enum>manually</enum>
      <enum>NTP</enum>
      <enum>PC</enum>
    </synchronizeType>
    <timeFormatModeType>
      <enum>12h</enum>
      <enum>24h</enum>
    </timeFormatModeType>
  </types>
  <time>
    <timeFormatMode type="timeFormatModeType">24h</timeFormatMode>
    <timezoneInfo>
      <timeZone type="string" maxLen="127"><![CDATA[CST-8]]></timeZone>
      <startTime type="string" maxLen="64"><![CDATA[M1.1.0/0]]></startTime>
      <endTime type="string" maxLen="64"><![CDATA[M2.1.1/0]]></endTime>
      <offSet type="uint16" min="30" max="120">120</offSet>
      <daylightSwitch type="uint32">0</daylightSwitch>
    </timezoneInfo>
    <synchronizeInfo>
      <type type="synchronizeType">manually</type>
      <ntpServer type="string" maxLen="127"><![CDATA[time.windows.com]]></ntpServer>
      <ntpSyncInterval type="uint32" min="30" max="10080">1440</ntpSyncInterval>
      <currentTime type="string"><![CDATA[2021-04-15 11:50:18]]></currentTime>
    </synchronizeInfo>
  </time>
</config>
```

**SetDateAndTime Request (v2.0):**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="2.0.0" xmlns="http://www.ipc.com/ver10">
  <time>
    <timezoneInfo>
      <timeZone><![CDATA[CST-8]]></timeZone>
    </timezoneInfo>
    <synchronizeInfo>
      <type>manually</type>
      <currentTime><![CDATA[2024-08-21 15:05:31]]></currentTime>
    </synchronizeInfo>
  </time>
</config>
```

---

## 3. Image Commands

### GetImageConfig / SetImageConfig

Get or set image parameters (brightness, contrast, saturation, etc.).

| Field | Value |
|-------|-------|
| **URL** | `POST` or `GET http://<host>[:port]/GetImageConfig[/channelId]` |
| **URL** | `POST http://<host>[:port]/SetImageConfig[/channelId]` |
| **Products** | IPC, NVR |
| **Channel ID** | Optional (default 1) |

**Response (v2.0):**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="2.0.0" xmlns="http://www.ipc.com/ver10">
  <types>
    <IRCutMode>
      <enum>auto</enum>
      <enum>day</enum>
      <enum>night</enum>
      <enum>time</enum>
      <enum>alarmInLink</enum>
    </IRCutMode>
    <whitebalanceMode>
      <enum>auto</enum>
      <enum>indoor</enum>
      <enum>outdoor</enum>
      <enum>manual</enum>
    </whitebalanceMode>
    <BLCMode>
      <enum>OFF</enum>
      <enum>HWDR</enum>
      <enum>HLC</enum>
      <enum>BLC</enum>
    </BLCMode>
  </types>
  <cfgFile type="configFileType" default="normal">normal</cfgFile>
  <image>
    <bright type="uint8" min="0" max="100" default="50">50</bright>
    <saturation type="uint8" min="0" max="100" default="50">50</saturation>
    <contrast type="uint8" min="0" max="100" default="50">50</contrast>
    <hue type="uint8" min="0" max="100" default="50">50</hue>
    <mirrorSwitch type="boolean" default="false">false</mirrorSwitch>
    <flipSwitch type="boolean" default="false">true</flipSwitch>
    <IRCutMode type="IRCutMode" default="auto">auto</IRCutMode>
    <whiteBalance>
      <mode type="whitebalanceMode" default="auto">auto</mode>
      <red min="0" max="100" default="50">50</red>
      <blue min="0" max="100" default="50">50</blue>
    </whiteBalance>
    <backlightCompensation>
      <mode type="BLCMode" default="OFF">OFF</mode>
    </backlightCompensation>
    <infraredMode type="infraredModeE" default="auto">auto</infraredMode>
  </image>
</config>
```

**Response (v1.9):**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="1.0" xmlns="http://www.ipc.com/ver10">
  <types>
    <frequency>
      <enum>60HZ</enum>
      <enum>50HZ</enum>
    </frequency>
    <whitebalanceMode>
      <enum>auto</enum>
      <enum>manual</enum>
      <enum>outdoor</enum>
      <enum>indoor</enum>
    </whitebalanceMode>
    <IRCutMode>
      <enum>auto</enum>
      <enum>day</enum>
      <enum>night</enum>
    </IRCutMode>
  </types>
  <image>
    <frequency type="frequency" default="50HZ">50HZ</frequency>
    <bright type="uint8" min="0" max="100" default="50">50</bright>
    <contrast type="uint8" min="0" max="100" default="55">55</contrast>
    <hue type="uint8" min="0" max="100" default="50">50</hue>
    <saturation type="uint8" min="0" max="100" default="50">50</saturation>
    <mirrorSwitch type="boolean" default="false">false</mirrorSwitch>
    <flipSwitch type="boolean" default="false">false</flipSwitch>
    <WDR>
      <switch type="boolean" default="false">false</switch>
      <value type="uint8" default="128">128</value>
    </WDR>
    <whiteBalance>
      <mode type="whitebalanceMode" default="auto">auto</mode>
      <red type="uint32" min="0" max="100" default="50">50</red>
      <blue type="uint32" min="0" max="100" default="50">50</blue>
    </whiteBalance>
    <IRCutMode type="IRCutMode" default="auto">auto</IRCutMode>
  </image>
</config>
```

> **v2.0 adds:** `sharpen`, `denoise`, `backlightCompensation` (with HWDR/HLC/BLC modes), `infraredMode`, `cfgFile` (normal/day/night config files), and `rebootPrompt` in Set requests.

**SetImageConfig example (partial update):**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="2.0.0" xmlns="http://www.ipc.com/ver10">
  <image>
    <bright>60</bright>
  </image>
</config>
```

This API supports partial parameter updates -- unspecified parameters remain unchanged.

---

### GetSnapshot / GetSnapshotByTime

Capture a live snapshot or retrieve a stored image by time.

| Field | Value |
|-------|-------|
| **URL** | `POST` or `GET http://<host>[:port]/GetSnapshot[/channelId]` |
| **URL** | `POST http://<host>[:port]/GetSnapshotByTime[/channelId]` |
| **Products** | IPC, NVR |
| **Channel ID** | Optional (default 1) |

**GetSnapshot** returns a JPEG-encoded image directly (check `Content-Type` header).

**GetSnapshotByTime request:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="2.0.0" xmlns="http://www.ipc.com/ver10">
  <search>
    <time><![CDATA[2024-08-23 15:07:28]]></time>
    <length>10</length>
  </search>
</config>
```

> **v2.0 difference:** Returns base64-encoded image in XML (`downloadOneImage/sourceBase64Data`). v1.9 may return raw JPEG or H.264/H.265 key frame data.

---

### GetVideoStreamConfig / SetVideoStreamConfig

Get or set video stream parameters (resolution, encoding, bitrate, GOP).

| Field | Value |
|-------|-------|
| **URL** | `POST` or `GET http://<host>[:port]/GetVideoStreamConfig[/channelId]` |
| **URL** | `POST http://<host>[:port]/SetVideoStreamConfig[/channelId]` |
| **Products** | IPC, NVR |
| **Channel ID** | Optional (default 1) |

**Response:**

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

**Notes:**
- `id="1"` is main stream, `id="2"` is sub stream.
- `maxBitRate` is in kbps.
- RTSP stream URL for NVR: `rtsp://<host>[:port]?chID=<channelId>&streamType=<main|sub>`
- RTSP stream URL for IPC: `rtsp://<host>[:port]/<streamName>`

---

### GetStreamCaps

Retrieves stream capabilities (supported resolutions, encoding types, frame rates).

| Field | Value |
|-------|-------|
| **URL** | `POST` or `GET http://<host>[:port]/GetStreamCaps[/channelId]` |
| **Products** | IPC, NVR |
| **Channel ID** | Optional (default 1) |

> **v1.9 only.** On v2.0 devices, stream capabilities are embedded in `GetVideoStreamConfig` response attributes.

**Response:**

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

---

### GetAudioStreamConfig

Retrieves audio stream configuration.

| Field | Value |
|-------|-------|
| **URL** | `POST` or `GET http://<host>[:port]/GetAudioStreamConfig[/channelId]` |
| **Products** | IPC, NVR |
| **Channel ID** | Optional (default 1) |

> **v2.0 only.**

**Response:**

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

---

### GetImageOsdConfig / SetImageOsdConfig

Get or set OSD (On-Screen Display) text overlay configuration.

| Field | Value |
|-------|-------|
| **URL** | `POST` or `GET http://<host>[:port]/GetImageOsdConfig[/channelId]` |
| **URL** | `POST http://<host>[:port]/SetImageOsdConfig[/channelId]` |
| **Products** | IPC |
| **Channel ID** | Optional (default 1) |

> **v1.9 only.**

**Response:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="1.0" xmlns="http://www.ipc.com/ver10">
  <types>
    <dateFormat>
      <enum>year-month-day</enum>
      <enum>month-day-year</enum>
      <enum>day-month-year</enum>
    </dateFormat>
  </types>
  <imageOsd>
    <time>
      <switch type="boolean">true</switch>
      <X type="uint32">0</X>
      <Y type="uint32">0</Y>
      <dateFormat type="dateFormat">year-month-day</dateFormat>
    </time>
    <channelName>
      <switch type="boolean">false</switch>
      <X type="uint32">0</X>
      <Y type="uint32">0</Y>
      <name type="string" maxLen="19"><![CDATA[name]]></name>
    </channelName>
  </imageOsd>
</config>
```

**Notes:** X and Y coordinates use a 10000x10000 normalized grid.

---

### GetPrivacyMaskConfig

Retrieves privacy mask configuration.

| Field | Value |
|-------|-------|
| **URL** | `POST` or `GET http://<host>[:port]/GetPrivacyMaskConfig[/channelId]` |
| **Products** | IPC |
| **Channel ID** | Optional (default 1) |

> **v1.9 only.**

**Response:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="1.0" xmlns="http://www.ipc.com/ver10">
  <types>
    <color>
      <enum>black</enum>
      <enum>white</enum>
      <enum>gray</enum>
    </color>
  </types>
  <privacyMask type="list" count="4">
    <itemType>
      <switch type="boolean"/>
      <rectangle>
        <X type="uint32"/>
        <Y type="uint32"/>
        <width type="uint32"/>
        <height type="uint32"/>
      </rectangle>
      <color type="color"/>
    </itemType>
    <item>
      <switch>false</switch>
      <rectangle>
        <X>0</X>
        <Y>0</Y>
        <width>0</width>
        <height>0</height>
      </rectangle>
      <color>black</color>
    </item>
  </privacyMask>
</config>
```

**Notes:** X and Y coordinates use a 640x480 grid.

---

## 4. PTZ Commands

### PtzGetCaps

Retrieves PTZ capabilities (speed range, preset count, cruise limits).

| Field | Value |
|-------|-------|
| **URL** | `POST` or `GET http://<host>[:port]/PtzGetCaps[/channelId]` |
| **Products** | IPC, NVR |
| **Channel ID** | Optional (default 1) |

**Response:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="2.0.0" xmlns="http://www.ipc.com/ver10">
  <caps>
    <controlMinSpeed type="uint32">1</controlMinSpeed>
    <controlMaxSpeed type="uint32">8</controlMaxSpeed>
    <presetMaxCount type="uint32">255</presetMaxCount>
    <cruiseMaxCount type="uint32">8</cruiseMaxCount>
    <cruisePresetMinSpeed type="uint32">1</cruisePresetMinSpeed>
    <cruisePresetMaxSpeed type="uint32">8</cruisePresetMaxSpeed>
    <cruisePresetMaxHoldTime type="uint32">240</cruisePresetMaxHoldTime>
    <cruisePresetMaxCount type="uint32">16</cruisePresetMaxCount>
  </caps>
</config>
```

---

### PtzControl

Controls PTZ movement.

| Field | Value |
|-------|-------|
| **URL** | `POST http://<host>[:port]/PtzControl[/channelId]/<action>` |
| **Products** | IPC, NVR |
| **Channel ID** | Optional (default 1) |
| **Action** | Movement command (see below) |

**Available actions:** `Up`, `Down`, `Left`, `Right`, `LeftUp`, `LeftDown`, `RightUp`, `RightDown`, `Near`, `Far`, `ZoomIn`, `ZoomOut`, `IrisOpen`, `IrisClose`, `Stop`

**Request:**

```xml
<?xml version="1.0" encoding="utf-8"?>
<actionInfo version="1.0" xmlns="http://www.ipc.com/ver10">
  <speed>4</speed>
</actionInfo>
```

---

### PtzGotoPreset / PtzGetPresets / PtzAddPreset / PtzDeletePreset

Manage and navigate to PTZ presets.

| Command | URL | Method | Entity Data |
|---------|-----|--------|-------------|
| **PtzGotoPreset** | `/PtzGotoPreset[/channelId]` | POST | Preset ID |
| **PtzGetPresets** | `/PtzGetPresets[/channelId]` | POST/GET | None |
| **PtzAddPreset** | `/PtzAddPreset[/channelId]` | POST | Preset name |
| **PtzDeletePreset** | `/PtzDeletePreset[/channelId]` | POST | Preset ID |

**Products:** IPC, NVR

**PtzGotoPreset request:**

```xml
<?xml version="1.0" encoding="utf-8"?>
<presetInfo version="1.0" xmlns="http://www.ipc.com/ver10">
  <id>2</id>
</presetInfo>
```

**PtzAddPreset request:**

```xml
<?xml version="1.0" encoding="utf-8"?>
<presetInfo version="1.0" xmlns="http://www.ipc.com/ver10">
  <name><![CDATA[preset1]]></name>
</presetInfo>
```

**PtzGetPresets response:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="1.0" xmlns="http://www.ipc.com/ver10">
  <presetInfo type="list" maxCount="360">
    <itemType type="string" maxLen="10"></itemType>
    <item id="1"><![CDATA[DDD]]></item>
  </presetInfo>
</config>
```

---

### PtzGetCruises / PtzRunCruise / PtzStopCruise

Manage PTZ cruise tours.

| Command | URL | Method | Entity Data |
|---------|-----|--------|-------------|
| **PtzGetCruises** | `/PtzGetCruises[/channelId]` | POST/GET | None |
| **PtzRunCruise** | `/PtzRunCruise[/channelId]` | POST | Cruise ID |
| **PtzStopCruise** | `/PtzStopCruise[/channelId]` | POST | None |

**Products:** IPC, NVR

---

## 5. Alarm Commands

### 5.1 Motion Detection

#### GetMotionConfig / SetMotionConfig

Get or set motion detection configuration.

| Field | Value |
|-------|-------|
| **URL** | `POST` or `GET http://<host>[:port]/GetMotionConfig[/channelId]` |
| **URL** | `POST http://<host>[:port]/SetMotionConfig[/channelId]` |
| **Products** | IPC, NVR |
| **Channel ID** | Optional (default 1) |

> **Note:** `SetMotionConfig` is documented for v1.9 only. On v2.0 devices, motion configuration may need to be set through the web interface.

**Response:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="1.0" xmlns="http://www.ipc.com/ver10">
  <motion>
    <switch type="boolean">false</switch>
    <sensitivity type="int32" min="0" max="8">4</sensitivity>
    <alarmHoldTime type="uint32">20</alarmHoldTime>
    <area type="list" count="18">
      <itemType type="string" minLen="22" maxLen="22"></itemType>
      <item><![CDATA[1111111111111111111111]]></item>
      <item><![CDATA[1111111111111111111111]]></item>
      <!-- ... 18 items total ... -->
    </area>
    <triggerAlarmOut type="list" count="1">
      <itemType type="boolean"></itemType>
      <item id="1">false</item>
    </triggerAlarmOut>
  </motion>
</config>
```

**Notes:** The `area` element is a 22x18 grid. Each character `1` = detection enabled, `0` = disabled.

---

### 5.2 Alarm Input/Output

#### GetAlarmInConfig

Retrieves alarm input configuration.

| Field | Value |
|-------|-------|
| **URL** | `POST` or `GET http://<host>[:port]/GetAlarmInConfig[/channelId]` |
| **Products** | IPC, NVR |

**Response:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="1.0" xmlns="http://www.ipc.com/ver10">
  <types>
    <alarmInVoltage>
      <enum>NO</enum>
      <enum>NC</enum>
    </alarmInVoltage>
  </types>
  <sensor>
    <id type="uint32">1</id>
    <sensorName type="string" maxLen="11"><![CDATA[Sensor1]]></sensorName>
    <switch type="boolean">true</switch>
    <voltage type="alarmInVoltage">NO</voltage>
    <alarmHoldTime type="uint32">10</alarmHoldTime>
    <triggerAlarmOut type="list" count="1">
      <itemType type="boolean"></itemType>
      <item id="1">true</item>
    </triggerAlarmOut>
  </sensor>
</config>
```

#### GetAlarmOutConfig

Retrieves alarm output configuration.

| Field | Value |
|-------|-------|
| **URL** | `POST` or `GET http://<host>[:port]/GetAlarmOutConfig[/channelId]` |
| **Products** | IPC, NVR |

#### ManualAlarmOut

Manually triggers or releases an alarm output (relay).

| Field | Value |
|-------|-------|
| **URL** | `POST http://<host>[:port]/ManualAlarmOut[/channelId]` |
| **Products** | IPC, NVR |

**Request:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="1.0" xmlns="http://www.ipc.com/ver10">
  <action>
    <status>true</status>
  </action>
</config>
```

> **Known firmware bug (IPC):** The camera forcibly resets the alarm output when a perimeter alarm cycle ends, even when alarm output mode is set to `manual_alarm` and `triggerAlarmOut` is unchecked. This makes `ManualAlarmOut` unreliable for automation while perimeter detection is active.

---

### 5.3 Alarm Status

#### GetAlarmStatus

Retrieves the current alarm trigger status for all detection types.

| Field | Value |
|-------|-------|
| **URL** | `POST` or `GET http://<host>[:port]/GetAlarmStatus` |
| **Products** | IPC, NVR |
| **Entity Data** | None |

> Tested: IPC v1.9 (firmware 5.1.4.0)

**Response:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="1.0" xmlns="http://www.ipc.com/ver10">
  <alarmStatusInfo>
    <motionAlarm type="boolean" id="1">false</motionAlarm>
    <motionAlarm type="boolean" id="2">true</motionAlarm>
    <sensorAlarmIn type="list" count="4">
      <itemType type="boolean"/>
      <item id="1">false</item>
      <item id="2">false</item>
      <item id="3">false</item>
      <item id="4">false</item>
    </sensorAlarmIn>
    <perimeterAlarm type="boolean">false</perimeterAlarm>
    <tripwireAlarm type="boolean">false</tripwireAlarm>
    <vfdAlarm type="boolean">false</vfdAlarm>
    <vehicleAlarm type="boolean" id="1">false</vehicleAlarm>
    <aoiEntryAlarm type="boolean" id="1">false</aoiEntryAlarm>
    <aoiLeaveAlarm type="boolean" id="1">false</aoiLeaveAlarm>
  </alarmStatusInfo>
</config>
```

**Notes:**
- `perimeterAlarm` goes true when detection triggers, stays true for `alarmHoldTime`, then drops to false even if the target is still present. There will be 5-20 second gaps. For continuous presence tracking, use `traject` (see [Section 6.6](#66-traject----real-time-target-tracking)).

#### TriggerVirtualAlarm

Triggers a virtual alarm input on the NVR. **NVR only.**

| Field | Value |
|-------|-------|
| **URL** | `GET http://<host>[:port]/TriggerVirtualAlarm/{virtualAlarmId}` |
| **Products** | NVR |
| **Entity Data** | None |

> **v2.0 only.** Undocumented command discovered through testing.

**Virtual alarm ID calculation:** IDs start after physical alarm inputs. If the NVR has 16 physical alarms, virtual alarm 1 = ID 17, virtual alarm 2 = ID 18, etc. Use `GetAlarmInInfo` to see the full list.

**Example:**

```bash
curl -u admin:password "http://192.168.0.147/TriggerVirtualAlarm/17"
```

**Response:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="2.0.0" xmlns="http://www.ipc.com/ver10" status="success" errorCode="0" errorDesc="Successful"></config>
```

**Use case:** External systems (AI inference boxes, third-party software) can trigger NVR alarm events, recording, and push notifications.

---

### 5.4 Legacy Alarm Server

A separate, older alarm server system. **IPC only.** Operates independently from the httpPost/httpPostV2 system in Section 5.5.

#### GetAlarmServerConfig / SetAlarmServerConfig

| Field | Value |
|-------|-------|
| **URL** | `POST` or `GET http://<host>[:port]/GetAlarmServerConfig` |
| **URL** | `POST http://<host>[:port]/SetAlarmServerConfig` |
| **Products** | IPC |

**Response:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="1.7" xmlns="http://www.ipc.com/ver10">
  <alarmServer>
    <serverAddr type="string"><![CDATA[]]></serverAddr>
    <serverPort type="uint16" min="1" max="65535">8010</serverPort>
    <enableHeartbeat type="boolean">false</enableHeartbeat>
    <heartbeatInterval type="uint16" min="10" max="1800">30</heartbeatInterval>
  </alarmServer>
</config>
```

> **Note:** `SetAlarmServerConfig` returned error 499 in testing. Use `SetHttpPostConfig` instead (Section 5.5).

#### SendAlarmStatus

Sent **by the device** to your alarm server when an alarm occurs. Your server must implement an endpoint to receive this.

| Field | Value |
|-------|-------|
| **URL** | `POST http://<alarm server>[:port]/SendAlarmStatus` |

**Alarm data format sent to your server:**

```xml
<config version="1.0" xmlns="http://www.ipc.com/ver10">
  <alarmStatusInfo>
    <motionAlarm type="boolean" id="1">true</motionAlarm>
  </alarmStatusInfo>
  <dataTime><![CDATA[2017-06-20 10:30:21]]></dataTime>
  <deviceInfo>
    <deviceName><![CDATA[Device Name]]></deviceName>
    <deviceNo.><![CDATA[1]]></deviceNo.>
    <sn><![CDATA[N563F0159MNK]]></sn>
    <ipAddress><![CDATA[192.168.3.100]]></ipAddress>
    <macAddress><![CDATA[78-24-AF-44-89-01]]></macAddress>
  </deviceInfo>
</config>
```

---

### 5.5 HTTP Post Configuration

The camera and NVR have a more advanced HTTP Post system alongside the legacy Alarm Server. The IPC supports two modes:

- **httpPost (v1)** -- Basic alarm server. One URL, one post per alarm event.
- **httpPostV2** -- Advanced subscription system. Up to 3 URLs, per-URL event type filtering, per-URL data type subscriptions. Supports continuous real-time `traject` tracking data.

Both are configured via `GetHttpPostConfig` / `SetHttpPostConfig` -- separate from the `GetAlarmServerConfig` endpoints in Section 5.4.

The NVR also has an HTTP Post system configured in its web interface. The NVR system sends alarm events using v2.0 XML format but does **not** support `traject`.

> Tested: IPC v1.9 (firmware 5.1.4.0, API version 1.7)

#### GetHttpPostConfig

| Field | Value |
|-------|-------|
| **URL** | `POST` or `GET http://<host>[:port]/GetHttpPostConfig` |
| **Products** | IPC |
| **Entity Data** | None |

**Response:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="1.7" xmlns="http://www.ipc.com/ver10">
  <httpPost>
    <bSwitch type="boolean">true</bSwitch>
    <protocolType><![CDATA[API]]></protocolType>
    <serverIp><![CDATA[192.168.0.53]]></serverIp>
    <serverPort>80</serverPort>
    <keepaliveTimeval>90</keepaliveTimeval>
    <onlineStatus type="boolean">true</onlineStatus>
    <URL><![CDATA[/API]]></URL>
  </httpPost>
  <httpPostV2>
    <postUrlConf>
      <urlList type="list" count="1" maxCount="3">
        <item>
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
        </item>
      </urlList>
    </postUrlConf>
  </httpPostV2>
</config>
```

#### SetHttpPostConfig

| Field | Value |
|-------|-------|
| **URL** | `POST http://<host>[:port]/SetHttpPostConfig` |
| **Products** | IPC |
| **Entity Data** | `httpPost` and/or `httpPostV2` element |

**Setting httpPost (v1):**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="1.0" xmlns="http://www.ipc.com/ver10">
<httpPost>
  <bSwitch>true</bSwitch>
  <serverIp><![CDATA[192.168.0.53]]></serverIp>
  <serverPort>80</serverPort>
  <keepaliveTimeval>90</keepaliveTimeval>
  <URL><![CDATA[/API]]></URL>
</httpPost>
</config>
```

**Setting httpPostV2:**

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
    <subscribeDateType type="list" count="5">
      <item>alarmStatus</item>
      <item>traject</item>
      <item>smartData</item>
      <item>sourceImage</item>
      <item>targetImage</item>
    </subscribeDateType>
    <subscriptionEvents type="list" count="1">
      <item>PERIMETER</item>
    </subscriptionEvents>
  </item></urlList>
</postUrlConf></httpPostV2>
</config>
```

**Notes:**
- httpPostV2 supports up to 3 URLs (`maxCount="3"`), each with independent event and data type subscriptions.
- `keepaliveTimeval` range is 30-120 seconds.
- Both v1 and v2 can be set in a single request by including both elements.

#### httpPostV2 Subscription Events

The `subscriptionEvents` field controls which detection types trigger posts:

```
ALL, MOTION, SENSOR, PERIMETER, TRIPWIRE, OSC, AVD,
AOIENTRY, AOILEAVE, PASSLINECOUNT, TRAFFIC, VSD, PVD, LOITER, ASD
```

#### httpPostV2 Data Types (subscribeDateType)

| Data Type | GUI Label | Description | Post Frequency | Post Size |
|-----------|-----------|-------------|----------------|-----------|
| `alarmStatus` | Alarm status data | Alarm on/off status | One per state change | ~660 bytes |
| `traject` | Smart track data | Continuous trajectory tracking | ~7 posts/sec while tracking | ~1.7 KB |
| `smartData` | Smart event data | Detection event with coordinates | One per event | ~2-3 KB (no images) |
| `sourceImage` | Original picture | Full frame JPEG (base64 in XML) | One per event | ~500-530 KB |
| `targetImage` | Target picture | Cropped target JPEG (base64 in XML) | One per event | Included with smartData |

> **Note:** `sourceImage` and `targetImage` are embedded in the smartData XML post as base64 data. Subscribing to `smartData` + `sourceImage` + `targetImage` produces a single large post per event.

See [Section 6.5](#65-httppostv2-data-types) for detailed usage guidance and [Section 6.6](#66-traject----real-time-target-tracking) for traject documentation.

---

### 5.6 Sound-Light Alarm

#### GetAudioAlarmOutConfig

Retrieves audio alarm output configuration. **IPC only.**

| Field | Value |
|-------|-------|
| **URL** | `POST` or `GET http://<host>[:port]/GetAudioAlarmOutConfig[/channelId]` |
| **Products** | IPC |

> **v2.0 only.**

#### GetWhiteLightAlarmOutConfig

Retrieves white light (strobe) alarm configuration. **IPC only.**

| Field | Value |
|-------|-------|
| **URL** | `POST` or `GET http://<host>[:port]/GetWhiteLightAlarmOutConfig[/channelId]` |
| **Products** | IPC |

> **v2.0 only.**

---

## 6. Receiving HTTP POST Events

### 6.1 Overview

Viewtron devices can push real-time AI detection events to your HTTP server as webhooks. There are two sources of HTTP POST data:

1. **IP Camera (direct)** -- The camera sends posts directly to your server using the IPC v1.x XML format (config version `1.0` or `1.7`). Supports the full httpPostV2 subscription system including real-time `traject` tracking.

2. **NVR (forwarded)** -- The NVR receives events from cameras on its PoE ports and forwards them to your server using the NVR v2.0 XML format (config version `2.0.0`). Does NOT support `traject`.

**Recommended setup for full coverage:**
1. Configure the **NVR** HTTP Post to send to your server (alarm events with images, v2.0 format)
2. Configure the **IPC** httpPostV2 to send to your server with `traject` subscribed (real-time tracking, v1.x format)
3. Your server receives both streams simultaneously

**Working Python server:** https://github.com/mikehaldas/IP-Camera-API -- handles both formats, extracts images, logs events to CSV, and supports traject-based relay control.

---

### 6.2 Quick Reference -- All Detection Types

| IPC smartType | NVR v2.0 smartType | Detection | Products | Tested |
|----|----|----|----|
| `PEA` (intrusion) | `regionIntrusion` | Perimeter / intrusion zone | IPC, NVR | Yes (IPC Nov 2025, NVR Feb 2026) |
| `PEA` (line cross) | `lineCrossing` | Tripwire / line crossing | IPC, NVR | Yes (NVR Feb 2026) |
| `VEHICE` | `vehicle` | License plate recognition (LPR) | IPC, NVR | Yes (NVR Feb 2026) |
| `VFD` | `videoFaceDetect` | Face detection with attributes | IPC, NVR | Yes (NVR Feb 2026) |
| `VFD_MATCH` | Not supported by NVR | Face recognition / match | IPC only | NVR does not forward match data |
| `VSD` | `videoMetadata` | Video metadata (full-frame detection) | IPC, NVR | Yes (NVR Feb 2026) |
| `PASSLINECOUNT` | `targetCountingByLine` | Object counting by line | IPC, NVR | Yes (NVR Feb 2026) |
| `TRAFFIC` | `targetCountingByArea` | Object counting by area | IPC, NVR | Yes (NVR Feb 2026) |
| `MOTION` | TBD | Motion detection | IPC, NVR | Not yet tested via HTTP Post |
| `AOIENTRY` | TBD | Region entry | IPC, NVR | Not yet tested via HTTP Post |
| `AOILEAVE` | TBD | Region exit | IPC, NVR | Not yet tested via HTTP Post |
| `OSC` | TBD | Object removal (left/missing) | IPC | Not yet tested via HTTP Post |
| `CPC` | TBD | People counting | IPC | Not yet tested via HTTP Post |
| `CDD` | TBD | Crowd density detection | IPC | Not yet tested via HTTP Post |
| `SENSOR` | TBD | Sensor alarm | IPC, NVR | Not yet tested via HTTP Post |

**Note:** IPC `PEA` is a single smartType that covers both intrusion and line crossing. The alarm data differentiates them by containing either a `<perimeter>` or `<tripwire>` block. The NVR uses separate smartType values (`regionIntrusion` vs `lineCrossing`).

---

### 6.3 IPC Format (v1.x)

IP cameras send alarm data using config version `1.0` or `1.7` with `Content-Type: application/xml; charset=utf-8` and `Connection: keep-alive`.

#### Keepalive

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

#### Alarm Status (alarmStatusInfo)

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

#### Alarm Data (smartData with images)

Full detection event with coordinates, zone boundary, and optionally images.

**PEA -- Perimeter Intrusion:**

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

**PEA with target crop (from Long Polling doc):**

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

**IPC smartData fields:**

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

#### IPC smartType Codes (Complete)

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

---

### 6.4 NVR Format (v2.0)

NVRs send alarm data using config version `2.0.0` with `Content-Type: application/soap+xml; charset=utf-8` and `Connection: close`. The NVR sends three message types identified by a `<messageType>` field (IPC posts do not have this field).

> Tested: NVR v2.0 (firmware 1.4.13), February-March 2026

#### Key Differences from IPC Format

| Feature | IPC Direct (v1.0/1.7) | NVR (v2.0.0) |
|---------|------------------------|--------------|
| **Config version** | `1.0` or `1.7` | `2.0.0` |
| **Content-Type** | `application/xml; charset=utf-8` | `application/soap+xml; charset=utf-8` |
| **Connection** | `keep-alive` | `close` |
| **messageType field** | Not present | `keepalive`, `alarmStatus`, `alarmData` |
| **deviceInfo block** | Varies | Always present with `deviceName`, `ip`, `mac`, `channelId` |
| **smartType values** | Codes: `PEA`, `VFD`, `VEHICE`, `VSD` | Spelled out: `regionIntrusion`, `lineCrossing`, `videoFaceDetect`, `videoMetadata`, `vehicle` |
| **Timestamp** | `dataTime` string or `currentTime` (10-16 digits) | `currentTime` Unix **microseconds** (16 digits) |
| **Event data** | `perimeter/perInfo` or `listInfo/item` | `eventInfo/item` with `eventId`, `targetId`, `boundary`, `pointGroup`, `rect` |
| **Image data** | `sourceDataInfo` + `listInfo/targetImageData` | `sourceDataInfo` + `targetListInfo/targetImageData` |
| **targetType** | Numeric: 1=person, 2=car, 4=bike | String: `person`, `car`, `motor` |
| **POST line** | `POST /API HTTP/1.1` (path only) | `POST http://192.168.0.56:5002/API HTTP/1.1` (full URL) |
| **Type annotations** | Present (`type="uint32"`) | Not present |

#### Keepalive

Heartbeat sent approximately every 10 seconds.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="2.0.0" xmlns="http://www.ipc.com/ver10">
    <messageType>keepalive</messageType>
    <deviceInfo>
        <deviceName><![CDATA[Device Name]]></deviceName>
        <ip><![CDATA[192.168.0.55]]></ip>
        <mac><![CDATA[58:5B:69:40:F4:0D]]></mac>
    </deviceInfo>
</config>
```

#### Alarm Status

Sent when alarm triggers or clears. Always arrives BEFORE the `alarmData` post.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="2.0.0" xmlns="http://www.ipc.com/ver10">
    <messageType>alarmStatus</messageType>
    <deviceInfo>
        <deviceName><![CDATA[Device Name]]></deviceName>
        <ip><![CDATA[192.168.0.55]]></ip>
        <mac><![CDATA[58:5B:69:40:F4:0D]]></mac>
        <channelId>1</channelId>
    </deviceInfo>
    <currentTime>1772056914000000</currentTime>
    <alarmStatusInfo>
        <perimeterAlarm><item id="1">true</item>
        </perimeterAlarm>
    </alarmStatusInfo>
</config>
```

**NVR alarmStatus field names by detection type:**

| Detection Type | alarmStatusInfo Field |
|----------------|----------------------|
| `regionIntrusion` | `perimeterAlarm` |
| `lineCrossing` | `perimeterAlarm` |
| `targetCountingByLine` | `passlineAlarm` |
| `targetCountingByArea` | `passlineAlarm` |
| `videoMetadata` | None (no alarmStatus sent) |
| `vehicle` | None observed |
| `videoFaceDetect` | `vfdAlarm` |

#### Alarm Data -- by Detection Type

All NVR alarm data posts share this outer structure:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="2.0.0" xmlns="http://www.ipc.com/ver10">
    <messageType>alarmData</messageType>
    <deviceInfo>
        <deviceName><![CDATA[...]]></deviceName>
        <ip><![CDATA[...]]></ip>
        <mac><![CDATA[...]]></mac>
        <channelId>1</channelId>
    </deviceInfo>
    <smartType>...</smartType>
    <currentTime>...</currentTime>
    <!-- detection-specific content below -->
</config>
```

**Three XML structures exist for NVR alarm data:**

1. **`eventInfo` + `targetListInfo`** -- for regionIntrusion, lineCrossing, targetCountingByLine, targetCountingByArea, videoMetadata
2. **`licensePlateListInfo`** -- for vehicle (LPR)
3. **`faceListInfo`** -- for videoFaceDetect

##### regionIntrusion

Perimeter / intrusion zone detection. NVR equivalent of IPC `PEA` (intrusion).

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="2.0.0" xmlns="http://www.ipc.com/ver10">
    <messageType>alarmData</messageType>
    <deviceInfo>
        <deviceName><![CDATA[Device Name]]></deviceName>
        <ip><![CDATA[192.168.0.55]]></ip>
        <mac><![CDATA[58:5B:69:40:F4:0D]]></mac>
        <channelId>1</channelId>
    </deviceInfo>
    <smartType>regionIntrusion</smartType>
    <currentTime>1772056914604000</currentTime>
    <eventInfo>
        <item>
            <eventId>916</eventId>
            <targetId>716</targetId>
            <boundary>area</boundary>
            <pointGroup>
                <item><x>1590</x><y>3080</y></item>
                <item><x>4715</x><y>3181</y></item>
                <item><x>4772</x><y>9217</y></item>
                <item><x>416</x><y>9141</y></item>
            </pointGroup>
            <rect><x1>3096</x1><y1>3715</y1><x2>4005</x2><y2>9861</y2></rect>
        </item>
    </eventInfo>
    <sourceDataInfo>
        <dataType>0</dataType>
        <width>1280</width>
        <height>720</height>
        <sourceBase64Length>400924</sourceBase64Length>
        <sourceBase64Data>... (base64 JPEG) ...</sourceBase64Data>
    </sourceDataInfo>
    <targetListInfo>
        <item>
            <targetId>716</targetId>
            <targetType>person</targetType>
            <targetImageData>
                <dataType>0</dataType>
                <width>336</width>
                <height>448</height>
                <targetBase64Length>78796</targetBase64Length>
                <targetBase64Data><![CDATA[... (base64 JPEG) ...]]></targetBase64Data>
            </targetImageData>
        </item>
    </targetListInfo>
</config>
```

##### lineCrossing

Tripwire / line crossing. NVR equivalent of IPC `PEA` (line cross).

The outer structure is identical to regionIntrusion. The `eventInfo` differs:

```xml
<eventInfo>
    <item>
        <eventId>1409</eventId>
        <targetId>1309</targetId>
        <boundary>tripwire</boundary>
        <directionLine>
            <startPoint><x>3579</x><y>2550</y></startPoint>
            <endPoint><x>3655</x><y>9797</y></endPoint>
        </directionLine>
        <rect><x1>3494</x1><y1>4409</y1><x2>4261</x2><y2>9791</y2></rect>
    </item>
</eventInfo>
```

**Key differences from regionIntrusion:**
- `boundary` is `tripwire` instead of `area`
- Uses `directionLine` (startPoint + endPoint) instead of `pointGroup` (polygon)
- The NVR does NOT include crossing direction (A-to-B vs B-to-A) in the post

##### targetCountingByLine

Object counting by line. NVR equivalent of IPC `PASSLINECOUNT`.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="2.0.0" xmlns="http://www.ipc.com/ver10">
    <messageType>alarmData</messageType>
    <deviceInfo>
        <deviceName><![CDATA[Device Name]]></deviceName>
        <ip><![CDATA[192.168.0.60]]></ip>
        <mac><![CDATA[58:5B:69:40:F4:0D]]></mac>
        <channelId>1</channelId>
    </deviceInfo>
    <smartType>targetCountingByLine</smartType>
    <currentTime>1772140991308000</currentTime>
    <eventInfo>
        <item>
            <eventId>1080</eventId>
            <targetId>480</targetId>
            <boundary>tripwire</boundary>
            <directionLine>
                <startPoint><x>3977</x><y>2146</y></startPoint>
                <endPoint><x>3977</x><y>9974</y></endPoint>
            </directionLine>
            <rect><x1>0</x1><y1>0</y1><x2>0</x2><y2>0</y2></rect>
        </item>
    </eventInfo>
    <sourceDataInfo>
        <dataType>0</dataType>
        <width>1280</width>
        <height>720</height>
        <sourceBase64Length>441256</sourceBase64Length>
        <sourceBase64Data>... (base64 JPEG) ...</sourceBase64Data>
    </sourceDataInfo>
    <targetListInfo>
        <item>
            <targetId>480</targetId>
            <targetType>person</targetType>
            <targetImageData>
                <dataType>0</dataType>
                <width>336</width>
                <height>448</height>
                <targetBase64Length>72896</targetBase64Length>
                <targetBase64Data>... (base64 JPEG) ...</targetBase64Data>
            </targetImageData>
        </item>
    </targetListInfo>
</config>
```

**Note:** The `rect` in `eventInfo` is all zeros for line counting -- the target crop in `targetListInfo` still captures the person. Uses `passlineAlarm` for alarm status.

##### targetCountingByArea

Object counting by area. NVR equivalent of IPC `TRAFFIC`.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="2.0.0" xmlns="http://www.ipc.com/ver10">
    <messageType>alarmData</messageType>
    <deviceInfo>
        <deviceName><![CDATA[Device Name]]></deviceName>
        <ip><![CDATA[192.168.0.60]]></ip>
        <mac><![CDATA[58:5B:69:40:F4:0D]]></mac>
        <channelId>1</channelId>
    </deviceInfo>
    <smartType>targetCountingByArea</smartType>
    <currentTime>1772145352968000</currentTime>
    <eventInfo>
        <item>
            <eventId>2904</eventId>
            <targetId>2204</targetId>
            <boundary>area</boundary>
            <pointGroup>
                <item><x>4450</x><y>4292</y></item>
                <item><x>4469</x><y>9015</y></item>
                <item><x>1079</x><y>8510</y></item>
                <item><x>1344</x><y>4166</y></item>
            </pointGroup>
            <rect><x1>4431</x1><y1>4409</y1><x2>4971</x2><y2>9791</y2></rect>
        </item>
    </eventInfo>
    <sourceDataInfo>
        <dataType>0</dataType>
        <width>1280</width>
        <height>720</height>
        <sourceBase64Length>414832</sourceBase64Length>
        <sourceBase64Data>... (base64 JPEG) ...</sourceBase64Data>
    </sourceDataInfo>
    <targetListInfo>
        <item>
            <targetId>2204</targetId>
            <targetType>person</targetType>
            <targetImageData>
                <dataType>0</dataType>
                <width>336</width>
                <height>448</height>
                <targetBase64Length>72136</targetBase64Length>
                <targetBase64Data>... (base64 JPEG) ...</targetBase64Data>
            </targetImageData>
        </item>
    </targetListInfo>
</config>
```

##### videoMetadata

Full-frame object detection. NVR equivalent of IPC `VSD`.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="2.0.0" xmlns="http://www.ipc.com/ver10">
    <messageType>alarmData</messageType>
    <deviceInfo>
        <deviceName><![CDATA[Device Name]]></deviceName>
        <ip><![CDATA[192.168.0.60]]></ip>
        <mac><![CDATA[58:5B:69:40:F4:0D]]></mac>
        <channelId>1</channelId>
    </deviceInfo>
    <smartType>videoMetadata</smartType>
    <currentTime>1772145578273000</currentTime>
    <eventInfo>
        <item>
            <eventId>3215</eventId>
            <targetId>2215</targetId>
            <boundary>area</boundary>
            <pointGroup>
                <item><x>23</x><y>0</y></item>
                <item><x>9880</x><y>158</y></item>
                <item><x>9904</x><y>9873</y></item>
                <item><x>0</x><y>9841</y></item>
            </pointGroup>
            <rect><x1>5284</x1><y1>4513</y1><x2>6079</x2><y2>9479</y2></rect>
        </item>
    </eventInfo>
    <sourceDataInfo>
        <dataType>0</dataType>
        <width>1280</width>
        <height>784</height>
        <sourceBase64Length>451968</sourceBase64Length>
        <sourceBase64Data>... (base64 JPEG) ...</sourceBase64Data>
    </sourceDataInfo>
    <targetListInfo>
        <item>
            <targetId>2215</targetId>
            <targetType>person</targetType>
            <targetImageData>
                <dataType>0</dataType>
                <width>288</width>
                <height>384</height>
                <targetBase64Length>45832</targetBase64Length>
                <targetBase64Data>... (base64 JPEG) ...</targetBase64Data>
            </targetImageData>
        </item>
    </targetListInfo>
</config>
```

**Key observations:**
- `pointGroup` covers nearly the entire frame (~0-9900 on both axes) -- VSD detects across the full scene
- Does NOT send `alarmStatus` messages -- only `alarmData`
- When multiple AI events are enabled simultaneously, the NVR sends separate posts for each

##### vehicle (LPR)

License plate recognition. NVR equivalent of IPC `VEHICE`. Uses a completely different XML structure -- `licensePlateListInfo` instead of `eventInfo` + `targetListInfo`.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="2.0.0" xmlns="http://www.ipc.com/ver10">
    <messageType>alarmData</messageType>
    <deviceInfo>
        <deviceName><![CDATA[Device Name]]></deviceName>
        <ip><![CDATA[192.168.0.60]]></ip>
        <mac><![CDATA[58:5B:69:40:F4:0D]]></mac>
        <channelId>2</channelId>
    </deviceInfo>
    <smartType>vehicle</smartType>
    <currentTime>18445822972087551616</currentTime>
    <sourceDataInfo>
        <dataType>0</dataType>
        <width>0</width>
        <height>0</height>
    </sourceDataInfo>
    <licensePlateListInfo>
        <item>
            <targetId>104</targetId>
            <rect>
                <x1>1104</x1><y1>546</y1>
                <x2>1232</x2><y2>610</y2>
            </rect>
            <licensePlateAttribute>
                <licensePlateNumber><![CDATA[JP116D]]></licensePlateNumber>
                <color>white</color>
            </licensePlateAttribute>
            <carRect>
                <x1>1</x1><y1>0</y1>
                <x2>1</x2><y2>0</y2>
            </carRect>
            <carAttribute>
                <carType><![CDATA[mpv]]></carType>
                <color><![CDATA[white]]></color>
                <brand><![CDATA[GMC]]></brand>
                <model><![CDATA[GMC_SAVANA]]></model>
            </carAttribute>
            <targetImageData>
                <dataType>0</dataType>
                <width>128</width>
                <height>64</height>
                <targetBase64Length>...</targetBase64Length>
                <targetBase64Data>... (base64 JPEG of plate crop) ...</targetBase64Data>
            </targetImageData>
        </item>
    </licensePlateListInfo>
</config>
```

**`licensePlateListInfo/item` fields:**

| Field | Description | Example |
|-------|-------------|---------|
| `targetId` | Detection tracking ID | `104` |
| `rect` | Plate bounding box (pixel coordinates) | `x1:1104, y1:546, x2:1232, y2:610` |
| `licensePlateAttribute/licensePlateNumber` | Detected plate text | `JP116D` |
| `licensePlateAttribute/color` | Plate color | `white` |
| `carRect` | Vehicle bounding box | May be zeros |
| `carAttribute/carType` | Vehicle classification | `mpv` |
| `carAttribute/color` | Vehicle color | `white` |
| `carAttribute/brand` | Vehicle brand | `GMC` |
| `carAttribute/model` | Vehicle model | `GMC_SAVANA` |
| `targetImageData` | Cropped plate image (128x64 JPEG) | base64 |

**Notable observations:**
- Vehicle attribute recognition identifies type, color, brand, and model -- far richer than IPC v1.x format
- `currentTime` anomaly: the 20-digit timestamp appears to be a firmware bug
- `sourceDataInfo` has zero dimensions but the post is ~628 KB
- No `alarmStatus` observed for this detection type

##### videoFaceDetect

Face detection with attribute analysis. NVR equivalent of IPC `VFD`. Uses `faceListInfo`.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="2.0.0" xmlns="http://www.ipc.com/ver10">
    <messageType>alarmData</messageType>
    <deviceInfo>
        <deviceName><![CDATA[Device Name]]></deviceName>
        <ip><![CDATA[192.168.0.60]]></ip>
        <mac><![CDATA[58:5B:69:40:F4:0D]]></mac>
        <channelId>1</channelId>
    </deviceInfo>
    <smartType>videoFaceDetect</smartType>
    <currentTime>1772212642929000</currentTime>
    <sourceDataInfo>
        <dataType>0</dataType>
        <width>1280</width>
        <height>720</height>
        <sourceBase64Length>440072</sourceBase64Length>
        <sourceBase64Data>... (base64 JPEG overview) ...</sourceBase64Data>
    </sourceDataInfo>
    <faceListInfo>
        <item>
            <targetId>50</targetId>
            <rect>
                <x1>854</x1><y1>176</y1>
                <x2>978</x2><y2>300</y2>
            </rect>
            <age>middleAged</age>
            <sex>male</sex>
            <glasses>unknown</glasses>
            <mask>unknown</mask>
            <targetImageData>
                <dataType>0</dataType>
                <width>184</width>
                <height>184</height>
                <targetBase64Length>14860</targetBase64Length>
                <targetBase64Data>... (base64 JPEG face crop) ...</targetBase64Data>
            </targetImageData>
        </item>
    </faceListInfo>
</config>
```

**`faceListInfo/item` fields:**

| Field | Description | Example |
|-------|-------------|---------|
| `targetId` | Detection tracking ID | `50` |
| `rect` | Face bounding box | `x1:854, y1:176, x2:978, y2:300` |
| `age` | Age classification | `middleAged` |
| `sex` | Gender classification | `male` |
| `glasses` | Glasses detection | `unknown` |
| `mask` | Mask detection | `unknown` |
| `targetImageData` | Square face crop (184x184 JPEG) | base64 |

**Notable observations:**
- Face match/recognition (`VFD_MATCH`) is NOT forwarded by the NVR via HTTP Post. Even with face database configured, only `videoFaceDetect` is sent.
- 4ch NVRs support face detection but NOT face database/recognition. 8ch NVRs support both.
- AlarmStatus uses `vfdAlarm`.

#### Image Configuration Options (NVR)

The NVR alarm server settings allow configuring which images are sent. The `eventInfo` and `targetListInfo` are always present regardless of image setting.

| NVR Setting | `sourceDataInfo` | `targetImageData` | `targetListInfo` | Typical Size |
|---|---|---|---|---|
| Both images | Present (overview JPEG) | Present (crop JPEG) | Present with image | ~524 KB |
| Original only | Present (overview JPEG) | **Absent** | Present, no image | ~418 KB |
| Target only | **Absent** | Present (crop JPEG) | Present with image | ~92 KB |
| No images | **Absent** | **Absent** | Present, no image | ~1 KB |

**Both images (~524 KB):**

```xml
<sourceDataInfo>
    <dataType>0</dataType>
    <width>1280</width>
    <height>720</height>
    <sourceBase64Length>443820</sourceBase64Length>
    <sourceBase64Data><![CDATA[... (base64 JPEG) ...]]></sourceBase64Data>
</sourceDataInfo>
<targetListInfo>
    <item>
        <targetId>1168</targetId>
        <targetType>person</targetType>
        <targetImageData>
            <dataType>0</dataType>
            <width>336</width>
            <height>448</height>
            <targetBase64Length>78796</targetBase64Length>
            <targetBase64Data><![CDATA[... (base64 JPEG) ...]]></targetBase64Data>
        </targetImageData>
    </item>
</targetListInfo>
```

**Original image only (~418 KB):**

```xml
<sourceDataInfo>
    <dataType>0</dataType>
    <width>1280</width>
    <height>720</height>
    <sourceBase64Length>416540</sourceBase64Length>
    <sourceBase64Data><![CDATA[... (base64 JPEG) ...]]></sourceBase64Data>
</sourceDataInfo>
<targetListInfo>
    <item>
        <targetId>1260</targetId>
        <targetType>person</targetType>
    </item>
</targetListInfo>
```

**Target image only (~92 KB):**

```xml
<targetListInfo>
    <item>
        <targetId>1275</targetId>
        <targetType>person</targetType>
        <targetImageData>
            <dataType>0</dataType>
            <width>336</width>
            <height>440</height>
            <targetBase64Length>90764</targetBase64Length>
            <targetBase64Data><![CDATA[... (base64 JPEG) ...]]></targetBase64Data>
        </targetImageData>
    </item>
</targetListInfo>
```

**No images (~1 KB):**

```xml
<targetListInfo>
    <item>
        <targetId>1254</targetId>
        <targetType>person</targetType>
    </item>
</targetListInfo>
```

**Key observation:** `targetListInfo` is ALWAYS present with at least `targetId` and `targetType`, even with images disabled. Target classification data is always available.

---

### 6.5 httpPostV2 Data Types

This section explains how the five httpPostV2 data types interact when subscribed together, and how to choose the right combination for your use case.

#### How Data Types Work Together

Each data type generates **separate HTTP Posts**. When a detection event occurs, the camera sends posts in this order:

1. **`traject`** -- Starts immediately when tracking begins. Continuous stream at ~7 posts/sec. Stops when target leaves.
2. **`alarmStatus`** -- One `true` post at alarm start, one `false` when alarm hold time expires.
3. **`smartData`** (+ `sourceImage`/`targetImage`) -- Detection event with coordinates and optionally images.

**Tested timeline (IPC IP-AX8D, March 29, 2026, all five data types subscribed):**

```
13:58:46.797  traject starts    -- person enters zone, target id=2157
13:58:47.258  smartData+images  -- PEA SMART_START event (517 KB)
13:58:47.436  alarmStatus       -- perimeterAlarm=true (658 bytes)
13:58:47-54   traject stream    -- continuous ~7 posts/sec
13:58:48.258  smartData+images  -- second PEA event (527 KB)
13:58:54.131  traject stops     -- person leaves zone, 50 traject posts total

              ~6 second gap -- zero traject posts (person out of zone)

13:59:00.616  traject starts    -- person re-enters, new target id=2160
13:59:01.446  smartData+images  -- PEA SMART_START event (511 KB)
13:59:01.605  smartData+images  -- second PEA event (524 KB)
13:59:01-08   traject stream    -- continuous tracking, 54 posts
13:59:08.546  traject stops     -- person leaves zone
13:59:19.056  alarmStatus       -- perimeterAlarm=false (659 bytes)

14:00:49+     keepalives        -- empty body posts every ~90 seconds
```

**Total: 104 traject posts, 4 smartData+image posts, 2 alarmStatus posts, 3 keepalives**

**Key observations:**
- traject starts before alarmStatus
- traject has zero gaps while the target is present
- alarmStatus is sparse -- only one true/false pair per alarm cycle
- New target IDs per entry (2157, then 2160)

#### Choosing Which Data Types to Subscribe

| Use Case | Recommended Data Types | Why |
|----------|----------------------|-----|
| **Real-time automation** (relay control, lighting) | `traject` only | Continuous presence signal, ~12 KB/sec |
| **Event logging with images** | `smartData` + `sourceImage` + `targetImage` | One post per event with full scene + target crop |
| **Event logging without images** | `smartData` or `alarmStatus` | Lightweight, ~660 bytes - 3 KB per event |
| **Full monitoring** | All five | Complete picture |
| **Counting/analytics** | `traject` + `smartData` | Track positions continuously, get event boundaries |

**Bandwidth:**
- `traject` alone: ~12 KB/sec per tracked target
- `smartData` + images: ~500-530 KB per event (one-time)
- `alarmStatus`: ~660 bytes per state change

**Subscribing to multiple data types:**

```xml
<subscribeDateType type="list" count="3">
  <item>traject</item>
  <item>smartData</item>
  <item>alarmStatus</item>
</subscribeDateType>
```

**Subscribing to all five:**

```xml
<subscribeDateType type="list" count="5">
  <item>alarmStatus</item>
  <item>traject</item>
  <item>smartData</item>
  <item>sourceImage</item>
  <item>targetImage</item>
</subscribeDateType>
```

---

### 6.6 traject -- Real-Time Target Tracking

When subscribed to `traject` via httpPostV2, the camera sends **continuous HTTP Posts** for the entire duration a target is being tracked. This is fundamentally different from alarm-based approaches.

> Tested: IPC v1.9 (firmware 5.1.4.0), March 27-29, 2026

#### Comparison vs Polling and Alarm Methods

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

#### traject Post Format

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

#### traject Fields

| Field | Type | Description |
|-------|------|-------------|
| `targetId` | uint32 | Unique ID for the tracked target. New ID per entry. |
| `point` | x, y | Target point (observed as 0,0 -- possibly unused) |
| `rect` | x1, y1, x2, y2 | Bounding box (normalized 0-10000 coordinates) |
| `velocity` | uint32 | Target velocity (observed as 0) |
| `direction` | uint32 | Target direction (observed as 0) |
| `targetType` | string | `person`, `car`, or `motor` |
| `trajectlength` | list | Trajectory path points (observed as empty) |

#### Test Results

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

**Post sizes by data type:**

| Data Type | Size | Frequency |
|-----------|------|-----------|
| `traject` | ~1.7 KB | ~7/sec continuous |
| `alarmStatus` | ~660 bytes | 1 per alarm cycle |
| `smartData` + images | ~510-530 KB | 1-2 per entry |
| keepalive | 0 bytes (empty body) | every ~90 sec |

#### Configuration

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

#### Important Notes

- **traject is IPC-only.** NVRs do not forward traject data and do not expose the smart track data subscription.
- **The "Smart track data" checkbox must be enabled** in the camera's HTTP Post V2 web interface (Edit HTTP POST dialog). The camera will not send traject even if configured via API unless this checkbox is also checked.
- **Works through NVR PoE.** The camera sends traject directly to your server, independent of the NVR. Format is identical.
- **Recommended dual setup:** NVR HTTP Post for alarm events + IPC httpPostV2 for traject tracking.

#### Use Cases

- Real-time presence detection (relay control, lighting automation)
- People/vehicle counting with continuous position tracking
- Dwell time analysis
- Custom alarm logic based on target position and movement
- Occupancy monitoring

**Example:** See the [Raspberry Pi Human Detection Relay Controller](https://github.com/mikehaldas/IP-Camera-API) for a working implementation using traject data.

---

### 6.7 Image Data Handling

#### Base64 Encoding

All images in HTTP Post data are JPEG files encoded as base64 strings embedded in XML.

#### sourceBase64Data vs targetBase64Data

| Field | Content | Typical Size | Location (NVR) | Location (IPC) |
|-------|---------|--------------|-----------------|-----------------|
| `sourceBase64Data` | Full frame overview | ~400-530 KB | `sourceDataInfo/sourceBase64Data` | `sourceDataInfo/sourceBase64Data` |
| `targetBase64Data` | Cropped target | ~14-100 KB | `targetListInfo/item/targetImageData/targetBase64Data` | `listInfo/item/targetImageData/targetBase64Data` |

#### Image Resolution by Detection Type

| Image Type | Detection Type | Typical Resolution |
|------------|---------------|--------------------|
| Source (overview) | Most types | 1280x720 or 1920x1080 |
| Source (overview) | videoMetadata | 1280x784 (may vary) |
| Source (overview) | vehicle | 0x0 metadata (firmware bug), but data present |
| Target (person crop) | regionIntrusion, lineCrossing, counting | 288x384 or 336x448 |
| Target (face crop) | videoFaceDetect | 184x184 (square) |
| Target (plate crop) | vehicle | 128x64 |

**Decoding images in Python:**

```python
import base64
image_bytes = base64.b64decode(source_base64_data)
with open("snapshot.jpg", "wb") as f:
    f.write(image_bytes)
```

---

### 6.8 Timestamp Handling

| Source | Field | Format | Example | Resolution |
|--------|-------|--------|---------|------------|
| IPC alarm push (v1.7) | `dataTime` | Formatted string | `2026-03-29 09:58:21` or `11-19-2025 12:15:11 PM` | Seconds |
| IPC alarm data (v1.0) | `currentTime` | Unix timestamp | `1732045234` (10 digits) or `1732045234000` (13 digits) | Seconds or milliseconds |
| IPC traject/smartData (v1.7) | `currentTime` | Unix microseconds | `1774646121524166` (16 digits) | Microseconds |
| NVR (v2.0) | `currentTime` | Unix microseconds | `1772056914000000` (16 digits) | Microseconds |

**To convert microsecond timestamps to seconds:** divide by 1,000,000 (not 1,000).

---

## 7. Playback Commands

### GetRecordType

Retrieves supported recording types.

| Field | Value |
|-------|-------|
| **URL** | `POST` or `GET http://<host>[:port]/GetRecordType` |
| **Products** | IPC, NVR |

**Response:**

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

**Note:** `nic broken` is IPC only.

---

### SearchByTime

Searches for recorded video segments by time range.

| Field | Value |
|-------|-------|
| **URL** | `POST` or `GET http://<host>[:port]/SearchByTime[/channelId]` |
| **Products** | IPC, NVR |
| **Channel ID** | Optional (default 1) |

**Request:**

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

**RTSP playback URL:**

```
rtsp://<host>[:rtspPort]/chID=0&date=2014-01-09&time=15:07:28&timelen=200&streamType=main&action=playback
```

---

## 8. Network Commands

### GetNetBasicConfig

Retrieves basic network configuration (IP, subnet, gateway, DNS).

| Field | Value |
|-------|-------|
| **URL** | `POST` or `GET http://<host>[:port]/GetNetBasicConfig` |
| **Products** | IPC, NVR |

---

### GetPortConfig

Retrieves port configuration (HTTP, RTSP, etc.).

| Field | Value |
|-------|-------|
| **URL** | `POST` or `GET http://<host>[:port]/GetPortConfig` |
| **Products** | IPC, NVR |

> **v1.9 only.**

---

## 9. Security Commands

### ModifyPassword

Modifies the user password.

| Field | Value |
|-------|-------|
| **URL** | `POST http://<host>[:port]/ModifyPassword` |
| **Products** | IPC, NVR |

---

## 10. Smart Detection Commands

### GetSmartPerimeterConfig

Retrieves intrusion/perimeter detection configuration.

| Field | Value |
|-------|-------|
| **URL** | `POST` or `GET http://<host>[:port]/GetSmartPerimeterConfig[/channelId]` |
| **Products** | IPC |
| **Channel ID** | Optional (default 1) |

**Response:**

```xml
<?xml version="1.0" encoding="utf-8"?>
<config xmlns="http://www.ipc.com/ver10" version="2.0.0">
  <perimeter>
    <switch type="boolean">true</switch>
    <alarmHoldTime type="uint32">20</alarmHoldTime>
    <objectFilter>
      <car>
        <switch type="boolean">true</switch>
        <sensitivity type="uint32" max="100" min="1" default="50">50</sensitivity>
      </car>
      <person>
        <switch type="boolean">true</switch>
        <sensitivity type="uint32" max="100" min="1" default="50">50</sensitivity>
      </person>
      <motor>
        <switch type="boolean">true</switch>
        <sensitivity type="uint32" max="100" min="1" default="50">50</sensitivity>
      </motor>
    </objectFilter>
    <saveTargetPicture type="boolean">false</saveTargetPicture>
    <saveSourcePicture type="boolean">false</saveSourcePicture>
    <regionInfo type="list" maxCount="4" count="1">
      <item>
        <pointGroup type="list" maxCount="8" count="4">
          <item>
            <X type="uint32">4075</X>
            <Y type="uint32">2466</Y>
          </item>
          <!-- Additional points... -->
        </pointGroup>
      </item>
    </regionInfo>
  </perimeter>
</config>
```

---

### GetSmartTripwireConfig

Retrieves line crossing/tripwire detection configuration.

| Field | Value |
|-------|-------|
| **URL** | `POST` or `GET http://<host>[:port]/GetSmartTripwireConfig[/channelId]` |
| **Products** | IPC |
| **Channel ID** | Optional (default 1) |

**Response:**

```xml
<?xml version="1.0" encoding="utf-8"?>
<config xmlns="http://www.ipc.com/ver10" version="2.0.0">
  <types>
    <tripwireDirection>
      <enum>none</enum>
      <enum>rightortop</enum>
      <enum>leftorbotton</enum>
    </tripwireDirection>
  </types>
  <tripwire>
    <switch type="boolean">false</switch>
    <alarmHoldTime type="uint32">20</alarmHoldTime>
    <objectFilter>
      <car>
        <switch type="boolean">true</switch>
        <sensitivity type="uint32" max="100" min="1" default="50">50</sensitivity>
      </car>
      <person>
        <switch type="boolean">true</switch>
        <sensitivity type="uint32" max="100" min="1" default="50">50</sensitivity>
      </person>
    </objectFilter>
    <lineInfo type="list" maxCount="4" count="1">
      <item>
        <direction type="tripwireDirection">rightortop</direction>
        <startPoint>
          <X type="uint32">10</X>
          <Y type="uint32">10</Y>
        </startPoint>
        <endPoint>
          <X type="uint32">1000</X>
          <Y type="uint32">1000</Y>
        </endPoint>
      </item>
    </lineInfo>
  </tripwire>
</config>
```

---

### GetSmartVfdConfig

Retrieves face detection configuration.

| Field | Value |
|-------|-------|
| **URL** | `POST` or `GET http://<host>[:port]/GetSmartVfdConfig[/channelId]` |
| **Products** | IPC |
| **Channel ID** | Optional (default 1) |

---

### GetSmartVehicleConfig / AddVehiclePlate / GetVehiclePlate

License plate recognition configuration and database management.

#### GetSmartVehicleConfig

| Field | Value |
|-------|-------|
| **URL** | `POST` or `GET http://<host>[:port]/GetSmartVehicleConfig[/channelId]` |
| **Products** | IPC |

**Response (v2.0):**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="2.0.0" xmlns="http://www.ipc.com/ver10">
  <types>
    <plateAreaType>
      <enum continent="NorthAmerica">U.S.A</enum>
      <enum continent="NorthAmerica">Canada</enum>
      <enum continent="Europe">Germany</enum>
      <enum continent="Europe">Britain</enum>
      <!-- Additional regions... -->
    </plateAreaType>
    <alarmListType>
      <enum>blackList</enum>
      <enum>whiteList</enum>
      <enum>strangerList</enum>
    </alarmListType>
  </types>
  <vehicle>
    <switch type="boolean">false</switch>
    <plateSencitivity type="uint8">49</plateSencitivity>
    <plateSupportArea type="plateAreaType">U.S.A</plateSupportArea>
    <saveTargetPicture type="boolean">false</saveTargetPicture>
    <saveSourcePicture type="boolean">false</saveSourcePicture>
    <dedupMode>
      <switch type="boolean">false</switch>
      <intervalTime type="uint32" default="5">5</intervalTime>
    </dedupMode>
    <regionInfo type="list" maxCount="1" count="1">
      <item>
        <X1 type="uint32">375</X1>
        <Y1 type="uint32">2866</Y1>
        <X2 type="uint32">9625</X2>
        <Y2 type="uint32">8800</Y2>
      </item>
    </regionInfo>
    <plateMatch>
      <alarmMode type="alarmModeType">plateOnly</alarmMode>
    </plateMatch>
  </vehicle>
</config>
```

> **v2.0 adds:** `dedupMode` (deduplication with interval) and `plateMatch/alarmMode`.

#### AddVehiclePlate

| Field | Value |
|-------|-------|
| **URL** | `POST http://<host>[:port]/AddVehiclePlate` |
| **Products** | IPC |

**Request:**

```xml
<?xml version="1.0" encoding="utf-8"?>
<config>
  <vehiclePlates type="list" count="1">
    <item>
      <carPlateNumber type="string"><![CDATA[ABC1234]]></carPlateNumber>
      <beginTime type="string"><![CDATA[2024/01/01 00:00:00]]></beginTime>
      <endTime type="string"><![CDATA[2024/12/31 23:59:59]]></endTime>
      <carOwner type="string"><![CDATA[John Doe]]></carOwner>
      <plateItemType type="string">whiteList</plateItemType>
    </item>
  </vehiclePlates>
</config>
```

#### GetVehiclePlate

Retrieves license plates from the database.

| Field | Value |
|-------|-------|
| **URL** | `POST` or `GET http://<host>[:port]/GetVehiclePlate` |
| **Products** | IPC |

> **v2.0 only.**

**Request:**

```xml
<config xmlns="http://www.ipc.com/ver10" version="2.0.0">
  <vehiclePlates type="list" maxCount="10000" count="1">
    <searchFilter>
      <item>
        <pageIndex type="uint32">0</pageIndex>
        <pageSize type="uint32">10</pageSize>
        <listType type="vehicleListTypes">allList</listType>
        <carPlateNum type="string"></carPlateNum>
      </item>
    </searchFilter>
  </vehiclePlates>
</config>
```

---

### GetSmartAoiEntryConfig / GetSmartAoiLeaveConfig

Region entry and exit detection configuration.

| Field | Value |
|-------|-------|
| **URL** | `POST` or `GET http://<host>[:port]/GetSmartAoiEntryConfig[/channelId]` |
| **URL** | `POST` or `GET http://<host>[:port]/GetSmartAoiLeaveConfig[/channelId]` |
| **Products** | IPC |
| **Channel ID** | Optional (default 1) |

---

### GetSmartPassLineCountConfig / GetPassLineCountStatistics

Target counting by line configuration and statistics.

#### GetSmartPassLineCountConfig

| Field | Value |
|-------|-------|
| **URL** | `POST` or `GET http://<host>[:port]/GetPassLineCountConfig[/channelId]` |
| **Products** | IPC |
| **Channel ID** | Optional (default 1) |

#### GetPassLineCountStatistics

Gets current entrance/exit counting statistics.

| Field | Value |
|-------|-------|
| **URL** | `POST` or `GET http://<host>[:port]/GetPassLineCountStatistics[/channelId]` |
| **Products** | IPC |
| **Channel ID** | Optional (default 1) |

> **v2.0 only.**

**Response:**

```xml
<?xml version="1.0" encoding="utf-8"?>
<config xmlns="http://www.ipc.com/ver10" version="2.0.0">
  <entranceCount>
    <person type="uint32">0</person>
    <car type="uint32">0</car>
    <bike type="uint32">0</bike>
  </entranceCount>
  <exitCount>
    <person type="uint32">0</person>
    <car type="uint32">0</car>
    <bike type="uint32">0</bike>
  </exitCount>
</config>
```

---

### GetSmartVsdConfig

Video metadata detection (full-frame object detection) configuration.

| Field | Value |
|-------|-------|
| **URL** | `POST` or `GET http://<host>[:port]/GetSmartVsdConfig[/channelId]` |
| **Products** | IPC |
| **Channel ID** | Optional (default 1) |

---

### GetSmartLoiteringConfig

Loitering detection configuration.

| Field | Value |
|-------|-------|
| **URL** | `POST` or `GET http://<host>[:port]/GetSmartLoiteringConfig[/channelId]` |
| **Products** | IPC |
| **Channel ID** | Optional (default 1) |

---

### GetSmartPvdConfig

Illegal parking detection configuration.

| Field | Value |
|-------|-------|
| **URL** | `POST` or `GET http://<host>[:port]/GetSmartPvdConfig[/channelId]` |
| **Products** | IPC |
| **Channel ID** | Optional (default 1) |

---

### GetMeasureTemperatureConfig

Thermal imaging temperature measurement configuration.

| Field | Value |
|-------|-------|
| **URL** | `POST` or `GET http://<host>[:port]/GetMeasureTemperatureConfig[/channelId]` |
| **Products** | IPC (Thermal cameras only) |
| **Channel ID** | Optional (default 1) |

> **v2.0 only.**

---

*Published by CCTV Camera Pros -- https://www.cctvcamerapros.com*

*Last updated: March 30, 2026*
