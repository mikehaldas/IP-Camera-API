---
title: "NVR Event Format (v2.0)"
description: "XML format reference for NVR v2.0 alarm events — keepalive, alarmStatus, and alarmData messages from Viewtron NVRs."
keywords: [nvr event format, viewtron api xml, nvr alarm data format]
sidebar_label: "NVR Format"
sidebar_position: 4
---

# NVR Event Format (v2.0)

NVRs send alarm data using config version `2.0.0` with `Content-Type: application/soap+xml; charset=utf-8` and `Connection: close`. The NVR sends three message types identified by a `<messageType>` field (IPC posts do not have this field).

> Tested: NVR v2.0 (firmware 1.4.13), February-March 2026

## Key Differences from IPC Format

| Feature | IPC Direct (v1.0/1.7) | NVR (v2.0.0) |
|---------|------------------------|--------------|
| **Config version** | `1.0` or `1.7` | `2.0.0` |
| **Content-Type** | `application/xml; charset=utf-8` | `application/soap+xml; charset=utf-8` |
| **Connection** | `keep-alive` | `close` |
| **messageType field** | Not present | `keepalive`, `alarmStatus`, `alarmData` |
| **deviceInfo block** | Varies | Always present with `deviceName`, `ip`, `mac`, `channelId` |
| **smartType values** | Codes: `PEA`, `VFD`, `VEHICE`, `VSD` | Spelled out: `regionIntrusion`, `lineCrossing`, `videoFaceDetect`, `videoMetadata`, `vehicle` |
| **Timestamp** | `dataTime` string or `currentTime` (10-16 digits) | `currentTime` Unix **microseconds** (16 digits) |
| **Event data** | `perimeter/perInfo` or `listInfo/item` | `eventInfo/item` with `eventId`, `targetId`, `boundary`, `pointGroup`, `rect` |
| **Image data** | `sourceDataInfo` + `listInfo/targetImageData` | `sourceDataInfo` + `targetListInfo/targetImageData` |
| **targetType** | Numeric: 1=person, 2=car, 4=bike | String: `person`, `car`, `motor` |
| **POST line** | `POST /API HTTP/1.1` (path only) | `POST http://192.168.0.56:5002/API HTTP/1.1` (full URL) |
| **Type annotations** | Present (`type="uint32"`) | Not present |

## Keepalive

Heartbeat sent approximately every 10 seconds.

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

## Alarm Status

Sent when alarm triggers or clears. Always arrives BEFORE the `alarmData` post.

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

### NVR alarmStatus Field Names by Detection Type

| Detection Type | alarmStatusInfo Field |
|----------------|----------------------|
| `regionIntrusion` | `perimeterAlarm` |
| `lineCrossing` | `perimeterAlarm` |
| `targetCountingByLine` | `passlineAlarm` |
| `targetCountingByArea` | `passlineAlarm` |
| `videoMetadata` | None (no alarmStatus sent) |
| `vehicle` | None observed |
| `videoFaceDetect` | `vfdAlarm` |

## Alarm Data -- Outer Structure

All NVR alarm data posts share this outer structure:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="2.0.0" xmlns="http://www.ipc.com/ver10">
    <messageType>alarmData</messageType>
    <deviceInfo>
        <deviceName><![CDATA[...]]></deviceName>
        <ip><![CDATA[...]]></ip>
        <mac><![CDATA[...]]></mac>
        <channelId>1</channelId>
    </deviceInfo>
    <smartType>...</smartType>
    <currentTime>...</currentTime>
    <!-- detection-specific content below -->
