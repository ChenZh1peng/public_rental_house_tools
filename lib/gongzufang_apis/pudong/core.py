import requests
from lib.utils import join_url
from lib.common_types import RequestType
from icecream import ic

class Core():

    gateway = "https://select.pdgzf.com"

    def __init__(self,
                 timeout=None,
                 logger=None) -> None:
        self.timeout = timeout
        self.logger = logger

    def request(self,
                path,
                method=RequestType.GET,
                params=None,
                data=None,
                files=None,
                headers={},):
        headers.update({
            "Host": "select.pdgzf.com",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:128.0) Gecko/20100101 Firefox/128.0",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Content-Type": "application/json",
            "token": "OSZKGDQ4NHJISFBE6ARRP3YB1BDLH2XR",
            "GZFAuthentication": None,
            "timestamp": "3S45GVG17CM5CPNYV7HYZ9MLIAX4B445",
            "nonce": "F3ML6T6FEERXA3KZORFOMEYS3WW2BVAH",
            "signature": "9ARSSEDX8CED8M6QWGVWNQ8MP7X8XE5N",
            #"Content-Length": "121",
            "Origin": "https://select.pdgzf.com",
            "Connection": "keep-alive",
            "Referer": "https://select.pdgzf.com/houseLists",
            "Cookie": "SECKEY_ABVK=KWMLm4DltmAUJy2W9u+W9I4thi+ZwjXsGObaIorL/QU%3D; BMAP_SECKEY=KWMLm4DltmAUJy2W9u-W9D5YrgkSZyO-iKFlanRPEaZpHJBhDH30qk8cW-ZxpYjxGCcOlXG7sHXhngKJAXvdmfDIgMheTtpfcUHkNjo2BAstHF3gnuibFUT0t8ja2iB3IDut03Y2RkxzUSu2v_Lol5nDYMOzdmmN6ZJlyQyys8_92zhBN491ra5A1CsMS6v5; LeSoft_V9_LoginUserKey=27CF9DAC4962C155FA5775F6597184221F3DC6A88B0A5DFE1F0D108964411A14011B210609458F3BA010C2449EB88AF522D84ADAD197516C7C1659FD1BDA6D0E1A0B589D1C69BF28A36C54B0435B334E3E7DEC6008D8854514287C1913A04E85EC1FBB1A77E9B9259661560E21D6510389CD7B132A163E6DE2EFDF6BDEEEECBA12254901AF617139415D829779BEDD5231BBFF1D5B531D8467B35F67536D526244A0BAA50D33B1C4D7E1E58F746F9D113E71B97BC3AB76EF890197DD040E6C15DED036F32FAC923FAE29FB6586DE33659D627066BD97B94563A46F83877322B3FCB647890521A46E224EC00C7194FAD70592DB93C4D88AB85EBF8C554FB6FBF49CB4D20AB5B1CD411E1F47316AAF72CD5C9DAF8CA694317D0D54C7EFA65E86297A518A5CAC9196128DE161D672ED2E3D6757E44B00357A2238196BC3A75A30BB0BCFCBEE7FBBBE311C02195DC07F8554EF8B44242551A4999695FF66B472D455E49835A45A9FFD3BC9054DB9CB9F87772CD17831C0462624D663888BB82ED78FDA5F6B693B27154CFDBF18D012323BAD9B8CAED7FBFDF39D1F263B3504D668B3611510C45D1049E9AA6B8BFB58E75189C8883B67D1E1637BA6A11D6B92FA2CFC; JSESSIONID=E45D6E90447803052D83E617553097A7",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache"
            
            })
        if self.logger:
            self.logger.debug(f"Request url: {join_url(self.gateway, path)}")
            self.logger.debug(f"Request type: {method.value}")
            self.logger.debug(f"Request headers: {headers}")
            self.logger.debug(f"Request params: {params}")
            self.logger.debug(f"Request data: {data}")
        if method == RequestType.POST:
            response = requests.post(url=join_url(self.gateway, path),
                                    headers=headers,
                                    json=None if files else data,
                                    # data=data if files else None,
                                    files=files,
                                    timeout=self.timeout)
        else:
            raise Exception(f"Amap api does not support this request method type: {method}")
        if self.logger:
            self.logger.debug(f"Response status code: {response.status_code}")
            self.logger.debug(f"Response headers: {response.headers}")
            self.logger.debug(f"Response content: {response.text}")
        if response.status_code != 200:
            if self.logger:
                self.logger.error(f"PUDONG response status is not 200 of path: {path}")
                raise Exception(f"PUDONG response status is not 200 of path: {path}")
        return response.json() \
            if 'application/json' in response.headers.get('Content-Type') \
            else response.content