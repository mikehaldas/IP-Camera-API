"""
Viewtron IP Camera API Client — control cameras and manage plate databases
using Basic HTTP authentication.

viewtron.py handles INBOUND events (camera sends HTTP POST to your server).
viewtron_client.py handles OUTBOUND calls (your app sends commands to the camera).

Usage:
    from viewtron_client import ViewtronCamera

    camera = ViewtronCamera("192.168.0.20", "admin", "password")

    # Plate management
    camera.add_plate("ABC1234")
    plates = camera.get_plates()
    camera.modify_plate("ABC1234", owner="Mike", telephone="555-1234")
    camera.delete_plate("ABC1234")

    # Device info
    info = camera.get_device_info()

You can find Viewtron IP cameras at https://www.Viewtron.com
"""

import requests
import xmltodict
import re


class ViewtronCamera:
    """Client for Viewtron IP camera API with Basic HTTP authentication."""

    CONFIG_WRAPPER = '<?xml version="1.0" encoding="UTF-8"?><config version="2.1.0" xmlns="http://www.ipc.com/ver10">{body}</config>'

    def __init__(self, host, username, password, port=80):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.base_url = f"http://{host}:{port}" if port != 80 else f"http://{host}"

    def _post(self, endpoint, body_xml):
        """Send a POST with Basic auth. Returns parsed XML as dict."""
        xml = self.CONFIG_WRAPPER.format(body=body_xml)
        resp = requests.post(
            f"{self.base_url}{endpoint}",
            data=xml.encode("utf-8"),
            headers={"Content-Type": "application/xml"},
            auth=(self.username, self.password),
            timeout=10,
        )
        # Strip namespace for easier parsing
        text = re.sub(r' xmlns="[^"]*"', '', resp.text)
        return xmltodict.parse(text)

    def _check_error(self, parsed, operation):
        """Check parsed response for errors. Raises RuntimeError on failure."""
        config = parsed.get("config", {})
        error_code = config.get("@errorCode", "0")
        if error_code != "0":
            error_desc = config.get("@errorDesc", "Unknown error")
            raise RuntimeError(f"{operation} failed: {error_desc} (code {error_code})")

    # ========================= DEVICE INFO =========================

    def get_device_info(self):
        """Get camera device information.

        Returns:
            dict with keys like 'deviceName', 'model', 'firmwareVersion', etc.
        """
        resp = requests.get(
            f"{self.base_url}/GetDeviceInfo",
            auth=(self.username, self.password),
            timeout=10,
        )
        text = re.sub(r' xmlns="[^"]*"', '', resp.text)
        parsed = xmltodict.parse(text)
        info = parsed.get("config", {}).get("deviceInfo", {})
        return {k: str(v.get("#text", v) if isinstance(v, dict) else v).strip()
                for k, v in info.items()}

    # ========================= PLATE DATABASE =========================

    def add_plate(self, plate_number, group_id="1"):
        """Add a plate to the camera database.

        Args:
            plate_number: The license plate (e.g., "ABC1234")
            group_id: Group ID ("1" = default/allow list)

        Returns:
            True if successful
        """
        body = (
            f'<licensePlates type="list" maxCount="100" count="1">'
            f"<item>"
            f"<index>1</index>"
            f"<licensePlateNumber><![CDATA[{plate_number}]]></licensePlateNumber>"
            f"<groupId><![CDATA[{group_id}]]></groupId>"
            f"</item>"
            f"</licensePlates>"
        )
        parsed = self._post("/AddLicensePlates", body)
        # Check per-item error code
        config = parsed.get("config", {})
        reply = config.get("licensePlatesReply", {})
        item = reply.get("item", {})
        if isinstance(item, list):
            item = item[0]
        error_code = item.get("errorCode", {})
        code = error_code.get("#text", str(error_code)) if isinstance(error_code, dict) else str(error_code)
        if code != "0":
            raise RuntimeError(f"AddLicensePlates failed: error code {code}")
        return True

    def add_plates(self, plate_numbers, group_id="1"):
        """Add multiple plates to the camera database.

        Args:
            plate_numbers: List of plate strings
            group_id: Group ID ("1" = default/allow list)

        Returns:
            True if all successful
        """
        items = ""
        for i, plate in enumerate(plate_numbers, 1):
            items += (
                f"<item>"
                f"<index>{i}</index>"
                f"<licensePlateNumber><![CDATA[{plate}]]></licensePlateNumber>"
                f"<groupId><![CDATA[{group_id}]]></groupId>"
                f"</item>"
            )
        body = f'<licensePlates type="list" maxCount="100" count="{len(plate_numbers)}">{items}</licensePlates>'
        parsed = self._post("/AddLicensePlates", body)
        self._check_error(parsed, "AddLicensePlates")
        return True

    def get_plates(self, max_results=50, offset=1, group_id="1"):
        """Query the plate database.

        Args:
            max_results: Maximum plates to return
            offset: Starting position (1-based — first plate is offset 1)
            group_id: Group ID to query

        Returns:
            List of plate dicts with keys: plate_number, group_id,
            begin_time, end_time, owner, telephone
        """
        body = (
            f"<searchFilter>"
            f"<maxResult>{max_results}</maxResult>"
            f"<resultOffset>{offset}</resultOffset>"
            f"<groupId><![CDATA[{group_id}]]></groupId>"
            f"</searchFilter>"
        )
        parsed = self._post("/GetLicensePlates", body)
        config = parsed.get("config", {})

        # Check for "Resources Not Exist" (empty database)
        if config.get("@errorCode") == "20":
            return []

        plates_info = config.get("licensePlates", {})
        items = plates_info.get("item", [])
        if not isinstance(items, list):
            items = [items] if items else []

        plates = []
        for item in items:
            def extract(val):
                if isinstance(val, dict):
                    return str(val.get("#text", "") or val.get("value", "")).strip()
                return str(val).strip() if val else ""

            plates.append({
                "plate_number": extract(item.get("licensePlateNumber", "")),
                "group_id": extract(item.get("groupId", "")),
                "begin_time": extract(item.get("beginTime", "")),
                "end_time": extract(item.get("endTime", "")),
                "owner": extract(item.get("carOwner", "")),
                "telephone": extract(item.get("telephone", "")),
            })

        return plates

    def modify_plate(self, plate_number, group_id="1", owner=None, telephone=None):
        """Update an existing plate's details.

        Args:
            plate_number: Plate to modify (must already exist)
            group_id: Group the plate belongs to
            owner: New owner name (optional)
            telephone: New phone number (optional)

        Returns:
            True if successful
        """
        fields = (
            f"<licensePlateNumber><![CDATA[{plate_number}]]></licensePlateNumber>"
            f"<groupId><![CDATA[{group_id}]]></groupId>"
        )
        if owner is not None:
            fields += f'<carOwner type="string"><![CDATA[{owner}]]></carOwner>'
        if telephone is not None:
            fields += f'<telephone type="string"><![CDATA[{telephone}]]></telephone>'

        body = f"<licensePlate>{fields}</licensePlate>"
        parsed = self._post("/ModifyLicensePlate", body)
        self._check_error(parsed, "ModifyLicensePlate")
        return True

    def delete_plate(self, plate_number, group_id="1"):
        """Delete a plate from the database.

        Args:
            plate_number: Plate to delete
            group_id: Group the plate belongs to

        Returns:
            True if successful
        """
        body = (
            f"<deleteAction>"
            f"<licensePlateNumber><![CDATA[{plate_number}]]></licensePlateNumber>"
            f"<groupId><![CDATA[{group_id}]]></groupId>"
            f"</deleteAction>"
        )
        parsed = self._post("/DeleteLicensePlate", body)
        self._check_error(parsed, "DeleteLicensePlate")
        return True

    def __repr__(self):
        return f"ViewtronCamera({self.host})"
