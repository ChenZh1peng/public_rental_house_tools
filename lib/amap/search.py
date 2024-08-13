from lib.common_types import RequestType
from .types import AmapApiKeyType
def search_poi_v2(self,
                  keywords=None,
                  types="120000|150000",
                  region=None,
                  city_limit=False,
                  show_fields=None,
                  page_size=10,
                  page_num=1,
                  sig=None,
                  output='json',
                  callback=None):
    """搜索POI 2.0 https://lbs.amap.com/api/webservice/guide/api-advanced/newpoisearch

    Args:
        keywords (str): 地点关键字
            需要被检索的地点文本信息。
            只支持一个关键字 ，文本总长度不可超过80字符
            必填（keyword 或者 types 二选一必填）. 
            Defaults to None.
        types (str, optional): 指定地点类型
            地点文本搜索接口支持按照设定的 POI 类型限定地点搜索结果；地点类型与 poi typecode 是同类内容，可以传入多个 poi typecode，
            相互之间用“|”分隔，内容可以参考 POI 分类码表；地点（POI）列表的排序会按照高德搜索能力进行综合权重排序；
            可选（keyword 或者 types 二选一必填）
            120000（商务住宅）150000（交通设施服务）. 
            Defaults to "120000|150000".
        region (str, optional): 搜索区划
	        增加指定区域内数据召回权重，如需严格限制召回数据在区域内，请搭配使用 city_limit 参数，可输入 citycode，adcode，cityname；
            cityname 仅支持城市级别和中文，如“北京市”。. 
            默认全国范围内搜索
            Defaults to None.
        city_limit (bool, optional): 指定城市数据召回限制
            可选值：true/false
            为 true 时，仅召回 region 对应区域内数据。. 
            Defaults to False.
        show_fields (str, optional): 返回结果控制
            show_fields 用来筛选 response 结果中可选字段。show_fields 的使用需要遵循如下规则：
            1、具体可指定返回的字段类请见下方返回结果说明中的“show_fields”内字段类型；
            2、多个字段间采用“,”进行分割；
            3、show_fields 未设置时，只返回基础信息类内字段。. 
            Defaults to None.
        page_size (int, optional): 当前分页展示的数据条数
            page_size 的取值1-25. 
            Defaults to 10.
        page_num (int, optional): 请求第几分页
            page_num 的取值1-100. 
            Defaults to 1.
        sig (str, optional): 
            请参考 数字签名获取和使用方法(https://lbs.amap.com/faq/account/key/72). 
            Defaults to None.
        output (str, optional): 返回结果格式类型        
            默认格式为 json，目前只支持 json 格式；. 
            Defaults to 'json'.
        callback (str, optional): 回调函数
            callback 值是用户定义的函数名称，此参数只在 output 参数设置为 JSON 时有效。. 
            Defaults to None.
    """

    if not keywords and not types:
        raise ValueError("keywords or types must have at least one be specified")
    
    params = dict(
        keywords = keywords,
        types = types,
        region = region or self.main_city,
        city_limit = city_limit,
        show_fields = show_fields,
        page_size = page_size,
        page_num = page_num,
        sig = sig,
        output = output,
        callback = callback
        )
    
    return self._core.request("/v5/place/text", api_type=AmapApiKeyType.WEB_SERVICE, method=RequestType.GET, params=params)
