---
title: "Line Counting Configuration & Statistics"
description: "API reference for line counting — configure counting lines and retrieve entrance/exit statistics on Viewtron IP cameras."
keywords: [ip camera people counting api, viewtron api, line counting statistics]
sidebar_label: "Line Counting"
sidebar_position: 6
---

# Line Counting Configuration & Statistics

:::tip Application Guide
For a complete walkthrough with code examples, see the [People Counting & Traffic Analytics](/docs/applications/people-counting-traffic-analytics-api) application guide.
:::

This section covers two endpoints for line counting:

- **GetSmartPassLineCountConfig** — read the counting line configuration
- **GetPassLineCountStatistics** — retrieve current entrance/exit counts

---

## GetSmartPassLineCountConfig

Retrieves target counting by line configuration. This defines the counting line position, direction, and which object types to count.

| Field | Value |
|-------|-------|
| **Endpoint** | `/GetPassLineCountConfig[/channelId]` |
| **Method** | `POST` or `GET` |
| **Products** | IPC |
| **Channel ID** | Optional (default `1`) |

### Response

The response returns the counting line configuration in the standard `<config>` XML wrapper, including line position coordinates, counting direction, and object filter settings. Query this endpoint against your camera to see the full XML structure for your firmware version.

### Notes

- The URL path uses `GetPassLineCountConfig` (without "Smart" prefix), unlike most other smart detection endpoints.
- The corresponding Set command is `SetPassLineCountConfig`.
- The counting line works similarly to a tripwire but accumulates entrance and exit counts rather than triggering one-time alarms.

---

## GetPassLineCountStatistics

Retrieves current entrance/exit counting statistics, broken down by object type (person, car, bike).

| Field | Value |
|-------|-------|
| **Endpoint** | `/GetPassLineCountStatistics[/channelId]` |
| **Method** | `POST` or `GET` |
| **Products** | IPC |
| **Channel ID** | Optional (default `1`) |

:::info v2.0 Only
This endpoint is available only on API v2.0 firmware.
:::

### Response Example

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

### Response Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `entranceCount.person` | uint32 | Number of persons that crossed the line in the entrance direction |
| `entranceCount.car` | uint32 | Number of cars that crossed in the entrance direction |
| `entranceCount.bike` | uint32 | Number of bikes that crossed in the entrance direction |
| `exitCount.person` | uint32 | Number of persons that crossed the line in the exit direction |
| `exitCount.car` | uint32 | Number of cars that crossed in the exit direction |
| `exitCount.bike` | uint32 | Number of bikes that crossed in the exit direction |

### Notes

- Counts accumulate from the time counting was enabled or last reset.
- Poll this endpoint periodically to build occupancy and traffic analytics.
- Combine entrance and exit counts to calculate current occupancy: `occupancy = entranceCount - exitCount`.
- The camera counts three object types independently: person, car, and bike (bicycle/motorcycle).

## Related Endpoints

| Endpoint | Purpose |
|----------|---------|
| [GetSmartTripwireConfig](/docs/api-reference/smart-detection/line-crossing-tripwire-config) | Line crossing detection (alarm-based, not counting) |
| [SetHttpPostConfig](/docs/api-reference/alarm/http-post-webhook-config) | Configure webhook destination for counting events |
