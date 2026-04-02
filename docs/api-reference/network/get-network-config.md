---
title: "GetNetBasicConfig — Network Settings"
description: "API reference for GetNetBasicConfig — retrieve IP address, subnet mask, gateway, and DNS settings on Viewtron IP cameras and NVRs."
keywords: [ip camera network config api, viewtron api, camera ip address settings]
sidebar_label: "Network Config"
sidebar_position: 1
---

# GetNetBasicConfig

Retrieves the basic network configuration of the device, including IP address, subnet mask, gateway, and DNS settings.

| Field | Value |
|-------|-------|
| **Endpoint** | `/GetNetBasicConfig` |
| **Method** | `POST` or `GET` |
| **Products** | IPC, NVR |
| **Request Body** | None |

---

## Expected Response Fields

The response contains the device's network interface configuration:

| Field | Description |
|-------|-------------|
| IP address | Device's current IP address |
| Subnet mask | Network subnet mask |
| Gateway | Default gateway address |
| DNS | Primary and secondary DNS server addresses |
| DHCP | Whether DHCP is enabled or a static IP is configured |

---

## Notes

- This is a read-only endpoint for retrieving the current network configuration.
- Use this endpoint to verify a device's network settings during initial setup or troubleshooting.
- Network configuration changes are typically made through the device's web interface to avoid accidental disconnection.
