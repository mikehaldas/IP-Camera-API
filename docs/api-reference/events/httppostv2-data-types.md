---
title: "httpPostV2 Data Types — Subscription Options"
description: "Reference for httpPostV2 data type subscriptions — traject, alarmStatus, smartData, and image options on Viewtron IP cameras."
keywords: [httppostv2 data types, viewtron api subscriptions, camera event data options]
sidebar_label: "Data Types"
sidebar_position: 5
---

# httpPostV2 Data Types

This page explains how the five httpPostV2 data types interact when subscribed together, and how to choose the right combination for your use case.

## How Data Types Work Together

Each data type generates **separate HTTP Posts**. When a detection event occurs, the camera sends posts in this order:

1. **`traject`** -- Starts immediately when tracking begins. Continuous stream at ~7 posts/sec. Stops when target leaves.
2. **`alarmStatus`** -- One `true` post at alarm start, one `false` when alarm hold time expires.
3. **`smartData`** (+ `sourceImage`/`targetImage`) -- Detection event with coordinates and optionally images.

## Tested Timeline

IPC IP-AX8D, March 29, 2026, all five data types subscribed:

```
13:58:46.797  traject starts    -- person enters zone, target id=2157
13:58:47.258  smartData+images  -- PEA SMART_START event (517 KB)
13:58:47.436  alarmStatus       -- perimeterAlarm=true (658 bytes)
13:58:47-54   traject stream    -- continuous ~7 posts/sec
13:58:48.258  smartData+images  -- second PEA event (527 KB)
13:58:54.131  traject stops     -- person leaves zone, 50 traject posts total

              ~6 second gap -- zero traject posts (person out of zone)

13:59:00.616  traject starts    -- person re-enters, new target id=2160
13:59:01.446  smartData+images  -- PEA SMART_START event (511 KB)
13:59:01.605  smartData+images  -- second PEA event (524 KB)
13:59:01-08   traject stream    -- continuous tracking, 54 posts
13:59:08.546  traject stops     -- person leaves zone
13:59:19.056  alarmStatus       -- perimeterAlarm=false (659 bytes)

14:00:49+     keepalives        -- empty body posts every ~90 seconds
```

**Total: 104 traject posts, 4 smartData+image posts, 2 alarmStatus posts, 3 keepalives**

**Key observations:**
- traject starts before alarmStatus
- traject has zero gaps while the target is present
- alarmStatus is sparse -- only one true/false pair per alarm cycle
- New target IDs per entry (2157, then 2160)

## Choosing Which Data Types to Subscribe

| Use Case | Recommended Data Types | Why |
|----------|----------------------|-----|
| **Real-time automation** (relay control, lighting) | `traject` only | Continuous presence signal, ~12 KB/sec |
| **Event logging with images** | `smartData` + `sourceImage` + `targetImage` | One post per event with full scene + target crop |
| **Event logging without images** | `smartData` or `alarmStatus` | Lightweight, ~660 bytes - 3 KB per event |
| **Full monitoring** | All five | Complete picture |
| **Counting/analytics** | `traject` + `smartData` | Track positions continuously, get event boundaries |

## Bandwidth

- `traject` alone: ~12 KB/sec per tracked target
- `smartData` + images: ~500-530 KB per event (one-time)
- `alarmStatus`: ~660 bytes per state change

## Subscription XML Examples

**Subscribing to multiple data types:**

```xml
<subscribeDateType type="list" count="3">
  <item>traject</item>
  <item>smartData</item>
  <item>alarmStatus</item>
</subscribeDateType>
```

**Subscribing to all five:**

```xml
<subscribeDateType type="list" count="5">
  <item>alarmStatus</item>
  <item>traject</item>
  <item>smartData</item>
  <item>sourceImage</item>
  <item>targetImage</item>
</subscribeDateType>
```

:::tip Application Guides
For step-by-step httpPostV2 configuration, see [Webhook Event Notification API](/docs/applications/webhook-event-notification-api). For traject-based automation, see [Relay Control & IoT Automation](/docs/applications/relay-control-iot-automation-api).
:::
