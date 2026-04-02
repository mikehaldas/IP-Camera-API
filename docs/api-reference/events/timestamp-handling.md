---
title: "Timestamp Handling"
description: "Reference for timestamp formats in Viewtron IP camera and NVR webhook events — Unix, microsecond, and formatted string types."
keywords: [ip camera timestamp format, viewtron api timestamps, camera event time parsing]
sidebar_label: "Timestamps"
sidebar_position: 8
---

# Timestamp Handling

Viewtron devices use several different timestamp formats across IPC and NVR posts. This page documents each format and how to interpret them.

## Timestamp Formats

| Source | Field | Format | Example | Resolution |
|--------|-------|--------|---------|------------|
| IPC alarm push (v1.7) | `dataTime` | Formatted string | `2026-03-29 09:58:21` or `11-19-2025 12:15:11 PM` | Seconds |
| IPC alarm data (v1.0) | `currentTime` | Unix timestamp | `1732045234` (10 digits) or `1732045234000` (13 digits) | Seconds or milliseconds |
| IPC traject/smartData (v1.7) | `currentTime` | Unix microseconds | `1774646121524166` (16 digits) | Microseconds |
| NVR (v2.0) | `currentTime` | Unix microseconds | `1772056914000000` (16 digits) | Microseconds |

## Converting Microsecond Timestamps

To convert microsecond timestamps to seconds, divide by 1,000,000 (not 1,000).

```python
# NVR or IPC v1.7 microsecond timestamp
current_time = 1772056914604000

# Convert to seconds
timestamp_seconds = current_time / 1_000_000  # 1772056914.604

# Convert to datetime
from datetime import datetime
dt = datetime.fromtimestamp(timestamp_seconds)
# 2026-02-26 10:21:54.604000
```

## Identifying the Format

You can determine the timestamp format by the number of digits:

| Digits | Format | Division Factor |
|--------|--------|----------------|
| 10 | Unix seconds | 1 |
| 13 | Unix milliseconds | 1,000 |
| 16 | Unix microseconds | 1,000,000 |

:::note Vehicle LPR timestamp anomaly
The NVR `vehicle` (LPR) detection type has been observed sending a 20-digit `currentTime` value (e.g., `18445822972087551616`). This appears to be a firmware bug. Use the server receive time as a fallback for LPR events.
:::

:::tip Application Guides
For a working implementation that handles all timestamp formats, see the [Webhook Event Notification API](/docs/applications/webhook-event-notification-api).
:::
