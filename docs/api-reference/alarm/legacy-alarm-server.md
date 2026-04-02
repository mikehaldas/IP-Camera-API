---
title: "Legacy Alarm Server Configuration"
description: "API reference for the legacy alarm server — configure the older alarm push system on Viewtron IP cameras (superseded by httpPostV2)."
keywords: [ip camera alarm server api, viewtron api, legacy alarm config]
sidebar_label: "Legacy Alarm Server"
sidebar_position: 5
---

# Legacy Alarm Server Configuration

:::tip Recommended Alternative
For new integrations, use the [HTTP POST Webhook Configuration](http-post-webhook-config.md) (httpPostV2) instead. It supports multiple URLs, event filtering, and data type subscriptions.
:::

A separate, older alarm server system. **IPC only.** This operates independently from the httpPost/httpPostV2 system. This page covers:

- **GetAlarmServerConfig / SetAlarmServerConfig** -- configure the legacy alarm server connection
- **SendAlarmStatus** -- the alarm data format sent by the device to your server

---

## GetAlarmServerConfig / SetAlarmServerConfig

| Field | Value |
|-------|-------|
| **Endpoint (Get)** | `/GetAlarmServerConfig` |
| **Endpoint (Set)** | `/SetAlarmServerConfig` |
| **Method (Get)** | `POST` or `GET` |
| **Method (Set)** | `POST` |
| **Products** | IPC |

### Response Example

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

### Parameters

| Parameter | Type | Range | Description |
|-----------|------|-------|-------------|
| `serverAddr` | string | -- | IP address or hostname of your alarm server |
| `serverPort` | uint16 | `1` - `65535` | Port your alarm server listens on |
| `enableHeartbeat` | boolean | `true` / `false` | Enable periodic keepalive to the server |
| `heartbeatInterval` | uint16 | `10` - `1800` | Heartbeat interval in seconds |

:::warning Known Issue
`SetAlarmServerConfig` returned error 499 in testing. Use `SetHttpPostConfig` instead (see [HTTP POST Webhook Configuration](http-post-webhook-config.md)).
:::

---

## SendAlarmStatus

This is **not** an endpoint you call. The camera sends this data **to your alarm server** when an alarm occurs. Your server must implement an HTTP endpoint to receive these POST requests.

| Field | Value |
|-------|-------|
| **URL** | `POST http://<your-alarm-server>[:port]/SendAlarmStatus` |
| **Direction** | Device to your server |

### Alarm Data Format

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

### Fields

| Field | Description |
|-------|-------------|
| `alarmStatusInfo` | Contains the alarm type and state (`true` = triggered) |
| `dataTime` | Timestamp of the alarm event |
| `deviceName` | User-configured device name |
| `deviceNo.` | Device number |
| `sn` | Device serial number |
| `ipAddress` | Device IP address |
| `macAddress` | Device MAC address |

---

## Notes

- This is a legacy system. The [httpPost/httpPostV2](http-post-webhook-config.md) system provides more features including event filtering, multiple server URLs, and data type subscriptions (images, tracking data).
- The legacy alarm server only sends basic alarm status changes -- it does not support smart detection event data, images, or traject tracking.
