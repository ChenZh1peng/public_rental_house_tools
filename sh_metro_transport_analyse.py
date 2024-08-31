import tomllib
from icecream import ic, install, argumentToString
install()
from lib import Amap
from lib.utils import get_keyword_search_result, check_amap_response_code
import os
import pandas as pd, styleframe
from multiprocessing import freeze_support
from tqdm import tqdm
import json
freeze_support()
import gmplot

targets = {"新金桥路1348号": 60, "芒果广场": 50}

with open("config.toml", "rb") as f:
    configs = tomllib.load(f)

with open("sh_metros.json") as f:
    sh_metros = json.load(f)

metro_stations = {}

for line, stations in sh_metros.items():
    for station in stations:
        station = station+'地铁站'
        if station in metro_stations.keys():
            metro_stations[station].append(line)
        else:
            metro_stations[station] = [line]

key = configs['amap']['key']
if key == '1234567890abcdef1234567890abcdef':
    try:
        key = os.environ['AMAP_KEY']
    except:
        print("\033[91mNo environ named AMAP_KEY")
        print("\033[91m请修改config中的key值或设置环境变量")
        raise Exception("")
    
amap = Amap(key, '021', logger=None)

gmaps = []
zoom = 14
apikey = ""
center_lon = "121.478233"
center_lat = "31.225647"
gmaps.append(gmplot.GoogleMapPlotter(center_lat, center_lon, title="所有平均", zoom=zoom, apikey=apikey, map_type="roadmap", scale_control=True))
for i, target in enumerate(targets.keys()):
    gmaps.append(gmplot.GoogleMapPlotter(center_lat, center_lon, title=target, zoom=zoom, apikey=apikey, map_type="roadmap", scale_control=True))


def get_transport_time(poi1, poi2):
    data_dir = os.path.join(os.getcwd(), "data", "metro")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    filename = 'sh_transport.json'
    file_path = os.path.join(data_dir, filename)

    station_search_result = get_keyword_search_result(amap, poi1, "metro", None)
    station_lon_lat_str = station_search_result['pois'][station_search_result['select']]['location']
    target_search_result = get_keyword_search_result(amap, poi2, "metro", None)
    target_lon_lat_str = target_search_result['pois'][target_search_result['select']]['location']

    name_pair = poi1 + '-' + poi2
    key = station_lon_lat_str + '-' + target_lon_lat_str

    result = {}
    if os.path.exists(file_path) :
        with open(file_path, 'r', encoding="UTF-8") as f:
            result = json.load(f)
    if key in result.keys():
        return result[key][0]

    route_result = amap.transit_integrated_direction_v2(station_lon_lat_str,
                                                    target_lon_lat_str,
                                                    strategy=configs['transport']['strategy'],
                                                    alternative_route=1,
                                                    night_flag=configs['transport']['night'],
                                                    time=configs['transport']['time'],
                                                    show_fields='cost')

    check_amap_response_code(route_result, None)
    
    route_result = route_result['route']['transits']
    if len(route_result) > 0:
        cost_min = int(int(route_result[0]['cost']['duration']) / 60)
    else:
        cost_min = 10

    result[key] = (cost_min, name_pair)

    with open(file_path, 'w', encoding="UTF-8") as f:
            f.writelines(json.dumps(result, ensure_ascii=False, indent=4))

    return cost_min

def min_to_color(min_t, max_t, time, scatter=False):
    # if marker == False, use the continuation colors below
    if not scatter:
        rgb_short = [0, 255, 0]
        rgb_long = [255, 0 , 0]
        l = (time - min_t) / (max_t - min_t)
        r = int(rgb_short[0] + (rgb_long[0] - rgb_short[0]) * l)
        g = int(rgb_short[1] + (rgb_long[1] - rgb_short[1]) * l)
        b = int(rgb_short[2] + (rgb_long[2] - rgb_short[2]) * l)
        # ic(r, g, b)
        r = hex(r)[2:]
        g = hex(g)[2:]
        b = hex(b)[2:]
        r = r if len(r) == 2 else '0' + r
        g = g if len(g) == 2 else '0' + g
        b = b if len(b) == 2 else '0' + b
        # ic(r,g,b)
        return '#'+r+g+b

    # if marker == True, use the scattered colors below
    colors = ['green', 'yellow', 'orange', 'red']
    l = (time - min_t) / (max_t - min_t)
    if l < 0.25:
        return colors[0]
    if l < 0.5:
        return colors[1]
    if l < 0.75:
        return colors[2]
    return colors[3]


