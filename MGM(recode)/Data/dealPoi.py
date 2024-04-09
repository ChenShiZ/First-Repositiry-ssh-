import math

# def readfile():

#     firstLevelArray=['不动产','采矿','车辆关联','大型综合店铺','电、气','电气设备','钢铁','海运','化学药品','机械','技术和专业人员','建筑','金融保险','金属制品','精密仪器','空运','陆运','其他','商业','生活相关商店','石油和煤炭产品','食品','水产农林','陶瓷/玻璃','体育设施','体育用品商店','通信和信息服务','纤维',
#                      '橡胶制品','学校和教养','医院福利','游乐场关联','有色金属','娱乐和饮食关系','运输设备','政府和公共机构','纸浆','其他产品']

#     reClassify=['商业功能','住宅功能','工作','公共服务','交通及运输设施','综合']

#     poiMap=dict()
#     N=300
#     for i in range(N):
#         poiSet = dict()
#         for j in range(len(reClassify)):
#             poiSet[reClassify[j]]=0
#         poiMap[i]=poiSet

#     with open('/data/nas/tokyo_23_poi_intersect.csv','r',encoding='UTF-8') as f:

#         f.readline()
#         line=f.readline().strip()

#         while line:
#             poiLevel = line.split(',')[4]
#             indexLevel = int(line.split(',')[-1][1:-2])

#             if (poiLevel=='大型综合店铺' or poiLevel=='电气设备'or poiLevel== '生活相关商店' or poiLevel=='体育用品商店' or poiLevel=='有色金属' or poiLevel=='娱乐和饮食关系'):
#                 poiMap[indexLevel]['商业功能'] += 1
#             if (poiLevel=='不动产'):
#                 poiMap[indexLevel]['住宅功能'] += 1
#             # if (poiLevel=='游乐场关联'):
#             #     poiMap[indexLevel]['景点'] += 1
#             if (poiLevel=='采矿'or poiLevel=='钢铁'or poiLevel== '建筑' or poiLevel=='金融保险' or poiLevel=='金属制品' or poiLevel=='陶瓷/玻璃'or poiLevel=='纤维'or poiLevel=='橡胶制品'or poiLevel=='纸浆'or poiLevel=='化学药品'):
#                 poiMap[indexLevel]['工作'] += 1
#             if (poiLevel=='电、气' or poiLevel=='技术和专业人员'or poiLevel== '体育设施' or poiLevel=='通信和信息服务' or poiLevel=='学校和教养' or poiLevel=='医院福利'or poiLevel=='政府和公共机构'):
#                 poiMap[indexLevel]['公共服务'] += 1
#             if (poiLevel == '其他' or poiLevel == '其他产品' or poiLevel == '水产农林' or poiLevel == '食品' or poiLevel == '精密仪器'or poiLevel == '电气设备'or poiLevel == '机械'or poiLevel=='游乐场关联'):
#                 poiMap[indexLevel]['综合'] += 1
#             if(poiLevel=='陆运' or poiLevel=='运输设备'or poiLevel== '车辆关联' or poiLevel=='空运' or poiLevel=='海运' ):
#                 poiMap[indexLevel]['交通及运输设施'] += 1


#             line=f.readline()
        
#         poiMap
#         return poiMap
    
# # 统计重要性并排序
# def tfidf(poiMap):
#     n=len(poiMap)
#     includeDoc=dict()
#     sumDoc = dict()
#     reClassify = ['商业功能', '住宅功能', '工作', '公共服务', '交通及运输设施', '综合']
# #计算idf 值
#     for j in range(len(reClassify)):
#         includeDoc[reClassify[j]] = n
#         sumDoc[reClassify[j]] = 0

#     for i in range(n):
#         for j in range(len(reClassify)):
#             sumDoc[reClassify[j]]+= poiMap[i][reClassify[j]]
#             if(poiMap[i][reClassify[j]] == 0):
#                 includeDoc[reClassify[j]] -=1

#     for j in range(len(reClassify)):
#         includeDoc[reClassify[j]] = math.log( n /(includeDoc[reClassify[j]]+1))
#     includeDoc

# #计算tf-idf值
#     classFiDict=[]
#     for i in range(n):
#         tempDict=[]
#         for j in range(len(reClassify)):
#             poiMap[i][reClassify[j]]=includeDoc[reClassify[j]]*( poiMap[i][reClassify[j]] /sumDoc[reClassify[j]] )
#             tempDict.append([poiMap[i][reClassify[j]]])
#         classFiDict.append(tempDict.index(max(tempDict)))

# #明天统计分析下，下一步就是匹配轨迹得到轨迹特征数据
#     classFiDict

#     return classFiDict

# # poimap是每个地块所包含各种类别poi的数量
# # classFiDict是每个地所属功能类别
# poiMap=readfile()
# classFiDict=tfidf(poiMap)

# wfile=open('/data/nas/300_功能属性.txt','w')

# for i in range(len(classFiDict)):
#     wfile.write('{},{}'.format(i,classFiDict[i]))
#     wfile.write('\n')

# 读文件，并存成向量
with open('/data/nas/zhangxiang/zone_embedding_500_Real','r',encoding='UTF-8') as f:
        zoneDict=dict()
        line=f.readline().strip()
        while line:
            zoneid = line.split(':')[0]
            zoneVector = line.split(':')[1].split(',')[:-1]
            zoneVector = [ float(x) for x in zoneVector]
            zoneDict[zoneid]=zoneVector
            line = f.readline()
zoneDict