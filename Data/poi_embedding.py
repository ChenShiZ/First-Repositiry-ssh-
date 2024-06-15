import pandas as pd
import numpy as np
import geopandas as gpd
import csv
import ast


def readPoiEmbedding(path):
        # 打开文件
    with open(path, 'r',encoding='GBK') as file:
        data_dict = {}
        # 逐行读取数据
        for line in file:
            # 去除换行符，并按空格分割
            line_data = line.strip().split()
            # 提取字符串和数值
            key = line_data[0]
            values = [float(value) for value in line_data[1:]]
            # 存储到字典中
            data_dict[key] = values
    return data_dict

def read_poiData(path):

    poi_df = pd.read_csv(path)

    filtered_data = poi_df[['SecondLeve', 'PoiID']]
    poi_dict = filtered_data.set_index('PoiID')['SecondLeve'].to_dict()
    return poi_dict

def getPoiEmbedding(PoiIDs):
    
    path='/data/nas/zhangxiang/japan_embeddings_semantic_result.txt'
    poiEmbedding=readPoiEmbedding(path)
    pois=read_poiData(path='/data/nas/zhangxiang/tokyo_23_poi_intersect.csv')
    embeddings=[]
    for PoiID in PoiIDs:
        if PoiID in pois:
            second_level=pois[PoiID]
        else: print(f"{PoiID}, no result")
        if second_level in poiEmbedding:
            Each_embedding=poiEmbedding[second_level]
            embeddings.append(Each_embedding)
        else: print(f"{second_level}, no result")
    
        # 将数据转换为NumPy数组
    data_array = np.array(embeddings)

    # 对多个64维向量进行求和
    sum_vector = np.sum(data_array, axis=0)
    # 计算结果向量的长度
    length = np.linalg.norm(sum_vector)

    # 将结果向量除以长度，得到单位向量
    unit_vector = sum_vector / length

    return unit_vector

def getLandPoi():
    file_path = "/data/nas/zhangxiang/匹配结果/land_poi.csv"
    # Open the input and output files
    input_file = '/data/nas/zhangxiang/匹配结果/land_poi.csv'
    output_file = '/data/nas/zhangxiang/匹配结果/land_poiEmbedding.csv'

    with open(input_file, 'r') as file, open(output_file, 'w', newline='') as output:
        reader = csv.reader(file)
        writer = csv.writer(output)
        
        # Write the header for the output file
        writer.writerow(['osm_id', 'poi_id'])
        
        next(reader)  # Skip header row
        for row in reader:
            osm_id, poi_id_str = row
            poi_id = ast.literal_eval(poi_id_str)
            PoiEmbedding=getPoiEmbedding(poi_id)
            
            # Write osm_id and poi_id to the output file
            writer.writerow([osm_id, PoiEmbedding])
            print(osm_id)

    print("Data processing and writing to file completed.")

getLandPoi()