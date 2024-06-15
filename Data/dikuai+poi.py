import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import time
from concurrent.futures import ThreadPoolExecutor


gdf = gpd.read_file('/data/nas/zhangxiang/关东地区地块/东京地块.shp')

poi_df = pd.read_csv('/data/nas/zhangxiang/tokyo_23_poi_intersect.csv')

poi_df['geometry'] = poi_df.apply(lambda x: Point((x.Lon, x.Lat)), axis=1)
poi_gdf = gpd.GeoDataFrame(poi_df, geometry='geometry')

result = []
start_time = time.time()
for index, row in gdf.iterrows():
    start_time = time.time()
    count = 0
    poi_ids = []
    print(row['id'])
    for idx, poi_row in poi_gdf.iterrows():
        if poi_row['geometry'].within(row['geometry']):
            count += 1
            poi_ids.append(poi_row['PoiID'])
            poi_gdf.drop(idx, inplace=True)  # 删除匹配到的POI
    if count > 0:
        print({'地块编号': row['id'], 'POI个数': count, 'POI编号': poi_ids})
        result.append({'地块编号': row['id'], 'POI个数': count, 'POI编号': poi_ids})
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("每次循环所使用的时间：", elapsed_time, "秒")
result_df = pd.DataFrame(result)

# 保留POI个数大于0的地块
gdf_filtered = gdf[gdf['id'].isin(result_df['地块编号'])]

# 将带有唯一ID字段的shp文件写入新的shp文件
gdf_filtered.to_file('/data/nas/zhangxiang/关东地区地块/afterFilter.shp')

# 将统计结果存为csv文件
result_df.to_csv('/data/nas/zhangxiang/poi_count_per_landparcel.csv', index=False)

end_time = time.time()
elapsed_time = end_time - start_time
print("总使用的时间：", elapsed_time, "秒")