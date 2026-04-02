---
title: "GetDeviceInfo — Device Information"
description: "API reference for GetDeviceInfo — query device model, firmware version, and capabilities on Viewtron IP cameras and NVRs."
keywords: [ip camera device info api, viewtron api, camera firmware version]
sidebar_label: "Device Info"
sidebar_position: 1
---

# GetDeviceInfo

Retrieves basic information about the device including model, firmware version, MAC address, capabilities, and API version.

## Endpoint

| Field | Value |
|-------|-------|
| **Method** | `POST` or `GET` |
| **URL** | `http://<host>[:port]/GetDeviceInfo` |
| **Products** | IPC, NVR |
| **Channel ID** | N/A |

> Tested: IPC v1.9 (firmware 5.1.4.0), NVR v2.0 (firmware 1.4.13)

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `deviceName` | string | User-assigned device name |
| `deviceDescription` | string | Device type descriptor |
| `apiVersion` | string | API protocol version (v2.0 only) |
| `softwareVersion` | string | Firmware version string |
| `softwareBuildDate` | string | Firmware build date |
| `kernelVersion` | string | Kernel version |
| `hardwareVersion` | string | Hardware revision |
| `model` | string | Device model number |
| `brand` | string | Brand identifier |
| `mac` | string | MAC address |
| `sn` | string | Serial number |
| `chlMaxCount` | uint32 | Maximum channel count |
| `audioInCount` | uint32 | Audio input count |
| `audioOutCount` | uint32 | Audio output count |
| `alarmInCount` | uint32 | Alarm input count |
| `alarmOutCount` | uint32 | Alarm output count |
| `integratedPtz` | boolean | Has integrated PTZ |
| `supportRS485Ptz` | boolean | Supports RS-485 PTZ control |
| `supportSDCard` | boolean | Supports SD card storage |

## Response (v2.0 IPC)

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

## Response (v2.0 NVR)

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

## Response (v1.9 IPC)

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

## Notes

- Use `apiVersion` to determine which protocol version the device supports.
- For fixed-channel devices (IPC, DVR): `audioInCount`, `audioOutCount`, `alarmInCount`, `alarmOutCount` are always included.
- For variable-channel devices (NVR): These may be optional. Use `GetChannelInfo`/`GetAlarmInInfo` for details.

:::info v2.0 Changes
v2.0 adds `apiVersion` and `httpPostVersion` fields directly in the response.
:::
