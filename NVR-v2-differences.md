# NVR v2.0 HTTP Post Differences

**Purpose:** Track differences between IP Camera (direct) and NVR HTTP Post alarm data to guide server updates and provide documentation feedback to the manufacturer.

**Test Date:** February 25, 2026
**NVR IP:** 192.168.0.55 (MAC: 58:5B:69:40:F4:0D)
**NVR Firmware:** Unknown (v2.0.0 protocol)
**Server IP:** 192.168.0.56:5002
**Camera Source (v1.0 reference):** 192.168.1.57 (IPC, tested Nov 2025), 192.168.1.192 (IPC, tested Nov 2025)
**Raw Posts Captured:** 49+ NVR posts (alarmData, alarmStatus, keepalive)

---

## 1. What the API Docs Cover vs What We Actually See

The manufacturer provides two API docs:
- **v1.9** (IPC 5.2 or earlier, NVR 1.4.12 or earlier)
- **v2.0** (IPC 5.3 or later, NVR 1.4.13 or later)

Both docs cover how to **query** the device (GetAlarmStatus, GetSmartPerimeterConfig, etc.) and describe a basic `SendAlarmStatus` command format. **Neither doc describes the actual format of HTTP Posts sent by the NVR alarm server feature.** The alarm server docs only show a simple alarmStatusInfo example with no image data and no event detail.

The NVR sends three message types: `keepalive`, `alarmStatus`, and `alarmData`. The XML structure, smartType naming, timestamp format, and image payload format are all different from what IP cameras send directly.

There is also a **Long Polling doc** (`API-LongPolling_20190719.docx`) from 2019 that documents the IPC `SendAlarmData` and `SendAlarmStatus` formats for the subscription/push model. This doc has the most detailed alarm data XML examples - with `smartType` codes, image structures, and the full alarm type mapping. However, it only covers IPC (v1.0/1.7) formats. The NVR v2.0 format is not documented anywhere.

### Three API Docs Available

| Document | Version | Date | Covers NVR Alarm Posts? |
|----------|---------|------|------------------------|
| API v1.9 Guide | 1.0 | Pre-2019 | No - only GetAlarmServerConfig (IPC only) |
| API v2.0 Guide | 2.0.0 | 2026 | No - same limited alarm server section |
| Long Polling Doc | 1.0/1.7 | July 2019 | **Partially** - documents IPC SendAlarmData/SendAlarmStatus in detail, but NVR uses different format |

---

## 2. Summary of Differences

| Feature | IPC Direct (v1.0/1.7) | NVR (v2.0.0) |
|---------|------------------------|--------------|
| **Config version** | `1.0` or `1.7` | `2.0.0` |
| **Content-Type** | `application/xml; charset=utf-8` | `application/soap+xml; charset=utf-8` |
| **Connection** | `keep-alive` | `close` |
| **Accept-Encoding** | `gzip, deflate` (present) | Not sent |
| **messageType field** | Not present | `keepalive`, `alarmStatus`, `alarmData` |
| **deviceInfo block** | Varies (sometimes DeviceInfo root, sometimes nested) | Always present with `deviceName`, `ip`, `mac`, `channelId` |
| **CDATA wrapping** | Selective | Extensive (deviceName, ip, mac) |
| **smartType values** | Codes: `PEA`, `VFD`, `VEHICE`/`VEHICLE`, `VSD`, `AOIENTRY`, `AOILEAVE` | Spelled out: `regionIntrusion` (others TBD) |
| **Timestamp field** | `currentTime` - Unix seconds/ms (10-13 digits) | `currentTime` - Unix **microseconds** (16 digits) |
| **Event data location** | `listInfo/item` | `eventInfo/item` with `eventId`, `targetId`, `boundary`, `pointGroup`, `rect` |
| **Image data location** | JPEG embedded as raw base64 after XML declaration, OR in `sourceDataInfo`/`targetImageData` | Clean XML with images in `sourceDataInfo/sourceBase64Data` |
| **Keepalive format** | `DeviceInfo` root element with `DeviceName`, `DeviceNo.`, `SN`, `ipAddress`, `macAddress` | `config` root with `messageType: keepalive` and `deviceInfo` block |
| **Alarm status format** | `alarmStatusInfo` with `vehiceAlarm type="boolean"` | `alarmStatusInfo` with `perimeterAlarm/item` |
| **Post URL** | Sends to configured endpoint (e.g., `/API`) | Sends full URL: `POST http://192.168.0.56:5002/API` |

