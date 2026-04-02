---
title: "Video Metadata Detection (VSD) Configuration"
description: "API reference for GetSmartVsdConfig — configure full-frame video metadata object detection on Viewtron IP cameras."
keywords: [ip camera video metadata api, viewtron api, vsd object detection config]
sidebar_label: "Video Metadata"
sidebar_position: 7
---

# Video Metadata Detection (VSD) Configuration

## GetSmartVsdConfig

Retrieves video metadata detection (VSD) configuration. VSD performs full-frame object detection and classification across the entire camera view, without requiring a defined detection zone.

| Field | Value |
|-------|-------|
| **Endpoint** | `/GetSmartVsdConfig[/channelId]` |
| **Method** | `POST` or `GET` |
| **Products** | IPC |
| **Channel ID** | Optional (default `1`) |

### Response

The response returns the VSD configuration in the standard `<config>` XML wrapper. Query this endpoint against your camera to see the full XML structure for your firmware version.

### Notes

- VSD (Video Structured Detection) differs from perimeter/intrusion detection in that it analyzes the entire frame rather than a specific zone.
- VSD is used for general-purpose object detection and metadata extraction, providing structured data about all detected targets in the scene.
- The corresponding Set command is `SetSmartVsdConfig` using the same XML structure returned by the Get command.
- VSD webhook events use `smartType` value `VSD` (IPC format).

## Related Endpoints

| Endpoint | Purpose |
|----------|---------|
| [GetSmartPerimeterConfig](/docs/api-reference/smart-detection/intrusion-perimeter-detection-config) | Zone-based intrusion detection (alternative to full-frame VSD) |
| [SetHttpPostConfig](/docs/api-reference/alarm/http-post-webhook-config) | Configure webhook destination |
