---
title: "HTTP POST Webhook Configuration"
description: "API reference for HTTP POST webhook configuration — set up httpPostV2 event subscriptions and URLs on Viewtron IP cameras."
keywords: [ip camera webhook config api, viewtron api, httppostv2 setup]
sidebar_label: "Webhook Config"
sidebar_position: 6
---

# HTTP POST Webhook Configuration

:::tip Application Guide
For a complete walkthrough of webhook setup with server examples, see the [Webhook Event Notification](/docs/applications/webhook-event-notification-api) application guide. For real-time tracking data, see [Real-Time Object Tracking](/docs/applications/real-time-object-tracking-api).
:::

Configure the HTTP POST webhook system that pushes real-time alarm events and AI detection data to your server. The IPC supports two modes:

- **httpPost (v1)** -- Basic alarm server. One URL, one post per alarm event.
- **httpPostV2** -- Advanced subscription system. Up to 3 URLs, per-URL event type filtering, per-URL data type subscriptions. Supports continuous real-time `traject` tracking data.

Both modes are configured via `GetHttpPostConfig` / `SetHttpPostConfig` -- these are separate from the [Legacy Alarm Server](legacy-alarm-server.md) endpoints.

The NVR also has an HTTP POST system configured through its web interface. The NVR system sends alarm events using v2.0 XML format but does **not** support `traject`.

> Tested: IPC v1.9 (firmware 5.1.4.0, API version 1.7)

---

## GetHttpPostConfig

Retrieves the current httpPost and httpPostV2 configuration.

| Field | Value |
|-------|-------|
| **Endpoint** | `/GetHttpPostConfig` |
| **Method** | `POST` or `GET` |
| **Products** | IPC |
| **Request Body** | None |

### Response Example

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

### httpPost (v1) Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `bSwitch` | boolean | Enable or disable httpPost v1 |
| `protocolType` | string | Protocol type (typically `API`) |
| `serverIp` | string | IP address of your receiving server |
| `serverPort` | uint16 | Port your server listens on |
| `keepaliveTimeval` | uint32 | Keepalive interval in seconds (30-120) |
| `onlineStatus` | boolean | Current connection status (read-only) |
| `URL` | string | URL path on your server (e.g., `/API`) |

### httpPostV2 Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `urlId` | uint32 | URL slot identifier (1, 2, or 3) |
| `switch` | boolean | Enable or disable this URL slot |
| `url.protocol` | string | `http` or `https` |
| `url.domain` | string | IP address or hostname of your server |
| `url.port` | uint16 | Port your server listens on |
| `url.path` | string | URL path on your server |
| `url.authentication` | string | Authentication type (`none` or other) |
| `heatBeatSwitch` | boolean | Enable keepalive heartbeat |
| `keepaliveTimeval` | uint32 | Keepalive interval in seconds (30-120) |
| `subscribeDateType` | list | Data types to include in posts (see table below) |
| `subscriptionEvents` | list | Detection event types to subscribe to (see list below) |

---

## SetHttpPostConfig

Sets the httpPost and/or httpPostV2 configuration.

| Field | Value |
|-------|-------|
| **Endpoint** | `/SetHttpPostConfig` |
| **Method** | `POST` |
| **Products** | IPC |
| **Request Body** | `httpPost` and/or `httpPostV2` XML element |

### Setting httpPost (v1)

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

### Setting httpPostV2

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

---

## httpPostV2 Subscription Events

The `subscriptionEvents` field controls which detection types trigger posts to this URL:

| Event | Description |
|-------|-------------|
| `ALL` | Subscribe to all event types |
| `MOTION` | Basic motion detection |
| `SENSOR` | Physical sensor alarm input |
| `PERIMETER` | AI perimeter / intrusion zone |
| `TRIPWIRE` | AI line crossing / tripwire |
| `OSC` | Object removal (left/missing) |
| `AVD` | Abnormal video detection |
| `AOIENTRY` | Region entry |
| `AOILEAVE` | Region exit |
| `PASSLINECOUNT` | Object counting by line |
| `TRAFFIC` | Object counting by area |
| `VSD` | Video metadata detection |
| `PVD` | Parking violation detection |
| `LOITER` | Loitering detection |
| `ASD` | Audio sound detection |

---

## httpPostV2 Data Types (subscribeDateType)

The `subscribeDateType` field controls what data is included in each post:

| Data Type | GUI Label | Description | Post Frequency | Post Size |
|-----------|-----------|-------------|----------------|-----------|
| `alarmStatus` | Alarm status data | Alarm on/off status change | One per state change | ~660 bytes |
| `traject` | Smart track data | Continuous trajectory tracking with real-time coordinates | ~7 posts/sec while tracking | ~1.7 KB |
| `smartData` | Smart event data | Detection event with coordinates and metadata | One per event | ~2-3 KB (no images) |
| `sourceImage` | Original picture | Full frame JPEG (base64 encoded in XML) | One per event | ~500-530 KB |
| `targetImage` | Target picture | Cropped target JPEG (base64 encoded in XML) | One per event | Included with smartData |

:::info Image Data
`sourceImage` and `targetImage` are embedded in the smartData XML post as base64 data. Subscribing to `smartData` + `sourceImage` + `targetImage` produces a single large post per event containing all three. See [httpPostV2 Data Types](/docs/api-reference/events/httppostv2-data-types) for detailed format documentation.
:::

---

## Configuration Notes

- httpPostV2 supports up to **3 URLs** (`maxCount="3"`), each with independent event and data type subscriptions. This lets you route different event types or data to different servers.
- `keepaliveTimeval` range is **30-120 seconds**.
- Both httpPost v1 and httpPostV2 can be set in a single request by including both elements in the XML body.
- For real-time tracking data, subscribe to `traject` in the `subscribeDateType`. See the [traject documentation](/docs/api-reference/events/real-time-target-tracking-traject) for details on the tracking data format.
- The NVR configures its HTTP POST system through the web interface, not through this API endpoint. The NVR sends events in v2.0 XML format and does not support `traject`.
