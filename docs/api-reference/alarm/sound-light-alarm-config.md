---
title: "Sound & Light Alarm Configuration"
description: "API reference for sound and light alarm config — control siren audio and white light strobe on Viewtron active deterrent cameras."
keywords: [ip camera active deterrent api, viewtron api, camera siren strobe config]
sidebar_label: "Sound & Light"
sidebar_position: 7
---

# Sound & Light Alarm Configuration

:::tip Application Guide
For active deterrent camera integration, see the [Active Deterrent Sound & Light Alarm](/docs/applications/active-deterrent-sound-light-alarm-api) application guide.
:::

Retrieve configuration for active deterrent features -- audio alarm (siren/voice) and white light (strobe) alarm outputs. These are available on Viewtron cameras equipped with built-in speakers and white LED lights.

This page covers two endpoints:

- **GetAudioAlarmOutConfig** -- audio alarm output settings
- **GetWhiteLightAlarmOutConfig** -- white light strobe alarm settings

:::caution Version Note
**v2.0 only.** These endpoints are only available on cameras running v2.0 firmware. They are not supported on v1.9 devices.
:::

---

## GetAudioAlarmOutConfig

Retrieves audio alarm output configuration, including siren type, volume, and duration settings. **IPC only.**

| Field | Value |
|-------|-------|
| **Endpoint** | `/GetAudioAlarmOutConfig[/channelId]` |
| **Method** | `POST` or `GET` |
| **Products** | IPC |
| **Channel ID** | Optional (default `1`) |

---

## GetWhiteLightAlarmOutConfig

Retrieves white light (strobe) alarm configuration, including flash pattern and duration settings. **IPC only.**

| Field | Value |
|-------|-------|
| **Endpoint** | `/GetWhiteLightAlarmOutConfig[/channelId]` |
| **Method** | `POST` or `GET` |
| **Products** | IPC |
| **Channel ID** | Optional (default `1`) |

---

## Notes

- These endpoints are read-only (Get). Active deterrent settings are typically configured through the camera's web interface.
- Active deterrent features are only available on camera models with built-in speakers and white LED lights (e.g., dual-LED models).
- Audio and white light alarms are triggered by the camera's AI detection events (perimeter, tripwire, etc.) based on the configured alarm linkage settings.