</config>
```

## Three XML Structure Types

NVR alarm data uses one of three XML structures depending on the detection type:

1. **`eventInfo` + `targetListInfo`** -- for regionIntrusion, lineCrossing, targetCountingByLine, targetCountingByArea, videoMetadata
2. **`licensePlateListInfo`** -- for vehicle (LPR)
3. **`faceListInfo`** -- for videoFaceDetect

---

## Detection-Specific XML Examples

### regionIntrusion

Perimeter / intrusion zone detection. NVR equivalent of IPC `PEA` (intrusion).

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
            <rect><x1>3096</x1><y1>3715</y1><x2>4005</x2><y2>9861</y2></rect>
        </item>
    </eventInfo>
    <sourceDataInfo>
        <dataType>0</dataType>
        <width>1280</width>
        <height>720</height>
        <sourceBase64Length>400924</sourceBase64Length>
        <sourceBase64Data>... (base64 JPEG) ...</sourceBase64Data>
    </sourceDataInfo>
    <targetListInfo>
        <item>
            <targetId>716</targetId>
            <targetType>person</targetType>
            <targetImageData>
                <dataType>0</dataType>
                <width>336</width>
                <height>448</height>
                <targetBase64Length>78796</targetBase64Length>
                <targetBase64Data><![CDATA[... (base64 JPEG) ...]]></targetBase64Data>
            </targetImageData>
        </item>
    </targetListInfo>
</config>
```

### lineCrossing

Tripwire / line crossing. NVR equivalent of IPC `PEA` (line cross). The outer structure is identical to regionIntrusion. The `eventInfo` differs:

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

**Key differences from regionIntrusion:**
- `boundary` is `tripwire` instead of `area`
- Uses `directionLine` (startPoint + endPoint) instead of `pointGroup` (polygon)
- The NVR does NOT include crossing direction (A-to-B vs B-to-A) in the post

### targetCountingByLine

Object counting by line. NVR equivalent of IPC `PASSLINECOUNT`.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="2.0.0" xmlns="http://www.ipc.com/ver10">
    <messageType>alarmData</messageType>
    <deviceInfo>
        <deviceName><![CDATA[Device Name]]></deviceName>
        <ip><![CDATA[192.168.0.60]]></ip>
        <mac><![CDATA[58:5B:69:40:F4:0D]]></mac>
        <channelId>1</channelId>
    </deviceInfo>
    <smartType>targetCountingByLine</smartType>
    <currentTime>1772140991308000</currentTime>
    <eventInfo>
        <item>
            <eventId>1080</eventId>
            <targetId>480</targetId>
            <boundary>tripwire</boundary>
            <directionLine>
                <startPoint><x>3977</x><y>2146</y></startPoint>
                <endPoint><x>3977</x><y>9974</y></endPoint>
            </directionLine>
            <rect><x1>0</x1><y1>0</y1><x2>0</x2><y2>0</y2></rect>
        </item>
    </eventInfo>
    <sourceDataInfo>
        <dataType>0</dataType>
        <width>1280</width>
        <height>720</height>
        <sourceBase64Length>441256</sourceBase64Length>
        <sourceBase64Data>... (base64 JPEG) ...</sourceBase64Data>
    </sourceDataInfo>
    <targetListInfo>
        <item>
            <targetId>480</targetId>
            <targetType>person</targetType>
            <targetImageData>
                <dataType>0</dataType>
                <width>336</width>
                <height>448</height>
                <targetBase64Length>72896</targetBase64Length>
                <targetBase64Data>... (base64 JPEG) ...</targetBase64Data>
            </targetImageData>
        </item>
    </targetListInfo>
