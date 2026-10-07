---
title: "IPC HTTP POST Format (v2.1)"
description: "Placeholder for the direct HTTP POST event format sent by Viewtron IP cameras on API 2.1."
keywords: [ip camera http post v2.1, viewtron api webhook, ipc event format]
sidebar_label: "IPC Format (v2.1)"
sidebar_position: 9
---

# IPC HTTP POST Format (v2.1)

Verification of direct camera posts on v2.1 firmware is in progress. Until this section is complete, log the raw post body and check for `messageType`, the `smartType` spelling, and where the plate list result appears.

Cameras on v2.1 firmware report `httpPostVersion` `2.1.0`. On a v2.1 LPR camera running 5.3.1 firmware, the HTTP POST V2 event list in the web interface is `ALL`, `MOTION`, `SENSOR`, `AVD`, and `VEHICLE`, and the data-type element is named `subDataType`. See [httpPostV2 Data Types](./httppostv2-data-types.md) and [Webhook Configuration](/docs/api-reference/alarm/http-post-webhook-config).
