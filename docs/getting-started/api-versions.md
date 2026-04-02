---
title: "API Versions — v1.9 and v2.0"
sidebar_label: "API Versions"
description: "Viewtron IP cameras ship with v1.9 or v2.0 firmware. The HTTP API is 95% identical between versions. Learn the differences and how to detect your version."
keywords:
  - viewtron api version
  - camera firmware api
  - ip camera api v2
sidebar_position: 3
---

# API Versions

Viewtron devices ship with one of two firmware generations. The HTTP API protocol is approximately **95% identical** between them. This documentation covers both versions as a unified reference, with inline callouts where they differ.

## Detecting Your Version

Send a `GetDeviceInfo` request. The response includes an `apiVersion` field:

```xml
<apiVersion type="string"><![CDATA[2.0.0]]></apiVersion>
```

If there is no `apiVersion` field, use `GetDeviceDetail` — the `apiVersion` appears in the `property` block. Devices without either field are running the v1.x protocol.

## Firmware-to-Protocol Mapping

| Firmware | API Protocol | Config Version in XML |
|----------|-------------|----------------------|
| IPC 5.2 or earlier | v1.9 (v1.0 / v1.7) | `1.0` or `1.7` |
| IPC 5.3 or later | v2.0.0 | `2.0.0` |
| NVR 1.4.12 or earlier | v1.9 | `1.0` or `1.7` |
| NVR 1.4.13 or later | v2.0.0 | `2.0.0` |

## What Changed in v2.0

### New Commands

| Command | Description |
|---------|-------------|
| [GetSupportedAPIs](/docs/api-reference/system/get-supported-apis) | Lists all available API endpoints on the device |
| [TriggerVirtualAlarm](/docs/api-reference/alarm/trigger-virtual-alarm) | Trigger a virtual alarm (NVR only) |
| [GetAudioStreamConfig](/docs/api-reference/image/get-audio-stream-config) | Audio stream configuration |
| [GetPassLineCountStatistics](/docs/api-reference/smart-detection/line-counting-config) | Current entrance/exit counts |
| [GetMeasureTemperatureConfig](/docs/api-reference/smart-detection/thermal-temperature-config) | Thermal camera temperature measurement |
| [GetVehiclePlate](/docs/api-reference/smart-detection/license-plate-recognition-config) | Query license plate database |

### Renamed Commands

| v1.9 Name | v2.0 Name | Change |
|-----------|-----------|--------|
| `GetChannelList` | `GetChannelInfo` | Richer response with channel types and names |
| `GetAlarmInList` | `GetAlarmInInfo` | Adds alarm type classification (local/virtual/remote) |

### Enhanced Responses

- `GetDeviceInfo` now includes `apiVersion` and `httpPostVersion` fields directly
- `GetImageConfig` adds `sharpen`, `denoise`, `backlightCompensation`, `infraredMode` fields
- `GetSnapshotByTime` returns base64 image data in XML (v1.9 returns raw JPEG)
- `GetDiskInfo` adds `storageType` (SD/HDD) and `locked` status
- Error codes expanded from 5 to 50+ with descriptive `errorDesc` attribute
- Responses include `Applicable Products` metadata (IPC, NVR, or both)

### Webhook Event Format Differences

The HTTP POST webhook format differs significantly between IPC (v1.x) and NVR (v2.0):

- **IPC v1.x** uses short smartType codes: `PEA`, `VFD`, `VEHICE`, `PASSLINECOUNT`
- **NVR v2.0** uses spelled-out names: `regionIntrusion`, `videoFaceDetect`, `vehicle`, `targetCountingByLine`
- NVR v2.0 adds `messageType` (keepalive, alarmStatus, alarmData) and `deviceInfo` with IP, MAC, and channel ID
- Timestamp precision: v1.x uses milliseconds, v2.0 uses microseconds

See the [Webhook Events](/docs/api-reference/events/webhook-overview) section for full format details.

## Using the Python Library

The [viewtron.py](https://github.com/mikehaldas/IP-Camera-API) library abstracts the differences between v1.x and v2.0 webhook formats. Both versions expose the same method interface — `get_alarm_type()`, `get_plate_number()`, `get_source_image()`, etc. — so your application code works identically regardless of firmware version.

```python
from viewtron import LPR, VehicleLPR

# v1.x IPC events use LPR class
# v2.0 NVR events use VehicleLPR class
# Both expose the same interface:
#   event.get_plate_number()
#   event.get_source_image()
#   event.images_exist()
```

After this section, you should not need to think about versions unless you encounter a specific callout in the documentation.
