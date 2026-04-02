---
title: "TriggerVirtualAlarm — Virtual Alarm Control"
description: "API reference for TriggerVirtualAlarm — trigger virtual alarm inputs on Viewtron NVRs for external system integration."
keywords: [nvr virtual alarm api, viewtron api, ip camera trigger alarm]
sidebar_label: "Virtual Alarm"
sidebar_position: 4
---

# TriggerVirtualAlarm

Triggers a virtual alarm input on the NVR. Virtual alarms allow external systems to fire NVR alarm events, triggering recording, push notifications, and alarm output actions just like a physical alarm input.

| Field | Value |
|-------|-------|
| **Endpoint** | `/TriggerVirtualAlarm/{virtualAlarmId}` |
| **Method** | `GET` |
| **Products** | NVR only |
| **Request Body** | None |

:::caution Version Note
**v2.0 only.** This is an undocumented command discovered through testing. It is not available on v1.9 firmware.
:::

---

## Virtual Alarm ID Calculation

Virtual alarm IDs start after the physical alarm inputs. If the NVR has 16 physical alarm inputs, then:

| Virtual Alarm | ID |
|---------------|-----|
| Virtual alarm 1 | 17 |
| Virtual alarm 2 | 18 |
| Virtual alarm 3 | 19 |
| ... | ... |

Use `GetAlarmInInfo` to see the full list of physical and virtual alarm inputs and determine the correct ID.

---

## Example

```bash
curl -u admin:password "http://192.168.0.147/TriggerVirtualAlarm/17"
```

---

## Response Example

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="2.0.0" xmlns="http://www.ipc.com/ver10" status="success" errorCode="0" errorDesc="Successful"></config>
```

---

## Use Cases

- **AI inference boxes** -- External AI systems can trigger NVR alarm events when they detect objects or events.
- **Third-party software integration** -- Business logic or automation software can trigger NVR recording and push notifications.
- **Home automation** -- IoT platforms can trigger NVR alarms based on sensor events (door contacts, motion sensors, etc.).

---

## Notes

- The virtual alarm behaves identically to a physical alarm input -- it will trigger any configured alarm actions (recording, alarm output relay, push notification, email).
- Virtual alarm configuration (linked actions, alarm output triggers) is done through the NVR web interface under Alarm settings.
- This endpoint uses `GET` rather than `POST`, making it simple to trigger from scripts, webhooks, or browser-based tools.