---

## 3. Message Types (NVR v2.0)

The NVR sends three distinct message types, identified by the `<messageType>` field. IP cameras do NOT use this field.

### 3.1 Keepalive

Heartbeat sent periodically. No alarm data.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="2.0.0" xmlns="http://www.ipc.com/ver10">
    <messageType>keepalive</messageType>
    <deviceInfo>
        <deviceName><![CDATA[Device Name]]></deviceName>
        <ip><![CDATA[192.168.0.55]]></ip>
        <mac><![CDATA[58:5B:69:40:F4:0D]]></mac>
    </deviceInfo>
</config>
```

**IPC equivalent (v1.0/1.7):**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<DeviceInfo>
    <DeviceName>Device Name</DeviceName>
    <DeviceNo.>1</DeviceNo.>
    <SN><![CDATA[NF40D099BCM0]]></SN>
    <ipAddress>192.168.1.192</ipAddress>
    <macAddress>58:5B:69:40:F4:0D</macAddress>
</DeviceInfo>
```

**Differences:**
- NVR uses `<config>` root; IPC uses `<DeviceInfo>` root
- NVR has `messageType` field; IPC does not
- NVR uses `ip`/`mac`; IPC uses `ipAddress`/`macAddress`
- NVR wraps values in CDATA; IPC mostly does not
- NVR does not include `SN` or `DeviceNo.`
- NVR keepalive has no `channelId`; IPC keepalive has `DeviceNo.`

### 3.2 Alarm Status

Sent when an alarm triggers or clears. Lightweight notification (no images).

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="2.0.0" xmlns="http://www.ipc.com/ver10">
    <messageType>alarmStatus</messageType>
    <deviceInfo>
        <deviceName><![CDATA[Device Name]]></deviceName>
        <ip><![CDATA[192.168.0.55]]></ip>
        <mac><![CDATA[58:5B:69:40:F4:0D]]></mac>
        <channelId>1</channelId>
    </deviceInfo>
    <currentTime>1772056914000000</currentTime>
    <alarmStatusInfo>
        <perimeterAlarm><item id="1">true</item>
        </perimeterAlarm>
    </alarmStatusInfo>
</config>
```

**IPC equivalent (v1.7):**
```xml
<?xml version="1.0" encoding="UTF-8" ?>
<config version="1.7" xmlns="http://www.ipc.com/ver10">
    <alarmStatusInfo>
        <vehiceAlarm type="boolean" id="1">true</vehiceAlarm>
    </alarmStatusInfo>
    <dataTime><![CDATA[11-19-2025 12:15:11 PM]]></dataTime>
    <deviceInfo>
        <deviceName><![CDATA[Viewtron IPC]]></deviceName>
        <deviceNo.><![CDATA[1]]></deviceNo.>
        <sn><![CDATA[I84BB0A8D59C]]></sn>
        <ipAddress><![CDATA[192.168.1.57]]></ipAddress>
        <macAddress><![CDATA[58:5b:69:5a:84:bb]]></macAddress>
    </deviceInfo>
