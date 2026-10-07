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

This section covers LPR configuration and plate database management.

**API 1.x–2.0** uses `GetSmartVehicleConfig`, `AddVehiclePlate`, and `GetVehiclePlate`. On v2.1 cameras those commands, and `GetVehicleConfig`, return HTTP 400 with `errorCode="1"` (Invalid Request).

**API 2.1** uses the commands below. Verified on a camera running 5.3.1 firmware:

- **GetSmartLicensePlateConfig / SetSmartLicensePlateConfig** — LPR detection settings
- **GetLicensePlateGroups** — plate group IDs and names
- **AddLicensePlates** — add plates to the database
- **GetLicensePlates** — query the plate database
- **ModifyLicensePlate** — update plate details
- **DeleteLicensePlate** — remove a plate from the database
- **SearchSnapLicensePlates / DownloadSnapLicensePlate** — plate snapshot search (request format to be documented)

---

## GetSmartVehicleConfig

> **Applies to API 1.x–2.0 firmware.** On v2.1 cameras `GetSmartVehicleConfig`, `AddVehiclePlate`, `GetVehiclePlate`, and `GetVehicleConfig` return HTTP 400 with `errorCode="1"` (Invalid Request). Use `GetSmartLicensePlateConfig` and the group-based plate commands below.

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

## GetSmartLicensePlateConfig / SetSmartLicensePlateConfig

v2.1 LPR detection settings. `GetSmartLicensePlateConfig` reads the detection `switch`, `direction` (for example `noLimit`), boundary area, and mask areas. The matching Set command is `SetSmartLicensePlateConfig`.

| Field | Value |
|-------|-------|
| **Endpoint (Get)** | `/GetSmartLicensePlateConfig` |
| **Endpoint (Set)** | `/SetSmartLicensePlateConfig` |
| **Method (Get)** | `POST` or `GET` |
| **Method (Set)** | `POST` |
| **Products** | IPC |

---

## Plate Database Management

Manage the on-camera license plate database — add, query, update, and delete plates. All endpoints use Basic Authentication. On v2.1, read group IDs from `GetLicensePlateGroups` before calling the plate commands. Do not hard-code them.

### GetLicensePlateGroups

Returns the plate groups on the camera and the numeric id for each name.

| Field | Value |
|-------|-------|
| **Endpoint** | `/GetLicensePlateGroups` |
| **Method** | `POST` or `GET` |
| **Auth** | Basic |
| **Products** | IPC |

On a camera running 5.3.1 firmware, `GetLicensePlateGroups` returned:

| groupId | name |
|---------|------|
| 1 | temporaryList |
| 2 | whiteList |
| 3 | blackList |

Read group IDs from `GetLicensePlateGroups`. Do not hard-code them. The `whiteList` group is not group 1.

`strangerList` appears as a plate-match alarm option. It is not a database group.

### Plate Status in HTTP POST Events

When a plate is detected, the camera includes a `vehicleListType` field in the HTTP POST event indicating the plate's current database status. The camera validates date ranges internally for **all** list types.

| Camera Setting | `vehicleListType` Value | Description |
|---|---|---|
| Allow list (valid dates) | `whiteList` | Plate is authorized |
| Block list (valid dates) | `blackList` | Plate is blocked |
| Temporary vehicle (valid dates) | `temporaryList` | Plate is temporarily authorized |
| Any list type (expired dates) | *(field absent)* | Treated the same as unknown |
| Not in database | *(field absent)* | Plate not recognized |

:::caution Date Ranges Apply to All List Types
Date range validation is not limited to temporary plates — it applies to **all** list types including allow list and block list. Any plate with an expired end date will have `vehicleListType` omitted from the HTTP POST event, making it indistinguishable from an unknown plate. Use "Valid Forever" in the camera firmware or set a far-future end date to prevent plates from silently expiring.
:::

:::note
The camera does not include start/end dates in the HTTP POST event. Date range validation happens entirely on-camera.
:::

