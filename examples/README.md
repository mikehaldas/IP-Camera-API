# XML Examples

Example XML payloads for all supported alarm types. These are based on actual captured data from Viewtron IP cameras and NVRs. Base64 image data has been replaced with descriptive placeholders.

Use these examples to understand the XML structure, test your parser, or build your own server without needing a physical camera.

## NVR v2.0 Format (`nvr-v2/`)

Posts forwarded by a Viewtron NVR from cameras connected to its PoE ports.

| File | smartType | Description |
|------|-----------|-------------|
| [region-intrusion.xml](nvr-v2/region-intrusion.xml) | `regionIntrusion` | Person/vehicle enters an intrusion zone |
| [line-crossing.xml](nvr-v2/line-crossing.xml) | `lineCrossing` | Person/vehicle crosses a tripwire line |
| [target-counting-by-line.xml](nvr-v2/target-counting-by-line.xml) | `targetCountingByLine` | Object counted crossing a line |
| [target-counting-by-area.xml](nvr-v2/target-counting-by-area.xml) | `targetCountingByArea` | Object counted within a zone |
| [video-metadata.xml](nvr-v2/video-metadata.xml) | `videoMetadata` | Continuous full-frame object detection |
| [vehicle-lpr.xml](nvr-v2/vehicle-lpr.xml) | `vehicle` | License plate detected with vehicle attributes |
| [face-detection.xml](nvr-v2/face-detection.xml) | `videoFaceDetect` | Face detected with age/sex/glasses/mask |
| [keepalive.xml](nvr-v2/keepalive.xml) | — | Periodic heartbeat (no alarm data) |
| [alarm-status.xml](nvr-v2/alarm-status.xml) | — | Alarm start/stop notification (no images) |

## IP Camera v1.x Format (`ipc-v1x/`)

Posts sent directly by a Viewtron IP camera (not through an NVR).

| File | smartType | Description |
|------|-----------|-------------|
| [lpr.xml](ipc-v1x/lpr.xml) | `VEHICE` | License plate detected with whitelist/blacklist |
| [face-detection.xml](ipc-v1x/face-detection.xml) | `VFD` | Face detected |
| [perimeter-intrusion.xml](ipc-v1x/perimeter-intrusion.xml) | `PEA` | Person/vehicle enters an intrusion zone |
| [line-crossing.xml](ipc-v1x/line-crossing.xml) | `PEA` | Person/vehicle crosses a tripwire line |
| [zone-entry.xml](ipc-v1x/zone-entry.xml) | `AOIENTRY` | Object enters a defined zone |
| [zone-exit.xml](ipc-v1x/zone-exit.xml) | `AOILEAVE` | Object exits a defined zone |
| [video-metadata.xml](ipc-v1x/video-metadata.xml) | `VSD` | Continuous full-frame object detection |
| [keepalive.xml](ipc-v1x/keepalive.xml) | — | Periodic heartbeat |
| [alarm-status.xml](ipc-v1x/alarm-status.xml) | — | Alarm start/stop notification |

## Key Differences Between Formats

| Feature | IPC v1.x | NVR v2.0 |
|---------|----------|----------|
| Config version | `1.0` or `1.7` | `2.0.0` |
| messageType field | Not present | `keepalive`, `alarmStatus`, `alarmData` |
| smartType naming | Codes: `PEA`, `VFD`, `VEHICE` | Descriptive: `regionIntrusion`, `videoFaceDetect`, `vehicle` |
| Timestamps | Unix seconds/ms or formatted date | Unix **microseconds** (16 digits, divide by 1,000,000) |
| Target type | Numeric: `1`=person, `2`=car, `4`=bike | String: `person`, `car` |
| Device info fields | `ipAddress`, `macAddress` | `ip`, `mac`, `channelId` |
| Event data | `perimeter/perInfo`, `tripwire/tripInfo`, `listInfo` | `eventInfo`, `targetListInfo`, `licensePlateListInfo`, `faceListInfo` |
| Type annotations | Present (`type="uint32"`) | Not present |

## Image Placeholders

In these examples, base64-encoded JPEG image data has been replaced with descriptive placeholders:

| Placeholder | Description |
|-------------|-------------|
| `BASE64_JPEG_OVERVIEW_IMAGE` | Full camera scene snapshot |
| `BASE64_JPEG_TARGET_CROP` | Cropped image of the detected person or vehicle |
| `BASE64_JPEG_PLATE_CROP` | Cropped image of the detected license plate |
| `BASE64_JPEG_FACE_CROP` | Cropped image of the detected face |
| `BASE64_JPEG_SOURCE_IMAGE` | Source/overview image (IPC format) |

In real posts, these are standard base64-encoded JPEG data. Decode with any base64 library and save as `.jpg`.

## Coordinate System

All bounding box coordinates (`rect`, `pointGroup`, `boundary`) use a normalized 0–10000 scale on both axes, regardless of actual image resolution. To convert to pixel coordinates:

```
pixel_x = (coordinate_x / 10000) * image_width
pixel_y = (coordinate_y / 10000) * image_height
```

## Testing with These Examples

You can POST these example files directly to the server for testing:

```bash
curl -X POST http://localhost:5002/API \
  -H "Content-Type: application/xml" \
  -d @examples/nvr-v2/vehicle-lpr.xml
```

Note: Image saving will fail since the base64 placeholders are not valid image data, but the server will still parse the XML, extract fields, and log the event to CSV.