</config>
```

**Differences:**
- NVR has `messageType: alarmStatus`; IPC does not have messageType
- NVR uses `currentTime` (Unix microseconds); IPC uses `dataTime` (formatted date string `MM-DD-YYYY HH:MM:SS AM/PM`)
- NVR alarm: `<perimeterAlarm><item id="1">true</item></perimeterAlarm>`; IPC alarm: `<vehiceAlarm type="boolean" id="1">true</vehiceAlarm>`
- NVR `channelId` is inside `deviceInfo`; IPC has no channelId in alarmStatus
- NVR `deviceInfo` uses `ip`/`mac`; IPC uses `ipAddress`/`macAddress` with different case (`sn` vs not present)
- NVR alarm status always arrives as a separate message BEFORE the `alarmData`

### 3.3 Alarm Data (with images)

The main event post with full details and images. This is the one that matters most.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="2.0.0" xmlns="http://www.ipc.com/ver10">
    <messageType>alarmData</messageType>
    <deviceInfo>
        <deviceName><![CDATA[Device Name]]></deviceName>
        <ip><![CDATA[192.168.0.55]]></ip>
        <mac><![CDATA[58:5B:69:40:F4:0D]]></mac>
        <channelId>1</channelId>
    </deviceInfo>
    <smartType>regionIntrusion</smartType>
    <currentTime>1772056914604000</currentTime>
    <eventInfo>
        <item>
            <eventId>916</eventId>
            <targetId>716</targetId>
            <boundary>area</boundary>
            <pointGroup>
                <item><x>1590</x><y>3080</y></item>
                <item><x>4715</x><y>3181</y></item>
                <item><x>4772</x><y>9217</y></item>
                <item><x>416</x><y>9141</y></item>
            </pointGroup>
            <rect>
                <x1>3096</x1><y1>3715</y1>
                <x2>4005</x2><y2>9861</y2>
            </rect>
        </item>
    </eventInfo>
    <sourceDataInfo>
        <dataType>0</dataType>
        <width>1280</width>
        <height>720</height>
        <sourceBase64Length>400924</sourceBase64Length>
        <sourceBase64Data>... (base64 JPEG) ...</sourceBase64Data>
    </sourceDataInfo>
</config>
```

**IPC equivalent:** IPC sends image data differently - the base64 JPEG is often embedded as raw data after the `<?xml` declaration, with structured XML containing `smartType`, `listInfo`, `sourceDataInfo`, and `targetImageData` blocks.

**Differences:**
- NVR wraps everything in clean XML; IPC sometimes sends raw base64 data mixed with XML
- NVR uses `eventInfo` with `eventId`, `targetId`, `boundary`, `pointGroup`, `rect`; IPC uses `listInfo/item` with `targetImageData`
- NVR `smartType` is spelled out (`regionIntrusion`); IPC uses codes (`PEA`)
- NVR includes `width`, `height`, `dataType` metadata for the image; IPC does not always include these
- NVR uses `targetListInfo` for target crops; IPC uses `listInfo`
- NVR `targetType` is a string (`person`); IPC uses numeric (`1`=person, `2`=car, `4`=bike)
- NVR `rect` gives bounding box for detected object; IPC puts this in `targetImageData` structure
- NVR `pointGroup` defines the intrusion zone polygon; IPC does not include this in alarm data posts

### 3.4 Image Configuration Options (NVR v2.0)

The NVR alarm server settings allow configuring which images are sent: **both**, **original only**, **target only**, or **none**. This changes which XML sections are included in `alarmData` posts. The `eventInfo` and `targetListInfo` are always present regardless of image setting.

#### Both Images (~524 KB)
Full scene overview + cropped target image.
```xml
<sourceDataInfo>
    <dataType>0</dataType>
    <width>1280</width>
    <height>720</height>
    <sourceBase64Length>443820</sourceBase64Length>
    <sourceBase64Data><![CDATA[...]]></sourceBase64Data>
</sourceDataInfo>
<targetListInfo>
    <item>
        <targetId>1168</targetId>
        <targetType>person</targetType>
        <targetImageData>
            <dataType>0</dataType>
            <width>336</width>
            <height>448</height>
            <targetBase64Length>78796</targetBase64Length>
            <targetBase64Data><![CDATA[...]]></targetBase64Data>
        </targetImageData>
    </item>
</targetListInfo>
```

#### Original Image Only (~418 KB)
Full scene overview only. `targetListInfo` still present but without `targetImageData`.
```xml
<sourceDataInfo>
    <dataType>0</dataType>
    <width>1280</width>
    <height>720</height>
    <sourceBase64Length>416540</sourceBase64Length>
    <sourceBase64Data><![CDATA[...]]></sourceBase64Data>
</sourceDataInfo>
<targetListInfo>
    <item>
        <targetId>1260</targetId>
        <targetType>person</targetType>
    </item>
</targetListInfo>
```

#### Target Image Only (~92 KB)
Cropped target only. No `sourceDataInfo` section at all.
```xml
<targetListInfo>
    <item>
        <targetId>1275</targetId>
        <targetType>person</targetType>
        <targetImageData>
            <dataType>0</dataType>
            <width>336</width>
            <height>440</height>
            <targetBase64Length>90764</targetBase64Length>
            <targetBase64Data><![CDATA[...]]></targetBase64Data>
        </targetImageData>
    </item>
</targetListInfo>
```