:::tip Python SDK
The [viewtron Python SDK](https://pypi.org/project/viewtron/) (`pip install viewtron`) handles all XML formatting automatically. See the [License Plate Recognition](/docs/applications/license-plate-recognition-camera-api) application guide for code examples.
:::

---

### AddLicensePlates

Add one or more plates to the camera's database.

| Field | Value |
|-------|-------|
| **Endpoint** | `/AddLicensePlates` |
| **Method** | `POST` |
| **Auth** | Basic |
| **Products** | IPC |

#### Request

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="2.1.0" xmlns="http://www.ipc.com/ver10">
    <licensePlates type="list" maxCount="100" count="1">
        <item>
            <index>1</index>
            <licensePlateNumber><![CDATA[ABC1234]]></licensePlateNumber>
            <groupId><![CDATA[2]]></groupId>
        </item>
    </licensePlates>
</config>
```

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `index` | integer | Item index (1-based) |
| `licensePlateNumber` | string (CDATA) | License plate number |
| `groupId` | string (CDATA) | Group ID from `GetLicensePlateGroups` (for example `2` = whiteList). Do not hard-code group IDs. |

#### Response (Success)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="2.1.0" xmlns="http://www.ipc.com/ver10">
    <licensePlatesReply>
        <item>
            <index type="uint32">1</index>
            <errorCode type="uint32">0</errorCode>
        </item>
    </licensePlatesReply>
</config>
```

#### Notes

- Multiple plates can be added in a single request — increase the `count` attribute and add additional `<item>` elements with incrementing `index` values.
- The camera automatically assigns begin/end validity times. To control these, use `ModifyLicensePlate` after adding.

#### curl Example

```bash
curl -u admin:password -X POST http://CAMERA_IP/AddLicensePlates \
  -H "Content-Type: application/xml" \
  -d '<?xml version="1.0" encoding="UTF-8"?>
<config version="2.1.0" xmlns="http://www.ipc.com/ver10">
    <licensePlates type="list" maxCount="100" count="1">
        <item>
            <index>1</index>
            <licensePlateNumber><![CDATA[ABC1234]]></licensePlateNumber>
            <groupId><![CDATA[2]]></groupId>
        </item>
    </licensePlates>
</config>'
```

---

### GetLicensePlates

Query the plate database with pagination.

| Field | Value |
|-------|-------|
| **Endpoint** | `/GetLicensePlates` |
| **Method** | `POST` |
| **Auth** | Basic |
| **Products** | IPC |

#### Request

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="2.1.0" xmlns="http://www.ipc.com/ver10">
    <searchFilter>
        <maxResult>10</maxResult>
        <resultOffset>1</resultOffset>
        <groupId><![CDATA[2]]></groupId>
    </searchFilter>
</config>
```

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `maxResult` | integer | Maximum number of results to return |
| `resultOffset` | integer | Starting position (1-based — first plate is offset `1`) |
| `groupId` | string (CDATA) | Group ID from `GetLicensePlateGroups` (for example `2` = whiteList). Do not hard-code group IDs. |

#### Response

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="2.1.0" xmlns="http://www.ipc.com/ver10">
    <licensePlates type="list" total="2" count="2">
        <item>
            <licensePlateNumber type="string"><![CDATA[ABC1234]]></licensePlateNumber>
            <groupId type="string"><![CDATA[2]]></groupId>
            <beginTime type="string"><![CDATA[2026-04-07 09:28:45]]></beginTime>
            <endTime type="string"><![CDATA[2037-12-30 10:59:59]]></endTime>
            <licensePlateType type="string"><![CDATA[]]></licensePlateType>
            <carOwner type="string"><![CDATA[Mike]]></carOwner>
            <cardNumber type="string"><![CDATA[]]></cardNumber>
            <telephone type="string"><![CDATA[]]></telephone>
        </item>
    </licensePlates>
</config>
```

#### Response Fields

| Field | Description |
|-------|-------------|
| `licensePlateNumber` | Plate number |
| `groupId` | Group this plate belongs to |
| `beginTime` | Start of validity period |
| `endTime` | End of validity period |
| `carOwner` | Vehicle owner name |
| `telephone` | Owner phone number |
| `cardNumber` | Associated card number |
| `licensePlateType` | Plate type |

#### Notes

- `resultOffset` is 1-based. Offset `0` returns errorCode 16 (Range Error).
- An empty result returns errorCode 20 (Resources Not Exist).

---

### ModifyLicensePlate

Update an existing plate's details (owner, phone, validity dates).

| Field | Value |
|-------|-------|
| **Endpoint** | `/ModifyLicensePlate` |
| **Method** | `POST` |
| **Auth** | Basic |
| **Products** | IPC |

#### Request

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="2.1.0" xmlns="http://www.ipc.com/ver10">
    <licensePlate>
        <licensePlateNumber><![CDATA[ABC1234]]></licensePlateNumber>
        <groupId><![CDATA[2]]></groupId>
        <carOwner type="string"><![CDATA[John Doe]]></carOwner>
        <telephone type="string"><![CDATA[555-123-4567]]></telephone>
    </licensePlate>
</config>
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `licensePlateNumber` | string (CDATA) | Yes | Plate number to modify (must already exist) |
| `groupId` | string (CDATA) | Yes | Group ID from `GetLicensePlateGroups` (for example `2` = whiteList). Do not hard-code group IDs. |
| `carOwner` | string (CDATA) | No | Updated owner name |
| `telephone` | string (CDATA) | No | Updated phone number |

#### Response (Success)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="2.1.0" xmlns="http://www.ipc.com/ver10" status="success" errorCode="0" errorDesc="No Error"/>
```

#### Notes

- Fields being modified must include the `type="string"` attribute or the camera returns a Range Error.
- The plate is identified by `licensePlateNumber` + `groupId` — both are required.

---

### DeleteLicensePlate

Delete a plate from the database.

| Field | Value |
|-------|-------|
| **Endpoint** | `/DeleteLicensePlate` |
| **Method** | `POST` |
| **Auth** | Basic |
| **Products** | IPC |

#### Request

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="2.1.0" xmlns="http://www.ipc.com/ver10">
    <deleteAction>
        <licensePlateNumber><![CDATA[ABC1234]]></licensePlateNumber>
        <groupId><![CDATA[2]]></groupId>
    </deleteAction>
</config>
```

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `licensePlateNumber` | string (CDATA) | Plate number to delete |
| `groupId` | string (CDATA) | Group ID from `GetLicensePlateGroups` (for example `2` = whiteList). Do not hard-code group IDs. |

#### Response (Success)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="2.1.0" xmlns="http://www.ipc.com/ver10" status="success" errorCode="0" errorDesc="No Error"/>
```

---

## SearchSnapLicensePlates / DownloadSnapLicensePlate

`SearchSnapLicensePlates` and `DownloadSnapLicensePlate` are available on v2.1. Request format to be documented.

---

## Related Endpoints

| Endpoint | Purpose |
|----------|---------|
| [SetHttpPostConfig](/docs/api-reference/alarm/http-post-webhook-config) | Configure webhook destination for LPR alerts |
| [GetAlarmStatus](/docs/api-reference/alarm/alarm-status) | Poll current alarm state |
