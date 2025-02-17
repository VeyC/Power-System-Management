# 根据日用电量对用户进行分类
from collections import Counter

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.cluster import KMeans
from sklearn import metrics




if __name__ == '__main__':
    dangan_path = 'F:\QQ\\a(1)\main\software_cup\data/test/new_test_dangan1.csv'
    month_path = 'F:\QQ\\a(1)\main\software_cup\data/test/new_test_month_result.csv'
    dangan_pd = pd.read_csv(dangan_path)
    dangan_pd = dangan_pd.fillna(0)
    # 数值化
    dangan_pd.prc_name[dangan_pd.prc_name == '居民生活<1kV(合表)'] = 0
    dangan_pd.prc_name[dangan_pd.prc_name == '居民合表电价(1-10千伏)'] = 1
    dangan_pd.prc_name[dangan_pd.prc_name == '居民生活1_10kV(合表)'] = 2
    print('***********')
    month_pd = pd.read_csv(month_path)
    month_pd = month_pd.fillna(0)

    dangan_pd = dangan_pd[['newID','elec_type_name', 'volt_name', 'prc_name','contract_cap','shift_no']]
    month_pd['pg_total'] = month_pd.iloc[:,1:].sum(axis=1)
    month_pd_choose = month_pd[['newID','pg_total']]

    data_pd = pd.merge(month_pd_choose, dangan_pd)
    print(data_pd.columns)
    data = np.array(data_pd.iloc[:, 1:])

    kmeans = KMeans(n_clusters = 6)  #K-Means算法模型，3类标签
    kmeans_fit = kmeans.fit(data) #模型训练
    y_predict = kmeans.predict(data)

    print(Counter(y_predict))
    #
    x1=data_pd.iloc[:, 5]
    y1=data_pd.iloc[:, 1]
    plt.figure(figsize=(14, 9))
    # print(x1)
    # print('******')
    # print(y1)
    print(y_predict)

    # alist = [[x1[i],y1[i]] for i in range(len(y_predict)) if y_predict[i]==0 ]
    # print(alist)
    # print(len(alist))
    plt.scatter(x1,y1, c=y_predict, cmap='winter',alpha=0.4) #画每一条的位置

    centers = kmeans.cluster_centers_  #每个分类的中心点
    # print(centers)
    label = [i for i in range(len(centers[:, 1]))]
    print(label)
    alist = [[centers[i,4],centers[i,0]] for i in range(len(centers))]
    print(alist)
    print(np.array(label))
    plt.scatter(centers[:, 4], centers[:, 0], c=np.array(label), cmap='gist_rainbow_r', s=150, alpha=1) #中心点
    # plt.show()  #显示图像
    plt.ylabel("total electricity consumption", fontdict={'family': 'Times New Roman', 'size': 20})
    plt.xlabel("contract capacity", fontdict={'family': 'Times New Roman', 'size': 20})
    plt.xlim((0, 2000))
    plt.ylim((0, 6000000))
    plt.xticks(size=14)
    plt.yticks(size=14)
    # plt.savefig('data/test/pic/kmeans.jpg')