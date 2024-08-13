import json
import datetime
import os
from .core import Core
from lib.common_types import RequestType

class PudongGZF():
    """浦东公租房接口类
    """

    def __init__(self,
                 timeout=None,
                 logger=None) -> None:
        self._core = Core(timeout=timeout,
                          logger=logger,)

    def _area_list(self):
        """条件找房-获取完整的可用区域列表（街道、镇）

        Returns:
            str: requests.response.text 详细数据结构见response_sample/area_list.json
        """
        data = dict(orderBy=dict(id='ASC'),
                    pageIndex=0,
                    pageSize=999,
                    where=dict(level=4, parentId="310115"))
        return self._core.request("/api/v1.0/app/gzf/area/list", method=RequestType.POST, data=data)

    def _project_list(self):
        """条件找房-仅获取有可选房源的小区项目列表

        Returns:
            str: requests.response.text 详细数据结构见response_sample/project_list.json
        """
        data= {"QueryJson": {"Type": 1}}
        return self._core.request("/api/v1.0/app/gzf/project/list", method=RequestType.POST, data=data)

    def _house_list(self, keywords="", project_id=None, rent=None, township=None, type_name=None):
        """条件找房-默认获取完整且信息详细的可选房源列表，也可筛选

        Args:
            keywords: str, optional, 房源名关键词
            project_id: int, optional
            rent: str, optional, like "Below1000", "Between1000And1999"
            township: str, optional, like "310115004", use types.TownshipCode enum
            type_name: str, optional, like "1", 房型, use types.HouseTypeNum

        Returns:
            str: dict 详细数据结构见response_sample/house_list.json
        """
        data= {
            "pageIndex": 0,
            "pageSize": 999,
            "where": {
                "keywords": keywords,
                "projectId": project_id,
                "rent": rent,
                "township": township,
                "typeName": type_name,
            }
        }
        return self._core.request("/api/v1.0/app/gzf/house/list", method=RequestType.POST, data=data)

    def _statistic(self):
        """地图找房-可获取到：不完整缺了一部分的area（type=0）；完整的project（type=1，即使无可选房源）；完整但信息简略的house（type=2）

        Returns:
            str: dict 详细数据结构见response_sample/get_statistic_list.json
        """
        data= {"Area": "", "HouseTypeName": "", "Rental": "", "keyword": ""}

        return self._core.request("/api/api/PStruct/GetStatistics", method=RequestType.POST, data=data)
    
    def area_list(self):
        """条件找房-获取完整的可用区域列表（街道、镇）

        Returns:
            str: requests.response.text 详细数据结构见response_sample/area_list.json
        """
        data_dir = os.path.join(os.getcwd(), "data/pudong")
        if not os.path.exists(data_dir):
            os.mkdir(data_dir)
        
        today = str(datetime.date.today())
        filename = "area_" + today + ".json"
        file_path = os.path.join(data_dir, filename)

        if os.path.exists(file_path) :
            with open(file_path, 'r', encoding="UTF-8") as f:
                return json.load(f)
            
        result = self._area_list()
        
        with open(file_path, 'w', encoding="UTF-8") as f:
            f.writelines(json.dumps(result, ensure_ascii=False, indent=4))

        return result

    def project_list(self):
        """条件找房-仅获取有可选房源的小区项目列表

        Returns:
            str: requests.response.text 详细数据结构见response_sample/project_list.json
        """
        data_dir = os.path.join(os.getcwd(), "data/pudong")
        if not os.path.exists(data_dir):
            os.mkdir(data_dir)
        
        today = str(datetime.date.today())
        filename = "project_" + today + ".json"
        file_path = os.path.join(data_dir, filename)

        if os.path.exists(file_path) :
            with open(file_path, 'r', encoding="UTF-8") as f:
                return json.load(f)
            
        result = self._project_list()
        
        with open(file_path, 'w', encoding="UTF-8") as f:
            f.writelines(json.dumps(result, ensure_ascii=False, indent=4))

        return result

    def house_list(self, keywords="", project_id=None, rent=None, township=None, type_name=None):
        """条件找房-默认获取完整且信息详细的可选房源列表，也可筛选

        Args:
            keywords: str, optional, 房源名关键词
            project_id: int, optional
            rent: str, optional, like "Below1000", "Between1000And1999"
            township: str, optional, like "310115004", use types.TownshipCode enum
            type_name: str, optional, like "1", 房型, use types.HouseTypeNum

        Returns:
            str: dict 详细数据结构见response_sample/house_list.json
        """

        data_dir = os.path.join(os.getcwd(), "data/pudong")
        if not os.path.exists(data_dir):
            os.mkdir(data_dir)
        
        today = str(datetime.date.today())
        filename = "house_" + today + ".json"
        file_path = os.path.join(data_dir, filename)

        if os.path.exists(file_path) :
            with open(file_path, 'r', encoding="UTF-8") as f:
                return json.load(f)
            
        result = self._house_list(keywords=keywords, project_id=project_id, rent=rent, township=township, type_name=type_name)
        
        with open(file_path, 'w', encoding="UTF-8") as f:
            f.writelines(json.dumps(result, ensure_ascii=False, indent=4))

        return result

    def statistic(self):
        """地图找房-可获取到：不完整缺了一部分的area（type=0）；完整的project（type=1，即使无可选房源）；完整但信息简略的house（type=2）

        Returns:
            str: dict 详细数据结构见response_sample/get_statistic_list.json
        """

        data_dir = os.path.join(os.getcwd(), "data/pudong")
        if not os.path.exists(data_dir):
            os.mkdir(data_dir)
        
        today = str(datetime.date.today())
        filename = "statistic_" + today + ".json"
        file_path = os.path.join(data_dir, filename)

        if os.path.exists(file_path) :
            with open(file_path, 'r', encoding="UTF-8") as f:
                return json.load(f)
            
        result = self._statistic()
        
        with open(file_path, 'w', encoding="UTF-8") as f:
            f.writelines(json.dumps(result, ensure_ascii=False, indent=4))

        return result