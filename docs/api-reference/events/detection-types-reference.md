---
title: "Detection Types Reference — All Event Types"
description: "Complete reference of all AI detection types and smartType codes supported by Viewtron IP cameras and NVRs via HTTP Post."
keywords: [ip camera detection types, viewtron api smart types, camera ai event codes]
sidebar_label: "Detection Types"
sidebar_position: 2
---

# Detection Types Reference

This page lists every detection type supported by Viewtron IP cameras and NVRs via HTTP Post, including the smartType codes used in each format, which products support them, and their test status.

## Quick Reference -- All Detection Types

| IPC smartType | NVR v2.0 smartType | Detection | Products | Tested |
|---|---|---|---|---|
| `PEA` (intrusion) | `regionIntrusion` | Perimeter / intrusion zone | IPC, NVR | Yes (IPC Nov 2025, NVR Feb 2026) |
| `PEA` (line cross) | `lineCrossing` | Tripwire / line crossing | IPC, NVR | Yes (NVR Feb 2026) |
| `VEHICE` | `vehicle` | License plate recognition (LPR) | IPC, NVR | Yes (NVR Feb 2026) |
| `VFD` | `videoFaceDetect` | Face detection with attributes | IPC, NVR | Yes (NVR Feb 2026) |
| `VFD_MATCH` | Not supported by NVR | Face recognition / match | IPC only | NVR does not forward match data |
| `VSD` | `videoMetadata` | Video metadata (full-frame detection) | IPC, NVR | Yes (NVR Feb 2026) |
| `PASSLINECOUNT` | `targetCountingByLine` | Object counting by line | IPC, NVR | Yes (NVR Feb 2026) |
| `TRAFFIC` | `targetCountingByArea` | Object counting by area | IPC, NVR | Yes (NVR Feb 2026) |
| `MOTION` | TBD | Motion detection | IPC, NVR | Not yet tested via HTTP Post |
| `AOIENTRY` | TBD | Region entry | IPC, NVR | Not yet tested via HTTP Post |
| `AOILEAVE` | TBD | Region exit | IPC, NVR | Not yet tested via HTTP Post |
| `OSC` | TBD | Object removal (left/missing) | IPC | Not yet tested via HTTP Post |
| `CPC` | TBD | People counting | IPC | Not yet tested via HTTP Post |
| `CDD` | TBD | Crowd density detection | IPC | Not yet tested via HTTP Post |
| `SENSOR` | TBD | Sensor alarm | IPC, NVR | Not yet tested via HTTP Post |

:::note PEA covers two detection types
IPC `PEA` is a single smartType that covers both intrusion and line crossing. The alarm data differentiates them by containing either a `<perimeter>` or `<tripwire>` block. The NVR uses separate smartType values (`regionIntrusion` vs `lineCrossing`).
:::

## IPC smartType Codes (Complete)

The following table lists all IPC smartType codes, their corresponding alarm data and alarm status fields, and whether they include images.

| smartType | Description | AlarmData Field | AlarmStatus Field | Images |
|-----------|-------------|-----------------|-------------------|--------|
| `MOTION` | Motion detection | `motion` (grid) | `motionAlarm` | Yes |
| `SENSOR` | Sensor alarm | None | `sensorAlarm` | No |
| `PEA` (intrusion) | Perimeter intrusion | `perimeter/perInfo` | `perimeterAlarm` | Yes |
| `PEA` (line cross) | Line crossing | `tripwire/tripInfo` | `tripwireAlarm` | Yes |
| `AVD` (blur) | Video blur | None | `clarityAbnormal` | No |
| `AVD` (cast) | Video cast | None | `colorAbnormal` | No |
| `AVD` (scene) | Scene change | None | `sceneChange` | No |
| `OSC` | Object removal | `smartType: OSC` | `oscAlarm` | Yes |
| `CPC` | People counting | `CPC` | `CPCAlarm` | Yes |
| `CDD` | Crowd density | `CDD` | `CDDAlarm` | Yes |
| `IPD` | People intrusion | `IPD` | `IPDAlarm` | Yes |
| `VFD` | Face detection | `VFD` | `VFDAlarm` | Yes |
| `VFD_MATCH` | Face recognition | `VFD_MATCH` | `VFDAlarm` | Yes |
| `VEHICE` | License plate | `VEHICE` | `vehiceAlarm` | Yes |
| `AOIENTRY` | Region entry | `AOIENTRY` | (undocumented) | Yes |
| `AOILEAVE` | Region exit | `AOILEAVE` | (undocumented) | Yes |
| `PASSLINECOUNT` | Line counting | `PASSLINECOUNT` | (undocumented) | Yes |
| `TRAFFIC` | Area counting | `TRAFFIC` | (undocumented) | Yes |

## NVR alarmStatus Field Names

When the NVR sends `alarmStatus` messages, the field name inside `<alarmStatusInfo>` varies by detection type:

| Detection Type | alarmStatusInfo Field |
|----------------|----------------------|
| `regionIntrusion` | `perimeterAlarm` |
| `lineCrossing` | `perimeterAlarm` |
| `targetCountingByLine` | `passlineAlarm` |
| `targetCountingByArea` | `passlineAlarm` |
| `videoMetadata` | None (no alarmStatus sent) |
| `vehicle` | None observed |
| `videoFaceDetect` | `vfdAlarm` |

:::tip Application Guides
For application-specific setup instructions for each detection type, see:
- [Human Detection & Intrusion](/docs/applications/human-detection-intrusion-api)
- [Perimeter Security & Line Crossing](/docs/applications/perimeter-security-line-crossing-api)
- [License Plate Recognition](/docs/applications/license-plate-recognition-camera-api)
- [Face Detection & Recognition](/docs/applications/face-detection-recognition-api)
- [People Counting & Traffic Analytics](/docs/applications/people-counting-traffic-analytics-api)
- [Vehicle Detection & Parking](/docs/applications/vehicle-detection-parking-management-api)
:::
