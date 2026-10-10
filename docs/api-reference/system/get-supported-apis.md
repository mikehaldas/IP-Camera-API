---
title: "GetSupportedAPIs — Available Endpoints"
description: "API reference for GetSupportedAPIs — discover all available HTTP API endpoints on a Viewtron IP camera or NVR."
keywords: [ip camera supported apis, viewtron api discovery, camera api endpoints]
sidebar_label: "Supported APIs"
sidebar_position: 2
---

# GetSupportedAPIs

Retrieves the list of all API endpoints supported by the device.

## Endpoint

| Field | Value |
|-------|-------|
| **Method** | `POST` or `GET` |
| **URL** | `http://<host>[:port]/GetSupportedAPIs` |
| **Products** | IPC, NVR |
| **Channel ID** | N/A |

:::caution v2.x only (2.0 and 2.1)
This command does not exist on v1.9 firmware.
:::

## Response

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

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `applicationInterfaces` | list | List of supported API endpoint names |
| `count` | attribute | Total number of supported endpoints |
| `item` | string | Individual API endpoint name |

## Notes

- Use the API names in each `<item>` to look up commands in this documentation.
- The `count` attribute may not equal the number of `<item>` elements, and a name can appear more than once. De-duplicate the names before use. Verified on a camera running 5.3.1 firmware, `count` was 111 and the list contained 90 unique names, with duplicates.
- This is the recommended way to check whether a command exists before calling it. Command sets differ by device type and firmware (for example, plate database commands on v2.1 cameras).
