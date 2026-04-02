---
title: "GetDateAndTime / SetDateAndTime — Time Configuration"
description: "API reference for GetDateAndTime and SetDateAndTime — configure timezone, NTP, and system clock on Viewtron IP cameras and NVRs."
keywords: [ip camera time config api, viewtron api, ntp camera configuration]
sidebar_label: "Date & Time"
sidebar_position: 8
---

# GetDateAndTime / SetDateAndTime

Get or set the system date, time, timezone, and NTP configuration.

## Endpoint

| Field | Value |
|-------|-------|
| **Method** | `POST` or `GET` (Get) / `POST` (Set) |
| **URL (Get)** | `http://<host>[:port]/GetDateAndTime` |
| **URL (Set)** | `http://<host>[:port]/SetDateAndTime` |
| **Products** | IPC, NVR |
| **Channel ID** | N/A |

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `timeZone` | string | POSIX timezone string (e.g., `CST-8`) |
| `type` | synchronizeType | Sync method: `manually`, `NTP`, or `PC` |
| `ntpServer` | string | NTP server hostname (max 127 chars) |
| `ntpSyncInterval` | uint32 | NTP sync interval in minutes (30--10080) |
| `currentTime` | string | Current device time (`YYYY-MM-DD HH:MM:SS`) |
| `timeFormatMode` | timeFormatModeType | 12-hour or 24-hour display (v1.9) |

## GetDateAndTime Response (v2.0)

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

## GetDateAndTime Response (v1.9)

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

## SetDateAndTime Request (v2.0)

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

## Notes

- The `timeZone` field uses POSIX timezone format (e.g., `CST-8` for China Standard Time, `EST5EDT` for US Eastern).
- v1.9 includes additional daylight saving time fields (`startTime`, `endTime`, `offSet`, `daylightSwitch`) in the `timezoneInfo` block.
- When setting time manually, provide the `currentTime` field in `YYYY-MM-DD HH:MM:SS` format.
- NTP sync interval ranges from 30 minutes to 10080 minutes (7 days). Default is 1440 minutes (24 hours).
