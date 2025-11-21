# IP-Camera-API
A simple HTTP server to integrate with the HTTP Post / XML API of Viewtron IP cameras.

Viewtron IP cameras have the ability to send an HTTP Post to an external server
when an alarm event occurs. This is particularly useful with Viewtron AI security cameras that support 
AI software alarm events like human detection, car detection, face detection / facial recognition, 
license plate detection / automatic license plate recogition.
https://www.cctvcamerapros.com/AI-security-cameras-s/1512.htm

IMPORTANT NOTE: the current version of the server currently only works well with Viewtron LPR cameras / license plate recognition events.
It is specifically tested with Viewtron license plate recognition camera model LPR-IP4.
https://www.cctvcamerapros.com/LPR-Camera-p/lpr-ip4.htm

I will update the server very soon to support Viewtron face detection / facial recognition camera events.
https://www.cctvcamerapros.com/face-recognition-cameras-s/1761.htm

All of the server connection information is configured on the Viewtron IP camera.
Instructions for IP camera configuration here.
https://www.cctvcamerapros.com/IP-Camera-API-s/1767.htm

You can find all Viewtron security camera system products here.
https://www.Viewtron.com

This IP camera API server was written by Mike Haldas, co-founder of CCTV Camera Pros.
mike@cctvcamerapros.net

Read INSTALL.md for installation instructions. Tested on Ubuntu Linux and Raspberry Pi Raspian OS.
