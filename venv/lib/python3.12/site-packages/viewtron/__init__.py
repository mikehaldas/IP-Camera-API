"""
Viewtron IP Camera Python SDK

Parse inbound alarm events from Viewtron IP cameras and NVRs,
and control cameras via the outbound API.

Inbound events (camera sends HTTP POST to your server):
    from viewtron import LPR, FaceDetection, IntrusionDetection, ...

Outbound API (your app sends commands to the camera):
    from viewtron import ViewtronCamera

Full documentation: https://github.com/mikehaldas/viewtron-python
Product page: https://www.Viewtron.com
"""

# === Inbound event classes (IPC v1.x) ===
from viewtron.events import (
    APIpost,
    LPR,
    FaceDetection,
    IntrusionDetection,
    IntrusionEntry,
    IntrusionExit,
    LoiteringDetection,
    IllegalParking,
    VideoMetadata,
    CommonImagesLocation,
    FaceDetectionImages,
    VT_alarm_types,
)

# === Inbound event classes (NVR v2.0) ===
from viewtron.events import (
    APIpostV2,
    VehicleLPR,
    FaceDetectionV2,
    RegionIntrusion,
    LineCrossing,
    TargetCountingByLine,
    TargetCountingByArea,
    VideoMetadataV2,
    VT_alarm_types_v2,
)

# === Outbound API client ===
from viewtron.client import ViewtronCamera

__version__ = "1.1.0"

__all__ = [
    # IPC v1.x
    "APIpost",
    "LPR",
    "FaceDetection",
    "IntrusionDetection",
    "IntrusionEntry",
    "IntrusionExit",
    "LoiteringDetection",
    "IllegalParking",
    "VideoMetadata",
    "CommonImagesLocation",
    "FaceDetectionImages",
    "VT_alarm_types",
    # NVR v2.0
    "APIpostV2",
    "VehicleLPR",
    "FaceDetectionV2",
    "RegionIntrusion",
    "LineCrossing",
    "TargetCountingByLine",
    "TargetCountingByArea",
    "VideoMetadataV2",
    "VT_alarm_types_v2",
    # Client
    "ViewtronCamera",
]
