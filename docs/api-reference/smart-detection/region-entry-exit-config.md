---
title: "Region Entry/Exit Detection Configuration"
description: "API reference for region entry and exit detection — configure area-of-interest triggers on Viewtron IP cameras."
keywords: [ip camera region entry exit api, viewtron api, aoi detection config]
sidebar_label: "Region Entry/Exit"
sidebar_position: 5
---

# Region Entry/Exit Detection Configuration

:::tip Application Guide
For a complete walkthrough with code examples, see the [Perimeter Security & Line Crossing](/docs/applications/perimeter-security-line-crossing-api) application guide.
:::

## GetSmartAoiEntryConfig

Retrieves region entry detection configuration. Triggers an alarm when a target enters a defined area (AOI — Area of Interest).

| Field | Value |
|-------|-------|
| **Endpoint** | `/GetSmartAoiEntryConfig[/channelId]` |
| **Method** | `POST` or `GET` |
| **Products** | IPC |
| **Channel ID** | Optional (default `1`) |

## GetSmartAoiLeaveConfig

Retrieves region exit detection configuration. Triggers an alarm when a target leaves a defined area.

| Field | Value |
|-------|-------|
| **Endpoint** | `/GetSmartAoiLeaveConfig[/channelId]` |
| **Method** | `POST` or `GET` |
| **Products** | IPC |
| **Channel ID** | Optional (default `1`) |

### Response

Both endpoints return configuration in the same XML format as other smart detection commands, with detection zone polygon coordinates and object filter settings. The structure follows the standard `<config>` wrapper.

### Notes

- Region entry and exit are configured independently — you can enable one without the other.
- These commands complement tripwire (line crossing) detection. Tripwire detects crossing a line; AOI entry/exit detects entering or leaving a polygon region.
- The corresponding Set commands are `SetSmartAoiEntryConfig` and `SetSmartAoiLeaveConfig` using the same XML structure returned by the Get commands.
- AOI entry webhook events use `smartType` value `AOI_ENTRY` (IPC) or `regionEntrance` (NVR). AOI exit events use `AOI_LEAVE` (IPC) or `regionExiting` (NVR).
- Query these endpoints against your camera to see the full XML response structure for your firmware version.

## Related Endpoints

| Endpoint | Purpose |
|----------|---------|
| [GetSmartTripwireConfig](/docs/api-reference/smart-detection/line-crossing-tripwire-config) | Line crossing detection (complementary to region entry/exit) |
| [GetSmartPerimeterConfig](/docs/api-reference/smart-detection/intrusion-perimeter-detection-config) | Intrusion zone detection |
| [SetHttpPostConfig](/docs/api-reference/alarm/http-post-webhook-config) | Configure webhook destination |
