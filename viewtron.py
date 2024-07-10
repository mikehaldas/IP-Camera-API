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

# These are all of the alarm types currrently supported by the Viewtron IP camera API
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
	'AOIENTRY': 'Intrusion Zone Entry',
	'AOILEAVE': 'Intrusion Zone Exit',
	'LOITER': 'Loitering Detection',
	'PASSLINECOUNT': 'Line Crossing Target Count',
	'TRAFFIC': 'Intrusion Target Count',
	'FALLING': 'Falling Object Detection',
	'EA': 'Motorcycle / Bicycle Detection',
	'VSD': 'Video Metadata',
	'PVD': 'Illegal Parking'
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

		# Convert the timestamp from microseconds to a formatted date to the second.
		time_stamp_trimmed = self.time_stamp[:10]
		self.time_stamp_formatted = dt.fromtimestamp(int(time_stamp_trimmed))

	def set_ip_address(self, ip_address):
		self.ip_address = ip_address
		return(1)

	def get_ip_address(self):
		return(self.ip_address)

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

	def get_plate_number(self):
		if hasattr(self, 'plate_number'):
			return(self.plate_number)
		else:
			return('<NO PLATE EXISTS>')

	def source_image_exists(self):
		if hasattr(self, 'has_source_image'):
			return(self.has_source_image)
		else:
			return False

	def target_image_exists(self):
		if hasattr(self, 'has_target_image'):
			return(self.has_target_image)
		else:
			return False

	def images_exist(self):
		if hasattr(self, 'has_images'):
			return(self.has_images)
		else:
			return False

	def get_source_image(self):
		if hasattr(self, 'source_image'):
			return(self.source_image)
		else:
			return None

	def get_target_image(self):
		if hasattr(self, 'target_image'):
			return(self.target_image)
		else:
			return None
		
	def dump_xml(self):
		print(self.xml)

	def dump_json(self):
		print(self.json)

# Some alarm types have the target and source image data in the same location in the XML doc
class CommonImagesLocation(APIpost):
	def __init__(self, post_body):
		self.json = xmltodict.parse(post_body)

		if "listInfo" in self.json['config']:
			if int(self.json['config']['listInfo']['@count']) > 0 and int(self.json['config']['listInfo']['item']['targetImageData']['targetBase64Length']['#text']):
				self.target_image = self.json['config']['listInfo']['item']['targetImageData']['targetBase64Data']['#text']
				self.has_target_image = True

		if 'sourceDataInfo' in self.json['config'] and 'sourceBase64Data' in self.json['config']['sourceDataInfo']:
			self.source_image = self.json['config']['sourceDataInfo']['sourceBase64Data']['#text']
			self.has_source_image = True

		# inherit base class
		super().__init__(post_body, self.json)


class FaceDetection(CommonImagesLocation, APIpost):
	def __init__(self, post_body):

		# inherit base class
		super().__init__(post_body)


class IntrusionDetection(CommonImagesLocation, APIpost):
	def __init__(self, post_body):

		# inherit base class
		super().__init__(post_body)

class IntrusionEntry(CommonImagesLocation, APIpost):
	def __init__(self, post_body):

		# inherit base class
		super().__init__(post_body)

class IntrusionExit(CommonImagesLocation, APIpost):
	def __init__(self, post_body):

		# inherit base class
		super().__init__(post_body)

class LoiteringDetection(CommonImagesLocation, APIpost):
	def __init__(self, post_body):

		# inherit base class
		super().__init__(post_body)

class IllegalParking(CommonImagesLocation, APIpost):
	def __init__(self, post_body):

		# inherit base class
		super().__init__(post_body)

class VideoMetadata(APIpost):
	def __init__(self, post_body):
		self.json = xmltodict.parse(post_body)

		if "vsd" in self.json['config'] and int(self.json['config']['vsd']['sourceDataInfo']['sourceBase64Length']['#text']) > 0:
				self.source_image = self.json['config']['vsd']['sourceDataInfo']['sourceBase64Data']['#text']
				self.has_source_image = True

		if "vsd" in self.json['config'] and int(self.json['config']['vsd']['targetImageData']['targetBase64Length']['#text']) > 0:
				self.target_image = self.json['config']['vsd']['targetImageData']['targetBase64Data']['#text']
				self.has_target_image = True

		# inherit base class
		super().__init__(post_body, self.json)

class LPR(APIpost):
	def __init__(self, post_body):
		self.json = xmltodict.parse(post_body)
		self.plate_number = self.json['config']['listInfo']['item'][1]['plateNumber']['#text']
		self.source_image = self.json['config']['listInfo']['item'][0]['targetImageData']['targetBase64Data']['#text']
		self.target_image = self.json['config']['listInfo']['item'][1]['targetImageData']['targetBase64Data']['#text']
		self.has_images = True

		# inherit base class
		super().__init__(post_body, self.json)