</config>
```

:::note
The `rect` in `eventInfo` is all zeros for line counting -- the target crop in `targetListInfo` still captures the person. Uses `passlineAlarm` for alarm status.
:::

### targetCountingByArea

Object counting by area. NVR equivalent of IPC `TRAFFIC`.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="2.0.0" xmlns="http://www.ipc.com/ver10">
    <messageType>alarmData</messageType>
    <deviceInfo>
        <deviceName><![CDATA[Device Name]]></deviceName>
        <ip><![CDATA[192.168.0.60]]></ip>
        <mac><![CDATA[58:5B:69:40:F4:0D]]></mac>
        <channelId>1</channelId>
    </deviceInfo>
    <smartType>targetCountingByArea</smartType>
    <currentTime>1772145352968000</currentTime>
    <eventInfo>
        <item>
            <eventId>2904</eventId>
            <targetId>2204</targetId>
            <boundary>area</boundary>
            <pointGroup>
                <item><x>4450</x><y>4292</y></item>
                <item><x>4469</x><y>9015</y></item>
                <item><x>1079</x><y>8510</y></item>
                <item><x>1344</x><y>4166</y></item>
            </pointGroup>
            <rect><x1>4431</x1><y1>4409</y1><x2>4971</x2><y2>9791</y2></rect>
        </item>
    </eventInfo>
    <sourceDataInfo>
        <dataType>0</dataType>
        <width>1280</width>
        <height>720</height>
        <sourceBase64Length>414832</sourceBase64Length>
        <sourceBase64Data>... (base64 JPEG) ...</sourceBase64Data>
    </sourceDataInfo>
    <targetListInfo>
        <item>
            <targetId>2204</targetId>
            <targetType>person</targetType>
            <targetImageData>
                <dataType>0</dataType>
                <width>336</width>
                <height>448</height>
                <targetBase64Length>72136</targetBase64Length>
                <targetBase64Data>... (base64 JPEG) ...</targetBase64Data>
            </targetImageData>
        </item>
    </targetListInfo>
</config>
```

### videoMetadata

Full-frame object detection. NVR equivalent of IPC `VSD`.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="2.0.0" xmlns="http://www.ipc.com/ver10">
    <messageType>alarmData</messageType>
    <deviceInfo>
        <deviceName><![CDATA[Device Name]]></deviceName>
        <ip><![CDATA[192.168.0.60]]></ip>
        <mac><![CDATA[58:5B:69:40:F4:0D]]></mac>
        <channelId>1</channelId>
    </deviceInfo>
    <smartType>videoMetadata</smartType>
    <currentTime>1772145578273000</currentTime>
    <eventInfo>
        <item>
            <eventId>3215</eventId>
            <targetId>2215</targetId>
            <boundary>area</boundary>
            <pointGroup>
                <item><x>23</x><y>0</y></item>
                <item><x>9880</x><y>158</y></item>
                <item><x>9904</x><y>9873</y></item>
                <item><x>0</x><y>9841</y></item>
            </pointGroup>
            <rect><x1>5284</x1><y1>4513</y1><x2>6079</x2><y2>9479</y2></rect>
        </item>
    </eventInfo>
    <sourceDataInfo>
        <dataType>0</dataType>
        <width>1280</width>
        <height>784</height>
        <sourceBase64Length>451968</sourceBase64Length>
        <sourceBase64Data>... (base64 JPEG) ...</sourceBase64Data>
    </sourceDataInfo>
    <targetListInfo>
        <item>
            <targetId>2215</targetId>
            <targetType>person</targetType>
            <targetImageData>
                <dataType>0</dataType>
                <width>288</width>
                <height>384</height>
                <targetBase64Length>45832</targetBase64Length>
                <targetBase64Data>... (base64 JPEG) ...</targetBase64Data>
            </targetImageData>
        </item>
    </targetListInfo>
