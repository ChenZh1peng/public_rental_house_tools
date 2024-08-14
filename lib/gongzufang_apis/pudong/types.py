"""types and enums
"""
from enum import Enum, unique

@unique
class HouseTypeNum(Enum):
    """Different types of rooms with vaulse as number string
    """
    YISHI = "1"
    YISHIYITING = "2"
    LIANGSHI = "3"
    LIANGSHIYITING = "4"
    SANSHI = "5"
    SANSHIYITING = "6"
    SISHI = "7"
    WUSHI = "8"

@unique
class HouseTypeLiteral(Enum):
    """Different types of rooms with values as literal strings
    """
    YISHI = "1"
    YISHIYITING = "2"
    LIANGSHI = "3"
    LIANGSHIYITING = "4"
    SANSHI = "5"
    SANSHIYITING = "6"
    SISHI = "7"
    WUSHI = "8"

@unique
class TownshipLiteral(Enum):
    """Different codes of towns with values as literal strings
    """
    UNKNOWN = "未知"
    WEIFANGXINCUN = "潍坊新村街道"
    LUJIAZUI = "陆家嘴街道"
    ZHOUJIADU = "周家渡街道"
    TANGQIAO = "塘桥街道"
    SHANGGANGXINCUN = "上钢新村街道"
    NANMATOULU = "南码头路街道"
    HUDONGXINCUN = "沪东新村街道"
    JINYANGXINCUN = "金杨新村街道"
    YANGJING = "洋泾街道"
    PUXINGLU = "浦兴路街道"
    DONGMINGLU = "东明路街道"
    HUAMU = "花木街道"
    CHUANSHA = "川沙新镇"
    GAOQIAO = "高桥镇"
    BEICAI = "北蔡镇"
    HEQING = "合庆镇"
    TANGZHEN = "唐镇"
    CAOLU = "曹路镇"
    JINQIAO = "金桥镇"
    GAOXING = "高行镇"
    GAODONG = "高东镇"
    ZHANGJIANG = "张江镇"
    SANLIN = "三林镇"
    HUINAN = "惠南镇"
    ZHOUPU = "周浦镇"
    XINCHANG = "新场镇"
    DATUAN = "大团镇"
    KANGQIAO = "康桥镇"
    HANGTOU = "航头镇"
    ZHUQIAO = "祝桥镇"

    def parse_code(code):
        if code == "310115004":
            return TownshipLiteral.WEIFANGXINCUN
        if code == "310115005":
            return TownshipLiteral.LUJIAZUI
        if code == "310115007":
            return TownshipLiteral.ZHOUJIADU
        if code == "310115008":
            return TownshipLiteral.TANGQIAO
        if code == "310115009":
            return TownshipLiteral.SHANGGANGXINCUN
        if code == "310115010":
            return TownshipLiteral.NANMATOULU
        if code == "310115011":
            return TownshipLiteral.HUDONGXINCUN
        if code == "310115012":
            return TownshipLiteral.JINYANGXINCUN
        if code == "310115013":
            return TownshipLiteral.YANGJING
        if code == "310115014":
            return TownshipLiteral.PUXINGLU
        if code == "310115015":
            return TownshipLiteral.DONGMINGLU
        if code == "310115016":
            return TownshipLiteral.HUAMU
        if code == "310115103":
            return TownshipLiteral.CHUANSHA
        if code == "310115104":
            return TownshipLiteral.GAOQIAO
        if code == "310115105":
            return TownshipLiteral.BEICAI
        if code == "310115110":
            return TownshipLiteral.HEQING
        if code == "310115114":
            return TownshipLiteral.TANGZHEN
        if code == "310115117":
            return TownshipLiteral.CAOLU
        if code == "310115120":
            return TownshipLiteral.JINQIAO
        if code == "310115121":
            return TownshipLiteral.GAOXING
        if code == "310115123":
            return TownshipLiteral.GAODONG
        if code == "310115125":
            return TownshipLiteral.ZHANGJIANG
        if code == "310115130":
            return TownshipLiteral.SANLIN
        if code == "310115131":
            return TownshipLiteral.HUINAN
        if code == "310115132":
            return TownshipLiteral.ZHOUPU
        if code == "310115133":
            return TownshipLiteral.XINCHANG
        if code == "310115134":
            return TownshipLiteral.DATUAN
        if code == "310115136":
            return TownshipLiteral.KANGQIAO
        if code == "310115137":
            return TownshipLiteral.HANGTOU
        if code == "310115139":
            return TownshipLiteral.ZHUQIAO
        return TownshipLiteral.UNKNOWN

@unique
class TownshipCode(Enum):
    """Different codes of towns with values as postcode strings
    """
    WEIFANGXINCUN = "310115004"
    LUJIAZUI = "310115005"
    ZHOUJIADU = "310115007"
    TANGQIAO = "310115008"
    SHANGGANGXINCUN = "310115009"
    NANMATOULU = "310115010"
    HUDONGXINCUN = "310115011"
    JINYANGXINCUN = "310115012"
    YANGJING = "310115013"
    PUXINGLU = "310115014"
    DONGMINGLU = "310115015"
    HUAMU = "310115016"
    CHUANSHA = "310115103"
    GAOQIAO = "310115104"
    BEICAI = "310115105"
    HEQING = "310115110"
    TANGZHEN = "310115114"
    CAOLU = "310115117"
    JINQIAO = "310115120"
    GAOXING = "310115121"
    GAODONG = "310115123"
    ZHANGJIANG = "310115125"
    SANLIN = "310115130"
    HUINAN = "310115131"
    ZHOUPU = "310115132"
    XINCHANG = "310115133"
    DATUAN = "310115134"
    KANGQIAO = "310115136"
    HANGTOU = "310115137"
    ZHUQIAO = "310115139"