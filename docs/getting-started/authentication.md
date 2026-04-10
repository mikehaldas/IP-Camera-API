---
title: "Authentication — Basic Access Authentication"
sidebar_label: "Authentication"
description: "All Viewtron IP camera API requests require HTTP Basic Authentication. Learn how to authenticate with Base64-encoded credentials."
keywords:
  - ip camera api authentication
  - camera api basic auth
  - viewtron api login
sidebar_position: 1
---

# Authentication

All API requests must be authenticated using **Basic Access Authentication** ([RFC 2617](https://datatracker.ietf.org/doc/html/rfc2617)). Include the `Authorization` header with every request.

## How It Works

Combine the username and password with a colon separator, then Base64-encode the result:

```
admin:123456 → Base64 → YWRtaW46MTIzNDU2
```

Include the encoded string in the `Authorization` header:

```http
POST http://192.168.0.50/GetDeviceInfo HTTP/1.1
Authorization: Basic YWRtaW46MTIzNDU2
```

## Unauthenticated Requests

A request without valid credentials returns:

```http
401 Unauthorized
WWW-Authenticate: Basic realm="XXXXXX"
```

## Python Example

```python
import requests
from requests.auth import HTTPBasicAuth

response = requests.get(
    "http://192.168.0.50/GetDeviceInfo",
    auth=HTTPBasicAuth("admin", "123456")
)
print(response.text)
```

## curl Example

```bash
curl -u admin:123456 http://192.168.0.50/GetDeviceInfo
```

## Using the Viewtron Python SDK

The [Viewtron Python SDK](/docs/getting-started/python-sdk) (`pip install viewtron`) handles authentication automatically. The `ViewtronCamera` client includes Basic Auth with every request, and the `ViewtronServer` handles inbound webhook events from cameras.

## Notes

- The default username is `admin`. The default password is set during initial camera setup.
- **v2.0 devices** also support Digest Authentication, but Basic Auth works on all firmware versions.
- For production deployments, always change the default password using the [ModifyPassword](/docs/api-reference/security/modify-password) endpoint.
- Use HTTPS when available to protect credentials in transit.