#### No Images (~1 KB)
Event data only. No `sourceDataInfo`. `targetListInfo` present but minimal.
```xml
<targetListInfo>
    <item>
        <targetId>1254</targetId>
        <targetType>person</targetType>
    </item>
</targetListInfo>
```

**Summary table:**

| NVR Setting | `sourceDataInfo` | `targetImageData` | `targetListInfo` | Typical Post Size |
|---|---|---|---|---|
| Both images | Present (overview JPEG) | Present (crop JPEG) | Present with image | ~524 KB |
| Original only | Present (overview JPEG) | **Absent** | Present, no image | ~418 KB |
| Target only | **Absent** | Present (crop JPEG) | Present with image | ~92 KB |
| No images | **Absent** | **Absent** | Present, no image | ~1 KB |

**Key observation:** `targetListInfo` is ALWAYS present with at least `targetId` and `targetType`, even when images are disabled. This means target classification data (person/car/etc.) is always available regardless of image settings.

### 3.5 Line Crossing (lineCrossing) vs Region Intrusion (regionIntrusion)

Both are v2.0 `alarmData` posts with the same overall structure. The difference is in `eventInfo`:

**regionIntrusion eventInfo:**
```xml
<eventInfo>
    <item>
        <eventId>1368</eventId>
        <targetId>1168</targetId>
        <boundary>area</boundary>
        <pointGroup>
            <item><x>1590</x><y>3080</y></item>
            <item><x>4715</x><y>3181</y></item>
            <item><x>4772</x><y>9217</y></item>
            <item><x>416</x><y>9141</y></item>
        </pointGroup>
        <rect><x1>1789</x1><y1>3645</y1><x2>3096</x2><y2>9513</y2></rect>
    </item>
</eventInfo>
```

**lineCrossing eventInfo:**
```xml
<eventInfo>
    <item>
        <eventId>1409</eventId>
        <targetId>1309</targetId>
        <boundary>tripwire</boundary>
        <directionLine>
            <startPoint><x>3579</x><y>2550</y></startPoint>
            <endPoint><x>3655</x><y>9797</y></endPoint>
        </directionLine>
        <rect><x1>3494</x1><y1>4409</y1><x2>4261</x2><y2>9791</y2></rect>
    </item>
</eventInfo>
```

| Field | regionIntrusion | lineCrossing |
|-------|----------------|--------------|
| `boundary` | `area` | `tripwire` |
| Zone definition | `pointGroup` (polygon, 4+ points) | `directionLine` (`startPoint` + `endPoint`) |
| `rect` | Bounding box of detected target | Same |
| `sourceDataInfo` | Same | Same |
| `targetListInfo` | Same | Same |

**Direction data:** The NVR does NOT include crossing direction in the post. When line crossing is configured for both directions (A→B and B→A), both crossings produce identical XML — the `directionLine` startPoint/endPoint is just the tripwire line definition (same every time), and there is no direction field indicating which way the target crossed. Only the `rect` bounding box differs (target position at time of crossing).

**IPC equivalent:** Both map to IPC `PEA` smartType. IPC differentiates by having either a `<perimeter>` or `<tripwire>` block in the alarm data. NVR differentiates by using separate smartType values.

---

## 4. smartType Mapping

The NVR uses descriptive names instead of the codes used by IP cameras. The Long Polling doc confirms the IPC codes and their alarm data/status field names.

### 4.1 IPC Alarm Types (from Long Polling Doc)

The Long Polling doc lists all IPC smartType codes and how they map to AlarmData and AlarmStatus:

| IPC smartType | Description | AlarmData Field | AlarmStatus Field | Has Images? |
|---------------|-------------|----------------|-------------------|-------------|
| `MOTION` | Motion Detection | `motion` (grid data) | `motionAlarm` | YES |
| `SENSOR` | Sensor Alarm | NONE | `sensorAlarm` | NO |
| `PEA` (intrusion) | Perimeter Intrusion | `perimeter/perInfo` | `perimeterAlarm` | YES |
| `PEA` (line cross) | Line Crossing / Tripwire | `tripwire/tripInfo` | `tripwireAlarm` | YES |
| `AVD` (blur) | Video Blur | NONE | `clarityAbnormal` | NO |
| `AVD` (cast) | Video Cast | NONE | `colorAbnormal` | NO |
| `AVD` (scene) | Scene Change | NONE | `sceneChange` | NO |
| `OSC` | Object Removal (left/missing) | `smartType: OSC` | `oscAlarm` | YES |
| `CPC` | People Counting | `CPC` | `CPCAlarm` | YES |
| `CDD` | Crowd Density Detection | `CDD` | `CDDAlarm` | YES |
| `IPD` | People Intrusion | `IPD` | `IPDAlarm` | YES |
| `VFD` | Face Detection | `VFD` | `VFDAlarm` | YES |
| `VFD_MATCH` | Face Match/Recognition | `VFD_MATCH` | `VFDAlarm` | YES |
| `VEHICE` | License Plate Detection | `VEHICE` | `vehiceAlarm` | YES |
| `AOIENTRY` | Region Entry | `AOIENTRY` | (not documented) | YES |
| `AOILEAVE` | Region Exit | `AOILEAVE` | (not documented) | YES |
| `PASSLINECOUNT` | Line Crossing Count | `PASSLINECOUNT` | (not documented) | YES |
| `TRAFFIC` | Intrusion Target Count | `TRAFFIC` | (not documented) | YES |

**Note:** `PEA` is a single smartType that covers BOTH intrusion and line crossing. The AlarmData differentiates them by containing either a `<perimeter>` or `<tripwire>` block.

### 4.2 NVR v2.0 smartType Values (observed + predicted)

| IPC Code | IPC AlarmData Field | NVR v2.0 smartType | Observed? |
|----------|--------------------|--------------------|-----------|
| `PEA` (intrusion) | `perimeter` | `regionIntrusion` | **YES** |
| `PEA` (line cross) | `tripwire` | `lineCrossing` | **YES** |
| `VEHICE` | `VEHICE` | TBD | Not yet tested |
| `VFD` | `VFD` | TBD (maybe `faceDetection`?) | Not yet tested |
| `VFD_MATCH` | `VFD_MATCH` | TBD | Not yet tested |
| `MOTION` | `motion` | TBD | Not yet tested |
| `AOIENTRY` | `AOIENTRY` | TBD (maybe `regionEntry`?) | Not yet tested |
| `AOILEAVE` | `AOILEAVE` | TBD (maybe `regionExit`?) | Not yet tested |
| `VSD` | (video metadata) | TBD | Not yet tested |
| `CDD` | `CDD` | TBD | Not yet tested |
| `CPC` | `CPC` | TBD | Not yet tested |
| `PASSLINECOUNT` | `PASSLINECOUNT` | TBD | Not yet tested |

### 4.3 IPC PEA Perimeter vs NVR regionIntrusion (side by side)

This is the only alarm type we have from both sources. The structure is significantly different:

**IPC PEA Perimeter (from Long Polling Doc):**
```xml
<config version="1.7" xmlns="http://www.ipc.com/ver10">
    <smartType type="openAlramObj">PEA</smartType>
    <subscribeRelation type="subscribeOption">FEATURE_RESULT</subscribeRelation>
    <currentTime type="tint64">1563528106584193</currentTime>
    <perimeter>
        <perInfo type="list" count="1">
            <item>
                <eventId type="uint32">220</eventId>
                <targetId type="uint32">20</targetId>
                <status type="smartStatus">SMART_START</status>
                <boundary type="list" count="4">
                    <item><point><x type="uint32">1625</x><y type="uint32">2133</y></point></item>
                    <item><point><x type="uint32">1725</x><y type="uint32">8800</y></point></item>
                    ...
                </boundary>
                <rect>
                    <x1 type="uint32">113</x1><y1 type="uint32">0</y1>
                    <x2 type="uint32">5511</x2><y2 type="uint32">8472</y2>
                </rect>
            </item>
        </perInfo>
    </perimeter>
    <sourceDataInfo>
        <dataType type="uint32">0</dataType>
        <width type="uint32">1920</width>
        <height type="uint32">1080</height>
        <sourceBase64Length type="uint32">161438</sourceBase64Length>
        <sourceBase64Data type="string"><![CDATA[...]]></sourceBase64Data>
    </sourceDataInfo>
    <listInfo type="list" count="1">
        <item>
            <targetId type="tuint32">20</targetId>
            <rect>...</rect>
            <targetImageData>
                <dataType type="uint32">0</dataType>
                <targetType type="uint32">1</targetType> <!-- 1:person, 2:car, 4:bike -->
                <Width type="tuint32">1276</Width>
                <Height type="tuint32">1080</Height>
                <targetBase64Length type="uint32">100774</targetBase64Length>
                <targetBase64Data type="string"><![CDATA[...]]></targetBase64Data>
            </targetImageData>
        </item>
    </listInfo>
</config>
```

