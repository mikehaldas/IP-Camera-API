---
title: "Loitering Detection Configuration"
description: "API reference for GetSmartLoiteringConfig — configure loitering detection time thresholds and zones on Viewtron IP cameras."
keywords: [ip camera loitering detection api, viewtron api, camera loitering alarm config]
sidebar_label: "Loitering"
sidebar_position: 8
---

# Loitering Detection Configuration

:::tip Application Guide
For a complete walkthrough with code examples, see the [Loitering Detection](/docs/applications/loitering-detection-api) application guide.
:::

## GetSmartLoiteringConfig

Retrieves loitering detection configuration. Loitering detection triggers an alarm when a person or vehicle remains within a defined zone for longer than a configured time threshold.

| Field | Value |
|-------|-------|
| **Endpoint** | `/GetSmartLoiteringConfig[/channelId]` |
| **Method** | `POST` or `GET` |
| **Products** | IPC |
| **Channel ID** | Optional (default `1`) |

### Response

The response returns the loitering detection configuration in the standard `<config>` XML wrapper, including the detection zone, dwell time threshold, and object filter settings. Query this endpoint against your camera to see the full XML structure for your firmware version.

### Notes

- Loitering detection combines zone-based detection with a time threshold — a target must remain in the zone for the configured duration before an alarm triggers.
- This is useful for detecting suspicious behavior such as someone lingering near a door, ATM, or restricted area.
- The corresponding Set command is `SetSmartLoiteringConfig` using the same XML structure returned by the Get command.
- Loitering webhook events use `smartType` value `LOITERING` (IPC format) or `loiterDetection` (NVR format).

## Related Endpoints

| Endpoint | Purpose |
|----------|---------|
| [GetSmartPerimeterConfig](/docs/api-reference/smart-detection/intrusion-perimeter-detection-config) | Intrusion detection (immediate trigger, no dwell time) |
| [GetSmartAoiEntryConfig](/docs/api-reference/smart-detection/region-entry-exit-config) | Region entry detection |
| [SetHttpPostConfig](/docs/api-reference/alarm/http-post-webhook-config) | Configure webhook destination for loitering alerts |
