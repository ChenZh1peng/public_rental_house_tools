"""core requests sending module of Amap class
"""
import requests
import json
from lib.utils import join_url
from lib.common_types import RequestType
from .types import AmapApiKeyType

class Core():
    """ 高德地图类，核心请求类
    """
    gateway = "https://restapi.amap.com"

    def __init__(self,
                 web_service_key,
                 timeout=5,
                 logger=None):
        self.web_service_key = web_service_key
        self.timeout = timeout
        self.logger = logger

    def request(self,
                path,
                api_type=AmapApiKeyType.WEB_SERVICE,
                method=RequestType.GET,
                params=None,
                data=None,
                files=None,
                headers={},):

        if self.logger:
            self.logger.debug(f"Request url: {join_url(self.gateway, path)}")
            self.logger.debug(f"Request api type: {api_type}")
            self.logger.debug(f"Request type: {method.value}")
            self.logger.debug(f"Request headers: {headers}")
            self.logger.debug(f"Request params: {params}")
            self.logger.debug(f"Request data: {data}")
        if method == RequestType.GET:
            if api_type == AmapApiKeyType.WEB_SERVICE:
                params.update({"key": self.web_service_key})
            else:
                raise Exception(f"Amap api does not support this key type: {api_type}")
            response = requests.get(url=join_url(self.gateway, path),
                                    headers=headers,
                                    params=params,
                                    timeout=self.timeout)
        else:
            raise Exception(f"Amap api does not support this request method type: {method}")
        if self.logger:
            self.logger.debug(f"Response status code: {response.status_code}")
            self.logger.debug(f"Response headers: {response.headers}")
            self.logger.debug(f"Response content: {response.text}")
        if response.status_code != 200:
            if self.logger:
                self.logger.error(f"Amap response status is not 200 of path: {path}")
            raise Exception(f"Amap response status is not 200 of path: {path}")
        return json.loads(response.text) \
            if 'application/json' in response.headers.get('Content-Type') \
            else response.content
        