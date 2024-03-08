"""
A simple HTTP server to integrate with the HTTP Post / XML API of Viewtron IP cameras.
Viewtron IP cameras have the ability to send an HTTP Post to an external server
when an alarm event occurs. Alarm events include human detection, car detection,
face detection / facial recognition, license plate detection / automatic license plate recogition.
All of the server connection information is configured on the Viewtron IP camera.
You can find Viewtron IP cameras at https://www.Viewtron.com
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime as dt
import xmltodict
import base64
import json
import csv

DEBUG = 1 
# set to 1 to print raw HTTP body and JSON conversion

SERVER_PORT = 5002 
# this must match the Server Port specified on the HTTP POST config screen of the IP camera

LPR_POST_URL = '/LPR' 
# this must match the URL specified on the HTTP POST config screen of the IP camera
# you can specify different URLs for different IP cameras, then add the corresponding handler in the server
# For now, I setup / LPR for licesne plate recognition events. Non-LPR events will not have fields
# in their XML response for license plate data, so a special handler is needed for LPR events.

IMG_DIR = '/home/admin/api/images/' 
# don't forget to create this on your file system before running

CSV_FILE = 'alarms.csv'
# each API post will be logged here

class handler(BaseHTTPRequestHandler):

	protocol_version = 'HTTP/1.1'
	# server must use http v1.1 protocol

	def do_GET(self):

		print("GET Request Received\n")
		self.send_response(200)
		self.send_header('Content-type','text/html')
		self.end_headers()
		message = "Hello, World! Here is a GET response"
		self.wfile.write(bytes(message, "utf8"))
		print("GET Request Received")

	def do_POST(self):
		
		print("POST Request Received\n")
		self.send_response(200)
		self.send_header('Content-type','text/html')
		self.end_headers()
		message = "Hello, World! Here is a POST response"
		self.wfile.write(bytes(message, "utf8"))

		content_len = int(self.headers.get('Content-Length'))
		post_body = self.rfile.read(content_len)

		if DEBUG == 1:

			print("BEGIN Raw Body Dump\n")
			print(post_body)
			print("END raw Body Dump\n")

		if ("<?xml" in str(post_body)):

			# convert XML to Python dictionary. Easier to work with
			my_dict = xmltodict.parse(post_body)

			if DEBUG == 1:
				print("Begin JSON Dump\n\n")
				print(json.dumps(my_dict))
				print("End JSON Dump\n\n")

				print("Possible Alarm Types: ")
				print(str(my_dict['config']['types']['openAlramObj']) + "\n")

				print("Possible Target Types: ")
				print(str(my_dict['config']['types']['targetType']) + "\n")

				print("Subscribe Option: ")
				print(str(my_dict['config']['subscribeOption']['#text']) + "\n")
	
			ip_cam = my_dict['config']['deviceName']['#text']
			print("IP Camera Name: " + ip_cam + "\n")

			alarm_type = my_dict['config']['smartType']['#text']
			print("Alarm Type: " + alarm_type + "\n")

			time_stamp = str(my_dict['config']['currentTime']['#text'])
			print("Raw Timestamp in microseconds: " + time_stamp + "\n")

			time_stamp_tr = time_stamp[:10]
			print("Timestamp with microseconds removed: " + time_stamp_tr + "\n")

			time_formatted = dt.fromtimestamp(int(time_stamp_tr))
			print("Timestamp Formatted: " + str(time_formatted) + "\n")

			#  if this is a LPR event, do this
			if self.path == LPR_POST_URL:

				print("Handling LPR request\n")

				plate_number = my_dict['config']['listInfo']['item'][1]['plateNumber']['#text']
				print("Plate Number: " + plate_number + "\n")

				# save plate snapshot
				plate_img_name = time_stamp + ".jpg"
				img_data = base64.b64decode(my_dict['config']['listInfo']['item'][1]['targetImageData']['targetBase64Data']['#text'])
				with open(IMG_DIR + plate_img_name, "wb") as fh:
					fh.write(img_data)

				# save overview snashot
				ov_img_name = time_stamp + "-oview.jpg" 
				img_data = base64.b64decode(my_dict['config']['listInfo']['item'][0]['targetImageData']['targetBase64Data']['#text'])
				with open(IMG_DIR + ov_img_name, "wb") as fh:
					fh.write(img_data)

				# add entry to csv file
				row = [ip_cam, alarm_type, time_formatted, IMG_DIR, plate_img_name, ov_img_name]
				with open(CSV_FILE, 'a', newline='', encoding='utf-8') as csvfile:
					csvwriter = csv.writer(csvfile)
					csvwriter.writerow(row)

		else:
			print("No_XML in POST request")

with HTTPServer(('', SERVER_PORT), handler) as server:
	print("Server Starting...\n")
	try:
		server.serve_forever()
	except KeyboardInterrupt:
		pass
	server.server_close()
	print("Server stopped...\n")

