import tomllib
import logging
import os
import styleframe.utils
from tqdm import tqdm
import json
import styleframe
import pandas as pd
import datetime
from icecream import ic, install
install()
from lib import Amap, PudongGZF
from lib.gongzufang_apis.pudong.types import TownshipLiteral
from sys import exit
# for pyinstaller compatibility
import cmath, mmap
# fix error when using pyinstaller for macos with tqdm
from multiprocessing import freeze_support

freeze_support()

def check_amap_response_code(result):
    if result['status'] != '1' or result['infocode'] != '10000':
        if result['infocode'] == '10001':
            logger.error(f"amap search result error: infocode: {result['infocode']}; status: {result['status']}, info:{result['info']}")
            print("\033[91m请检查高德地图key是否有效")
            raise Exception("请检查高德地图key是否有效")
        elif result['infocode'] == '10003':
            logger.error(f"amap search result error: infocode: {result['infocode']}; status: {result['status']}, info:{result['info']}")
            print("\033[91m高德访问量超出日限制，请明日再试")
            raise Exception("高德访问量超出日限制，请明日再试")
        elif result['infocode'] == '10021':
            logger.error(f"amap search result error: infocode: {result['infocode']}; status: {result['status']}, info:{result['info']}")
            print("\033[91m高德地图并发过大")
            raise Exception("高德地图并发过大")
        elif result['infocode'] == '10013':
            logger.error(f"amap search result error: infocode: {result['infocode']}; status: {result['status']}, info:{result['info']}")
            print("\033[91m高德地图key被删除，请更换")
            raise Exception("高德地图key被删除，请更换")
        else:
            logger.error(f"amap search result error: infocode: {result['infocode']}; status: {result['status']}, info:{result['info']}")
            print("\033[91m高德地图搜索接口返回信息出错")
            raise Exception("amap search result error")