</config>
```

**Key observations:**
- `pointGroup` covers nearly the entire frame (~0-9900 on both axes) -- VSD detects across the full scene
- Does NOT send `alarmStatus` messages -- only `alarmData`
- When multiple AI events are enabled simultaneously, the NVR sends separate posts for each

### vehicle (LPR)

License plate recognition. NVR equivalent of IPC `VEHICE`. Uses a completely different XML structure -- `licensePlateListInfo` instead of `eventInfo` + `targetListInfo`.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="2.0.0" xmlns="http://www.ipc.com/ver10">
    <messageType>alarmData</messageType>
    <deviceInfo>
        <deviceName><![CDATA[Device Name]]></deviceName>
        <ip><![CDATA[192.168.0.60]]></ip>
        <mac><![CDATA[58:5B:69:40:F4:0D]]></mac>
        <channelId>2</channelId>
    </deviceInfo>
    <smartType>vehicle</smartType>
    <currentTime>18445822972087551616</currentTime>
    <sourceDataInfo>
        <dataType>0</dataType>
        <width>0</width>
        <height>0</height>
    </sourceDataInfo>
    <licensePlateListInfo>
        <item>
            <targetId>104</targetId>
            <rect>
                <x1>1104</x1><y1>546</y1>
                <x2>1232</x2><y2>610</y2>
            </rect>
            <licensePlateAttribute>
                <licensePlateNumber><![CDATA[JP116D]]></licensePlateNumber>
                <color>white</color>
            </licensePlateAttribute>
            <carRect>
                <x1>1</x1><y1>0</y1>
                <x2>1</x2><y2>0</y2>
            </carRect>
            <carAttribute>
                <carType><![CDATA[mpv]]></carType>
                <color><![CDATA[white]]></color>
                <brand><![CDATA[GMC]]></brand>
                <model><![CDATA[GMC_SAVANA]]></model>
            </carAttribute>
            <targetImageData>
                <dataType>0</dataType>
                <width>128</width>
                <height>64</height>
                <targetBase64Length>...</targetBase64Length>
                <targetBase64Data>... (base64 JPEG of plate crop) ...</targetBase64Data>
            </targetImageData>
        </item>
    </licensePlateListInfo>
</config>
```

#### licensePlateListInfo/item Fields

| Field | Description | Example |
|-------|-------------|---------|
| `targetId` | Detection tracking ID | `104` |
| `rect` | Plate bounding box (pixel coordinates) | `x1:1104, y1:546, x2:1232, y2:610` |
| `licensePlateAttribute/licensePlateNumber` | Detected plate text | `JP116D` |
| `licensePlateAttribute/color` | Plate color | `white` |
| `carRect` | Vehicle bounding box | May be zeros |
| `carAttribute/carType` | Vehicle classification | `mpv` |
| `carAttribute/color` | Vehicle color | `white` |
| `carAttribute/brand` | Vehicle brand | `GMC` |
| `carAttribute/model` | Vehicle model | `GMC_SAVANA` |
| `targetImageData` | Cropped plate image (128x64 JPEG) | base64 |

**Notable observations:**
- Vehicle attribute recognition identifies type, color, brand, and model -- far richer than IPC v1.x format
- `currentTime` anomaly: the 20-digit timestamp appears to be a firmware bug
- `sourceDataInfo` has zero dimensions but the post is ~628 KB
- No `alarmStatus` observed for this detection type

### videoFaceDetect

Face detection with attribute analysis. NVR equivalent of IPC `VFD`. Uses `faceListInfo`.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="2.0.0" xmlns="http://www.ipc.com/ver10">
    <messageType>alarmData</messageType>
    <deviceInfo>
        <deviceName><![CDATA[Device Name]]></deviceName>
        <ip><![CDATA[192.168.0.60]]></ip>
        <mac><![CDATA[58:5B:69:40:F4:0D]]></mac>
        <channelId>1</channelId>
    </deviceInfo>
    <smartType>videoFaceDetect</smartType>
    <currentTime>1772212642929000</currentTime>
    <sourceDataInfo>
        <dataType>0</dataType>
        <width>1280</width>
        <height>720</height>
        <sourceBase64Length>440072</sourceBase64Length>
        <sourceBase64Data>... (base64 JPEG overview) ...</sourceBase64Data>
    </sourceDataInfo>
    <faceListInfo>
        <item>
            <targetId>50</targetId>
            <rect>
                <x1>854</x1><y1>176</y1>
                <x2>978</x2><y2>300</y2>
            </rect>
            <age>middleAged</age>
            <sex>male</sex>
            <glasses>unknown</glasses>
            <mask>unknown</mask>
            <targetImageData>
                <dataType>0</dataType>
                <width>184</width>
                <height>184</height>
                <targetBase64Length>14860</targetBase64Length>
                <targetBase64Data>... (base64 JPEG face crop) ...</targetBase64Data>
            </targetImageData>
        </item>
    </faceListInfo>
