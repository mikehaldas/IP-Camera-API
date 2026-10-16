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

## V2 rows and the V1 sender

On LPR-IP4 firmware 5.3.1, saving a V2 (`httpPostV2`) row in the web interface also turned on the legacy V1 `httpPost` sender, aimed at the same host, port, and path. The page has no separate V1 switch. In testing with a V2 row saved for `VEHICLE`, every post received used the V1 layout: config version `1.7`, no `messageType` on plate posts, and `smartType` `VEHICE`. No V2-format posts were received. Plate posts from this firmware therefore follow the [IPC Event Format (v1.x)](./ipc-event-format.md#lpr-event-vehice--vehicle), including `vehicleListType` for listed plates.

No V2.1-format post body has been captured yet, so this page does not document one.
