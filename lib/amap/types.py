"""types and enums
"""
from enum import Enum, unique

@unique
class AmapApiKeyType(Enum):
    """Different types of amap's api key 
    """
    ANDROID = 0
    IOS = 1
    JSAPI = 2
    WEB_SERVICE = 3
    SMART_HARDWARE = 4
    WX_MINIAPP = 5
    HARMONY_NEXT = 6
