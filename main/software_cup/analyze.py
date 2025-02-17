# 分析档案文件中的相关性
import csv
from collections import Counter

import numpy as np
import pandas as pd
import seaborn
from matplotlib import pyplot as plt
from pandas import DataFrame

dangan_path = 'F:\QQ\\a(1)\main\software_cup\data/test/new_test_dangan.csv'

# 清洗后数据的相关性
def heat():
    data = pd.read_csv(dangan_path, encoding='utf-8')
    x = [1,2,3,4,5]
    r_name = ['elec_type_name', 'volt_name', 'prc_name', 'contract_cap']
    # 数值化
    # data[data['prc_name'] == '居民生活<1kV(合表)'] = 0
    # data[data['prc_name'] == '居民合表电价(1-10千伏）'] = 1
    # data[data['prc_name'] == '居民生活1_10kV(合表)'] = 2
    data.prc_name[data.prc_name == '居民生活<1kV(合表)'] = 0
    data.prc_name[data.prc_name == '居民合表电价(1-10千伏)'] = 1
    data.prc_name[data.prc_name == '居民生活1_10kV(合表)'] = 2

    data['prc_name'] = data['prc_name'].astype('int')
    data = data.iloc[:,x]
    #计算相关系数
    cor = DataFrame(data).corr()
    print(cor)
    #画出热力图
    plt.figure(figsize=(9,6))
    seaborn.heatmap(cor,vmin=0,vmax=1,center=0,annot=True,fmt='.2f',annot_kws={'size':10,'weight':'bold'},cmap='YlGnBu_r')
    #设置colorbar的刻度字体大小
    cax = plt.gcf().axes[-1]
    cax.tick_params(labelsize=10)
    plt.subplots_adjust(left=0.15, right=1.0, top=0.98, bottom=0.2)
    plt.xticks(x,r_name,rotation=60,fontproperties = 'Times New Roman', size = 12)
    plt.yticks(x,r_name,rotation=0,fontproperties = 'Times New Roman', size = 12)
    # plt.show()
    # plt.savefig('data/test/pic/heat.jpg')


# 堆叠柱状图相关性,elec_type_name,volt_name
def zhuzhuang_relation_1():
    data = pd.read_csv(dangan_path, encoding='utf-8')
    r_name = ['elec_type_name', 'volt_name', 'prc_name', 'contract_cap']

    elec_type_name_value = data['elec_type_name'].to_numpy().tolist()  #0,1,,,,7
    volt_name = data['volt_name'].to_numpy().tolist()   # 220, 380,,,

    elec_type_name_value_count = set(elec_type_name_value)
    x = [i for i in elec_type_name_value_count]
    y1 = [9609,0,149,166,0,18,6156,4,0,1,1]  #220
    y2 = [3064,10,75,221,2,18,2326,22,0,1,0]  #380
    y3 = [142,6,28,7,62,58,29,12,42,0,0] #10000
    for i in range(len(y1)):
        total = y1[i] + y2[i] + y3[i]
        y1[i] = y1[i] / total
        y2[i] = y2[i] / total
        y3[i] = y3[i] / total
    aa = []
    for i in elec_type_name_value_count:
        volt_uq_type = data[data['elec_type_name']==i]['volt_name'].to_numpy().tolist()
        bb = dict(Counter(volt_uq_type))  # 220:xx, 380:xx
        aa.append(bb)

    print(aa)
    color = ['b','g','r','c','m','y','k','w']
    print(y1)
    print(y2)
    print(y3)
    # 并列柱状图
    plt.figure(figsize=(9, 8))
    plt.bar(x, y1, lw=0.4, fc=color[3], width=0.4, label="220 V")
    plt.bar(x, y2, lw=0.4, fc=color[4], width=0.4, label="380 V",bottom=y1)
    plt.bar(x, y3, lw=0.4, fc=color[5], width=0.4, label="10000 V",bottom=y1)
    plt.legend(bbox_to_anchor=(1.04, 1.15))
    # plt.title("relation analyze",fontdict={'family': 'Times New Roman', 'size': 28})
    plt.ylabel("volt name percentage",fontdict={'family': 'Times New Roman', 'size': 20})
    plt.xlabel("elec type name",fontdict={'family': 'Times New Roman', 'size': 20})


    # plt.savefig('data/test/pic/elec_type_volt.jpg')
    print("finish")


