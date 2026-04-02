---
title: "Image Data Handling — Base64 Encoding"
description: "Guide to handling base64-encoded JPEG images in webhook event data from Viewtron IP cameras and NVRs."
keywords: [ip camera base64 image, viewtron api image data, camera snapshot decoding]
sidebar_label: "Image Data"
sidebar_position: 7
---

# Image Data Handling

All images in HTTP Post data are JPEG files encoded as base64 strings embedded in XML.

## Base64 Encoding

Both IPC and NVR posts embed images as base64-encoded JPEG data within `<sourceBase64Data>` and `<targetBase64Data>` XML elements. The base64 string can be decoded directly to a valid JPEG file.

## sourceBase64Data vs targetBase64Data

| Field | Content | Typical Size | Location (NVR) | Location (IPC) |
|-------|---------|--------------|-----------------|-----------------|
| `sourceBase64Data` | Full frame overview | ~400-530 KB | `sourceDataInfo/sourceBase64Data` | `sourceDataInfo/sourceBase64Data` |
| `targetBase64Data` | Cropped target | ~14-100 KB | `targetListInfo/item/targetImageData/targetBase64Data` | `listInfo/item/targetImageData/targetBase64Data` |

## Image Resolution by Detection Type

| Image Type | Detection Type | Typical Resolution |
|------------|---------------|--------------------|
| Source (overview) | Most types | 1280x720 or 1920x1080 |
| Source (overview) | videoMetadata | 1280x784 (may vary) |
| Source (overview) | vehicle | 0x0 metadata (firmware bug), but data present |
| Target (person crop) | regionIntrusion, lineCrossing, counting | 288x384 or 336x448 |
| Target (face crop) | videoFaceDetect | 184x184 (square) |
| Target (plate crop) | vehicle | 128x64 |

## Decoding Images in Python

```python
import base64

image_bytes = base64.b64decode(source_base64_data)
with open("snapshot.jpg", "wb") as f:
    f.write(image_bytes)
```

:::tip Application Guides
For NVR image configuration options (both images, original only, target only, or no images), see the [NVR Event Format](./nvr-event-format.md#image-configuration-options) page. For working code that extracts and saves images from webhook posts, see the [Webhook Event Notification API](/docs/applications/webhook-event-notification-api).
:::
