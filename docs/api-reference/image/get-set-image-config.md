---
title: "GetImageConfig / SetImageConfig — Image Settings"
description: "API reference for GetImageConfig and SetImageConfig — adjust brightness, contrast, saturation, and Smart IR intensity on Viewtron IP cameras."
keywords: [ip camera image settings api, viewtron api, camera brightness contrast, smart ir, manual ir intensity, ircut mode]
sidebar_label: "Image Config"
sidebar_position: 1
---

# GetImageConfig / SetImageConfig

Get or set image parameters (brightness, contrast, saturation, etc.).

## Endpoint

| Field | Value |
|-------|-------|
| **Method** | `POST` or `GET` (Get) / `POST` (Set) |
| **URL (Get)** | `http://<host>[:port]/GetImageConfig[/channelId]` |
| **URL (Set)** | `http://<host>[:port]/SetImageConfig[/channelId]` |
| **Products** | IPC, NVR |
| **Channel ID** | Optional (default 1) |

## Image Parameters

| Field | Type | Range | Default | Description |
|-------|------|-------|---------|-------------|
| `bright` | uint8 | 0--100 | 50 | Brightness level |
| `contrast` | uint8 | 0--100 | 50 | Contrast level |
| `saturation` | uint8 | 0--100 | 50 | Color saturation |
| `hue` | uint8 | 0--100 | 50 | Color hue |
| `mirrorSwitch` | boolean | -- | false | Horizontal mirror |
| `flipSwitch` | boolean | -- | false | Vertical flip |
| `IRCutMode` | enum | auto, day, night, time, alarmInLink | auto | IR cut filter mode |
| `whiteBalance.mode` | enum | auto, indoor, outdoor, manual | auto | White balance mode |
| `whiteBalance.red` | uint8/uint32 | 0--100 | 50 | Red gain (manual mode) |
| `whiteBalance.blue` | uint8/uint32 | 0--100 | 50 | Blue gain (manual mode) |
| `backlightCompensation.mode` | enum | OFF, HWDR, HLC, BLC | OFF | Backlight compensation (v2.0) |
| `infraredMode` | enum | auto, on, off | auto | Infrared LED mode (v2.0) |
| `smartIRV2.mode` | enum | off, manual, auto | -- | Smart IR mode (dome cameras). Set to `manual` to control IR intensity |
| `smartIRV2.lightLevel[].id` | uint32 | -- | 1 | IR lamp-group ID |
| `smartIRV2.lightLevel[].level` | uint8 | 0--100 | 50 | **IR intensity level.** Dependent — writable only when `smartIRV2.mode` = `manual` |

## Response (v2.0)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="2.0.0" xmlns="http://www.ipc.com/ver10">
  <types>
    <IRCutMode>
      <enum>auto</enum>
      <enum>day</enum>
      <enum>night</enum>
      <enum>time</enum>
      <enum>alarmInLink</enum>
    </IRCutMode>
    <whitebalanceMode>
      <enum>auto</enum>
      <enum>indoor</enum>
      <enum>outdoor</enum>
      <enum>manual</enum>
    </whitebalanceMode>
    <BLCMode>
      <enum>OFF</enum>
      <enum>HWDR</enum>
      <enum>HLC</enum>
      <enum>BLC</enum>
    </BLCMode>
    <smartIRMode>
      <enum>off</enum>
      <enum>manual</enum>
      <enum>auto</enum>
    </smartIRMode>
  </types>
  <cfgFile type="configFileType" default="normal">normal</cfgFile>
  <image>
    <bright type="uint8" min="0" max="100" default="50">50</bright>
    <saturation type="uint8" min="0" max="100" default="50">50</saturation>
    <contrast type="uint8" min="0" max="100" default="50">50</contrast>
    <hue type="uint8" min="0" max="100" default="50">50</hue>
    <mirrorSwitch type="boolean" default="false">false</mirrorSwitch>
    <flipSwitch type="boolean" default="false">true</flipSwitch>
    <IRCutMode type="IRCutMode" default="auto">auto</IRCutMode>
    <whiteBalance>
      <mode type="whitebalanceMode" default="auto">auto</mode>
      <red min="0" max="100" default="50">50</red>
      <blue min="0" max="100" default="50">50</blue>
    </whiteBalance>
    <backlightCompensation>
      <mode type="BLCMode" default="OFF">OFF</mode>
    </backlightCompensation>
    <smartIRV2>
      <mode type="smartIRMode">manual</mode>
      <lightLevel type="list" maxCount="1" count="1">
        <item>
          <id type="uint32">1</id>
          <level type="uint8" min="0" max="100" default="50">50</level>
        </item>
      </lightLevel>
    </smartIRV2>
    <infraredMode type="infraredModeE" default="auto">auto</infraredMode>
  </image>
