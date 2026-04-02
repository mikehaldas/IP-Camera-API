---
title: "Thermal Temperature Measurement Configuration"
description: "API reference for GetMeasureTemperatureConfig — retrieve thermal temperature measurement settings on Viewtron thermal cameras."
keywords: [thermal camera api, viewtron api, temperature measurement config]
sidebar_label: "Thermal"
sidebar_position: 10
---

# Thermal Temperature Measurement Configuration

## GetMeasureTemperatureConfig

Retrieves thermal imaging temperature measurement configuration. This endpoint is specific to Viewtron thermal cameras with temperature measurement capability.

| Field | Value |
|-------|-------|
| **Endpoint** | `/GetMeasureTemperatureConfig[/channelId]` |
| **Method** | `POST` or `GET` |
| **Products** | IPC (Thermal cameras only) |
| **Channel ID** | Optional (default `1`) |

:::info v2.0 Only
This endpoint is available only on API v2.0 firmware.
:::

### Response

The response returns the temperature measurement configuration in the standard `<config>` XML wrapper, including measurement zones, temperature thresholds, and alarm settings. Query this endpoint against your thermal camera to see the full XML structure for your firmware version.

### Notes

- This endpoint is only available on Viewtron thermal imaging cameras — standard visible-light cameras do not support temperature measurement.
- Thermal cameras can measure temperature across defined zones and trigger alarms when thresholds are exceeded.
- The corresponding Set command is `SetMeasureTemperatureConfig` using the same XML structure returned by the Get command.
- Temperature measurement can be combined with other smart detection features (e.g., intrusion detection) on dual-sensor thermal cameras.

## Related Endpoints

| Endpoint | Purpose |
|----------|---------|
| [SetHttpPostConfig](/docs/api-reference/alarm/http-post-webhook-config) | Configure webhook destination for temperature alerts |
| [GetAlarmStatus](/docs/api-reference/alarm/alarm-status) | Poll current alarm state |
