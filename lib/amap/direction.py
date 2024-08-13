from lib.common_types import RequestType
from .types import AmapApiKeyType

def transit_integrated_direction_v2(self,
                                    origin_str,
                                    destination_str,
                                    city1=None,
                                    city2=None,
                                    origin_poi=None,
                                    destination_poi=None,
                                    ad1=None,
                                    ad2=None,
                                    strategy=0,
                                    alternative_route=5,
                                    multi_export=0,
                                    night_flag=0,
                                    date=None,
                                    time=None,
                                    show_fields=None,
                                    sig=None,
                                    output='json',
                                    callback=None):
    """路线规划2.0——公交线路规划 https://lbs.amap.com/api/webservice/guide/api/newroute

    Args:
        origin_str (str): 起点经纬度；经度在前，纬度在后，经度和纬度用","分割，经纬度小数点后不得超过6位。
        destination_str (str): 目的地经纬度；经度在前，纬度在后，经度和纬度用","分割，经纬度小数点后不得超过6位。
        city1 (str): 起点所在城市；仅支持 citycode，相同时代表同城，不同时代表跨城. 填None时使用self.main_city.
        city2 (str): 目的地所在城市；仅支持 citycode，相同时代表同城，不同时代表跨城. 填None时使用self.main_city.
        origin_poi (str, optional): 起点 POI ID;1、起点 POI ID 与起点经纬度均填写时，服务使用起点 POI ID；2、该字段必须和目的地 POI ID 成组使用。. 
            Defaults to None.
        destination_poi (str, optional): 目的地 POI ID;1、目的地 POI ID 与目的地经纬度均填写时，服务使用目的地  POI ID；2、该字段必须和起点 POI ID 成组使用。. 
            Defaults to None.
        ad1 (str, optional): 起点所在行政区域编码;仅支持 adcode，参考行政区域编码表. Defaults to None.
        ad2 (str, optional): 终点所在行政区域编码;仅支持 adcode，参考行政区域编码表. Defaults to None.
        strategy (int, optional): 公共交通换乘策略
            可选值：
            0：推荐模式，综合权重，同高德APP默认
            1：最经济模式，票价最低
            2：最少换乘模式，换乘次数少
            3：最少步行模式，尽可能减少步行距离
            4：最舒适模式，尽可能乘坐空调车
            5：不乘地铁模式，不乘坐地铁路线
            6：地铁图模式，起终点都是地铁站
            （地铁图模式下 originpoi 及 destinationpoi 为必填项）
            7：地铁优先模式，步行距离不超过4KM
            8：时间短模式，方案花费总时间最少. 
            Defaults to 0.
        alternative_route (int, optional): 返回方案条数;可传入1-10的阿拉伯数字，代表返回的不同条数。. Defaults to 5.
        multi_export (int, optional): 地铁出入口数量
	        0：只返回一个地铁出入口
            1：返回全部地铁出入口. 
            Defaults to 0.
        night_flag (int, optional): 考虑夜班车
            可选值：
            0：不考虑夜班车
            1：考虑夜班车. 
            Defaults to 0.
        date (str, optional): 请求日期;例如:2013-10-28. Defaults to None.
        time (str, optional): 请求时间;例如:9-54. Defaults to None.
        show_fields (str, optional): 返回结果控制
            show_fields 用来筛选 response 结果中可选字段。show_fields 的使用需要遵循如下规则：
            1、具体可指定返回的字段类请见下方返回结果说明中的“show_fields”内字段类型；
            2、多个字段间采用“,”进行分割；
            3、show_fields 未设置时，只返回基础信息类内字段。. 
            Defaults to None.
        sig (str, optional): 数字签名
            请参考 数字签名获取和使用方法(https://lbs.amap.com/faq/account/key/72). 
            Defaults to None.
        output (str, optional): 返回结果格式类型;可选值：JSON. Defaults to 'json'.
        callback (str, optional): 回调函数;callback 值是用户定义的函数名称，此参数只在 output 参数设置为 JSON 时有效。. Defaults to None.
    """
    params = dict(
        origin=origin_str,
        destination=destination_str,
        city1=city1 or self.main_city,
        city2=city2 or self.main_city,
        originpoi=origin_poi,
        destinationpoi = destination_poi,
        ad1 = ad1,
        ad2 = ad2,
        strategy=strategy,
        AlternativeRoute=alternative_route,
        multiexport = multi_export,
        nightflag=night_flag,
        date=date,
        time=time,
        show_fields=show_fields,
        sig=sig,
        output=output,
        callback=callback,
        )
    
    return self._core.request("/v5/direction/transit/integrated", api_type=AmapApiKeyType.WEB_SERVICE, method=RequestType.GET, params=params)