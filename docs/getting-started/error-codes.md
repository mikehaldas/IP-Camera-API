---
title: "Error Codes Reference"
sidebar_label: "Error Codes"
description: "Complete error code reference for the Viewtron IP camera HTTP API, including base codes and specialized audio, face recognition, and LPR error codes."
keywords:
  - ip camera api error codes
  - camera api troubleshooting
  - viewtron api errors
sidebar_position: 4
---

# Error Codes Reference

When an API request fails, the response includes an `errorCode` attribute and (on v2.0 devices) an `errorDesc` with a human-readable description.

```xml
<?xml version="1.0" encoding="utf-8" ?>
<config status="failed" errorCode="1" errorDesc="Invalid Request"/>
```

:::note
v1.9 devices return only the numeric `errorCode`. v2.0 adds the `errorDesc` attribute.
:::

## Base Error Codes

These codes apply to all API commands on both v1.9 and v2.0 devices.

| Code | Description |
|------|-------------|
| 0 | Successful |
| 1 | **Invalid Request** — command name, channel ID, or action name not recognized |
| 2 | **Invalid XML Format** — XML cannot be parsed |
| 3 | **Invalid XML Content** — incomplete message or out-of-range parameters |
| 4 | **Permission Denied** — user lacks permission |
| 5 | **Network Port Error** — network port number error (v1.9) / client restricted by blacklist/whitelist (v2.0) |

## Extended Error Codes (v2.0)

These additional codes are available on v2.0 firmware.

| Code | Description |
|------|-------------|
| 6 | **Sensor ID Error** — invalid sensor ID |
| 7 | **System Busy** — system upgrading or importing config |
| 8 | **Password Expired** — change password and retry |
| 9 | **Unauthorized** — incorrect username or password |
| 10 | **User Locked** — user account locked |
| 11 | **Unsupported Function** — function not supported on this device |
| 12 | **Channel Error** — invalid channel ID |
| 13 | **SD Error** — SD card status error |
| 14 | **Action Error** — invalid action name in URL |
| 15 | **Missing Required Parameters** |
| 16 | **Range Error** — parameter value out of range |
| 17 | **Service Not Enabled** — API service not enabled |
| 18 | **Modification Not Allowed** — change would cause system restart |
| 19 | **Over Specifications** — exceeding system limits |
| 79 | **Internal Error** — device processing error |
| 80 | **Upgrade Error** |
| 81 | **Upgrade Version Same** |
| 82 | **Upgrade Package Error** — package doesn't match device |
| 83 | **Upgrade Signature Error** |
| 84 | **Upgrade Incompatible** |

## Audio Error Codes (v2.0)

Returned by audio-related commands.

| Code | Description |
|------|-------------|
| 101 | Audio not working |
| 102 | Audio parameter error |
| 103 | Audio not PCM format |
| 104 | Audio not Wave format |
| 105 | Audio sampling rate error |
| 106 | Audio save failed |
| 107 | Audio file count over limit |
| 108 | Audio file too large |
| 109 | Audio file does not exist |
| 110 | Audio alarm already active |
| 111 | Audio file occupied by another process |

## Face Processing Error Codes (v2.0)

Returned by [face detection configuration](/docs/api-reference/smart-detection/face-detection-config) commands.

| Code | Description |
|------|-------------|
| 150 | General face processing error |
| 151 | Exceeding maximum face sample library limit |
| 152 | Face picture format not supported |
| 153 | No face or more than one face in the picture |
| 154 | Picture is too large |
| 155 | Same face already exists in face sample library |
| 156 | Face does not exist |
| 157 | Face group already exists |
| 158 | Exceeding maximum face groups limit |
| 159 | Face group does not exist |

## License Plate Processing Error Codes (v2.0)

Returned by [license plate recognition configuration](/docs/api-reference/smart-detection/license-plate-recognition-config) commands.

| Code | Description |
|------|-------------|
| 201 | General license plate processing error |
| 202 | Exceeding maximum license plate library limit |
| 203 | Same license plate already exists |
| 204 | License plate not found |
| 205 | License plate group already exists |
| 206 | Exceeding maximum license plate groups limit |
| 207 | License plate group does not exist |
