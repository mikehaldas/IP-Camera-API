"""
Viewtron IP Camera API Client — manages sessions and provides simple methods
for camera configuration and plate database management.

viewtron.py handles INBOUND events (camera sends HTTP POST to your server).
viewtron_client.py handles OUTBOUND calls (your app sends commands to the camera).

Usage:
    from viewtron_client import ViewtronCamera

    camera = ViewtronCamera("192.168.0.20", "admin", "password")
    camera.login()

    # Plate management
    plates = camera.get_plates()
    camera.add_plate("ABC123", owner="Mike", list_type="whiteList")
    camera.delete_plate(key_id=1775415327)

    # Device info
    info = camera.get_device_info()

You can find Viewtron IP cameras at https://www.Viewtron.com
"""

import hashlib
import requests
import xmltodict
import re


class ViewtronCamera:
    """Client for Viewtron IP camera API with automatic session management."""

    def __init__(self, host, username, password, port=80):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.base_url = f"http://{host}:{port}" if port != 80 else f"http://{host}"
        self.session_id = None
        self.token = None

    # ========================= SESSION MANAGEMENT =========================

    def login(self):
        """Authenticate with the camera. Called automatically on first API call."""
        # Step 1: Request login to get session ID and nonce
        req_xml = (
            f'<?xml version="1.0" encoding="utf-8"?>'
            f'<config><userName>{self.username}</userName></config>'
        )
        resp = self._post_raw("/ReqLogin_I", req_xml)
        parsed = xmltodict.parse(resp)
        config = parsed.get('config', {})

        if config.get('@status') != 'success':
            raise ConnectionError(f"ReqLogin failed: {resp}")

        req_session = self._extract_cdata(config.get('sessionId', ''))
        nonce = self._extract_cdata(config.get('nonce', ''))

        # Step 2: Compute hash — SHA512( MD5(password).upper() + nonce )
        md5_upper = hashlib.md5(self.password.encode()).hexdigest().upper()
        hash_token = hashlib.sha512((md5_upper + nonce).encode()).hexdigest()

        # Step 3: DoLogin
        login_xml = (
            f'<?xml version="1.0" encoding="UTF-8"?>'
            f'<config version="1.7" xmlns="http://www.ipc.com/ver10">'
            f'<Authentication type="authenticationMode">Token</Authentication>'
            f'<username type="string"><![CDATA[{self.username}]]></username>'
            f'<password type="string"><![CDATA[{hash_token}]]></password>'
            f'</config>'
            f'<sessionId type="string"><![CDATA[{req_session}]]></sessionId>'
        )
        resp = self._post_raw("/DoLogin_I", login_xml)
        parsed = xmltodict.parse(resp)
        config = parsed.get('config', {})

        if config.get('@status') != 'success':
            error = config.get('@errorCode', 'Unknown error')
            raise ConnectionError(f"DoLogin failed: {error}")

        self.session_id = self._extract_cdata(config.get('sessionId', ''))
        self.token = self._extract_cdata(config.get('token', ''))
        return True

    def logout(self):
        """End the session."""
        if self.session_id:
            try:
                self._post_authenticated("/DoLogout_I", "<config></config>")
            except Exception:
                pass
            self.session_id = None
            self.token = None

    def _ensure_session(self):
        """Login if not already authenticated."""
        if not self.session_id or not self.token:
            self.login()

    def _post_raw(self, endpoint, body):
        """Send a raw POST without session auth."""
        resp = requests.post(
            f"{self.base_url}{endpoint}",
            data=body.encode('utf-8'),
            headers={
                'Content-Type': 'text/plain;charset=UTF-8',
            },
            cookies={'Secure': '', 'lang_type': 'en-us'},
            timeout=10,
        )
        return resp.text

    def _post_authenticated(self, endpoint, config_xml):
        """Send a POST with session ID and token appended after </config>."""
        self._ensure_session()
        body = (
            f'{config_xml}'
            f'<sessionId type="string"><![CDATA[{self.session_id}]]></sessionId>'
            f'<token type="string"><![CDATA[{self.token}]]></token>'
        )
        resp = self._post_raw(endpoint, body)

        # If auth failed (Unauthorized or session expired error 499), re-login and retry
        if 'Unauthorized' in resp or 'errorCode="499"' in resp:
            self.login()
            body = (
                f'{config_xml}'
                f'<sessionId type="string"><![CDATA[{self.session_id}]]></sessionId>'
                f'<token type="string"><![CDATA[{self.token}]]></token>'
            )
            resp = self._post_raw(endpoint, body)

        return resp

    @staticmethod
    def _extract_cdata(value):
        """Extract text from xmltodict parsed CDATA or dict values."""
        if value is None:
            return ''
        if isinstance(value, dict):
            return str(value.get('#text', '') or value.get('value', '') or '').strip()
        return str(value).strip()

    # ========================= DEVICE INFO =========================

    def get_device_info(self):
        """Get camera device information using session auth."""
        config_xml = '<?xml version="1.0" encoding="UTF-8"?><config></config>'
        resp = self._post_authenticated("/GetDeviceInfo_I", config_xml)
        parsed = xmltodict.parse(resp)
        info = parsed.get('config', {}).get('deviceInfo', {})
        return {k: self._extract_cdata(v) for k, v in info.items()}

    # ========================= PLATE DATABASE =========================

    def get_plates(self, list_type="allList", page=0, page_size=10):
        """Query the plate database.

        Args:
            list_type: "allList", "whiteList", "blackList", or "strangerList"
            page: Page index (0-based)
            page_size: Results per page

        Returns:
            List of plate dicts with keys: key_id, plate_number, begin_time,
            end_time, owner, list_type, plate_color, plate_type, telephone
        """
        config_xml = (
            f'<?xml version="1.0" encoding="UTF-8"?>'
            f'<config>'
            f'<searchFilter>'
            f'<pageIndex type ="unit32">{page}</pageIndex>'
            f'<pageSize>{page_size}</pageSize>'
            f'<listType>{list_type}</listType>'
            f'<carPlateNum></carPlateNum>'
            f'</searchFilter>'
            f'<dataSensitive type="dataFlag">sensitive</dataSensitive>'
            f'</config>'
        )
        resp = self._post_authenticated("/GetVehiclePlate_I", config_xml)
        # xmltodict can't handle the namespace prefix cleanly, strip it
        resp_clean = re.sub(r' xmlns="[^"]*"', '', resp)
        parsed = xmltodict.parse(resp_clean)
        config = parsed.get('config', {})
        plates_info = config.get('vehiclePlates', {})

        items = plates_info.get('item', [])
        if not isinstance(items, list):
            items = [items] if items else []

        plates = []
        for item in items:
            plates.append({
                'key_id': int(self._extract_cdata(item.get('keyId', '0'))),
                'plate_number': self._extract_cdata(item.get('carPlateNumber', '')),
                'begin_time': self._extract_cdata(item.get('beginTime', '')),
                'end_time': self._extract_cdata(item.get('endTime', '')),
                'owner': self._extract_cdata(item.get('carOwner', '')),
                'list_type': self._extract_cdata(item.get('plateItemType', '')),
                'plate_color': self._extract_cdata(item.get('carPlateColor', '')),
                'plate_type': self._extract_cdata(item.get('carPlateType', '')),
                'telephone': self._extract_cdata(item.get('telephone', '')),
            })

        return plates

    def add_plate(self, plate_number, owner="", list_type="whiteList",
                  begin_time="2020/01/01 00:00:00", end_time="2030/12/31 23:59:59",
                  telephone=""):
        """Add a plate to the database.

        Args:
            plate_number: The license plate (e.g., "ABC123")
            owner: Vehicle owner name
            list_type: "whiteList" or "blackList"
            begin_time: Start of valid period (YYYY/MM/DD HH:MM:SS)
            end_time: End of valid period (YYYY/MM/DD HH:MM:SS)
            telephone: Owner phone number

        Returns:
            True if successful
        """
        config_xml = (
            f'<?xml version="1.0" encoding="UTF-8"?>'
            f'<config>'
            f'<vehiclePlates type="list" count="1">'
            f'<item>'
            f'<carPlateNumber type="string"><![CDATA[{plate_number}]]></carPlateNumber>'
            f'<beginTime type="string"><![CDATA[{begin_time}]]></beginTime>'
            f'<endTime type="string"><![CDATA[{end_time}]]></endTime>'
            f'<carOwner type="string"><![CDATA[{owner}]]></carOwner>'
            f'<plateItemType type="string">{list_type}</plateItemType>'
            f'<telephone type="string"><![CDATA[{telephone}]]></telephone>'
            f'</item>'
            f'</vehiclePlates>'
            f'</config>'
        )
        resp = self._post_authenticated("/AddVehiclePlate_I", config_xml)
        if 'errorCode' in resp:
            parsed = xmltodict.parse(resp)
            error = parsed.get('config', {}).get('@errorCode', 'Unknown')
            raise RuntimeError(f"AddVehiclePlate failed: {error}")
        return True

    def delete_plate(self, key_id):
        """Delete a plate by its key ID.

        Args:
            key_id: The keyId from get_plates() results

        Returns:
            True if successful
        """
        config_xml = (
            f'<?xml version="1.0" encoding="UTF-8"?>'
            f'<config>'
            f'<vehiclePlates>'
            f'<keyList type="list" count="1">'
            f'<item><keyId type="unit32">{key_id}</keyId></item>'
            f'</keyList>'
            f'<listType>allList</listType>'
            f'<carPlateNum><![CDATA[]]></carPlateNum>'
            f'</vehiclePlates>'
            f'</config>'
        )
        resp = self._post_authenticated("/DeleteVehiclePlate_I", config_xml)
        if 'errorCode' in resp:
            parsed = xmltodict.parse(resp)
            error = parsed.get('config', {}).get('@errorCode', 'Unknown')
            raise RuntimeError(f"DeleteVehiclePlate failed: {error}")
        return True

    def delete_plates(self, key_ids):
        """Delete multiple plates by key IDs.

        Args:
            key_ids: List of keyId values from get_plates() results

        Returns:
            True if successful
        """
        items = ''.join(f'<item><keyId type="unit32">{kid}</keyId></item>' for kid in key_ids)
        config_xml = (
            f'<?xml version="1.0" encoding="UTF-8"?>'
            f'<config>'
            f'<vehiclePlates>'
            f'<keyList type="list" count="{len(key_ids)}">'
            f'{items}'
            f'</keyList>'
            f'<listType>allList</listType>'
            f'<carPlateNum><![CDATA[]]></carPlateNum>'
            f'</vehiclePlates>'
            f'</config>'
        )
        resp = self._post_authenticated("/DeleteVehiclePlate_I", config_xml)
        if 'errorCode' in resp:
            parsed = xmltodict.parse(resp)
            error = parsed.get('config', {}).get('@errorCode', 'Unknown')
            raise RuntimeError(f"DeleteVehiclePlates failed: {error}")
        return True

    def __repr__(self):
        status = "connected" if self.session_id else "disconnected"
        return f"ViewtronCamera({self.host}, {status})"

    def __enter__(self):
        self.login()
        return self

    def __exit__(self, *args):
        self.logout()
