---
title: "GetDeviceDetail — Extended Device Properties"
description: "API reference for GetDeviceDetail — retrieve extended device properties and smart feature flags from Viewtron IP cameras."
keywords: [ip camera device detail api, viewtron api, camera smart features]
sidebar_label: "Device Detail"
sidebar_position: 7
---

# GetDeviceDetail

Retrieves detailed device information including smart feature support flags. **IPC only.**

## Endpoint

| Field | Value |
|-------|-------|
| **Method** | `POST` or `GET` |
| **URL** | `http://<host>[:port]/GetDeviceDetail` |
| **Products** | IPC |
| **Channel ID** | N/A |

## Response

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

## Response Blocks

The response contains four property blocks:

### `<property>` -- Device Identity

Basic device identification fields (same as `GetDeviceInfo`).

### `<smart>` -- AI/Analytics Feature Support

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

### `<image>` -- Image Feature Support

| Field | Description |
|-------|-------------|
| `supportAZ` | Auto-zoom support |
| `supportROI` | Region of Interest encoding |
| `supportInfraredLamp` | IR illuminator control |
| `supportWatermark` | Video watermark |
| `supportPrivateMask` | Privacy masking zones |

### `<alarm>` -- Alarm Feature Support

| Field | Description |
|-------|-------------|
| `supportMultiMotionSensitivity` | Multiple motion sensitivity zones |
| `supportAlarmServer` | External alarm server integration |
| `supportAudioAlarmOut` | Audio alarm output |
| `supportWhiteLightAlarmOut` | White light alarm output |

## Notes

- This endpoint provides the most comprehensive feature discovery for IPC devices.
- Use the `<smart>` block to determine which AI detection APIs are available before configuring them.
- The `<system>` block duplicates some fields from `GetDeviceInfo` for convenience.
