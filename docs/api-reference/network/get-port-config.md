---
title: "GetPortConfig — Port Configuration"
description: "API reference for GetPortConfig — retrieve HTTP, HTTPS, RTSP, and service port settings on Viewtron IP cameras."
keywords: [ip camera port config api, viewtron api, camera rtsp http port]
sidebar_label: "Port Config"
sidebar_position: 2
---

# GetPortConfig

Retrieves the port configuration of the device, including HTTP, HTTPS, RTSP, and other service ports.

| Field | Value |
|-------|-------|
| **Endpoint** | `/GetPortConfig` |
| **Method** | `POST` or `GET` |
| **Products** | IPC, NVR |
| **Request Body** | None |

:::caution Version Note
**v1.9 only.** This endpoint has been tested on v1.9 firmware. Availability on v2.0 devices has not been confirmed.
:::

---

## Expected Response Fields

The response contains the device's configured service ports:

| Field | Description |
|-------|-------------|
| HTTP port | Web interface and API port (default: 80) |
| HTTPS port | Secure web interface port (default: 443) |
| RTSP port | Video streaming port (default: 554) |
| Other service ports | Additional ports for SDK, ONVIF, etc. |

---

## Notes

- This is a read-only endpoint for retrieving the current port configuration.
- Knowledge of the configured ports is important for constructing correct API URLs and RTSP streaming URLs.
- If the HTTP port has been changed from the default (80), you must include the port in all API request URLs: `http://<host>:<port>/endpoint`.
- Port configuration changes are typically made through the device's web interface.