try:
    with open("config.toml", "rb") as f:
        configs = tomllib.load(f)

    level = logging.INFO
    try:
        level_str = os.environ['LOG_LEVEL']
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
    log_path = os.path.join(log_dir, 'transport_analyse.log')

    logging.basicConfig(filename=log_path,
                        level=level,
                        filemode='a',
                        format="%(asctime)s - %(process)s - %(levelname)s - %(message)s")

    logger = logging.getLogger("transport_analyse")

    key = configs['amap']['key']
    if key == '1234567890abcdef1234567890abcdef':
        try:
            key = os.environ['AMAP_KEY']
        except:
            print("\033[91mNo environ named AMAP_KEY")
            print("\033[91m请修改config中的key值或设置环境变量")
            raise Exception("")
        
    amap = Amap(key, '021', logger=logger)

    pudong = PudongGZF(logger=logger)

    if configs['transport']['all'] == 1:
        projects = list(filter(lambda x: x['Type'] == 1, pudong.statistic()['Data']['Lst']))
    elif configs['transport']['all'] == 0:
        projects = pudong.project_list()['data']['data']
    else:
        logger.error(f"transport.all in config should not be {configs['transport']['all']}")
        print("\033[“all”字段值只能为0或1")
        raise ValueError(f"transport.all in config should not be {configs['transport']['all']}")

    poi_infos = []

    def get_keyword_search_result(keyword):
        """get result from file cache or amap api

        Args:
            keyword (str): keyword to search for

        Raises:
            Exception: request fail

        Returns:
            dict: result with a idx called 'select' indicates with poi to select
        """
        data_dir = os.path.join(os.getcwd(), "data", "pudong")
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        filename = keyword + '.json'
        file_path = os.path.join(data_dir, filename)

        if os.path.exists(file_path) :
            with open(file_path, 'r', encoding="UTF-8") as f:
                return json.load(f)
        
        result = amap.search_poi_v2(keywords=keyword, region='021', city_limit=True, show_fields='navi', page_size=5)

        check_amap_response_code(result)
        
        result = {
            'select': 0,
            "pois": result['pois']
        }

        with open(file_path, 'w', encoding="UTF-8") as f:
                f.writelines(json.dumps(result, ensure_ascii=False, indent=4))

        return result

    def convert_segments(amap_segments_list):
        """convert amap segments list structure to a paragraph of description.

        Args:
            amap_segments_list (list): amap transit direction api's responsive segment list

        Returns:
            str: description of segments

        """
        return_string = ""
        idx = 0
        for segment in amap_segments_list:
            means = segment.keys()
            for mean in means:
                idx += 1
                if mean == "walking":
                    return_string += f"{str(idx)}. 步行{segment[mean]['distance']}米，用时{str(int(int(segment[mean]['cost']['duration'])/60))}分钟； \n"
                elif mean == "bus":
                    for line in segment[mean]['buslines']:
                        return_string += f"{str(idx)}. 乘{line['name']}从{line['departure_stop']['name']}到{line['arrival_stop']['name']}，共{int(line['via_num'])+1}站，用时{str(int(int(line['cost']['duration'])/60))}分钟； \n"
                elif mean == "taxi":
                    return_string += f"{str(idx)}. 打的到{segment[mean]['endname']}， {float(segment[mean]['distance']) / 1000.}公里，用时{str(int(int(segment[mean]['drivetime'])/60))}分钟，花费约{segment[mean]['price']}元;\n"
                else:
                    logger.error(f"Unknown segment type: {mean}")
                    print("\033[91m高德公交路径规划返回了新的类型，请联系作者。")
                    raise ValueError("Unknown segment type")


        return return_string

    for poi_name, time_limit in zip(configs['transport']['poi'], configs['transport']['time_limit']):

        poi_info = {"search_keyword": poi_name, "time_limit": time_limit}

        amap_search_result = get_keyword_search_result(poi_name)
        poi_result = amap_search_result['pois'][amap_search_result['select']]

        poi_info.update({
            "lon_lat_str": poi_result['navi']['entr_location'] or poi_result['navi']['exit_location'] or poi_result['location'],
            "name": poi_result['name'],
        })

        poi_infos.append(poi_info)

    transport_time_results = []

    class ContinueProjectLoop(Exception):
        pass

    # using tqdm causes pyinstaller (target macos arm64 platform) packed executive becoming multi-processed and running unproperly
    for n, project in tqdm(enumerate(projects), 
                        total=len(projects),
                        desc="正在计算所有可选小区项目的通勤情况"):
    # for n, project in enumerate(projects):
    #     print(f"!!!{n}")
        try:
            each_project_result = {
                'name': None,
                'town': None,
                'pois': []
            }

            # processing each project's name, town name, and coordinates
            lon_lat_pair = []
            if configs['transport']['all'] == 1:
                lon_lat_pair.append(project["LNG"])
                lon_lat_pair.append(project['LAT'])
                each_project_result['name'] = project['Name']
                each_project_result['town'] = TownshipLiteral.parse_code(project['Parentid']).value
            elif configs['transport']['all'] == 0:
                lon_lat_pair.append(project["longitude"])
                lon_lat_pair.append(project['latitude'])
                each_project_result['name'] = project['name']
                each_project_result['town'] = project['townshipName']
            else:
                logger.error(f"transport.all in config should not be {configs['transport']['all']}")
                print("\033[“all”字段值只能为0或1")
                raise ValueError(f"transport.all in config should not be {configs['transport']['all']}")

            # fix pudong gzf's stupid error aboud coordinates and assemble the lon-lat string asked by amap
            # sometimes wront data presents with LAT, LNG as null, while Parentid is empty string
            fuck_stupid_staff = False  # 🖕🖕🖕
            if lon_lat_pair[0] == None or lon_lat_pair[1] == None:
                fuck_stupid_staff = True
            # sometimes they swap the longitude and latitude by mistake
            if (30.5 < lon_lat_pair[0] < 32.) and (120.5 < lon_lat_pair[1] < 122.5):
                lon_lat_pair[0], lon_lat_pair[1] = lon_lat_pair[1],lon_lat_pair[0]
                # though flag is False, still fuck stupid staff
            # sometimes lon and lat is set to 0
            if not (30.5 < lon_lat_pair[1] < 32.) or not (120.5 < lon_lat_pair[0] < 122.5):
                fuck_stupid_staff = True
            if fuck_stupid_staff:
                # 　　　　　　   ／¯)
                # 　　　　　　 ／ ／
                # 　　　　　  ／ ／
                # 　　　_／¯／  ／'¯ )
                # 　　／／ ／  ／  ／ ('＼
                # 　（（ （　（  （　 ） )
                # 　　＼　　　　  ＼／ ／
                # 　　  ＼　　　　　  ／
                # 　　　 ＼　　　　 ／
                # 　　　　＼　　　 ＼ /
                logger.warning(f"公租房官方数据有误，使用高德数据，建议在官网确认该小区的有效性：{each_project_result['name']}")
                print(f"\033[33m提醒：公租房官方数据有误，使用高德数据，建议在官网确认该小区的有效性：{each_project_result['name']}\033[0m")

                amap_search_result = get_keyword_search_result(each_project_result['name'])
                LON_LAT_STR = amap_search_result['pois'][amap_search_result['select']]['location']
            else:
                LON_LAT_STR = str(lon_lat_pair[0]) + ',' + str(lon_lat_pair[1])

            for poi in poi_infos:
                route_result = amap.transit_integrated_direction_v2(LON_LAT_STR,
                                                                    poi['lon_lat_str'],
                                                                    strategy=configs['transport']['strategy'],
                                                                    alternative_route=1,
                                                                    night_flag=configs['transport']['night'],
                                                                    time=configs['transport']['time'],
                                                                    show_fields='cost')
                check_amap_response_code(route_result)
                
                route_result = route_result['route']['transits'][0]

                each_poi_result = {}
                each_poi_result.update(poi)

                each_poi_result['cost_min'] = int(int(route_result['cost']['duration']) / 60)
                each_poi_result['cost_fee'] = route_result['cost']['transit_fee']
                each_poi_result['walk_distance'] = route_result['walking_distance']
                each_poi_result['segments_description'] = convert_segments(route_result['segments'])

                if poi['time_limit'] >= 0 and each_poi_result['cost_min'] > poi['time_limit']:
                    logger.info(f"通勤时间({each_poi_result['cost_min']}分钟)超出【{poi['name']}】限制, 跳过：{each_project_result['name']}")
                    print(f"通勤时间({each_poi_result['cost_min']}分钟)超出【{poi['name']}】限制, 跳过：{each_project_result['name']}")
                    raise ContinueProjectLoop
                each_project_result['pois'].append(each_poi_result)
                # time.sleep(0.2)

            transport_time_results.append(each_project_result)
        except ContinueProjectLoop:
            pass

    for project in transport_time_results:
        total_cost_fee = 0
        total_cost_min = 0
        count = 0
        for poi in project['pois']:
            count += 1
            total_cost_fee += float(poi['cost_fee'])
            total_cost_min += poi['cost_min']
        project['total_cost_fee'] = total_cost_fee
        project['total_cost_min'] = total_cost_min
        project['average_cost_fee'] = total_cost_fee / count
        project['average_cost_min'] = total_cost_min / count

    def df_parse(transport_result):
        if len(transport_result) == 0:
            logger.warning("无满足所有筛选条件的房源，请考虑是否适当调整条件。")
            print("\033[33m无满足所有筛选条件的房源，请考虑是否适当调整条件。\033[33m")
            exit(0)
        data = {
            '小区': [],
            '街道': [],
            '总耗时（分钟）': [],
            '总花费（元）': [],
            '平均耗时（分钟）': [],
            '平均花费（元）': [],
        }

        poi_n = len(transport_result[0]['pois'])
        
        for i in range(1, poi_n+1):
            data['目的地关键词'+str(i)] = []
            data['目的地'+str(i)] = []
            data['通勤时间（分钟）'+str(i)] = []
            data['通勤花费（元）'+str(i)] = []
            data['需要步行距离（米）'+str(i)] = []
            data['通勤方案'+str(i)] = []

        for project in transport_result:
            data['小区'].append(project['name'])
            data['街道'].append(project['town'])
            data['总耗时（分钟）'].append(project['total_cost_min'])
            data['总花费（元）'].append(project['total_cost_fee'])
            data['平均耗时（分钟）'].append(project['average_cost_min'])
            data['平均花费（元）'].append(project['average_cost_fee'])

            for i, poi in enumerate(project['pois']):
                data['目的地关键词'+str(i+1)].append(poi['search_keyword'])
                data['目的地'+str(i+1)].append(poi['name'])
                data['通勤时间（分钟）'+str(i+1)].append(poi['cost_min'])
                data['通勤花费（元）'+str(i+1)].append(poi['cost_fee'])
                data['需要步行距离（米）'+str(i+1)].append(poi['walk_distance'])
                data['通勤方案'+str(i+1)].append(poi['segments_description'])

        return pd.DataFrame(data), poi_n

    df, poi_n = df_parse(transport_time_results)

    dt = str(datetime.datetime.now()).replace(' ', '_').replace(':', "-")

    output_root = os.path.join(os.getcwd(), 'result')

    if not os.path.exists(output_root):
        os.makedirs(output_root)

    filename_prefix = "通勤计算结果(全部小区）_" if configs['transport']['all'] == 1 else '通勤计算结果(今日可选小区）_' 
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
    row_style = styleframe.Styler(shrink_to_fit=True,
                            bg_color="#32CD32",
                            horizontal_alignment=styleframe.utils.horizontal_alignments.left,
                            font_size=8)

    sf.apply_headers_style(header_style)
    sf.apply_column_style(sf.columns, content_style)
    bg_colored_indexes = list(range(1,len(sf), 2))
    sf.apply_style_by_indexes(bg_colored_indexes, styler_obj=row_style)

    column_width_dict = {}
    for i in range(1, poi_n+1):
        column_width_dict['通勤方案'+str(i)] = 80

    sf.set_column_width_dict(column_width_dict)

    excel_writer = sf.to_excel(output_path)
    excel_writer.close()

    # df.to_excel(output_path, index=None)

    print("分析完成，结果已导出至result目录下！")
except Exception as e:
    print(f"Exception: {e}")
finally:
    input("按回车键退出")