</config>
```

:::note Smart IR — manual IR intensity control
On cameras with controllable infrared LEDs (typically dome models), IR brightness is set through the **`smartIRV2`** block:

- Set **`smartIRV2.mode`** to `manual` to take manual control (`auto` lets the camera adjust intensity automatically; `off` disables Smart IR).
- Then set **`smartIRV2.lightLevel.item.level`** (0–100) — this is the IR intensity value. It is only honored when `mode` is `manual`.
- `id` identifies the IR lamp group; cameras with a single IR array use `id` `1`.

**Set example (manual IR at 80%):**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="2.0.0" xmlns="http://www.ipc.com/ver10">
  <image>
    <smartIRV2>
      <mode>manual</mode>
      <lightLevel type="list" maxCount="1" count="1">
        <item>
          <id>1</id>
          <level>80</level>
        </item>
      </lightLevel>
    </smartIRV2>
  </image>
</config>
```

**If `GetImageConfig` does not return a `smartIRV2` (or `smartIR`) block**, the camera's current firmware or hardware does not expose controllable Smart IR, and `SetImageConfig` writes to those fields are silently ignored. Confirm the model supports it (check `supportInfraredLamp` in [GetDeviceDetail](../system/get-device-detail)) and that the camera is on current firmware — `smartIRV2` was introduced in a later firmware revision than the base v2.0 image config.

**Legacy firmware** exposes a simpler single-lamp form instead:

```xml
<smartIR>
  <mode type="smartIRMode">manual</mode>
  <level type="uint8" min="0" max="100" default="50">50</level>
</smartIR>
```
:::

## Response (v1.9)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="1.0" xmlns="http://www.ipc.com/ver10">
  <types>
    <frequency>
      <enum>60HZ</enum>
      <enum>50HZ</enum>
    </frequency>
    <whitebalanceMode>
      <enum>auto</enum>
      <enum>manual</enum>
      <enum>outdoor</enum>
      <enum>indoor</enum>
    </whitebalanceMode>
    <IRCutMode>
      <enum>auto</enum>
      <enum>day</enum>
      <enum>night</enum>
    </IRCutMode>
  </types>
  <image>
    <frequency type="frequency" default="50HZ">50HZ</frequency>
    <bright type="uint8" min="0" max="100" default="50">50</bright>
    <contrast type="uint8" min="0" max="100" default="55">55</contrast>
    <hue type="uint8" min="0" max="100" default="50">50</hue>
    <saturation type="uint8" min="0" max="100" default="50">50</saturation>
    <mirrorSwitch type="boolean" default="false">false</mirrorSwitch>
    <flipSwitch type="boolean" default="false">false</flipSwitch>
    <WDR>
      <switch type="boolean" default="false">false</switch>
      <value type="uint8" default="128">128</value>
    </WDR>
    <whiteBalance>
      <mode type="whitebalanceMode" default="auto">auto</mode>
      <red type="uint32" min="0" max="100" default="50">50</red>
      <blue type="uint32" min="0" max="100" default="50">50</blue>
    </whiteBalance>
    <IRCutMode type="IRCutMode" default="auto">auto</IRCutMode>
  </image>
</config>
```

## SetImageConfig Example

This API supports partial parameter updates -- unspecified parameters remain unchanged.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="2.0.0" xmlns="http://www.ipc.com/ver10">
  <image>
    <bright>60</bright>
  </image>
</config>
```

## Notes

- v1.9 includes `frequency` (50HZ/60HZ) and `WDR` (wide dynamic range with switch and value) fields that are not present in v2.0.
- v1.9 `IRCutMode` only supports `auto`, `day`, `night`. v2.0 adds `time` and `alarmInLink` modes.

:::info v2.0 Changes
v2.0 adds `sharpen`, `denoise`, `backlightCompensation` (with HWDR/HLC/BLC modes), `infraredMode`, `cfgFile` (normal/day/night config files), and `rebootPrompt` in Set requests.
:::
