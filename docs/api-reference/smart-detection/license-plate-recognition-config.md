---
title: "License Plate Recognition (LPR) Configuration"
description: "API reference for LPR configuration — set up license plate detection and manage plate databases on Viewtron IP cameras."
keywords: [ip camera lpr api, viewtron api, license plate recognition config]
sidebar_label: "LPR Config"
sidebar_position: 4
---

# License Plate Recognition (LPR) Configuration

:::tip Application Guide
For a complete walkthrough with code examples, see the [License Plate Recognition](/docs/applications/license-plate-recognition-camera-api) application guide.
:::

This section covers three endpoints for LPR configuration and plate database management:

- **GetSmartVehicleConfig** — read LPR detection settings
- **AddVehiclePlate** — add plates to the whitelist/blacklist database
- **GetVehiclePlate** — search the plate database

---

## GetSmartVehicleConfig

Retrieves license plate recognition configuration, including detection sensitivity, supported region, deduplication settings, and detection zone.

| Field | Value |
|-------|-------|
| **Endpoint** | `/GetSmartVehicleConfig[/channelId]` |
| **Method** | `POST` or `GET` |
| **Products** | IPC |
| **Channel ID** | Optional (default `1`) |

### Response Example (v2.0)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="2.0.0" xmlns="http://www.ipc.com/ver10">
  <types>
    <plateAreaType>
      <enum continent="NorthAmerica">U.S.A</enum>
      <enum continent="NorthAmerica">Canada</enum>
      <enum continent="Europe">Germany</enum>
      <enum continent="Europe">Britain</enum>
      <!-- Additional regions... -->
    </plateAreaType>
    <alarmListType>
      <enum>blackList</enum>
      <enum>whiteList</enum>
      <enum>strangerList</enum>
    </alarmListType>
  </types>
  <vehicle>
    <switch type="boolean">false</switch>
    <plateSencitivity type="uint8">49</plateSencitivity>
    <plateSupportArea type="plateAreaType">U.S.A</plateSupportArea>
    <saveTargetPicture type="boolean">false</saveTargetPicture>
    <saveSourcePicture type="boolean">false</saveSourcePicture>
    <dedupMode>
      <switch type="boolean">false</switch>
      <intervalTime type="uint32" default="5">5</intervalTime>
    </dedupMode>
    <regionInfo type="list" maxCount="1" count="1">
      <item>
        <X1 type="uint32">375</X1>
        <Y1 type="uint32">2866</Y1>
        <X2 type="uint32">9625</X2>
        <Y2 type="uint32">8800</Y2>
      </item>
    </regionInfo>
    <plateMatch>
      <alarmMode type="alarmModeType">plateOnly</alarmMode>
    </plateMatch>
  </vehicle>