**NVR regionIntrusion (actual captured data):**
```xml
<config version="2.0.0" xmlns="http://www.ipc.com/ver10">
    <messageType>alarmData</messageType>
    <deviceInfo>
        <deviceName><![CDATA[Device Name]]></deviceName>
        <ip><![CDATA[192.168.0.55]]></ip>
        <mac><![CDATA[58:5B:69:40:F4:0D]]></mac>
        <channelId>1</channelId>
    </deviceInfo>
    <smartType>regionIntrusion</smartType>
    <currentTime>1772056914604000</currentTime>
    <eventInfo>
        <item>
            <eventId>916</eventId>
            <targetId>716</targetId>
            <boundary>area</boundary>
            <pointGroup>
                <item><x>1590</x><y>3080</y></item>
                <item><x>4715</x><y>3181</y></item>
                ...
            </pointGroup>
            <rect>
                <x1>3096</x1><y1>3715</y1>
                <x2>4005</x2><y2>9861</y2>
            </rect>
        </item>
    </eventInfo>
    <sourceDataInfo>
        <dataType>0</dataType>
        <width>1280</width>
        <height>720</height>
        <sourceBase64Length>400924</sourceBase64Length>
        <sourceBase64Data>...</sourceBase64Data>
    </sourceDataInfo>
</config>
```

**Key structural differences:**
- IPC: event in `<perimeter><perInfo>` → NVR: event in `<eventInfo>`
- IPC: `<boundary type="list">` with `<point><x>` → NVR: `<boundary>area</boundary>` + separate `<pointGroup>` with `<x>`
- IPC: `<status type="smartStatus">SMART_START</status>` → NVR: no status field
- IPC: `<subscribeRelation>` and `<types>` block → NVR: none of this
- IPC: has `<listInfo>` with `<targetImageData>` (cropped target) → NVR: uses `<targetListInfo>` (see Section 3.4)
- IPC: type annotations (`type="uint32"`) on all fields → NVR: no type annotations
- IPC: `targetType` is numeric (1=person, 2=car, 4=bike) → NVR: `targetType` is string (`person`)

---

## 5. Timestamp Differences

| Source | Field | Format | Example | Resolution |
|--------|-------|--------|---------|------------|
| IPC (v1.7) | `dataTime` | Formatted string | `11-19-2025 12:15:11 PM` | Seconds |
| IPC (v1.0) | `currentTime` | Unix timestamp | `1732045234` (10 digits) or `1732045234000` (13 digits) | Seconds or milliseconds |
| NVR (v2.0) | `currentTime` | Unix microseconds | `1772056914000000` (16 digits) | Microseconds |

**Note:** To convert NVR timestamp to seconds, divide by 1,000,000 (not 1,000).

---

## 6. HTTP Header Differences

| Header | IPC Direct | NVR v2.0 |
|--------|-----------|----------|
| Content-Type | `application/xml; charset=utf-8` | `application/soap+xml; charset=utf-8` |
| Connection | `keep-alive` | `close` |
| Accept-Encoding | `gzip, deflate` | Not sent |
| POST line | `POST /API HTTP/1.1` | `POST http://192.168.0.56:5002/API HTTP/1.1` (full URL) |

The NVR sends the full absolute URL in the POST line, which is unusual for HTTP/1.1 (more typical of proxy requests). The IPC sends just the path.

---

## 7. Documentation Gaps (for manufacturer)

These are things **not documented** or **inconsistent** across the three API documents.