# cost_min_dict = {}
cost_min_dict_filtered = {}
for target in targets:
    # cost_min_dict[target] = {}
    cost_min_dict_filtered[target] = {}

for station in tqdm(metro_stations.keys(), total=len(metro_stations), desc="正在获取所有地铁站的通勤时间"):
    for target in targets.keys():
        cost_min = get_transport_time(station, target)
        # cost_min_dict[target][station] = cost_min
        if cost_min <= targets[target]:
            cost_min_dict_filtered[target][station] = cost_min

bounds = {"max":[0], "min":[999]}

for i, target in enumerate(targets.keys()):
    bounds['max'].append(max(cost_min_dict_filtered[target].values()))
    bounds['min'].append(min(cost_min_dict_filtered[target].values()))

bounds['max'][0] = max(bounds['max'])
bounds['min'][0] = min(bounds['min'])

station_mean_time = {}
targets_names = list(targets.keys())
station_intersection = set(cost_min_dict_filtered[targets_names[0]].keys())
# ic(len(station_intersection))
for i in range(1, len(targets_names)):
    station_intersection = station_intersection & set(cost_min_dict_filtered[targets_names[i]].keys())
station_intersection = list(station_intersection)
# ic(len(station_intersection))

target_lons = []
target_lats = []
target_size = 300 # meters
target_alpha = 0.6
target_edge_width = 10 # pixels

for target_ in targets.keys():
    target_lon_lat = get_keyword_search_result(amap, target_, "metro", None)
    target_lon_lat = target_lon_lat['pois'][target_lon_lat['select']]['location'].split(',')
    target_lats.append(float(target_lon_lat[1]))
    target_lons.append(float(target_lon_lat[0]))

for i, target in enumerate(targets.keys()):
    stations_time = cost_min_dict_filtered[target]
    colors = []
    lats = []
    lons = []
    marker = True
    titles = []

    for station, time in stations_time.items():
        if station in station_intersection:
            if station in station_mean_time.keys():
                station_mean_time[station] += time
            else:
                station_mean_time[station] = time
        colors.append(min_to_color(bounds['min'][i+1], bounds['max'][i+1], time, scatter=True))
        station_search_result = get_keyword_search_result(amap, station, "metro", None)
        station_lon_lat = station_search_result['pois'][station_search_result['select']]['location'].split(',')
        lats.append(float(station_lon_lat[1]))
        lons.append(float(station_lon_lat[0]))
        titles.append(station+" "+str(time))
    gmaps[i+1].scatter(target_lats, target_lons, color='cyan', marker=False, size=target_size, edge_width=target_edge_width, fa=target_alpha, ea=1.0)
    gmaps[i+1].scatter(lats, lons, color=colors, marker=marker, title=titles)
    gmaps[i+1].draw(target+'.html')


targets_num = len(targets)
for station in station_mean_time.keys():
    station_mean_time[station] = int(station_mean_time[station] / targets_num)
bounds['max'][0] = max(station_mean_time.values())
bounds['min'][0] = min(station_mean_time.values())
# ic(station_mean_time)
colors = []
lats = []
lons = []
marker = True
titles = []
for station, time in station_mean_time.items():
    colors.append(min_to_color(bounds['min'][0], bounds['max'][0], time, scatter=True))
    station_search_result = get_keyword_search_result(amap, station, "metro", None)
    station_lon_lat = station_search_result['pois'][station_search_result['select']]['location'].split(',')
    lats.append(float(station_lon_lat[1]))
    lons.append(float(station_lon_lat[0]))
    detail = '_'.join([target + ' ' + str(cost_min_dict_filtered[target][station]) for target in targets.keys()])
    titles.append(station+" "+str(time)+ ";" + detail)

gmaps[0].scatter(target_lats, target_lons, color='cyan', marker=False, size=target_size, edge_width=target_edge_width, fa=target_alpha, ea=1.0)
gmaps[0].scatter(lats, lons, color=colors, marker=marker, title=titles)
html_name = "-".join(targets.keys()) + '平均.html'
gmaps[0].draw(html_name)