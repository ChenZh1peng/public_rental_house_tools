"""common utility functions
"""
import os, json

def join_url(url1, url2):
    """合并url的两部分，主要处理两部分中间的 /

    Args:
        url1 (str): url前半部分，如"https://a.b.com"
        url2 (str): url后半部分，如"/api/user/get"
    """
    url1_suffix_slash = url1[-1] == '/'
    url2_prefix_slash = url2[0] == '/'
    if  (not url1_suffix_slash and url2_prefix_slash) or \
        (url1_suffix_slash and not url2_prefix_slash):
        return url1 + url2
    if not url1_suffix_slash and not url2_prefix_slash:
        return url1 + '/' + url2
    if url1_suffix_slash and url2_prefix_slash:
        return url1.rstrip('/') + url2

def get_keyword_search_result(amap, keyword, logger=None):
        """get result from file cache or amap api

        Args:
            keyword (str): keyword to search for

        Raises:
            Exception: request fail

        Returns:
            dict: result with a idx called 'select' indicates with poi to select
        """
        # for safety of name becomming part of path
        keyword = keyword.replace('/', '_')
        data_dir = os.path.join(os.getcwd(), "data", "pudong")
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        filename = keyword + '.json'
        file_path = os.path.join(data_dir, filename)

        if os.path.exists(file_path) :
            with open(file_path, 'r', encoding="UTF-8") as f:
                return json.load(f)
        
        result = amap.search_poi_v2(keywords=keyword, region='021', city_limit=True, show_fields='navi', page_size=5)

        check_amap_response_code(result, logger)
        
        result = {
            'select': 0,
            "pois": result['pois']
        }

        with open(file_path, 'w', encoding="UTF-8") as f:
                f.writelines(json.dumps(result, ensure_ascii=False, indent=4))

        return result

def check_amap_response_code(result, logger=None):
    if result['status'] != '1' or result['infocode'] != '10000':
        if result['infocode'] == '10001':
            if logger:
                logger.error(f"amap search result error: infocode: {result['infocode']}; status: {result['status']}, info:{result['info']}")
            print("\033[91m请检查高德地图key是否有效")
            raise Exception("请检查高德地图key是否有效")
        elif result['infocode'] == '10003':
            if logger:
                logger.error(f"amap search result error: infocode: {result['infocode']}; status: {result['status']}, info:{result['info']}")
            print("\033[91m高德访问量超出日限制，请明日再试")
            raise Exception("高德访问量超出日限制，请明日再试")
        elif result['infocode'] == '10021':
            if logger:
                logger.error(f"amap search result error: infocode: {result['infocode']}; status: {result['status']}, info:{result['info']}")
            print("\033[91m高德地图并发过大")
            raise Exception("高德地图并发过大")
        elif result['infocode'] == '10013':
            if logger:
                logger.error(f"amap search result error: infocode: {result['infocode']}; status: {result['status']}, info:{result['info']}")
            print("\033[91m高德地图key被删除，请更换")
            raise Exception("高德地图key被删除，请更换")
        else:
            if logger:
                logger.error(f"amap search result error: infocode: {result['infocode']}; status: {result['status']}, info:{result['info']}")
            print("\033[91m高德地图搜索接口返回信息出错")
            raise Exception("amap search result error")
        
def match_name_token_in_string(name: str, string: str) -> bool: 
    """break name into tokens by some rules, then tell if all tokens shows up in the string
    """
    word_list = []
    token_list = []
    # break by breakers
    breakers = ["(", ")", "（", "）", "/", "\\", "-", "_", "-", "—", "[", "]", "【", "】", "弄", "号", " ", "\t"]

    temp_str = ""
    for char in name:
        if char in breakers:
            if temp_str != "":
                word_list.append(temp_str)
                temp_str = ""
        else:
            temp_str += char
    if temp_str != "":
        word_list.append(temp_str)
    # break by number/character difference
    temp_str = ""
    numbers = '0123456789'
    last = -1 # -1: initial state, 0: last character is numeric, 1: last character is a non-numeric character
    for word in word_list:
        for char in word:
            if last == -1:
                if char in numbers:
                    last = 0
                else:
                    last = 1
                temp_str += char
            else:
                if char in numbers and last != 0:
                    token_list.append(temp_str)
                    temp_str = char
                    last = 0
                    continue
                if char not in numbers and last != 1:
                    token_list.append(temp_str)
                    temp_str = char
                    last = 1
                    continue
                temp_str += char
        last = -1
        token_list.append(temp_str)
        temp_str = ""
    
    # check every token
    for token in token_list:
        if token not in string:
            return False
    return True

if __name__ == "__main__":
    from icecream import ic
    ic(match_name_token_in_string("妙川路800弄（川沙博景苑）", "妙川路800弄（川沙博景苑）/112号/5楼/503"))
    ic(match_name_token_in_string("妙川路800弄（川沙博景苑）", "妙川路800弄（川沙博景苑）"))

