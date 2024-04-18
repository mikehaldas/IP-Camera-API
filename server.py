#!/usr/bin/python3
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
import subprocess
import base64
import requests
import json
import csv

# will document Zapier integration soon.
#ZAPIER_URL = ''

DEBUG = 0 
# set to 1 to print raw XML from HTTP body, JSON conversion, and dump XML to a file

SERVER_PORT = 5002 
# this must match the Server Port specified on the HTTP POST config screen of the IP camera

KEEP_ALIVE_URL = '/SendKeepalive'
DUMP_POST_URL = '/DUMP' 
FACE_POST_URL = '/FACE' 
INTRUSION_POST_URL = '/INTRUSION' 

API_POST_URL = '/API'
# API_POST_URL is used for face detection, intrusion detection, line crossing, line counting events

CSV_FILE = 'events.csv'
# all events eccept for LPR events will be logged here.

IMG_DIR = '/home/admin/api/images/' 
# don't forget to create this on your file system before running

LPR_POST_URL = '/LPR' 
# license plate detection events have a different XML structure.
# this must match the URL specified on the HTTP POST config screen of the IP camera.
# you can specify different URLs for different IP cameras, then add the corresponding handler in the server.

PLATE_CSV_FILE = 'plates.csv'
# each License Place recognition API post will be logged here.

PLATE_IMG_DIR = '/home/admin/api/images/plates/' 
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
		post_body = self.rfile.read(content_len)

		if DEBUG == 1 or self.path == DUMP_POST_URL:

			print("BEGIN Raw Body Dump\n")
			print(post_body)
			print("END raw Body Dump\n")

		if ("<?xml" in str(post_body)):

			# convert XML to Python dictionary. Easier to work with.
			my_dict = xmltodict.parse(post_body)

			if DEBUG == 1 or DUMP_POST_URL:

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

			if self.path == DUMP_POST_URL:
				print("Post Body Dumped. Nothing else to do.")

			elif self.path == API_POST_URL:

				# do snapshot images exist?
				if int(my_dict['config']['listInfo']['@count']) > 0 and int(my_dict['config']['listInfo']['item']['targetImageData']['targetBase64Length']['#text']):
					print("Snapshots exist in the post")

					# turn on light that is connected to Raspberry Pi. Will document this soon.
					#subprocess.Popen(["/usr/bin/python3", "/home/admin/api/relay.py"])

					# save overview snapshot
					ov_img_name = time_stamp + "-oview.jpg"
					img_data = base64.b64decode(my_dict['config']['sourceDataInfo']['sourceBase64Data']['#text'])
					with open(IMG_DIR + ov_img_name, "wb") as fh:
						fh.write(img_data)

					# save cropped image snapshot
					img_name = time_stamp + "-event.jpg"
					img_data = base64.b64decode(my_dict['config']['listInfo']['item']['targetImageData']['targetBase64Data']['#text'])
					with open(IMG_DIR + img_name, "wb") as fh:
						fh.write(img_data)

					# add entry to csv file
					row = [ip_cam, alarm_type, time_formatted, IMG_DIR + img_name, IMG_DIR + ov_img_name]
					with open(CSV_FILE, 'a', newline='', encoding='utf-8') as csvfile:
						csvwriter = csv.writer(csvfile)
						csvwriter.writerow(row)

					if DEBUG == 1:
						with open("XML.txt", "a") as xmlfile:
							xmlfile.write("\n____________________BEGIN________________________\n")
							xmlfile.write(str(post_body))
							xmlfile.write("\n______________________END________________________\n")


			#  if this is a LPR event, do this
			elif self.path == LPR_POST_URL:

				print("Handling LPR post\n")

				plate_number = my_dict['config']['listInfo']['item'][1]['plateNumber']['#text']
				print("Plate Number: " + plate_number + "\n")

				# save plate snapshot
				print("Saving plate snapshot\n")
				plate_img_name = time_stamp + ".jpg"
				img_data = base64.b64decode(my_dict['config']['listInfo']['item'][1]['targetImageData']['targetBase64Data']['#text'])
				with open(PLATE_IMG_DIR + plate_img_name, "wb") as fh:
					fh.write(img_data)

				# save overview snashot
				print("Saving overview snapshot\n")
				ov_img_name = time_stamp + "-oview.jpg" 
				img_data = base64.b64decode(my_dict['config']['listInfo']['item'][0]['targetImageData']['targetBase64Data']['#text'])
				with open(PLATE_IMG_DIR + ov_img_name, "wb") as fh:
					fh.write(img_data)

				# add entry to csv file
				print("Adding CSV entry\n")
				row = [ip_cam, alarm_type, time_formatted, plate_number, PLATE_IMG_DIR, plate_img_name, ov_img_name]
				with open(PLATE_CSV_FILE, 'a', newline='', encoding='utf-8') as csvfile:
					csvwriter = csv.writer(csvfile)
					csvwriter.writerow(row)

				if DEBUG == 1:
					with open("XML.txt", "a") as xmlfile:
						xmlfile.write("\n_____________________BEGIN_______________________\n")
						xmlfile.write(str(post_body))
						xmlfile.write("\n______________________END________________________\n")

				# commenting Zapier integration out until I document it. It does work very well.
				#print("Sending data to Zapier\n")
				#zap_data = {'camera_name': ip_cam, 'plate_number': plate_number, 'time_stamp': str(time_formatted)}
				#response = requests.post(
				#	ZAPIER_URL, data=json.dumps(zap_data),
				#	headers={'Content-Type': 'application/json'}
				#)
				#if response.status_code != 200:
				#	raise ValueError( 
				#		'Request to Zapier returned an error %s, the response is:\n%s'
				#		% (response.status_code, response.text)
				#)
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

