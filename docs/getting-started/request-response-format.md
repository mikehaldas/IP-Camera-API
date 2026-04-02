---
title: "Request & Response Format"
sidebar_label: "Request & Response"
description: "Viewtron IP camera API requests use HTTP POST with XML payloads. Learn the URL format, XML conventions, data types, and response structure."
keywords:
  - ip camera api format
  - camera api xml
  - http post camera api
  - viewtron api request format
sidebar_position: 2
---

# Request & Response Format

The Viewtron API uses **HTTP POST** requests with **XML payloads** and returns XML responses. GET also works for read-only commands on most firmware versions, but POST is the recommended method.

## URL Format

```
http://<host>[:port]/<command>[/channelId][/action]
```

| Component | Description |
|-----------|-------------|
| `host` | IP address or hostname of the device |
| `port` | HTTP port (default 80) |
| `command` | API command name (e.g., `GetDeviceInfo`, `PtzControl`) |
| `channelId` | Channel number (optional, default `1`). For single-channel IP cameras, can be omitted. |
| `action` | Sub-operation for some commands (e.g., `PtzControl/1/Up`) |

**Examples:**

```
http://192.168.0.50/GetDeviceInfo
http://192.168.0.50/GetImageConfig/1
http://192.168.0.50/PtzControl/1/Up
```

## Request with XML Body

For SET commands that modify configuration, include an XML body:

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

## Response Format

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

:::note
v2.0 adds the `errorDesc` attribute with human-readable error descriptions. v1.9 returns only the numeric `errorCode`. See the [Error Codes](/docs/getting-started/error-codes) reference for all codes.
:::

## XML Conventions

### Element Naming

All elements use **camelCase** (e.g., `deviceName`, `alarmHoldTime`).

### Data Types

Each element has a `type` attribute defining its data type:

| Type | Description |
|------|-------------|
| `boolean` | `true` or `false` |
| `int8` / `uint8` | 8-bit signed/unsigned integer |
| `int16` / `uint16` | 16-bit signed/unsigned integer |
| `int32` / `uint32` | 32-bit signed/unsigned integer |
| `int64` / `uint64` | 64-bit signed/unsigned integer |
| `string` | Character string (value wrapped in CDATA) |
| `list` | List of items |

### Numeric Elements

Numeric elements may include `min`, `max`, and `default` attributes defining valid ranges:

```xml
<bright type="uint8" min="0" max="100" default="50">50</bright>
```

### String Elements

String elements may include `minLen`, `maxLen`, `minCharNum`, `maxCharNum` attributes. Values are wrapped in CDATA:

```xml
<ntpServer type="string" minLen="0" maxLen="127">
  <![CDATA[time.windows.com]]>
</ntpServer>
```

### List Elements

Lists use `maxCount` for the maximum allowed items and `count` for the current number:

```xml
<content type="list" count="2" maxCount="6">
  <itemType type="string" minLen="0" maxLen="32"/>
  <item><![CDATA[111111]]></item>
  <item><![CDATA[222222]]></item>
</content>
```

### Enum Types

When basic data types are insufficient, the response defines enum types in a `<types>` element:

```xml
<types>
  <userType>
    <enum>administrator</enum>
    <enum>advance</enum>
    <enum>normal</enum>
  </userType>
</types>
```

These enums are defined by the device and used as type references elsewhere in the response.

:::note
v2.0 adds annotation conventions: `<!--Required-->`, `<!--Optional-->`, `<!--Dependent-->` comments in XML blocks indicate whether fields are mandatory.
:::