### Gaps in v1.9 and v2.0 API Guides

1. **No documentation of NVR alarm server HTTP Post format.** The `GetAlarmServerConfig` / `SendAlarmStatus` sections only show a basic `alarmStatusInfo` example. The actual NVR posts with `messageType`, `eventInfo`, `sourceDataInfo` are completely undocumented. The Long Polling doc has detailed IPC examples but the NVR format is different.

2. **No documentation of `messageType` field.** The NVR uses `keepalive`, `alarmStatus`, `alarmData` - none of these are mentioned in any API doc. The Long Polling doc uses `SendAlarmData` and `SendAlarmStatus` as command names but doesn't use a `messageType` XML field.

3. **No documentation of NVR `eventInfo` structure.** The NVR puts event data in `<eventInfo>` with flat `<eventId>`, `<targetId>`, `<boundary>`, `<pointGroup>`, `<rect>`. The Long Polling doc shows the IPC puts equivalent data in `<perimeter><perInfo>` with typed fields. Neither format is cross-referenced.

4. **No documentation of NVR `smartType` values.** The NVR uses `regionIntrusion` which doesn't appear in any doc. The Long Polling doc lists IPC codes (`PEA`, `VFD`, `VEHICE`, etc.) but no mapping to the NVR's descriptive names.

5. **No documentation of NVR keepalive format.** The IPC keepalive uses a `<DeviceInfo>` root element. The NVR keepalive uses `<config>` root with `<messageType>keepalive</messageType>`. Neither format is documented in the API guides.

6. **No documentation of timestamp format differences.** The NVR uses 16-digit Unix microseconds. The IPC uses `tint64` (also microseconds per Long Polling doc) OR formatted date strings (`dataTime`). The Long Polling doc shows `currentTime type="tint64"` with 16-digit values matching the NVR, but the alarm server posts from IPCs use `dataTime` with formatted strings. Confusing.

7. **`GetAlarmServerConfig` is listed as "IPC only" in v2.0 docs**, but NVRs clearly have this feature too.

8. **No documentation of which alarm types the NVR forwards.** Does the NVR forward all camera alarm types? Does it aggregate multiple cameras? Can you configure which events get forwarded? None of this is documented.

### Gaps in Long Polling Doc

9. **Long Polling doc is from 2019** and only covers IPC v1.0/1.7. It doesn't acknowledge that NVRs can also push alarm data, or that the NVR format is different.

10. **`targetListInfo` structure undocumented.** The NVR sends target crops in `<targetListInfo>` (not `<listInfo>` like IPC). Each item has `targetId`, `targetType` (string, e.g. `person`), and optionally `targetImageData` with base64 crop. The IPC uses `<listInfo>` with numeric `targetType` (1=person, 2=car, 4=bike). Neither the different element name nor the string-vs-numeric targetType is documented.

11. **`subscribeRelation` and `types` block missing from NVR.** The IPC includes a full `<types>` enum block and `<subscribeRelation>` in every alarm post. The NVR sends none of this. Is this because the NVR uses the alarm server model (not long polling subscription)?

### Questions for Manufacturer

- What are ALL the NVR v2.0 `smartType` values? We only have `regionIntrusion` so far.
- ~~Does the NVR ever send `targetImageData` (cropped target images)?~~ **ANSWERED:** Yes. In `targetListInfo`, configurable via alarm server image settings.
- ~~Does the NVR include `targetType` (person/car/bike classification) anywhere?~~ **ANSWERED:** Yes. `targetType` in `targetListInfo/item` as a string (e.g., `person`). Always present even with images disabled.
- Is the NVR alarm server the same as the IPC alarm server, or a different feature?
- Can the NVR be configured to use the Long Polling subscription model (`SetSubscribe`)?
- Why does the NVR use `Connection: close` while the IPC uses `keep-alive`?
- Does lineCrossing ever include crossing direction (A→B vs B→A)? Tested with bidirectional crossing — no direction field observed.

---

## 8. Server Changes Needed

