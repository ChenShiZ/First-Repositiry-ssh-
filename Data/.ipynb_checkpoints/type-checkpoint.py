import geopandas as gpd
import pandas as pd
from collections import Counter
import csv

def most_common(plot_poiType):
    # 使用Counter计算每个值的出现次数
    counter = Counter(plot_poiType)
    # most_common(1)会返回一个列表，其中包含一个元组，元组的第一个元素就是出现次数最多的值
    most_common_element = counter.most_common(1)[0][0]
    return most_common_element

def Poi_Match_Plot(poi,plot):
    poi = poi.copy()
    for plt_idx,plot_row in plot.iterrows():
        plot_poiType=[]
        for idx,poi_row in poi.iterrows():
            if poi_row['geometry'].within(plot_row['geometry']):
                plot_poiType.append(poi_row['cls1'])
                most_common_value = most_common(plot_poiType)
                poi.drop(idx, inplace=True)

        result = [plot_row['unique_id'], most_common_value]
        print(result)
        with open('/data/nas/zhangxiang/landparcel_type.csv', mode='a', newline='') as file:
        # Step 2: Create a csv.writer object
            writer = csv.writer(file)

            # Step 3: Write the result list to the CSV file
            writer.writerow(result)

# 读取shp文件
file_path = "/data/nas/zhangxiang/东京23区建筑物分类结果/东京23区建筑物属性.shp"
gdf_poi = gpd.read_file(file_path)
grouped_poi = gdf_poi.groupby('NAME_2')
group_names = grouped_poi.groups.keys()
print(group_names)


# 读取shp文件
# Poi_path = "/data/nas/zhangxiang/东京地块分区/东京23区poi分区.shp"
# gdf_poi = gpd.read_file(Poi_path)
# grouped_poi = gdf_poi.groupby('NAME_2')
# group_names = grouped_poi.groups.keys()
# print(group_names)

# 读取shp文件
file_path = "/data/nas/zhangxiang/东京23区地块_无POI.shp"
gdf_plot = gpd.read_file(file_path)
grouped_plot = gdf_plot.groupby('NAME_2')

group_names = grouped_plot.groups.keys()
print(group_names)

unique_values = gdf_plot['NAME_2'].unique()

finished=[]

for value in unique_values:

    if value in grouped_poi.groups:
        poi=grouped_poi.get_group(value)
        plot=grouped_plot.get_group(value)
        print("正在处理")
        print(value)
        Poi_Match_Plot(poi,plot)
        print("finished")
        finished.append(value)

for value in finished:
    gdf_poi = gdf_poi.query("NAME_2 != @value")
    gdf_plot = gdf_plot.query("NAME_2 != @value")

Poi_Match_Plot(gdf_poi,gdf_plot)
