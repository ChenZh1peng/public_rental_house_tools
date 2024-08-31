import tomllib
import logging
from icecream import ic, install, argumentToString
install()
import os
from sys import exit
import requests
from lib import PudongGZF, Amap
from lib.utils import get_keyword_search_result, check_amap_response_code, match_name_token_in_string
from lib.gongzufang_apis.pudong.types import HouseTypeLiteral
import pandas as pd, styleframe
import datetime
from tqdm import tqdm
# fix error when using pyinstaller for macos with tqdm
from multiprocessing import freeze_support

freeze_support()

def push_subscription_message(total_num, houses):
    """send a message to everyone in the config file settings by WxPusher. https://wxpusher.zjiecode.com/docs/#/?id=send-msg
        if needing more apis of WxPusehr, consider use their sdk. https://github.com/wxpusher/wxpusher-client
    Args:
        projects: list of projects to be pushed into message
    """
    if len(houses) == 0:
        message = "<h1 style=\"background-color: #33ff99\">再等等看，好房子会有的！！！🏡🍜🐕🐈🙆‍♂️🙆‍♀️</h1>"
    else:
        message = f"<h1 style=\"background-color: #ff6600\">今日共有{total_num}房源上架，其中你关注的有【{len(houses)}】个🎉🎉</h1><br>"
        for house in houses:
            message += f"<ul style=\"font-size: 1.4rem;\"><li style=\"background-color: #33ff99\">{house['name']}</li><li>门牌号：{house['plate']}</li><li style=\"font-weight:bold\">面积：{house['area']}</li><li>户型：{house['type']}</li><li style=\"font-weight:bold\">租金：{house['rent']}</li><li>朝向：{house['towards']}</li>"
            if 'transport' in house.keys():
                for item in house['transport']:
                    message += f"<li>{item['name']}：{item['cost_min']}</li>"
            message += "</ul><br>"

    res = requests.post("https://wxpusher.zjiecode.com/api/send/message", json={
        "appToken": globals()['wx_pusher_token'],
        "content": message,
        "summary": "快来看看今天有哪些好房子:)" if len(houses) > 0 else "啊噢，今天没有好房子:(",
        "contentType": 2,
        # "topicIds": [],
        "uids": globals()['configs']['wx_pusher']['uid'],
        # "url": "",
        "verifyPayType": 0
    })
    if res.status_code != 200:
        globals()['logger'].error(f"Request to wxpusher's response code is not 200: {res.content}")
        exit(-1)
    res = res.json()
    if res['code'] != 1000:
        globals()['logger'].error(f"Failed to send message to wxpusher: {res['msg']}")
        exit(-1)
    for each_res in res['data']:
        if each_res['code'] != 1000:
            globals()['logger'].error(f"Failed to send message to user of {each_res['uid']} with message: {each_res['status']}")

# print json detail of requests' response
@argumentToString.register(requests.Response)
def _(obj):
    return f"requests' response: {obj.json()}"

# logger initialization
level = logging.INFO
try:
    level_str = os.environ['LOG_LEVEL']
    print(level_str)
    if level_str == 'error':
        level = logging.ERROR
    elif level_str == 'warning':
        level = logging.WARNING
    elif level_str == 'info':
        level = logging.INFO
    elif level_str == 'critical':
        level = logging.CRITICAL
    elif level_str == 'debug':
        level = logging.DEBUG
    else:
        logging.critical(f"Unknown log level: {level_str}")
except KeyError:
    pass

log_dir = os.path.join(os.getcwd(), 'log')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
log_path = os.path.join(log_dir, 'project_subscription.log')

logger = logging.getLogger("project_subscription")
logger.setLevel(level)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)
file_handler = logging.FileHandler(filename=log_path, mode='a',encoding='utf8')
file_handler.setLevel(level)
file_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
logger.addHandler(file_handler)

# load configuration
with open("config.toml", "rb") as f:
    configs = tomllib.load(f)

# get today's house details
pudong = PudongGZF(logger=logging)
houses = pudong.house_list()['data']['data']

# process result list
result = []
for sub_name in configs['subscription']['pudong']['house']:
    for house in houses:
        if match_name_token_in_string(sub_name, house['fullName']) or match_name_token_in_string(sub_name, house['project']['name']):
            result.append({
                "name": house['fullName'],
                "towards": house['toward'] or "未知",
                "plate": house['name'] or "未知",
                "type": HouseTypeLiteral.parse_code(house['typeName']).value or "未知",
                "rent": house['rent'] or "未知",
                "area": house['area'] or "未知"
            })
# amap init
key = configs['amap']['key']
if key == '1234567890abcdef1234567890abcdef':
    try:
        key = os.environ['AMAP_KEY']
    except:
        print("\033[91mNo environ named AMAP_KEY")
        print("\033[91m请修改config中的key值或设置环境变量")
        raise Exception("")
    
