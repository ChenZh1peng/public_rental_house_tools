import requests as r
from bs4 import BeautifulSoup
from icecream import ic
import json

# url = "https://m.sh.bendibao.com/ditie/linemap.shtml"
# response = r.get(url)
# response.encoding = response.apparent_encoding
# with open('sh_metros_html.txt', 'w') as f:
#     f.write(response.text)
# soup = BeautifulSoup(response.text, 'html.parser')

with open('sh_metros_html.txt', 'r') as f:
    soup =  BeautifulSoup(''.join(f.readlines()), 'html.parser')

result = {}
line_lists = soup.find_all('div', {"class": "line-list"})
for line_list in line_lists:
    line_name = line_list.find('div', {"class": "list-title"}).find('a').getText().rstrip("运营时间").lstrip("地铁")
    stations = [station.getText() for station in line_list.find('ul', {'class':'station-li'}).find_all('a')]
    result[line_name] = stations

with open('sh_metros.json', 'w') as f:
    f.write(json.dumps(result, indent=4, ensure_ascii=False))