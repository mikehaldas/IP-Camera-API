---
title: "Line Crossing & Tripwire Configuration"
description: "API reference for GetSmartTripwireConfig — configure line crossing detection, direction, and object filters on Viewtron IP cameras."
keywords: [ip camera line crossing api, viewtron api, tripwire detection config]
sidebar_label: "Line Crossing"
sidebar_position: 2
---

# Line Crossing & Tripwire Configuration

:::tip Application Guide
For a complete walkthrough with code examples, see the [Perimeter Security & Line Crossing](/docs/applications/perimeter-security-line-crossing-api) application guide.
:::

## GetSmartTripwireConfig

Retrieves line crossing/tripwire detection configuration. Returns the tripwire lines, crossing direction, object filters, and alarm settings.

| Field | Value |
|-------|-------|
| **Endpoint** | `/GetSmartTripwireConfig[/channelId]` |
| **Method** | `POST` or `GET` |
| **Products** | IPC |
| **Channel ID** | Optional (default `1`) |

### Response Example

```xml
<?xml version="1.0" encoding="utf-8"?>
<config xmlns="http://www.ipc.com/ver10" version="2.0.0">
  <types>
    <tripwireDirection>
      <enum>none</enum>
      <enum>rightortop</enum>
      <enum>leftorbotton</enum>
    </tripwireDirection>
  </types>
  <tripwire>
    <switch type="boolean">false</switch>
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
    </objectFilter>
    <lineInfo type="list" maxCount="4" count="1">
      <item>
        <direction type="tripwireDirection">rightortop</direction>
        <startPoint>
          <X type="uint32">10</X>
          <Y type="uint32">10</Y>
        </startPoint>
        <endPoint>
          <X type="uint32">1000</X>
          <Y type="uint32">1000</Y>
        </endPoint>
      </item>
    </lineInfo>
  </tripwire>
</config>
```

### Parameters

| Parameter | Type | Range | Description |
|-----------|------|-------|-------------|
| `switch` | boolean | `true` / `false` | Enable or disable tripwire detection |
| `alarmHoldTime` | uint32 | — | Duration (seconds) to hold the alarm state after detection |
| `objectFilter.car.switch` | boolean | `true` / `false` | Enable car/vehicle detection |
| `objectFilter.car.sensitivity` | uint32 | 1–100 (default 50) | Car detection sensitivity |
| `objectFilter.person.switch` | boolean | `true` / `false` | Enable person detection |
| `objectFilter.person.sensitivity` | uint32 | 1–100 (default 50) | Person detection sensitivity |
| `lineInfo` | list | maxCount: 4 | Tripwire lines (up to 4 lines) |
| `lineInfo.item.direction` | tripwireDirection | `none`, `rightortop`, `leftorbotton` | Crossing direction that triggers the alarm |
| `lineInfo.item.startPoint.X` | uint32 | — | X coordinate of the tripwire start point |
| `lineInfo.item.startPoint.Y` | uint32 | — | Y coordinate of the tripwire start point |
| `lineInfo.item.endPoint.X` | uint32 | — | X coordinate of the tripwire end point |
| `lineInfo.item.endPoint.Y` | uint32 | — | Y coordinate of the tripwire end point |

### Direction Values

| Value | Description |
|-------|-------------|
| `none` | Trigger on crossing in either direction |
| `rightortop` | Trigger only when crossing from left-to-right or bottom-to-top |
| `leftorbotton` | Trigger only when crossing from right-to-left or top-to-bottom |

### Notes

- Up to 4 independent tripwire lines can be configured.
- Each line is defined by a start point and end point, with a crossing direction filter.
- The `tripwireDirection` enum values are defined in the `<types>` block of the response.
- The spelling `leftorbotton` (not "bottom") matches the firmware's XML — use this exact value when setting configuration.
- The corresponding Set command is `SetSmartTripwireConfig` using the same XML structure.

## Related Endpoints

| Endpoint | Purpose |
|----------|---------|
| [GetSmartPerimeterConfig](/docs/api-reference/smart-detection/intrusion-perimeter-detection-config) | Intrusion zone detection (polygon regions) |
| [GetSmartAoiEntryConfig](/docs/api-reference/smart-detection/region-entry-exit-config) | Region entry detection |
| [SetHttpPostConfig](/docs/api-reference/alarm/http-post-webhook-config) | Configure webhook destination |
