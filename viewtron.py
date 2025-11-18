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
import base64


VT_alarm_types = {
    'MOTION': 'Motion Detection',
    'SENSOR': 'External Sensor',
    'PEA': 'Line Crossing / Intrusion',
    'AVD': 'Exception Detection',
    'OSC': 'Missing Object or Abandoned Object',
    'CDD': 'Crowd Density Detection',
    'VFD': 'Face Detection',
    'VFD_MATCH': 'Face Match',
    'VEHICE': 'License Plate Detection',
    'VEHICLE': 'License Plate Detection',
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


class APIpost:
    def __init__(self, post_body, json):
        self.xml = str(post_body)
        self.json = json
        config = json.get('config', {})

        # === SAFE PARSING ===
        types = config.get('types', {})
        self.alarm_types = types.get('openAlramObj', {})
        self.target_types = types.get('targetType', {})

        device_name = config.get('deviceName', {})
        self.ip_cam = (
            device_name.get('#text') if isinstance(device_name, dict) else
            device_name.get('value') if isinstance(device_name, dict) else
            str(device_name or 'Unknown Camera')
        )

        smart_type = config.get('smartType', {})
        self.alarm_type = (
            smart_type.get('#text') if isinstance(smart_type, dict) else
            smart_type.get('value') if isinstance(smart_type, dict) else
            smart_type.get('@type') if isinstance(smart_type, dict) else
            str(smart_type)
        ).strip()

        self.alarm_description = VT_alarm_types.get(self.alarm_type, 'Unknown Alarm')

        current_time = config.get('currentTime', {})
        time_text = (
            current_time.get('#text') if isinstance(current_time, dict) else
            current_time.get('value') if isinstance(current_time, dict) else
            str(current_time or '')
        )
        try:
            time_val = int(time_text)
            if time_val > 1_000_000_000_000:  # milliseconds
                time_val = time_val // 1000
            self.time_stamp_formatted = dt.fromtimestamp(time_val)
        except:
            self.time_stamp_formatted = dt.now()

    def set_ip_address(self, ip_address):
        self.ip_address = ip_address
        return 1

    def get_ip_address(self):
        return getattr(self, 'ip_address', 'Unknown')

    def get_alarm_types(self):
        return self.alarm_types

    def get_alarm_description(self):
        return self.alarm_description

    def get_target_types(self):
        return self.target_types

    def get_time_stamp_formatted(self):
        return str(self.time_stamp_formatted)

    def get_time_stamp(self):
        return str(int(dt.now().timestamp()))

    def get_ip_cam(self):
        return self.ip_cam

    def get_alarm_type(self):
        return self.alarm_type

    def get_plate_number(self):
        return getattr(self, 'plate_number', '<NO PLATE EXISTS>')

    def source_image_exists(self):
        return getattr(self, 'has_source_image', False) and bool(getattr(self, 'source_image', ''))

    def target_image_exists(self):
        return getattr(self, 'has_target_image', False) and bool(getattr(self, 'target_image', ''))

    def images_exist(self):
        return self.source_image_exists() or self.target_image_exists()

    def get_source_image(self):
        return getattr(self, 'source_image', '') if self.source_image_exists() else None

    def get_target_image(self):
        return getattr(self, 'target_image', '') if self.target_image_exists() else None

    def dump_xml(self):
        print(self.xml)

    def dump_json(self):
        print(self.json)

class CommonImagesLocation(APIpost):
    def __init__(self, post_body):
        self.json = xmltodict.parse(post_body)
        config = self.json.get('config', {})
        list_info = config.get('listInfo', {})
        self.has_source_image = self.has_target_image = False
        self.source_image = self.target_image = ''

        if isinstance(list_info, dict) and list_info.get('@count', '0') != '0':
            item = list_info.get('item', {})
            if isinstance(item, list):
                item = item[0] if item else {}
            target_data = item.get('targetImageData', {})
            length = target_data.get('targetBase64Length', {})
            length = length.get('#text', '0') if isinstance(length, dict) else str(length)
            if length and int(length) > 0:
                base64_data = target_data.get('targetBase64Data', {}) or target_data.get('sourceBase64Data', {})
                self.target_image = (
                    base64_data.get('#text') if isinstance(base64_data, dict) else
                    base64_data.get('value') if isinstance(base64_data, dict) else
                    str(base64_data)
                ).strip()
                self.has_target_image = bool(self.target_image)

        source_info = config.get('sourceDataInfo', {})
        if source_info:
            base64_data = source_info.get('sourceBase64Data', {})
            self.source_image = (
                base64_data.get('#text') if isinstance(base64_data, dict) else
                base64_data.get('value') if isinstance(base64_data, dict) else
                str(base64_data)
            ).strip()
            self.has_source_image = bool(self.source_image)

        super().__init__(post_body, self.json)


class FaceDetection(CommonImagesLocation, APIpost):
    def __init__(self, post_body):
        super().__init__(post_body)

class IntrusionDetection(CommonImagesLocation, APIpost):
    def __init__(self, post_body):
        super().__init__(post_body)

class IntrusionEntry(CommonImagesLocation, APIpost):
    def __init__(self, post_body):
        super().__init__(post_body)

class IntrusionExit(CommonImagesLocation, APIpost):
    def __init__(self, post_body):
        super().__init__(post_body)

class LoiteringDetection(CommonImagesLocation, APIpost):
    def __init__(self, post_body):
        super().__init__(post_body)

class IllegalParking(CommonImagesLocation, APIpost):
    def __init__(self, post_body):
        super().__init__(post_body)

class VideoMetadata(APIpost):
    def __init__(self, post_body):
        self.json = xmltodict.parse(post_body)
        config = self.json.get('config', {})
        vsd = config.get('vsd', {})
        source_info = vsd.get('sourceDataInfo', {})
        length = source_info.get('sourceBase64Length', {})
        Parsed_length = length.get('#text', '0') if isinstance(length, dict) else str(length)
        if Parsed_length and int(Parsed_length) > 0:
            base64_data = source_info.get('sourceBase64Data', {})
            self.source_image = (
                base64_data.get('#text') if isinstance(base64_data, dict) else
                base64_data.get('value') if isinstance(base64_data, dict) else
                str(base64_data)
            ).strip()
            self.has_source_image = bool(self.source_image)

        target_data = vsd.get('targetImageData', {})
        length = target_data.get('targetBase64Length', {})
        Parsed_length = length.get('#text', '0') if isinstance(length, dict) else str(length)
        if Parsed_length and int(Parsed_length) > 0:
            base64_data = target_data.get('targetBase64Data', {})
            self.target_image = (
                base64_data.get('#text') if isinstance(base64_data, dict) else
                base64_data.get('value') if isinstance(base64_data, dict) else
                str(base64_data)
            ).strip()
            self.has_target_image = bool(self.target_image)

        super().__init__(post_body, self.json)


class LPR(APIpost):
    def __init__(self, post_body):
        self.json = xmltodict.parse(post_body)
        config = self.json.get('config', {})
        list_info = config.get('listInfo', {})
        items = list_info.get('item', [])
        if not isinstance(items, list):
            items = [items] if items else []

        self.has_source_image = self.has_target_image = False
        self.source_image = self.target_image = ''
        self.plate_number = '<NO PLATE>'
        self.confidence = 0

        for idx, item in enumerate(items):
            if not isinstance(item, dict):
                continue

            # Overview image (item 0)
            if idx == 0:
                img_data = item.get('targetImageData', {})
                length_elem = img_data.get('targetBase64Length', {})
                length = length_elem.get('#text') if isinstance(length_elem, dict) else str(length_elem)
                if length and int(length) > 0:
                    base64_elem = img_data.get('targetBase64Data', {})
                    self.source_image = (
                        base64_elem.get('#text') if isinstance(base64_elem, dict) else
                        base64_elem.get('value') if isinstance(base64_elem, dict) else
                        str(base64_elem)
                    ).strip()
                    self.has_source_image = bool(self.source_image)

            # Plate info and image (item 1 or only item)
            if idx == 1 or (idx == 0 and len(items) == 1):
                plate_num = item.get('plateNumber', {})
                self.plate_number = (
                    plate_num.get('#text') if isinstance(plate_num, dict) else
                    plate_num.get('value') if isinstance(plate_num, dict) else
                    str(plate_num)
                ).strip()

                confidence = item.get('confidence', {})
                try:
                    self.confidence = int(
                        confidence.get('#text', '0') if isinstance(confidence, dict) else str(confidence)
                    )
                except:
                    self.confidence = 0

                img_data = item.get('targetImageData', {})
                length_elem = img_data.get('targetBase64Length', {})
                length = length_elem.get('#text') if isinstance(length_elem, dict) else str(length_elem)
                if length and int(length) > 0:
                    base64_elem = img_data.get('targetBase64Data', {})
                    self.target_image = (
                        base64_elem.get('#text') if isinstance(base64_elem, dict) else
                        base64_elem.get('value') if isinstance(base64_elem, dict) else
                        str(base64_elem)
                    ).strip()
                    self.has_target_image = bool(self.target_image)

        # === FALLBACK: some firmware puts overview in sourceDataInfo ===
        if not self.has_source_image:
            source_info = config.get('sourceDataInfo', {})
            if source_info:
                base64_data = source_info.get('sourceBase64Data', {})
                src = (
                    base64_data.get('#text') if isinstance(base64_data, dict) else
                    base64_data.get('value') if isinstance(base64_data, dict) else
                    str(base64_data)
                ).strip()
                if src:
                    self.source_image = src
                    self.has_source_image = True

        super().__init__(post_body, self.json)

    def get_confidence(self):
        return self.confidence
