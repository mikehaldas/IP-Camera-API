# Viewtron IP Camera API Server
A Python HTTP server to integrate with the HTTP Post / XML API of Viewtron IP cameras.

Viewtron IP cameras have an API for software developers to create custom applications, business automation, and home automation.
The IP cameras API can send an HTTP Post with an XML payload to an external server's webhook end point.
The XML payload contains information about the alarm event that the camera detected. This is particularly useful with Viewtron AI security cameras
that perform AI inference on the camera. Certain Viewtron AI camera models support he following AI detected alarm events:
license plate detection, automatic license plate recogition, license plate authorized / not authorized database,
human detection, car detection, perimeter intrusion detection, line crossing detection, face detection / facial recognition.

Please note that only certain models support license plate recongition, face recognition, human and vehicle object detection.
https://www.cctvcamerapros.com/AI-security-cameras-s/1512.htm

## License Plate Capture Video Demo

[![Watch the Video Demo](https://img.youtube.com/vi/aifIKamg-ls/maxresdefault.jpg)](https://www.youtube.com/watch?v=aifIKamg-ls)

Here is video demo of the server recieving HTTP Posts from a Viewtron license plate recognition camera. You can see how the server
writes the event to CSV log file, saves the licese plate images to a directory, and prints the relevant info to the screen. 
The video also shows how to setup the LPR camera's plate detection zone, authorized license plate database, and HTTP Post endpost.

The current version of the server works well in processing Viewtron LPR cameras / license plate recognition events.
It is specifically tested with Viewtron license plate recognition camera model LPR-IP4. It is also important to know
that license plate recognition events are ONLY supported by Viewtron LPR cameras models.
https://www.cctvcamerapros.com/LPR-Camera-p/lpr-ip4.htm

11/23/2025 Update: The server has been updated to support face detection events. Just like LPR events,
face detection events send a snapshot image and a cropped image of the face that was detected which can be saved to disk. 
You can find all of the Viewtron IP cameras that support face detection / facial recognition here.
https://www.cctvcamerapros.com/face-recognition-cameras-s/1761.htm

Human detection / perimeter intrusion, vehicle detection / perimeter intrusion are also now supported. You can use any of these Viewtron IP
cameras for human detection and vehicle detection permiter alarms and line crossing alarms.
https://www.cctvcamerapros.com/AI-security-cameras-s/1512.htm

All of the server connection information is configured on the Viewtron IP camera.
Instructions for IP camera configuration here.
https://videos.cctvcamerapros.com/v/lpr-camera-api.html

You can find all Viewtron security camera system products here.
https://www.Viewtron.com

This IP camera API server was written by Mike Haldas, co-founder of CCTV Camera Pros.
mike@cctvcamerapros.net

Read INSTALL.md for installation instructions. Tested on Ubuntu Linux and Raspberry Pi Raspian OS.
