"""
运行轨迹路线可视化
"""

import folium
import pandas as pd
import numpy as np

df = pd.read_excel('..\\..\\data\\原始数据\\文件3.xlsx').iloc[::60, :]

print('读取数据完毕...\n')

lng = df['经度']
lat = df['纬度']

route = np.array([lat, lng]).T.tolist()
print(route)

# 声明地图的中心，以及我们希望地图放大多少倍
map_handle = folium.Map([sum(lat)/len(lat), sum(lng)/len(lng)], zoom_start=11)
map_handle
folium.PolyLine(route,
                weight=3,
                color='red',
                opacity=0.7).add_to(map_handle)                 # 描绘轨迹点
map_handle.save("..\\..\\Figures\\1_google_map.html")           # 显示图
print("over")

