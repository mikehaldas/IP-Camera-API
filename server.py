"""
A simple HTTP server to integrate with the HTTP Post / XML API of Viewtron IP cameras.
Viewtron IP cameras have the ability to send an HTTP Post to an external server
when an alarm event occurs. Alarm events include human detection, car detection,
face detection / facial recognition, license plate detection / automatic license plate recogition.
All of the server connection information is configured on the Viewtron IP camera.
You can find Viewtron IP cameras at https://www.Viewtron.com.
Contact mike@cctvcamerapros.net for questions.
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime as dt
from viewtron import * 
import xmltodict
import subprocess
import base64
import requests
import json
import csv

# will document Zapier integration soon.
#ZAPIER_URL = 'https://hooks.zapier.com/'
SEND_ZAP = 0

DEBUG = 0 
# set to 1 to print raw XML from HTTP body, JSON conversion, and dump XML to a file

SERVER_PORT = 5002 
# this must match the Server Port specified on the HTTP POST config screen of the IP camera

KEEP_ALIVE_URL = '/SendKeepalive'
DUMP_POST_URL = '/DUMP' 

API_POST_URL = '/API'
# API_POST_URL is used to process all IP Camera API events

CSV_FILE = '/home/admin/api/events.csv'
# all events eccept for LPR events will be logged here.

IMG_DIR = '/home/admin/api/images/' 
# don't forget to create this on your file system before running

class handler(BaseHTTPRequestHandler):

	# server must use http v1.1 protocol
	protocol_version = 'HTTP/1.1'

	def do_GET(self):

		print("GET Request Received\n")
		self.send_response(200)
		self.send_header('Content-type','text/html')
		self.end_headers()
		message = "Thank you for the GET."
		self.wfile.write(bytes(message, "utf8"))

	def do_POST(self):
		
		print("POST Request Received\n")
		self.send_response(200)
		self.send_header('Content-type','text/html')
		self.end_headers()
		message = "Thank you for the POST."
		self.wfile.write(bytes(message, "utf8"))

		content_len = int(self.headers.get('Content-Length'))
		post_ip = self.headers.get('Host')
		post_body = self.rfile.read(content_len)

		if DEBUG == 1 or self.path == DUMP_POST_URL:

			print("BEGIN Raw Body Dump\n")
			print(post_body)
			print("END raw Body Dump\n")

		if ("<?xml" in str(post_body)):

			# convert XML to Python dictionary. Easier to work with.
			my_dict = xmltodict.parse(post_body)

			alarm_type = my_dict['config']['smartType']['#text']
			print("Alarm Type: " + alarm_type + "\n")

			class_lookup = { 
				'VFD': {'class' : FaceDetection },
				'VSD': {'class' : VideoMetadata },
				'VEHICE': {'class' : LPR },
				'PEA': {'class' : IntrusionDetection }
			}

			VT = class_lookup[alarm_type]['class'](post_body)
			VT.set_ip_address(post_ip)

			print("IP Camera Name: " + VT.get_ip_cam() + "\n")
			print("Alarm Type: " + VT.get_alarm_type() + "\n")
			print("Timestamp Formatted: " + str(VT.get_time_stamp_formatted()) + "\n")

			if self.path == DUMP_POST_URL:
				print("Post Body Dumped. Nothing else to do.")

			elif self.path == API_POST_URL:

				if DEBUG == 1:
					with open("post.xml", "a") as xmlfile:
						xmlfile.write(str(post_body))
						xmlfile.write("-------END------\n\n\n\n")

				# Do snapshot images exist? Some API posts do not contain images.
				# They are used to track the location of objects that are detected during the same alarm event.
				if VT.has_images == True:
					print("YES! Snapshots exist in the post")

					# turn on light that is connected to Raspberry Pi. Comment out if not using a RPi.
					subprocess.Popen(["/usr/bin/python3", "/home/admin/api/relay.py"])

					# save overview snapshot
					ov_img_name = VT.get_time_stamp() + "-overview.jpg"
					img_data = base64.b64decode(VT.get_source_image())
					with open(IMG_DIR + ov_img_name, "wb") as fh:
						fh.write(img_data)

					# save cropped image snapshot
					target_img_name = VT.get_time_stamp() + "-target.jpg"
					img_data = base64.b64decode(VT.get_target_image())
					with open(IMG_DIR + target_img_name, "wb") as fh:
						fh.write(img_data)

					# add entry to csv file
					row = [VT.get_ip_cam(), VT.get_ip_address(),  VT.get_alarm_type(), VT.get_alarm_description(), VT.get_plate_number(), VT.get_time_stamp_formatted(), IMG_DIR + target_img_name, IMG_DIR + ov_img_name]
					with open(CSV_FILE, 'a', newline='', encoding='utf-8') as csvfile:
						csvwriter = csv.writer(csvfile)
						csvwriter.writerow(row)

					if SEND_ZAP:
						print("Sending data to Zapier\n")
						zap_data = {'camera_name': VT.get_ip_cam(), 'plate_number': VT.get_plate_number(), 'time_stamp': VT.get_time_stamp_formatted()}
						response = requests.post(
							ZAPIER_URL, data=json.dumps(zap_data),
							headers={'Content-Type': 'application/json'}
						)
						if response.status_code != 200:
							raise ValueError( 
								'Request to Zapier returned an error %s, the response is:\n%s'
								% (response.status_code, response.text)
						)
		else:
			print("No_XML in POST request")
	
with HTTPServer(('', SERVER_PORT), handler) as server:
	print("Server Starting on port " + str(SERVER_PORT))
	try:
		server.serve_forever()
	except KeyboardInterrupt:
		pass
	server.server_close()
	print("Server stopped...\n")

