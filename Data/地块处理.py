import geopandas as gpd
import pandas as pd

def Poi_Match_Plot(poi,plot):
    poi = poi.copy()
    for plt_idx,plot_row in plot.iterrows():
        plot_pois=[]
        count=0
        for idx,poi_row in poi.iterrows():
            if poi_row['geometry'].within(plot_row['geometry']):
                count+=1
                plot_pois.append(poi_row['PoiID'])
                poi.drop(idx, inplace=True)
        result = {'地块编号': plot_row['unique_id'], 'POI个数': count, 'POI编号': plot_pois}
        print(result)
        result_df = pd.DataFrame(result)
        result_df.to_csv('/data/nas/zhangxiang/poi_count_per_landparcel.csv',header="null", mode='a',index=False)

# # 读取shp文件
# file_path = "/data/nas/zhangxiang/东京23区建筑物分类结果/tokyo23_pred.shp"
# gdf_poi = gpd.read_file(file_path)
# unique_values = gdf_poi['zone'].unique()
# print(unique_values)


# 读取shp文件
Poi_path = "/data/nas/zhangxiang/东京地块分区/东京23区poi分区.shp"
gdf_poi = gpd.read_file(Poi_path)
grouped_poi = gdf_poi.groupby('NAME_2')
group_names = grouped_poi.groups.keys()
print(group_names)

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