</config>
```

### Parameters

| Parameter | Type | Range | Description |
|-----------|------|-------|-------------|
| `switch` | boolean | `true` / `false` | Enable or disable LPR detection |
| `plateSencitivity` | uint8 | 0–100 | Plate detection sensitivity (note firmware spelling) |
| `plateSupportArea` | plateAreaType | See enum list | Region/country for plate format recognition |
| `saveTargetPicture` | boolean | `true` / `false` | Save cropped plate image on detection |
| `saveSourcePicture` | boolean | `true` / `false` | Save full-frame source image on detection |
| `dedupMode.switch` | boolean | `true` / `false` | Enable plate deduplication |
| `dedupMode.intervalTime` | uint32 | default: 5 | Minimum seconds between duplicate plate reports |
| `regionInfo` | list | maxCount: 1 | Detection zone (rectangular region) |
| `regionInfo.item.X1` | uint32 | — | Left X coordinate of detection zone |
| `regionInfo.item.Y1` | uint32 | — | Top Y coordinate of detection zone |
| `regionInfo.item.X2` | uint32 | — | Right X coordinate of detection zone |
| `regionInfo.item.Y2` | uint32 | — | Bottom Y coordinate of detection zone |
| `plateMatch.alarmMode` | alarmModeType | — | Plate matching alarm mode (e.g., `plateOnly`) |

### Supported Plate Regions

The `plateAreaType` enum includes regions grouped by continent:

| Continent | Regions |
|-----------|---------|
| North America | U.S.A, Canada |
| Europe | Germany, Britain, and others |

Query your camera's `GetSmartVehicleConfig` response for the complete list of supported regions on your firmware version.

### Notes

:::info v2.0 Additions
API v2.0 adds `dedupMode` (deduplication with configurable interval) and `plateMatch/alarmMode` to the vehicle configuration. These fields are not present in v1.x responses.
:::

- The spelling `plateSencitivity` (not "sensitivity") matches the firmware's XML — use this exact spelling when setting configuration.
- The detection zone uses a single rectangular region (maxCount: 1), unlike intrusion detection which supports polygon regions.
- The corresponding Set command is `SetSmartVehicleConfig` using the same XML structure.

---

## AddVehiclePlate

Adds one or more license plates to the camera's plate database (whitelist, blacklist, or stranger list).

| Field | Value |
|-------|-------|
| **Endpoint** | `/AddVehiclePlate` |
| **Method** | `POST` |
| **Products** | IPC |

### Request Example

```xml
<?xml version="1.0" encoding="utf-8"?>
<config>
  <vehiclePlates type="list" count="1">
    <item>
      <carPlateNumber type="string"><![CDATA[ABC1234]]></carPlateNumber>
      <beginTime type="string"><![CDATA[2024/01/01 00:00:00]]></beginTime>
      <endTime type="string"><![CDATA[2024/12/31 23:59:59]]></endTime>
      <carOwner type="string"><![CDATA[John Doe]]></carOwner>
      <plateItemType type="string">whiteList</plateItemType>
    </item>
  </vehiclePlates>
</config>
```

### Request Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `carPlateNumber` | string (CDATA) | License plate number |
| `beginTime` | string (CDATA) | Start date/time for plate validity (`YYYY/MM/DD HH:MM:SS`) |
| `endTime` | string (CDATA) | End date/time for plate validity (`YYYY/MM/DD HH:MM:SS`) |
| `carOwner` | string (CDATA) | Name of the vehicle owner |
| `plateItemType` | string | List type: `whiteList`, `blackList`, or `strangerList` |

### Notes

- Multiple plates can be added in a single request by increasing the `count` attribute and adding more `<item>` elements.
- The `beginTime` and `endTime` fields define the validity window — the plate is only active during this period.
- Use `whiteList` for authorized vehicles (e.g., gate access) and `blackList` for vehicles that should trigger alerts.

---

## GetVehiclePlate

Retrieves license plates from the camera's plate database with pagination and filtering.

| Field | Value |
|-------|-------|
| **Endpoint** | `/GetVehiclePlate` |
| **Method** | `POST` or `GET` |
| **Products** | IPC |

:::info v2.0 Only
This endpoint is available only on API v2.0 firmware.
:::

### Request Example

```xml
<config xmlns="http://www.ipc.com/ver10" version="2.0.0">
  <vehiclePlates type="list" maxCount="10000" count="1">
    <searchFilter>
      <item>
        <pageIndex type="uint32">0</pageIndex>
        <pageSize type="uint32">10</pageSize>
        <listType type="vehicleListTypes">allList</listType>
        <carPlateNum type="string"></carPlateNum>
      </item>
    </searchFilter>
  </vehiclePlates>
</config>
```

### Request Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `pageIndex` | uint32 | Page number (0-based) for pagination |
| `pageSize` | uint32 | Number of results per page |
| `listType` | vehicleListTypes | Filter by list type: `allList`, `whiteList`, `blackList`, or `strangerList` |
| `carPlateNum` | string | Filter by plate number (empty string returns all) |

### Notes

- The database supports up to 10,000 plates (`maxCount="10000"`).
- Use `pageIndex` and `pageSize` to paginate through large plate databases.
- Set `carPlateNum` to a specific plate number to search for a single plate, or leave empty to return all plates matching the `listType` filter.

## Related Endpoints

| Endpoint | Purpose |
|----------|---------|
| [SetHttpPostConfig](/docs/api-reference/alarm/http-post-webhook-config) | Configure webhook destination for LPR alerts |
| [GetAlarmStatus](/docs/api-reference/alarm/alarm-status) | Poll current alarm state |
