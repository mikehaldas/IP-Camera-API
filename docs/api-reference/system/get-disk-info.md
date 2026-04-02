---
title: "GetDiskInfo — Storage Status"
description: "API reference for GetDiskInfo — check disk capacity, free space, and storage status on Viewtron IP cameras and NVRs."
keywords: [ip camera disk info api, viewtron api, nvr storage status]
sidebar_label: "Disk Info"
sidebar_position: 3
---

# GetDiskInfo

Retrieves disk/storage information including capacity, free space, and status.

## Endpoint

| Field | Value |
|-------|-------|
| **Method** | `POST` or `GET` |
| **URL** | `http://<host>[:port]/GetDiskInfo` |
| **Products** | IPC, NVR |
| **Channel ID** | N/A |

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Disk identifier |
| `totalSpace` | uint32 | Total disk capacity in MB |
| `freeSpace` | uint32 | Available space in MB |
| `imageFreeSpace` | uint32 | Free space for image storage in MB (IPC only) |
| `status` | diskStatus | Current disk status |
| `storageType` | diskType | Storage type: SD or HDD (v2.0 only) |

### Disk Status Values

| Status | Description |
|--------|-------------|
| `read` | Read-only mode |
| `read/write` | Normal read/write operation |
| `unformat` | Disk is unformatted |
| `formatting` | Disk is currently being formatted |
| `exception` | Disk error |
| `locked` | Disk is locked (v2.0 only) |

## Response (v2.0 IPC)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="2.0.0" xmlns="http://www.ipc.com/ver10">
  <types>
    <diskStatus>
      <enum>read</enum>
      <enum>read/write</enum>
      <enum>unformat</enum>
      <enum>formatting</enum>
      <enum>exception</enum>
      <enum>locked</enum>
    </diskStatus>
  </types>
  <diskInfo type="list" count="1">
    <item>
      <id type="string"><![CDATA[disk1]]></id>
      <totalSpace type="uint32">30371</totalSpace>
      <freeSpace type="uint32">0</freeSpace>
      <imageFreeSpace type="uint32">2985</imageFreeSpace>
      <status type="diskStatus">read/write</status>
      <storageType type="diskType">SD</storageType>
    </item>
  </diskInfo>
</config>
```

## Response (v1.9)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="1.0" xmlns="http://www.ipc.com/ver10">
  <types>
    <diskStatus>
      <enum>read</enum>
      <enum>read/write</enum>
      <enum>unformat</enum>
      <enum>formatting</enum>
      <enum>exception</enum>
    </diskStatus>
  </types>
  <diskInfo type="list" count="1">
    <item>
      <id type="string"><![CDATA[{5B457B2A-D467-834E-B1E8-22F3450DA873}]]></id>
      <totalSpace type="uint32">953869</totalSpace>
      <freeSpace type="uint32">847872</freeSpace>
      <imageFreeSpace type="uint32">847872</imageFreeSpace>
      <diskStatus type="diskStatus">read/write</diskStatus>
    </item>
  </diskInfo>
</config>
```

## Notes

- `totalSpace` and `freeSpace` are in megabytes (MB).
- If no disk is present, the `diskInfo` node will be empty.
- `imageFreeSpace` is IPC only.

:::info v2.0 Changes
v2.0 adds `storageType` (SD/HDD) and `locked` disk status.
:::
