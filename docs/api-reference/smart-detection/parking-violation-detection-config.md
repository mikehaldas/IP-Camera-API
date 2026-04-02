---
title: "Parking Violation Detection Configuration"
description: "API reference for GetSmartPvdConfig — configure illegal parking detection zones and time thresholds on Viewtron IP cameras."
keywords: [ip camera parking detection api, viewtron api, parking violation config]
sidebar_label: "Parking Detection"
sidebar_position: 9
---

# Parking Violation Detection Configuration

:::tip Application Guide
For a complete walkthrough with code examples, see the [Vehicle Detection & Parking Management](/docs/applications/vehicle-detection-parking-management-api) application guide.
:::

## GetSmartPvdConfig

Retrieves illegal parking / parking violation detection (PVD) configuration. PVD triggers an alarm when a vehicle parks in a prohibited zone for longer than a configured time threshold.

| Field | Value |
|-------|-------|
| **Endpoint** | `/GetSmartPvdConfig[/channelId]` |
| **Method** | `POST` or `GET` |
| **Products** | IPC |
| **Channel ID** | Optional (default `1`) |

### Response

The response returns the parking violation detection configuration in the standard `<config>` XML wrapper, including the no-parking zone, dwell time threshold, and detection sensitivity. Query this endpoint against your camera to see the full XML structure for your firmware version.

### Notes

- PVD works similarly to loitering detection but is specifically designed for vehicles in no-parking zones.
- The detection zone defines the prohibited parking area — a vehicle must remain stationary in the zone beyond the time threshold to trigger an alarm.
- The corresponding Set command is `SetSmartPvdConfig` using the same XML structure returned by the Get command.
- Parking violation webhook events use `smartType` value `PVD` (IPC format).

## Related Endpoints

| Endpoint | Purpose |
|----------|---------|
| [GetSmartVehicleConfig](/docs/api-reference/smart-detection/license-plate-recognition-config) | License plate recognition (identify parked vehicles) |
| [GetSmartLoiteringConfig](/docs/api-reference/smart-detection/loitering-detection-config) | Loitering detection (similar dwell-time concept for people) |
| [SetHttpPostConfig](/docs/api-reference/alarm/http-post-webhook-config) | Configure webhook destination for parking alerts |
