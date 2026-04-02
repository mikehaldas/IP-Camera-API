---
title: "Face Detection Configuration"
description: "API reference for GetSmartVfdConfig — configure face detection zones and sensitivity on Viewtron AI IP cameras."
keywords: [ip camera face detection api, viewtron api, camera face recognition config]
sidebar_label: "Face Detection"
sidebar_position: 3
---

# Face Detection Configuration

:::tip Application Guide
For a complete walkthrough with code examples, see the [Face Detection & Recognition](/docs/applications/face-detection-recognition-api) application guide.
:::

## GetSmartVfdConfig

Retrieves face detection configuration for the specified channel.

| Field | Value |
|-------|-------|
| **Endpoint** | `/GetSmartVfdConfig[/channelId]` |
| **Method** | `POST` or `GET` |
| **Products** | IPC |
| **Channel ID** | Optional (default `1`) |

### Response

The response returns the face detection configuration in the same XML format used by other smart detection commands. The structure follows the standard `<config>` wrapper with detection-specific settings.

### Notes

- Face detection is available on Viewtron AI cameras with face detection firmware.
- The API guide defines the endpoint but does not include a detailed response example for this command. Use `GetSmartVfdConfig` against your camera to see the full XML structure for your firmware version.
- The corresponding Set command is `SetSmartVfdConfig` using the same XML structure returned by the Get command.
- Face detection webhook events use `smartType` value `VFD` (IPC format) or `faceDetection` (NVR format).

## Related Endpoints

| Endpoint | Purpose |
|----------|---------|
| [SetHttpPostConfig](/docs/api-reference/alarm/http-post-webhook-config) | Configure webhook destination for face detection alerts |
| [GetSmartPerimeterConfig](/docs/api-reference/smart-detection/intrusion-perimeter-detection-config) | Intrusion detection (often used alongside face detection) |
