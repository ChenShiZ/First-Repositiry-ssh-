import random
from collections import defaultdict
import numpy as np


def get_TrajPoiEmbedding(traj_list):

    from dealPoi import zoneDict
    poiEmbedding=[]
    for traj in traj_list:
        poiArray = []
        for location in traj:
            # print("location is")
            # print(location)
            location=str(location)
            if location in zoneDict:
                print("找到对应poi向量")
                poiArray.append(zoneDict[location])
            else:
                # print("无对应poi种类向量")
                poiArray.append(zoneDict['1'])
        poiEmbedding.append(poiArray)

    return poiEmbedding
    #poi数据处理


def get_traj(path):
    allTraj=[]
    trajList=[]
    with open(path,'r') as f:
        linestr=f.readline().strip()
        preid='0'
        trajList.append(int(preid))
        while linestr:
            user_id=linestr.split(',')[0]
            position_index=int(linestr.split(',')[1])
            if preid==user_id:
                trajList.append(position_index)
            else:
                allTraj.append(trajList)
                preid=user_id
                trajList=[]
                trajList.append(int(user_id))
                trajList.append(position_index)
            
            linestr=f.readline().strip()
    return allTraj

def get_timeStamp(path,max_sequece,paddingNum):
    trajList = []
    idTimeDict=defaultdict(list)
    with open(path, 'r') as f:
        f.readline()
        linestr = f.readline().strip()
        preid = '0'
        while linestr:
            id = linestr.split(',')[0]
            timeindex = int(((int(linestr.split(',')[5])-1659884400)/3600)%24)
            if preid == id:
                trajList.append(timeindex)
            else:
                idTimeDict[int(preid)] =trajList
                preid = id
                trajList = []
                trajList.append(timeindex)
            linestr = f.readline().strip()

    for key in idTimeDict:
            lst = idTimeDict[key]
            while len(lst) < max_sequece:
                lst.append(paddingNum)
            idTimeDict[key] = lst

    timeStamp=idTimeDict
    return timeStamp
    
def data_padding(data,paddingNum):
    preMax = 0
    for i in data:
        maxIndex = len(i)
        if(maxIndex>preMax):
            preMax=maxIndex
    for i in data:
        while len(i)!=preMax:
            i.append(paddingNum)
    
    return preMax,data

def data_SplistBatch(data,batchSize):
    groups=zip(*(iter(data),)*batchSize)
    endList=[list(i)for i in groups]
    count = len(data) % batchSize
    endList.append(data[-count:]) if count != 0 else endList
    return endList[:-1]



def TrajEmbedding(path,batchSize):

    trajList=get_traj(path)
    max,padding_trajList=data_padding(trajList,500)
    end_trajList=data_SplistBatch(padding_trajList,batchSize)

    return max,trajList,end_trajList

trajlist=get_traj('/data/nas/zhangxiang/0712_newtraj_500.csv')

max_squence,padding_trajList=data_padding(trajlist,500)
end_trajList=data_SplistBatch(padding_trajList,64)

poi=get_TrajPoiEmbedding(padding_trajList)
end_poiEmbedding=data_SplistBatch(poi,64)



