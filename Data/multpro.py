
import geopandas as gpd
import csv

# 读取shp文件
gdf = gpd.read_file('/data/nas/zhangxiang/匹配结果/poi_land.shp')

# 创建一个空字典来存储每个面id包含的点的类别数目
face_id_count = {}


result = gdf.groupby('osm_id')['PoiID'].apply(list).reset_index()

# 3. 将统计结果写入文件
result.to_csv('/data/nas/zhangxiang/匹配结果/land_poi.csv', index=False)

# # 遍历所有点要素
# for index, row in gdf.iterrows():
#     face_id = row['osm_id']
#     cls1 = row['FristLevel']
#     print(face_id,cls1)
#     # 更新每个面id包含的点的类别数目
#     if face_id in face_id_count:
#         if cls1 not in face_id_count[face_id]:
#             face_id_count[face_id].append(cls1)
#     else:
#         face_id_count[face_id] = [cls1]

# # 统计每个面要素中各类别出现的次数
# face_id_max_cls = {}
# for face_id, cls_list in face_id_count.items():
#     cls_count = {}
#     for cls in cls_list:
#         if cls in cls_count:
#             cls_count[cls] += 1
#         else:
#             cls_count[cls] = 1
#     max_cls = max(cls_count, key=cls_count.get)
#     face_id_max_cls[face_id] = max_cls


# # 写入CSV文件
# with open('/data/nas/zhangxiang/匹配结果/land_poi.csv', 'w', newline='') as csvfile:
#     csvwriter = csv.writer(csvfile)
#     csvwriter.writerow(['面id', 'poi'])
#     for face_id, max_cls in face_id_max_cls.items():
#         csvwriter.writerow([face_id, max_cls])

# print("结果已写入result_max_cls.csv文件")