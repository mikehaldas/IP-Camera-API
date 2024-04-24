"""
Abstration layer for Viewtron IP camera API. Transforms XML from 
the HTTP Post from IP cameras to usable objects to build a Python server.
Viewtron IP cameras have the ability to send an HTTP Post to an external server
when an alarm event occurs. Alarm events include human detection, car detection,
face detection / facial recognition, license plate detection / automatic license plate recogition.
All of the server connection information is configured on the Viewtron IP camera.
You can find Viewtron IP cameras at https://www.Viewtron.com
"""

import xmltodict
from datetime import datetime as dt

VT_alarm_types = {
	'MOTION': 'Motion Detection',
	'SENSOR': 'External Sensor',
	'PEA': 'Line Crossing / Intrusion',
	'AVD': 'Exception Detection',
	'OSC': 'Missing Object or Abondonded Object',
	'CDD': 'Crowd Density Detection',
	'VFD': 'Face Detection',
	'VFD_MATCH': 'Face Match',
	'VEHICE': 'License Plate Detection',
	'AOIENTRY': 'Entered Intrusion Zone',
	'AOILEAVE': 'Exited Intrusion Zone',
	'PASSLINECOUNT': 'Line Crossing Target Count',
	'TRAFFIC': 'Intrusion Target Count',
	'FALLING': 'Falling Object Detection',
	'EA': 'Motorcycle / Bicycle Detection',
	'VSD': 'Video Metadata',
	'PVD': 'Illegal Parking Detection'
}

# Base Class
class APIpost():
	def __init__(self, post_body, json):
		self.xml = str(post_body)
		self.json = json

		self.alarm_types = json['config']['types']['openAlramObj']
		self.target_types = json['config']['types']['targetType']

		self.ip_cam = json['config']['deviceName']['#text']
		self.alarm_type = json['config']['smartType']['#text']
		self.alarm_description = VT_alarm_types[json['config']['smartType']['#text']]
		self.time_stamp = json['config']['currentTime']['#text']

		time_stamp_trimmed = self.time_stamp[:10]
		self.time_stamp_formatted = dt.fromtimestamp(int(time_stamp_trimmed))

	def get_alarm_types(self):
		return(self.alarm_types)

	def get_alarm_description(self):
		return(self.alarm_description)

	def get_target_types(self):
		return(self.target_types)

	def get_time_stamp_formatted(self):
		return(str(self.time_stamp_formatted))

	def get_time_stamp(self):
		return(str(self.time_stamp))

	def get_ip_cam(self):
		return(self.ip_cam)

	def get_alarm_type(self):
		return(self.alarm_type)

	def has_images(self):
		return(self.has_images)
		
	def dump_xml(self):
		print(self.xml)

	def dump_json(self):
		print(self.json)

class CommonAPI(APIpost):
	def __init__(self, post_body):
		self.json = xmltodict.parse(post_body)
		if int(self.json['config']['listInfo']['@count']) > 0 and int(self.json['config']['listInfo']['item']['targetImageData']['targetBase64Length']['#text']):
			self.source_image = self.json['config']['sourceDataInfo']['sourceBase64Data']['#text']
			self.target_image = self.json['config']['listInfo']['item']['targetImageData']['targetBase64Data']['#text']
			self.has_images = 1

		else:
			self.source_image = '0'
			self.target_image = '0'
			self.has_images = 0

		# inherit base class
		super().__init__(post_body, self.json)

	def get_source_image(self):
		return(self.source_image)

	def get_target_image(self):
		return(self.target_image)

class FaceDetection(CommonAPI, APIpost):
	def __init__(self, post_body):

		# inherit base class
		super().__init__(post_body)


class IntrusionDetection(CommonAPI, APIpost):
	def __init__(self, post_body):

		# inherit base class
		super().__init__(post_body)

class VideoMetadata(APIpost):
	def __init__(self, post_body):
		self.json = xmltodict.parse(post_body)

		if int(self.json['config']['vsd']['sourceDataInfo']['sourceBase64Length']['#text']) and int(self.json['config']['vsd']['targetImageData']['targetBase64Length']['#text']):
			self.source_image = self.json['config']['vsd']['sourceDataInfo']['sourceBase64Data']['#text']
			self.target_image = self.json['config']['vsd']['targetImageData']['targetBase64Data']['#text']
			self.has_images = 1
		else:
			self.source_image = '0'
			self.target_image = '0'
			self.has_images = 0

		# inherit base class
		super().__init__(post_body, self.json)

	def get_source_image(self):
		return(self.source_image)

	def get_target_image(self):
		return(self.target_image)

class LPR(APIpost):
	def __init__(self, post_body):
		self.json = xmltodict.parse(post_body)

		print("JSON DUMP: " + str(self.json))

		self.plate_number = self.json['config']['listInfo']['item'][1]['plateNumber']['#text']
		self.source_image = self.json['config']['listInfo']['item'][0]['targetImageData']['targetBase64Data']['#text']
		self.target_image = self.json['config']['listInfo']['item'][1]['targetImageData']['targetBase64Data']['#text']
		self.has_images = 1

		# inherit base class
		super().__init__(post_body, self.json)

	def get_plate_number(self):
		return(self.plate_number)

	def get_source_image(self):
		return(self.source_image)

	def get_target_image(self):
		return(self.target_image)

