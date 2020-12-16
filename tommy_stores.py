import pandas as pd
from pyecharts.charts import *
from pyecharts import options as opts
from pyecharts.commons.utils import JsCode
from pyecharts.globals import ThemeType, ChartType
from bs4 import BeautifulSoup
from pyecharts.render import make_snapshot
from snapshot_selenium import snapshot
from retrying import retry
import random
from pyecharts.datasets.coordinates import get_coordinate, search_coordinates_by_keyword
from pyecharts.components import Image
from pyecharts.options import ComponentTitleOpts
from MyQR import myqr
import os
from pyecharts.datasets import register_url
from pyecharts.faker import Collector, Faker
from pyecharts.datasets import register_url
import json
from collections import Counter
import time

t1 = time.stime()   
with open('E:/splash/tommy/getOfflineStoreListOrParms.json', 'r',encoding='utf-8') as data_file:
    json_data = data_file.read()

data = json.loads(json_data)
# print(data)
# type(data)
provinces_list = []
cities_list = []
store_coord = dict()
shanghai_store_coord = dict()
beijing_store_coord = dict()
t2 = time.time()
print(f'文件加载 耗时{t2-t1}秒')
for i in data:
#     print(i['name'], i['ename2'], i['province'], i['city'], i['district'], i['address'], i['hours'])
#     print('\n')
    if i['province'].startswith('新疆'):
        provinces_list.append('新疆')
    elif i['province'].startswith('宁夏'):
        provinces_list.append('宁夏')
    elif i['province'].startswith('内蒙古'):
        provinces_list.append('内蒙古')
    elif i['province'].startswith('广西'):
        provinces_list.append('广西')      
    if i['city'] == '请选择市/区-':
        i['city'] = i['name'][:2] + '市'
    provinces_list.append(i['province'].replace('省', '').replace('自治区', ''))
    cities_list.append(i['city'])
    store_coord[i['name']] =  [float(h) for h in i['ename2'].split(',')] # 坐标点"121.525051,31.306016" > [121.525051,31.306016]
    shanghai_store_coord[i['name']] =  [float(h) for h in i['ename2'].split(',') if '上海' in i['name']] # 坐标点"121.525051,31.306016" > [121.525051,31.306016]

    if len(shanghai_store_coord[i['name']])==0:
        del shanghai_store_coord[i['name']]

    beijing_store_coord[i['name']] =  [float(h) for h in i['ename2'].split(',') if '北京' in i['name']] # 坐标点"121.525051,31.306016" > [121.525051,31.306016]

    if len(beijing_store_coord[i['name']])==0:
        del beijing_store_coord[i['name']]
t3 = time.time()       
print(f'数据处理耗时{t3-t2}秒')
print(store_coord)
with open('E:/splash/tommy/city_stores.json', 'w', encoding='utf8') as json_file:
    json.dump(store_coord, json_file, ensure_ascii=False, indent=4, sort_keys=True)

                
type(Counter(provinces_list))
# TommyHifilger全国分布图
area_data = (dict(Counter(provinces_list)))
city_data = (dict(Counter(cities_list)))
# print(area_data)
# list(area_data)
# list(area_data.values())

area_map = (
    Map(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS))
        .add("num of stores", [list(z) for z in zip(list(area_data), list(area_data.values()))], "china",
             is_map_symbol_show=False, label_opts=opts.LabelOpts(color="#fff"),
             tooltip_opts=opts.TooltipOpts(is_show=True), zoom=1.2, center=[105, 35])
        .set_series_opts(label_opts=opts.LabelOpts(is_show=True))
        .set_global_opts(title_opts=opts.TitleOpts(title="Distribution of TommyHilfiger Stores", pos_top='5%',
                                                   title_textstyle_opts=opts.TextStyleOpts(color="#FF0000")),
                         visualmap_opts=opts.VisualMapOpts(is_piecewise=True, pos_right=0, pos_bottom=0,
                                                           textstyle_opts=opts.TextStyleOpts(color="#F5FFFA"),
                                                           pieces=[
                                                               {"min": 40, "label": '>40', "color": "#893448"},
                                                               {"min": 30, "max": 39, "label": '30-39',
                                                                "color": "#ff585e"},
                                                               {"min": 20, "max": 29, "label": '20-29',
                                                                "color": "#fb8146"},
                                                               {"min": 10, "max": 19, "label": '10-19',
                                                                "color": "#ffb248"},
                                                               {"min": 0, "max": 9, "label": '0-9',
                                                                "color": "#fff2d1"}])))
# area_map.render_notebook()
t4 = time.time()
print(f'区域分布图耗时{t4-t3}秒')
big_city_data = {key: value for (key, value) in city_data.items() if value > 20 }
major_city_data = {key: value for (key, value) in city_data.items() if value > 30 }