# 堆叠柱状图相关性, volt_name,prc_name
def zhuzhuang_relation_2():
    data = pd.read_csv(dangan_path, encoding='utf-8')
    r_name = ['elec_type_name', 'volt_name', 'prc_name', 'contract_cap']

    data.prc_name[data.prc_name == '居民生活<1kV(合表)'] = 0
    data.prc_name[data.prc_name == '居民合表电价(1-10千伏)'] = 1
    data.prc_name[data.prc_name == '居民生活1_10kV(合表)'] = 2

    prc_name = data['prc_name'].to_numpy().tolist()  #0,1,,,,7
    volt_name = data['volt_name'].to_numpy().tolist()   # 220, 380,,,

    prc_name_count = set(prc_name)
    x = [i for i in prc_name_count]
    y1 = [16104,0,0]  #220
    y2 = [5723,1,3]  #380
    y3 = [0,157,229] #10000
    for i in range(len(y1)):
        total = y1[i] + y2[i] + y3[i]
        y1[i] = y1[i] / total
        y2[i] = y2[i] / total
        y3[i] = y3[i] / total
    aa = []
    for i in prc_name_count:
        volt_uq_type = data[data['prc_name']==i]['volt_name'].to_numpy().tolist()
        bb = dict(Counter(volt_uq_type))  # 220:xx, 380:xx
        aa.append(bb)

    print(aa)
    color = ['b','g','r','c','m','y','k','w']
    print(y1)
    print(y2)
    print(y3)
    # 并列柱状图
    plt.figure(figsize=(9, 8))
    plt.bar(x, y1, lw=0.3, fc=color[3], width=0.2, label="220 V")
    plt.bar(x, y2, lw=0.3, fc=color[4], width=0.2, label="380 V",bottom=y1)
    plt.bar(x, y3, lw=0.3, fc=color[5], width=0.2, label="10000 V",bottom=y1)
    plt.legend(bbox_to_anchor=(1.04, 1.15))
    # plt.title("relation analyze",fontdict={'family': 'Times New Roman', 'size': 28})
    plt.ylabel("volt name percentage",fontdict={'family': 'Times New Roman', 'size': 20})
    plt.xlabel("prc name",fontdict={'family': 'Times New Roman', 'size': 20})


    # plt.savefig('data/test/pic/prc_volt.jpg')
    print("finish")



# 多条折线相关性, volt_name,contract_cap
def zhexian_relation_3():
    data = pd.read_csv(dangan_path, encoding='utf-8')
    r_name = ['elec_type_name', 'volt_name', 'prc_name', 'contract_cap']

    contract_cap = data['contract_cap'].to_numpy().tolist()  #0,1,,,,4000
    volt_name = data['volt_name'].to_numpy().tolist()   # 220, 380,,,
    x = [i for i in range(len(data))]
    contract_cap_list = []
    for i in set(volt_name):
        contract_cap_list.append(data[data['volt_name']==i]['contract_cap'].to_numpy().tolist())

    print(contract_cap_list[0][:20])
    print(contract_cap_list[1][:20])
    print(contract_cap_list[2][:20])
    plt.plot([i for i in range(20)],contract_cap_list[0][:20],label="220 V")
    plt.plot([i for i in range(20)],contract_cap_list[1][:20],label="380 V",)
    plt.plot([i for i in range(20)],contract_cap_list[2][:20],label="10000 V",)
    plt.ylabel("contract_cap",fontdict={'family': 'Times New Roman', 'size': 20})
    plt.xlabel('sample number',fontdict={'family':'Times New Roman', 'size': 16})
    # plt.xlim((0, 20))
    plt.xticks([i for i in range(0,21)])
    # plt.ylabel('price',fontdict={'family':'Times New Roman', 'size': 16})
    plt.legend(prop={'family':'Times New Roman', 'size': 12})
    # plt.savefig('data/test/pic/volt_contract.jpg')
    print("finish")


    # plt.figure(figsize=(9, 6))
    # plt.scatter(contract_cap, volt_name,alpha=0.5)
    # plt.xlabel('contract cap', fontdict={'family': 'Times New Roman', 'size': 28})
    # plt.ylabel('volt name', fontdict={'family': 'Times New Roman', 'size': 28})  # 坐标轴范围
    # # plt.xticks(size=22)
    # # plt.yticks(size=22)
    # # plt.xlim((0, 300))
    # # plt.ylim((0, 100))
    # plt.savefig('data/test/pic/volt_contract_cap.jpg')


    # print("finish")



if __name__ == '__main__':
    # zhuzhuang_relation_1()
    # heat()
    # zhuzhuang_relation_2()
    zhexian_relation_3()