</config>
```

#### faceListInfo/item Fields

| Field | Description | Example |
|-------|-------------|---------|
| `targetId` | Detection tracking ID | `50` |
| `rect` | Face bounding box | `x1:854, y1:176, x2:978, y2:300` |
| `age` | Age classification | `middleAged` |
| `sex` | Gender classification | `male` |
| `glasses` | Glasses detection | `unknown` |
| `mask` | Mask detection | `unknown` |
| `targetImageData` | Square face crop (184x184 JPEG) | base64 |

**Notable observations:**
- Face match/recognition (`VFD_MATCH`) is NOT forwarded by the NVR via HTTP Post. Even with face database configured, only `videoFaceDetect` is sent.
- 4ch NVRs support face detection but NOT face database/recognition. 8ch NVRs support both.
- AlarmStatus uses `vfdAlarm`.

---

## Image Configuration Options

The NVR alarm server settings allow configuring which images are sent. The `eventInfo` and `targetListInfo` are always present regardless of image setting.

| NVR Setting | `sourceDataInfo` | `targetImageData` | `targetListInfo` | Typical Size |
|---|---|---|---|---|
| Both images | Present (overview JPEG) | Present (crop JPEG) | Present with image | ~524 KB |
| Original only | Present (overview JPEG) | **Absent** | Present, no image | ~418 KB |
| Target only | **Absent** | Present (crop JPEG) | Present with image | ~92 KB |
| No images | **Absent** | **Absent** | Present, no image | ~1 KB |

**Both images (~524 KB):**

```xml
<sourceDataInfo>
    <dataType>0</dataType>
    <width>1280</width>
    <height>720</height>
    <sourceBase64Length>443820</sourceBase64Length>
    <sourceBase64Data><![CDATA[... (base64 JPEG) ...]]></sourceBase64Data>
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
            <targetBase64Data><![CDATA[... (base64 JPEG) ...]]></targetBase64Data>
        </targetImageData>
    </item>
</targetListInfo>
```

**Original image only (~418 KB):**

```xml
<sourceDataInfo>
    <dataType>0</dataType>
    <width>1280</width>
    <height>720</height>
    <sourceBase64Length>416540</sourceBase64Length>
    <sourceBase64Data><![CDATA[... (base64 JPEG) ...]]></sourceBase64Data>
</sourceDataInfo>
<targetListInfo>
    <item>
        <targetId>1260</targetId>
        <targetType>person</targetType>
    </item>
</targetListInfo>
```

**Target image only (~92 KB):**

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
            <targetBase64Data><![CDATA[... (base64 JPEG) ...]]></targetBase64Data>
        </targetImageData>
    </item>
</targetListInfo>
```

**No images (~1 KB):**

```xml
<targetListInfo>
    <item>
        <targetId>1254</targetId>
        <targetType>person</targetType>
    </item>
</targetListInfo>
```

:::info
`targetListInfo` is ALWAYS present with at least `targetId` and `targetType`, even with images disabled. Target classification data is always available.
:::

:::tip Application Guides
For NVR webhook setup instructions, see [Webhook Event Notification API](/docs/applications/webhook-event-notification-api). For detection-specific guides, see:
- [Human Detection & Intrusion](/docs/applications/human-detection-intrusion-api)
- [Perimeter Security & Line Crossing](/docs/applications/perimeter-security-line-crossing-api)
- [License Plate Recognition](/docs/applications/license-plate-recognition-camera-api)
- [Face Detection & Recognition](/docs/applications/face-detection-recognition-api)
- [People Counting & Traffic Analytics](/docs/applications/people-counting-traffic-analytics-api)
:::
