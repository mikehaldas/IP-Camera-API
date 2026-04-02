---
title: "Alarm Input/Output Configuration"
description: "API reference for alarm I/O configuration — read sensor settings and control relay outputs on Viewtron IP cameras and NVRs."
keywords: [ip camera alarm io api, viewtron api, camera relay control]
sidebar_label: "Alarm I/O"
sidebar_position: 2
---

# Alarm Input/Output Configuration

:::tip Application Guide
For relay control and IoT automation examples, see the [Relay Control & IoT Automation](/docs/applications/relay-control-iot-automation-api) application guide.
:::

Configure and control hardware alarm inputs (sensors) and outputs (relays). This page covers three endpoints:

- **GetAlarmInConfig** -- read alarm input sensor settings
- **GetAlarmOutConfig** -- read alarm output relay settings
- **ManualAlarmOut** -- manually trigger or release an alarm output relay

---

## GetAlarmInConfig

Retrieves alarm input configuration including sensor name, voltage type, and linked alarm outputs.

| Field | Value |
|-------|-------|
| **Endpoint** | `/GetAlarmInConfig[/channelId]` |
| **Method** | `POST` or `GET` |
| **Products** | IPC, NVR |

### Response Example

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="1.0" xmlns="http://www.ipc.com/ver10">
  <types>
    <alarmInVoltage>
      <enum>NO</enum>
      <enum>NC</enum>
    </alarmInVoltage>
  </types>
  <sensor>
    <id type="uint32">1</id>
    <sensorName type="string" maxLen="11"><![CDATA[Sensor1]]></sensorName>
    <switch type="boolean">true</switch>
    <voltage type="alarmInVoltage">NO</voltage>
    <alarmHoldTime type="uint32">10</alarmHoldTime>
    <triggerAlarmOut type="list" count="1">
      <itemType type="boolean"></itemType>
      <item id="1">true</item>
    </triggerAlarmOut>
  </sensor>
</config>
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | uint32 | Sensor input number |
| `sensorName` | string (max 11 chars) | User-defined name for this sensor input |
| `switch` | boolean | Enable or disable this alarm input |
| `voltage` | enum | Contact type: `NO` (normally open) or `NC` (normally closed) |
| `alarmHoldTime` | uint32 | Duration (seconds) alarm stays active after trigger |
| `triggerAlarmOut` | list | Which alarm output relays to activate when this sensor triggers |

---

## GetAlarmOutConfig

Retrieves alarm output (relay) configuration.

| Field | Value |
|-------|-------|
| **Endpoint** | `/GetAlarmOutConfig[/channelId]` |
| **Method** | `POST` or `GET` |
| **Products** | IPC, NVR |

---

## ManualAlarmOut

Manually triggers or releases an alarm output (relay). Set `status` to `true` to activate or `false` to deactivate.

| Field | Value |
|-------|-------|
| **Endpoint** | `/ManualAlarmOut[/channelId]` |
| **Method** | `POST` |
| **Products** | IPC, NVR |

### Request Example

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config version="1.0" xmlns="http://www.ipc.com/ver10">
  <action>
    <status>true</status>
  </action>
</config>
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `status` | boolean | `true` to activate the relay, `false` to deactivate |

---

## Known Issues

:::warning Firmware Bug (IPC)
The camera forcibly resets the alarm output when a perimeter alarm cycle ends, even when the alarm output mode is set to `manual_alarm` and `triggerAlarmOut` is unchecked. This makes `ManualAlarmOut` unreliable for automation while perimeter detection is active. If you need reliable relay control alongside AI detection, consider using the NVR's alarm outputs instead, or use an external relay controller (such as an ESP8266) driven by [traject data](/docs/api-reference/events/real-time-target-tracking-traject).
:::

---

## Notes

- On NVR systems, include the `channelId` to target a specific camera channel's alarm I/O.
- The `voltage` setting must match the physical wiring of the connected sensor (normally open vs. normally closed).