amap = Amap(key, '021', logger=logger)

# process transport time
pois = []
for poi_name in configs['transport']['poi']:

    poi_info = {"search_keyword": poi_name}

    amap_search_result = get_keyword_search_result(amap, poi_name, logger, sub_dir='pudong')
    poi_result = amap_search_result['pois'][amap_search_result['select']]

    poi_info.update({
        "lon_lat_str": poi_result['navi']['entr_location'] if 'entr_location' in poi_result['navi'].keys() else poi_result['navi']['exit_location'] if 'exit_location' in poi_result['navi'].keys() else poi_result['location'],
    })

    pois.append(poi_info)

for item in tqdm(result, total=len(result), desc="正在处理今日关注房源"):
    item_search_result = get_keyword_search_result(amap, item['name'], logger, sub_dir='pudong')
    item_search_result = item_search_result['pois'][item_search_result['select']]
    item_lon_lat_str = item_search_result['navi']['entr_location'] if 'entr_location' in item_search_result['navi'].keys() else item_search_result['navi']['exit_location'] if 'exit_location' in item_search_result['navi'].keys() else item_search_result['location']
    for poi in pois:
        route_result = amap.transit_integrated_direction_v2(item_lon_lat_str,
                                                            poi['lon_lat_str'],
                                                            strategy=configs['transport']['strategy'],
                                                            alternative_route=1,
                                                            night_flag=configs['transport']['night'],
                                                            time=configs['transport']['time'],
                                                            show_fields='cost')
        check_amap_response_code(route_result, logger)
        
        route_result = route_result['route']['transits'][0]
        cost_min = int(int(route_result['cost']['duration']) / 60)
        if not 'transport' in item.keys():
            item['transport'] = []
        item['transport'].append({"name": poi['search_keyword']+'通勤(分钟)', "cost_min": cost_min})

# push or save results
# save .xlsx table
if configs['subscription']['mode'] == 0 or configs['subscription']['mode'] == 2:
    if len(result) == 0:
        logger.info("今日无订阅的房源上新，跳过结果生成。")
    else:
        def df_parse(result_list):
            data = {
                '房源': [],
                '门牌号': [],
                '面积': [],
                '户型': [],
                '租金': [],
                '朝向': [],
            }
            if 'transport' in result_list[0].keys():
                for item in result_list[0]['transport']:
                    data[item['name']] = []
            for house in result_list:
                data['房源'].append(house['name'])
                data['门牌号'].append(house['plate'])
                data['面积'].append(house['area'])
                data['户型'].append(house['type'])
                data['租金'].append(house['rent'])
                data['朝向'].append(house['towards'])
                if 'transport' in result_list[0].keys():
                    for item in house['transport']:
                        data[item['name']].append(item['cost_min'])
            return pd.DataFrame(data)
        df = df_parse(result)
        dt = str(datetime.datetime.now()).replace(' ', '_').replace(':', "-")
        output_root = os.path.join(os.getcwd(), 'result')
        if not os.path.exists(output_root):
            os.makedirs(output_root)
        filename_prefix = "今日关注房源日报"
        output_path = os.path.join(output_root, filename_prefix + dt +'.xlsx')

        sf = styleframe.StyleFrame(df)

        header_style = styleframe.Styler(
            bg_color="yellow",
            bold=True,
            font_size=12,
            horizontal_alignment=styleframe.utils.horizontal_alignments.center,
            vertical_alignment=styleframe.utils.vertical_alignments.center,
        )
        content_style = styleframe.Styler(
            shrink_to_fit=True,
            font_size=8,
            horizontal_alignment=styleframe.utils.horizontal_alignments.left,
        )
        bold_column_style = styleframe.Styler(
            bold=True
        )
        row_style = styleframe.Styler(shrink_to_fit=True,
                                bg_color="#32CD32",
                                horizontal_alignment=styleframe.utils.horizontal_alignments.left,
                                font_size=8)

        sf.apply_headers_style(header_style)
        sf.apply_column_style(sf.columns, content_style)
        sf.apply_column_style(["面积", "租金"], bold_column_style)
        bg_colored_indexes = list(range(1,len(sf), 2))
        sf.apply_style_by_indexes(bg_colored_indexes, styler_obj=row_style)

        excel_writer = sf.to_excel(output_path)
        excel_writer.close()

        # df.to_excel(output_path, index=None)

        print("今日订阅完成，结果已导出至result目录下！")

# wxpusher
if configs['subscription']['mode'] == 1 or configs['subscription']['mode'] == 2:
    wx_pusher_token = configs['wx_pusher']['token']
    if wx_pusher_token == "":
        wx_pusher_token = os.getenv('WX_PUSHER_TOKEN')
    if wx_pusher_token == None:
        logger.critical("请设置subscription.toml/wx_pusher中的token，或环境变量WX_PUSHER_TOKEN")
        exit(-1)
    push_subscription_message(len(houses), result)

