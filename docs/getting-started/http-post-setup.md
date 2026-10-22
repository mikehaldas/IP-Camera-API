---
title: "Enable HTTP POST on Cameras and NVRs"
sidebar_label: "Enable HTTP POST"
description: "Step-by-step guide to enable HTTP POST webhooks on Viewtron IP cameras and NVRs so they send AI detection events to your server."
keywords:
  - enable camera http post
  - viewtron webhook setup
  - ip camera api setup
  - nvr webhook configuration
  - camera http post enable
sidebar_position: 5
---

# Enable HTTP POST on Cameras and NVRs

Before your server can receive AI detection events, you need to enable HTTP POST on the device that will send them. This page walks through the web interface setup for both IP cameras and NVRs.

:::tip Which device should send events?
- **IP Camera (direct)** — camera sends HTTP POST directly to your server. Requires the camera to be on your local network via a PoE switch (not through NVR PoE ports).
- **NVR (forwarded)** — NVR receives events from connected cameras and forwards them to your server. Use this when cameras are connected to the NVR's built-in PoE ports, or when you want a single endpoint for all cameras.
- **Both** — for maximum flexibility, configure the NVR to forward alarm events with images, and configure individual cameras to send `traject` real-time tracking data directly. Your server receives both streams.
:::

---

## IP Camera Setup

### Step 1: Access the Camera Web Interface

Open a web browser and navigate to your camera's IP address. Log in with administrator credentials.

### Step 2: Navigate to HTTP POST Settings

In the left menu, click **Network**. On the Network page, click the **HTTP POST** tab.

On some firmware this screen is labeled **HTTP Notification** instead of **HTTP POST**. For example, on LPR-IP4 firmware 5.3.1 the path is **Config > Network > More... > HTTP Notification** tab, and the page heading reads **Network Advanced**.

At the top of the HTTP Notification page (LPR-IP4 firmware 5.3.1) are three settings:

| Setting | Description |
|---------|-------------|
| **Push Protocol Version** | `V1` or `V2`. Selects the HTTP POST protocol version the camera uses |
| **Push Type** | `Push by Subscription` or `Actively Push` |
| **Subscription Listening Port** | Port number field |

