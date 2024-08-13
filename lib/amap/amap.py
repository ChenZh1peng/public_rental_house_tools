from .core import Core

class Amap():
    '''
    高德地图接口类，包含所有高德API实现
    '''

    def __init__(self,
                 web_service_key,
                 main_city,
                 timeout=None,
                 logger=None):
        '''传入高德地图相关参数，初始化类

        Args:
            web_service_key: 高德开发平台应用申请的web服务类型key值
            main_city: 高德定义的citycode类型；此类的所有接口关注的默认城市
        '''
        self._core = Core(web_service_key = web_service_key,
                          timeout = timeout,
                          logger = logger)
        self.main_city = main_city

    from .search import search_poi_v2

    from .direction import transit_integrated_direction_v2