city_heat_geo = (
    Geo(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS, bg_color='transparent'))
        .add_schema(maptype="china", zoom=1.2, center=[105, 35])
        .add("Less Stores", [list(z) for z in zip(list(city_data), list(city_data.values()))], symbol_size=6)        
        .add("Less Stores", [list(z) for z in zip(list(big_city_data), list(big_city_data.values()))],  # 超20的城市
             type_=ChartType.EFFECT_SCATTER, effect_opts=opts.EffectOpts(is_show=True, color="black",
                                                                         symbol_size=20, scale=3, period=1))
        .add("Most Stores", [list(z) for z in zip(list(major_city_data), list(major_city_data.values()))],type_=ChartType.HEATMAP)
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
        visualmap_opts=opts.VisualMapOpts(range_size=[0, 5, 10, 15, 20, 25, 30, 35], orient='horizontal', max_=40,is_calculable=True,     
                                          pos_bottom=0),
        title_opts=opts.TitleOpts(title="TommyHilfiger Stores HeatMap", pos_top='5%'),
        legend_opts=opts.LegendOpts(pos_bottom='10%', pos_left=0)))
city_heat_geo.render_notebook()
city_heat_geo.render('E:/splash/tommy/all_city_stores.html')
t5 = time.time()
print(f'城市分布地理信息图耗时{t5-t4}秒')
print(shanghai_store_coord)
print(beijing_store_coord)
# shanghai [121, 31], beijing [116, 40]
def geo_store(city_name, city_store_coord, list_coord):
    city_geo = (
        Geo(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS, bg_color='transparent'))
            .add_coordinate_json(json_file='E:/splash/tommy/city_stores.json')
            .add_schema(maptype=city_name, zoom=1.2, center=list_coord)
            .add("Store Location", [list(z) for z in zip(list(city_store_coord), [1 for i in range(len(city_store_coord))])], symbol_size=6)        
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(           
            title_opts=opts.TitleOpts(title="TommyHilfiger Stores HeatMap", pos_top='5%'),
            )) # legend_opts=opts.LegendOpts(pos_bottom='10%', pos_left=0)
    city_geo.render_notebook()

    city_geo.render('E:/splash/tommy/' + city_name + 'city_stores.html')
    return city_geo
beijing_city_geo = geo_store('北京', beijing_store_coord, [116, 40])    
shanghai_city_geo = geo_store('上海', shanghai_store_coord, [121, 31])
t6 = time.time()
# 图片汇总
print(f'北京上海地理信息图耗时{t6-t5}秒')
tab = Tab()
tab.add(area_map, "TommyHilfiger Store Distribution in China")
tab.add(city_heat_geo, "TommyHilfiger Store Distribution in China")
tab.add(shanghai_city_geo, "TommyHilfiger Store Distribution in Shanghai")
tab.add(beijing_city_geo, "TommyHilfiger Store Distribution in Beijing")
tab.render('E:/splash/tommy/Tommy_tab.html')
with open("E:/splash/tommy/Tommy_tab.html", "r+", encoding='utf-8') as html:
    html_bf = BeautifulSoup(html, 'lxml')
    divs = html_bf.select('.chart-container')
    body = html_bf.find("body")
    body["style"] = "background-color:#333333;"
    meta = html_bf.find("meta")
    meta["name"] = "viewport"
    meta["content"] = "width=device-width, initial-scale=1.0"  
    print('$$$$$$$$$$$$$$$$$$$$$')
    html_new = str(html_bf)
    html.seek(0, 0)
    
    html.truncate()
    print('???????????')
    html.write(html_new)
#    make_snapshot(snapshot, '2019-nCov数据一览2.html', "2019-nCoV数据一览2.png")
    html.close()
# page = (Page(page_title="2019-nCov",layout=Page.DraggablePageLayout)
page = (Page(page_title="2020-TommyHilfiger-Store-Analysis")        
        .add(area_map)
        .add(city_heat_geo)
        .add(shanghai_city_geo)
        .add(beijing_city_geo)
        ).render("E:/splash/tommy/2020-TommyHilfiger-Store-Analysis_v2.html")
with open("E:/splash/tommy/2020-TommyHilfiger-Store-Analysis_v2.html", "r+", encoding='utf-8') as html:
    html_bf = BeautifulSoup(html, 'lxml')
    divs = html_bf.select('.chart-container')
    divs[0][
        "style"] = "width:605px;height:303px;position:absolute;top:16px;left:605px;border-style:solid;border-color:#444444;border-width:0px;"
    divs[1][
        'style'] = "width:605px;height:303px;position:absolute;top:16px;left:0px;border-style:solid;border-color:#444444;border-width:0px;"
    divs[2][
        "style"] = "width:405px;height:303px;position:absolute;top:323px;left:605px;border-style:solid;border-color:#444444;border-width:0px;"
    divs[3][
        "style"] = "width:405px;height:303px;position:absolute;top:323px;left:0px;border-style:solid;border-color:#444444;border-width:0px;"
        
    body = html_bf.find("body")
    body["style"] = "background-color:#333333;"
    meta = html_bf.find("meta")
    meta["name"] = "viewport"
    meta["content"] = "width=device-width, initial-scale=1.0"    
    print('$$$$$$$$$$$$$$$$$$$$$')
    html_new = str(html_bf)
    html.seek(0, 0)
    
    html.truncate()
    print('???????????')
    html.write(html_new)
#    make_snapshot(snapshot, '2019-nCov数据一览2.html', "2019-nCoV数据一览2.png")
    html.close()
t7 = time.time()
print(f'html 耗时{t7-t6}秒')
