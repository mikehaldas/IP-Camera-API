---
title: "Intrusion & Perimeter Detection Configuration"
description: "API reference for GetSmartPerimeterConfig — configure intrusion zones, object filters, and alarm settings on Viewtron IP cameras."
keywords: [ip camera intrusion detection api, viewtron api, perimeter security config]
sidebar_label: "Intrusion Detection"
sidebar_position: 1
---

# Intrusion & Perimeter Detection Configuration

:::tip Application Guide
For a complete walkthrough with code examples, see the [Human Detection & Intrusion Detection](/docs/applications/human-detection-intrusion-api) application guide.
:::

## GetSmartPerimeterConfig

Retrieves intrusion/perimeter detection configuration. Returns the detection zone polygons, object filter settings, and alarm hold time for each configured intrusion region.

| Field | Value |
|-------|-------|
| **Endpoint** | `/GetSmartPerimeterConfig[/channelId]` |
| **Method** | `POST` or `GET` |
| **Products** | IPC |
| **Channel ID** | Optional (default `1`) |

### Response Example

```xml
<?xml version="1.0" encoding="utf-8"?>
<config xmlns="http://www.ipc.com/ver10" version="2.0.0">
  <perimeter>
    <switch type="boolean">true</switch>
    <alarmHoldTime type="uint32">20</alarmHoldTime>
    <objectFilter>
      <car>
        <switch type="boolean">true</switch>
        <sensitivity type="uint32" max="100" min="1" default="50">50</sensitivity>
      </car>
      <person>
        <switch type="boolean">true</switch>
        <sensitivity type="uint32" max="100" min="1" default="50">50</sensitivity>
      </person>
      <motor>
        <switch type="boolean">true</switch>
        <sensitivity type="uint32" max="100" min="1" default="50">50</sensitivity>
      </motor>
    </objectFilter>
    <saveTargetPicture type="boolean">false</saveTargetPicture>
    <saveSourcePicture type="boolean">false</saveSourcePicture>
    <regionInfo type="list" maxCount="4" count="1">
      <item>
        <pointGroup type="list" maxCount="8" count="4">
          <item>
            <X type="uint32">4075</X>
            <Y type="uint32">2466</Y>
          </item>
          <!-- Additional points... -->
        </pointGroup>
      </item>
    </regionInfo>
  </perimeter>
</config>
```

### Parameters

| Parameter | Type | Range | Description |
|-----------|------|-------|-------------|
| `switch` | boolean | `true` / `false` | Enable or disable perimeter detection |
| `alarmHoldTime` | uint32 | — | Duration (seconds) to hold the alarm state after detection |
| `objectFilter.car.switch` | boolean | `true` / `false` | Enable car/vehicle detection |
| `objectFilter.car.sensitivity` | uint32 | 1–100 (default 50) | Car detection sensitivity |
| `objectFilter.person.switch` | boolean | `true` / `false` | Enable person detection |
| `objectFilter.person.sensitivity` | uint32 | 1–100 (default 50) | Person detection sensitivity |
| `objectFilter.motor.switch` | boolean | `true` / `false` | Enable motorcycle/bicycle detection |
| `objectFilter.motor.sensitivity` | uint32 | 1–100 (default 50) | Motorcycle detection sensitivity |
| `saveTargetPicture` | boolean | `true` / `false` | Save cropped target image on detection |
| `saveSourcePicture` | boolean | `true` / `false` | Save full-frame source image on detection |
| `regionInfo` | list | maxCount: 4 | Intrusion detection zones (up to 4 regions) |
| `regionInfo.item.pointGroup` | list | maxCount: 8 | Polygon vertices defining the zone boundary (up to 8 points per region) |
| `regionInfo.item.pointGroup.item.X` | uint32 | — | X coordinate of polygon vertex |
| `regionInfo.item.pointGroup.item.Y` | uint32 | — | Y coordinate of polygon vertex |

### Notes

- Coordinates use the camera's internal coordinate system (typically 0–10000 range).
- Up to 4 independent intrusion zones can be configured, each with up to 8 polygon points.
- Each object filter (car, person, motor) can be independently enabled/disabled with its own sensitivity.
- The corresponding Set command is `SetSmartPerimeterConfig` using the same XML structure.

## Related Endpoints

| Endpoint | Purpose |
|----------|---------|
| [SetHttpPostConfig](/docs/api-reference/alarm/http-post-webhook-config) | Configure webhook destination for intrusion alerts |
| [GetAlarmStatus](/docs/api-reference/alarm/alarm-status) | Poll current alarm state |
