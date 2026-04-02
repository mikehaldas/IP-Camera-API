---
title: "ModifyPassword — Change User Password"
description: "API reference for ModifyPassword — change the user password on Viewtron IP cameras and NVRs via authenticated HTTP POST."
keywords: [ip camera change password api, viewtron api, camera security password]
sidebar_label: "Modify Password"
sidebar_position: 1
---

# ModifyPassword

Modifies the user password on the device. This endpoint requires authentication with the current credentials.

| Field | Value |
|-------|-------|
| **Endpoint** | `/ModifyPassword` |
| **Method** | `POST` |
| **Products** | IPC, NVR |

---

## Notes

- This endpoint requires `POST` -- `GET` is not supported.
- You must authenticate with the current username and password (HTTP Digest authentication) to change the password.
- After a successful password change, all subsequent API requests must use the new credentials.
- Password changes take effect immediately -- existing sessions using the old password will be invalidated.

:::warning Security Best Practice
Always use strong, unique passwords for your cameras and NVRs. Never use the default password in production environments. Change the default password during initial device setup before connecting the device to a network.
:::
