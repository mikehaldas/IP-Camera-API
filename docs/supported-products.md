---
title: "Supported Products — Viewtron IP Cameras and NVRs"
sidebar_label: "Supported Products"
description: "All Viewtron IP cameras and NVRs support the HTTP API. Browse AI cameras, LPR cameras, face recognition cameras, PTZ cameras, and NVRs with built-in API access."
keywords:
  - viewtron ip camera
  - security camera with api
  - ip camera sdk
  - ndaa compliant camera with api
  - open api security camera
sidebar_position: 2
---

# Supported Products

The Viewtron HTTP API applies to **all Viewtron IP cameras and NVRs** sold by [CCTV Camera Pros](https://www.cctvcamerapros.com). Every product listed below has built-in HTTP API support — no additional software licenses, cloud services, or monthly fees required. All products are NDAA compliant.

## AI Security Cameras

AI-powered IP cameras with built-in human detection, vehicle detection, and smart event webhooks. All AI inference runs on the camera hardware.

**API capabilities:** Intrusion detection, line crossing, people counting, video metadata, real-time traject tracking, snapshot capture, PTZ control (on PTZ models), alarm relay output, webhook event notifications with images.

**[Browse AI Security Cameras →](https://www.cctvcamerapros.com/AI-security-cameras-s/1512.htm)**

---

## License Plate Recognition (LPR) Cameras

Dedicated LPR/ALPR cameras that capture and read license plates with built-in optical character recognition.

**API capabilities:** Plate number extraction via webhook, plate database management (whitelist/blacklist/stranger), Wiegand output for gate access control, vehicle attributes (type, color, brand, model on v2.0), snapshot capture.

**[Browse LPR Cameras →](https://www.cctvcamerapros.com/License-Plate-Recognition-Systems-s/1518.htm)**

---

## Face Recognition Cameras

AI cameras with built-in face detection and facial recognition. Detect faces with attribute extraction (age, sex, glasses, mask) and match against a stored face database.

**API capabilities:** Face detection webhooks with face crop images, face attributes (age, sex, glasses, mask), face sample library management, face match alerts (IPC direct only), snapshot capture.

**[Browse Face Recognition Cameras →](https://www.cctvcamerapros.com/face-recognition-cameras-s/1761.htm)**

---

## PTZ Cameras

Pan-tilt-zoom cameras with optical zoom, motorized movement, preset positions, and cruise tour patrols. Some models include AI auto-tracking.

**API capabilities:** Full PTZ movement control (pan, tilt, zoom, focus, iris), preset save/recall/delete, cruise tour management, AI auto-tracking (on supported models), snapshot capture, all smart detection features.

**[Browse PTZ Cameras →](https://www.cctvcamerapros.com/PTZ-Security-Cameras-s/45.htm)**

---

## IP Camera NVRs

Network video recorders with built-in PoE ports. Record IP cameras, manage AI detection across all channels, and forward alarm events to your server via HTTP POST.

**API capabilities:** Device and channel management, disk status, alarm status across all channels, HTTP POST event forwarding (v2.0 format), virtual alarm triggering, snapshot capture, recorded video playback via RTSP, alarm relay output.

**Key difference from cameras:** NVRs forward events from connected cameras using the v2.0 XML format. They do not support direct `traject` streaming — configure cameras individually for real-time tracking.

**[Browse IP Camera NVRs →](https://www.cctvcamerapros.com/IP-Camera-NVRs-s/1472.htm)**

---

## Which Product Do I Need?

| Use Case | Recommended Product | Key API Feature |
|----------|-------------------|-----------------|
| Human/vehicle detection alerts | [AI Security Camera](https://www.cctvcamerapros.com/AI-security-cameras-s/1512.htm) | [Human Detection](/docs/applications/human-detection-intrusion-api) |
| License plate reading & gate access | [LPR Camera](https://www.cctvcamerapros.com/License-Plate-Recognition-Systems-s/1518.htm) | [LPR API](/docs/applications/license-plate-recognition-camera-api) |
| Face detection & visitor management | [Face Recognition Camera](https://www.cctvcamerapros.com/face-recognition-cameras-s/1761.htm) | [Face Detection API](/docs/applications/face-detection-recognition-api) |
| Remote camera control & monitoring | [PTZ Camera](https://www.cctvcamerapros.com/PTZ-Security-Cameras-s/45.htm) | [PTZ Control API](/docs/applications/ptz-camera-control-api) |
| People counting & traffic analytics | [AI Security Camera](https://www.cctvcamerapros.com/AI-security-cameras-s/1512.htm) | [People Counting API](/docs/applications/people-counting-traffic-analytics-api) |
| Multi-camera recording & event aggregation | [IP Camera NVR](https://www.cctvcamerapros.com/IP-Camera-NVRs-s/1472.htm) | [Webhook Events](/docs/applications/webhook-event-notification-api) |
| Real-time presence tracking & automation | [AI Security Camera](https://www.cctvcamerapros.com/AI-security-cameras-s/1512.htm) | [Real-Time Tracking](/docs/applications/real-time-object-tracking-api) |

## Questions & Development Inquiries

- **Email:** mike@viewtron.com
- **Phone:** 561-433-8488
- **Forum:** [NVR Webhook Setup Guide](https://videos.cctvcamerapros.com/support/topic/setup-nvr-api-webhooks)

Mike Haldas is available for questions, consultation, and custom software development for Viewtron API related projects. Email details about your project to mike@viewtron.com.