![Navigate to Network > HTTP POST](https://videos.cctvcamerapros.com/wp-content/files/IP-Camera-HTTP-Post.jpg)

### Step 3: Edit the Configuration

The HTTP POST screen shows a table of configured server destinations. Click the **Edit** button to modify the configuration.

Each row in the table shows:

| Column | Meaning |
|--------|---------|
| **Index** | Row number of the server entry |
| **Enable** | Whether this entry is active |
| **IP address/domain**, **Port**, **Path** | Where the camera sends events |
| **Connection Status** | **Online** or **Offline**: whether the camera can reach your server. **Offline** means the server is unreachable or is not acknowledging posts (see [Server Requirements](#server-requirements)) |
| **Connection Type** | Persistent or Non-Persistent connection (LPR-IP4 firmware 5.3.1) |
| **Send heartbeat** | Whether keepalive posts are on |
| **Heartbeat Interval(Second)** | Seconds between keepalives |
| **Smart Alarm Type** | Detection types this entry sends |

The camera supports up to **3 server entries**. Each entry has its own data and alarm type selections, so you can send different events to different servers.

The eye icon next to the **Edit** button shows or hides sensitive data in the table, such as the server address.

![HTTP POST server list with Edit button](https://videos.cctvcamerapros.com/wp-content/files/http-post-server-add.jpg)

After you click **Edit**, the **Add**, **Modify**, **Delete**, and **Test** buttons appear above the table, plus a **Save** button for the page. **Add** opens the **Add HTTP Notification** dialog for a new entry. **Modify** opens **Edit HTTP Notification**, the same form, for the selected entry. Click **Add** to create a new server entry. Fill in your API server details:

![Edit HTTP POST server settings](https://videos.cctvcamerapros.com/wp-content/files/http-post-settings.jpg)

Configure the following settings:

| Setting | Description | Example |
|---------|-------------|---------|
| **Enable** | Check to activate HTTP POST | Checked |
| **Protocol Type** | `http` or `https`. LPR-IP4 firmware 5.3.1 offers `HTTP` only | `http` |
| **HTTP Request Method** | `POST` or `GET` (LPR-IP4 firmware 5.3.1) | `POST` |
| **Domain/IP** | IP address of your API server | `192.168.0.53` |
| **Server Port** | Port your server listens on (1-65535) | `5002` |
| **Path** | URL path for the webhook endpoint | `/API` |
| **User Name / Password** | Optional authentication for your server. Check the **Enable** box to the right of User Name to turn it on | Leave unchecked unless your server requires it |
| **Heartbeat Interval** | Seconds between keepalive messages. Range is 30-120 seconds per the API reference (the web interface shows no range) | `90` |
| **Send heartbeat** | Check to receive periodic keepalive POSTs | Checked |
| **Connection Type** | `Persistent Connection` or `Non-Persistent Connection` (LPR-IP4 firmware 5.3.1) | `Persistent Connection` |

Heartbeats (keepalives) are small periodic POSTs, often with an empty body, that confirm the connection is up while no events occur. Your server must acknowledge each one (see [Server Requirements](#server-requirements)).

The **Push Protocol Version** (V1/V2) selector is at the top of the page, not in this dialog (see Step 2).

### Step 4: Select Smart Alarm Data

Choose what data to include with each event. **Select All** checks every option in this group.

| Option | What It Sends | When to Use |
|--------|--------------|-------------|
| **Alarm status data** | Alarm on/off state changes (~660 bytes) | When you need to know when detection starts and stops |
| **Smart track data** | Continuous real-time target tracking (~1.7 KB at ~7/sec) | When you need live bounding box coordinates for tracking targets across the frame |
| **Smart event data** | Detection event with coordinates (~2-3 KB) | When you need detection events with classification data |
| **Original picture** | Full-frame JPEG snapshot, base64 encoded (~500-530 KB) | When you want an overview image of the scene |
| **Target picture** | Cropped target JPEG, base64 encoded (included in the event post) | When you want a close-up of the detected person, vehicle, or plate |

**Original picture** and **Target picture** are sub-options of **Smart event data**. The images are embedded in the same event post, not sent as separate posts. Each one can be turned off on its own. For example, an LPR camera can send plate events with no images.

:::tip
For most applications, enable **Smart event data** + **Original picture** + **Target picture** to receive complete detection events with images. Add **Smart track data** if you need continuous real-time object tracking (e.g., for PTZ auto-follow or trajectory analysis).
:::

### Step 5: Select Smart Alarm Types

Check which AI detection types should trigger HTTP POST events. **Select All** checks every type.

| Alarm Type | Detection |
|------------|-----------|
| **Region Intrusion** | Person or vehicle enters a defined zone |
| **Line Crossing** | Person or vehicle crosses a virtual tripwire |
| **Region Entrance** | Target enters a zone |
| **Region Exiting** | Target exits a zone |
| **Target Counting by Line** | Count targets crossing a line |
| **Target Counting by Area** | Count targets in a zone |
| **Motion Detection** | Any motion (not AI-filtered) |
| **Video Metadata** | Full-frame object detection data |
| **Loitering Detection** | Person stays in a zone too long |
| **Illegal Parking Detection** | Vehicle parked in a restricted zone |
| **Alarm In** | Physical alarm input (sensor) on the camera |
| **Video Exception** | Abnormal video detection (AVD in the API reference; LPR-IP4 firmware 5.3.1) |
| **License Plate Detection** | License plate read (LPR cameras) |

The alarm type list depends on the camera model and firmware. Only the types your camera supports are shown. For example, LPR-IP4 firmware 5.3.1 offers Motion Detection, Alarm In, Video Exception, and License Plate Detection. The screenshot above shows three of them.

:::note
AI detection rules (intrusion zones, tripwires, etc.) must be configured separately in the camera's **Event** settings before the camera will generate these alarm types. Enabling them here only controls whether events are forwarded via HTTP POST.
:::

### Step 6: Save

Click **Save** to apply the configuration. The camera will begin sending HTTP POST events to your server immediately when detections occur. No reboot is needed.

:::note LPR-IP4 firmware 5.3.1
On LPR-IP4 firmware 5.3.1, saving an entry here also turns on the older V1 HTTP POST sender, aimed at the same host, port, and path. There is no separate V1 switch on the page. In testing, posts arrived in the V1 layout.
:::

---

## NVR Setup

### Step 1: Access the NVR Web Interface

Open a web browser and navigate to your NVR's IP address. Log in with administrator credentials.

### Step 2: Navigate to HTTP POST Settings

Navigate to **Network** in the top menu bar, then click **HTTP POST** in the submenu. In the left sidebar, you'll find it under **Integration** > **HTTP POST**.

The menu name varies by NVR firmware. On some firmware there is no page named HTTP POST. Instead, go to **Function Panel > Event Notification > Alarm Server**, where the page title is **Alarm Server**.

### Step 3: Enable and Configure

Check **Enable** to activate HTTP POST, then enter your server details:

![NVR HTTP POST Configuration](https://videos.cctvcamerapros.com/wp-content/files/IP-Camera-API-NVR-setup.jpg)

| Setting | Description | Example |
|---------|-------------|---------|
| **Server Address** | IP address of your API server | `192.168.0.53` |
| **Port** | Port your server listens on | `5002` |
| **Path** | URL path for the webhook endpoint | `/API` |
| **Protocol** | `HTTP` or `HTTPS` | `HTTP` |
| **Connection** | `Non-Persistent Connection` or `Persistent Connection` | `Non-Persistent Connection` |
| **Anonymous Login** | Check if your server doesn't require authentication | Checked |
| **Username / Password** | Credentials for your server. Available when **Anonymous Login** is unchecked | Blank |
| **Send Heartbeat** | Check to send periodic keepalive POSTs. **Interval Time(s)** is greyed out until this is checked | Unchecked in the screenshot |
| **Interval Time(s)** | Heartbeat interval in seconds (used only when **Send Heartbeat** is checked) | `10` |
| **Schedule** | When to send events (24x7 or custom schedule) | `24x7` |

The **Manage** button next to Schedule opens the schedule window. It has a week grid and presets for 24x7, 24x5, 24x2, and Night.

On NVR firmware that uses the **Alarm Server** page, the fields are: Enable, Server Address, URL (the path), Port, Protocol (`XML`), Send Heartbeat, Interval Time[s] (up to 65535), Schedule with Manage, Alarm Type with **Configure**, Test, and Apply. That page has no Username/Password, Connection, or Attaching Image fields, and no Default button. The **Default** button in the screenshot above appears on other NVR firmware.

### Step 4: Configure Image Options

Under **Attaching Image**, check **Snap** (cropped target) and/or **Original** (full scene). The combinations are:

| Option | What's Sent | Typical Size |
|--------|------------|--------------|
| **Snap + Original** | Cropped target + full scene overview | ~0.5-0.6 MB per event |
| **Original only** | Full scene overview | ~500-530 KB |
| **Snap only** | Cropped target (person/vehicle/plate) | Much smaller than Original |
| **Neither** | Event data only, no images | ~1 KB |

### Step 5: Select Event Types

Click the **Configure** button next to **Event Type** (labeled **Alarm Type** on the Alarm Server page) to open the event selection dialog:

![NVR Event Type Selection](https://videos.cctvcamerapros.com/wp-content/files/IP-Camera-API-enable-events.jpg)

The left **Event** column shows all available event types. The right **Send Event** column shows which events will be forwarded via HTTP POST.

Besides AI detections, the Event list includes NVR system events such as IP Address Conflict, Disk IO Error, Disk Full, Illegal Access, Network Disconnected, No Disk, HDD is pulled out, Disk Failure, and Alarm Server Offline. Use the **`<<`** button to remove an event from the **Send Event** column.

1. Select event types from the left list (e.g., Line Crossing, Region Intrusion, Plate Recognition)
2. Click the **>>** button to move them to the **Send Event** column
3. Click **OK**
4. Click **Apply** on the HTTP POST screen

### Step 6: Test the Connection

If your server is running, click the **Test** button to verify the NVR can reach your server. A successful test confirms network connectivity between the NVR and your application. It does not prove your server acknowledges events and keepalives correctly. See [Server Requirements](#server-requirements).

Like the camera, the NVR starts sending as soon as you click **Apply**. No reboot is needed. The NVR forwards events in the v2.0 XML format and does not send **Smart track data** (traject). That is camera-only.

---

## Server Requirements

The camera or NVR stops sending if your server does not answer correctly. Any server that receives these posts must:

1. **Acknowledge every POST immediately.** This includes empty-body keepalives. Return HTTP 200 with an XML success body *before* parsing the post. If the device does not get this response, it treats the server as unreachable (Connection Status shows **Offline**) and stops sending.
2. **Support HTTP/1.1 persistent connections.** Cameras send `Connection: keep-alive` and hold the TCP connection open. Set your server's keepalive timeout to **60 seconds or more**. For example, the Node.js default of 5 seconds drops the connection between heartbeats.
3. **Handle requests concurrently.** Parsing one camera's large image post must not delay another camera's keepalive acknowledgment.
4. **Treat empty POSTs as keepalives.** Acknowledge them and skip parsing.

The Python server below already does all of this.

---

## Verify Events Are Arriving

The quickest way to verify your setup is to run the Python alarm server from the [GitHub repository](https://github.com/mikehaldas/IP-Camera-API):

```bash
git clone https://github.com/mikehaldas/IP-Camera-API.git
cd IP-Camera-API
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install viewtron
python3 server.py
```

Then trigger a detection event (walk in front of a camera with an intrusion zone configured). You should see event data printed to the console within seconds.

## Troubleshooting

| Problem | Check |
|---------|-------|
| No events received | Is your server listening on the correct port? Can the camera/NVR reach your server's IP? |
| Events arrive but no images | Check image/picture options in the HTTP POST configuration |
| Intermittent events | Check the heartbeat interval — if your server doesn't respond to keepalives, the connection drops |
| Events stop after a few posts, Connection Status shows Offline | Your server is not acknowledging every POST and keepalive with HTTP 200 + XML success, or its keepalive timeout is too short. See [Server Requirements](#server-requirements) |
| Events from camera but not NVR (or vice versa) | Camera direct and NVR forwarded are independent configurations — set up both if you want both |
| AI alarm types not firing | AI detection rules (intrusion zones, tripwires) must be enabled in the camera's Event settings separately |

## Next Steps

- **[Webhook Event Notification API](/docs/applications/webhook-event-notification-api)** — XML format reference, detection types, and code examples for processing events
- **[Authentication](/docs/getting-started/authentication)** — how API request authentication works
- **[Supported Products](/docs/supported-products)** — which cameras and NVRs support HTTP POST