### Must Have (to accept NVR v2.0 posts)
- [x] Detect API version from `<config version="2.0.0">` vs `<config version="1.0">` — **Done Feb 25, 2026** (`server.py` checks `@version`)
- [x] Handle `messageType` routing: `keepalive` → log, `alarmStatus` → log, `alarmData` → process event — **Done Feb 25, 2026**
- [x] Map new `smartType` values: `regionIntrusion` → `RegionIntrusion` class — **Done Feb 25, 2026** (`v2_class_lookup` in `server.py`)
- [x] Parse `deviceInfo` block for NVR format (`ip`, `mac`, `channelId`) vs IPC format (`ipAddress`, `macAddress`) — **Done Feb 25, 2026** (`APIpostV2` in `viewtron.py`)
- [x] Handle 16-digit microsecond timestamps (divide by 1,000,000) — **Done Feb 25, 2026**
- [x] Parse `eventInfo` structure (new in v2.0) for event details — **Parsed during object creation**
- [x] Parse `sourceDataInfo` for image extraction — **Done Feb 25, 2026** (overview image)
- [x] Parse `targetListInfo/targetImageData` for target crop — **Done Feb 25, 2026** (first target item)
- [x] Handle all 4 image configurations (both/original/target/none) — **Tested Feb 25, 2026**

### Should Have
- [x] Log `channelId` - NVR can forward events from multiple cameras — **Available via `get_channel_id()`**, not yet in CSV
- [ ] Add `channelId` to CSV log output
- [ ] Log `eventId` and `targetId` from `eventInfo` for event deduplication / correlation
- [ ] Store bounding box `rect` data for target location
- [ ] Store intrusion zone `pointGroup` polygon data
- [ ] Track alarm state from `alarmStatus` messages (true/false transitions)
- [x] Handle NVR keepalive separately (different format from IPC keepalive) — **Done Feb 25, 2026**

### Nice to Have
- [ ] Unified event model that normalizes IPC and NVR posts into the same internal structure
- [x] Auto-detect whether source is IPC or NVR based on post format — **Done Feb 25, 2026** (version check)
- [ ] Store image resolution metadata (`width`, `height`) from NVR posts
- [ ] Handle multiple targets in `targetListInfo` (currently only saves first target crop)

### Testing Needed
- [ ] Test NVR with LPR camera connected - what smartType does it use? (`VEHICLE`? `licensePlate`? something else?)
- [ ] Test NVR with face detection camera - what smartType?
- [x] Test NVR with line crossing configured — **ANSWERED: `lineCrossing`** with `boundary: tripwire` and `directionLine` (startPoint/endPoint). See Section 3.5.
- [ ] Test NVR with multiple cameras - does channelId increment?
- [ ] Test NVR with zone entry/exit - what smartType?
- [ ] Test NVR with video metadata (VSD) camera
- [x] Does NVR ever send `targetImageData` (cropped target image) or only `sourceDataInfo` (full scene)? — **ANSWERED: NVR sends BOTH.** `targetImageData` is inside `targetListInfo` (not `listInfo`). Configurable per NVR settings (both/original/target/none). See Section 3.4.

---

## 9. Raw Post Samples

All raw posts from this test session are saved in `raw_posts/` with naming convention:
```
raw_YYYY-MM-DD_HH-MM-SS.fff_IP.xml
```

Key samples:
- **Keepalive:** `raw_2026-02-25_22-01-43.919_192-168-0-55.xml` (441 bytes)
- **Alarm Status (true):** `raw_2026-02-25_22-01-53.309_192-168-0-55.xml` (617 bytes)
- **Alarm Status (false):** `raw_2026-02-25_22-02-06.909_192-168-0-55.xml` (618 bytes)
- **Alarm Data (both images):** `raw_2026-02-25_22-39-12.393_192-168-0-55.xml` (~524 KB)
- **Alarm Data (original only):** `raw_2026-02-25_22-59-22.383_192-168-0-55.xml` (~418 KB)
- **Alarm Data (target only):** `raw_2026-02-25_23-00-46.493_192-168-0-55.xml` (~92 KB)
- **Alarm Data (no images):** `raw_2026-02-25_22-58-18.692_192-168-0-55.xml` (~1 KB)
- **Line Crossing (both images):** `raw_2026-02-25_23-04-50.920_192-168-0-55.xml` (~532 KB)

---

*Last updated: February 25, 2026 — Added image configuration options (Section 3.4), updated server changes to done, answered targetImageData and targetType questions*
