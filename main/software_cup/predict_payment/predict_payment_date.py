# 使用随机森林预测缴费日期和时间
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import numpy as np
import joblib
from datetime import datetime
import time
import os
# from tqdm import tqdm

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def train():
    """
    function: 模型训练用，不用于外部接口
    """
    path = BASE_DIR+'/data/train/train_cost_month_second.csv'
    dangan_path = BASE_DIR+'/data/train/train_Result_dangan.csv'
    # path = '../data/train/train_date_result.csv'
    # 回归器
    regressor = RandomForestRegressor(
        n_estimators=160,
        bootstrap=True,
        oob_score=False,
        n_jobs=3,
        random_state=0,
        max_depth=10
    )
    # 加载数据集
    data_pd = pd.read_csv(path)
    data_pd = data_pd.fillna(0)
    # 日期化成秒
    # for i in tqdm(range(len(data_pd))):
    #     date_unit = data_pd.iloc[i,1]
    #     # print(i, date_unit)
    #     date_object = datetime.strptime(date_unit, '%Y/%m/%d')
    #     secends_unit = time.mktime(date_object.timetuple())
    #     data_pd.iloc[i,1] = secends_unit

    # data_pd['payment_date'] = data_pd['payment_date'].astype('float')

    dangan_pd = pd.read_csv(dangan_path)
    dangan_pd = dangan_pd.fillna(0)
    dangan_pd = dangan_pd[['ID', "elec_type_name","volt_name","run_cap"]]
    new_month_feature = []   # 为新生成的列取名
    for i in range(18, 0,-1):
        new_month_feature.append(str(i) + '_date')
        # new_month_feature.append(str(i) + '_cost')
    data_pd["date_second"] = data_pd["date_second"]/60/60/24

    # 先统一处理成12次，向前补0
    data_pd["m"] = data_pd["date_second"].astype("str")
    # data_pd["m"] = data_pd["payment_date"].astype("str")
    dd = data_pd.groupby('id')['m'].agg('*'.join)
    dd = pd.DataFrame(data=dd)
    dd = dd['m'].str.split('*', expand=True)
    dd.columns = new_month_feature
    dd = dd.fillna(0)
    # month_dangan = dd.merge(dangan_pd, how='left', on='id')
    cost_month_pd = pd.merge( dd, dangan_pd, left_on='id', right_on='ID')
    # cost_month_pd.drop('ID', axis=1, inplace=True)
    cost_month_np = np.array(cost_month_pd).tolist()
    for i in range(len(cost_month_np)):
        for j in range(17,0,-1):
            if cost_month_np[i][j] != 0:
                cost_month_np_new = cost_month_np[i][18:] + cost_month_np[i][j+1:18] + cost_month_np[i][0:j+1]    # 换位置
                cost_month_np[i] = cost_month_np_new
                break
    # print(cost_month_np[1])

    cost_month_list = np.array(cost_month_np,dtype=np.float64).astype(np.int64).tolist()
    # 变成差值
    for i in range(len(cost_month_list)):
        for j in range(4, 22):
            before = 0 if j==4 else cost_month_list[i][j-1]
            cost_month_list[i].append(cost_month_list[i][j]-before)

    cost_month_array = np.array(cost_month_list)
    important = [1,2,3] + [i for i in range(22,39)]
    train = cost_month_array[:, important]
    label = cost_month_array[:, -1]

    # 切分数据集
    X_train, X_test, y_train, y_test = train_test_split(train, label, test_size=0.2, random_state=0)
    print("----------start to train----------")
    regressor.fit(X_train, y_train)  # 训练数据

    predictions = regressor.predict(X_test)  # 得到预测结果
    print(predictions)
    # 保存模型
    joblib.dump(regressor, "model/payment_date_model.m")   #elec_date_model_last_
    # 评测指标
    print("R^2: ", regressor.score(X_test, y_test))


def predict_payment_cost(id:str):
    """
    function: 输入用户的id,返回用户后下个月的缴费金额 int，外部接口
    """
    path = BASE_DIR+'/data/test/new_test_cost_month_second.csv'
    dangan_path = BASE_DIR+'/data/test/new_test_dangan.csv'
    data_pd = pd.read_csv(path)
    data_pd = data_pd.fillna(0)
    dangan_pd = pd.read_csv(dangan_path)
    dangan_pd = dangan_pd[['newID',"elec_type_name", "volt_name", "run_cap"]]
    dangan_pd = dangan_pd.fillna(0)

    new_month_feature = []
    for i in range(18, 1,-1):
        new_month_feature.append(str(i) + '_cost')

    # 先统一处理成12次，向前补0
    data_pd["m"] = data_pd["payment_cost"].astype("str")
    dd = data_pd.groupby('newID')['m'].agg('*'.join)

    dd = pd.DataFrame(data=dd)

    dd = dd['m'].str.split('*', expand=True)
    dd.columns = new_month_feature
    dd = dd.fillna(0)
    cost_month_pd = pd.merge(dd, dangan_pd, on='newID')
    # 少了一列，加上
    cost_month_pd.insert(loc=len(new_month_feature)+1, column='1_cost', value=0)
    cost_month_pd['newID'] = cost_month_pd['newID'].astype('str')
    user = np.array(cost_month_pd[cost_month_pd['newID']==id]).tolist()
    for j in range(18, 1, -1):
        if user[0][j] != 0:
            cost_month_np_new = [user[0][0]] +user[0][19:] + user[0][j + 1:19] + user[0][1:j + 1]  # 换位置
            user[0] = cost_month_np_new
            break
    print(user)

    user_array = np.array(user,dtype=np.int64)
    regressor = joblib.load(BASE_DIR+"/model/payment_cost_model.m")
    print("------------- predict payment cost ------------")
    predictions = regressor.predict(user_array[:,1:-1]).astype('int')  # 得到预测结果

    return predictions[0]


def predict_payment_date(id:str):
    """
        function: 输入用户的id,返回用户下一次的缴费日期，外部接口
    """
    path = BASE_DIR+'/data/test/new_test_cost_month_second.csv'
    dangan_path = BASE_DIR+'/data/test/new_test_dangan.csv'
    # 加载数据集
    data_pd = pd.read_csv(path)
    data_pd = data_pd.fillna(0)
    data_pd = data_pd[["newID","payment_cost","date_second"]]

    dangan_pd = pd.read_csv(dangan_path)
    dangan_pd = dangan_pd.fillna(0)
    dangan_pd = dangan_pd[['newID', "elec_type_name", "volt_name", "run_cap"]]
    new_month_feature = []  # 为新生成的列取名
    for i in range(18, 1, -1):
        new_month_feature.append(str(i) + '_date')
    data_pd["date_second"] = (data_pd["date_second"] / 60 / 60 / 24).astype('int')
    # 先统一处理成12次，向前补0
    data_pd["m"] = data_pd["date_second"].astype("str")
    dd = data_pd.groupby('newID')['m'].agg('*'.join)
    dd = pd.DataFrame(data=dd)
    dd = dd['m'].str.split('*', expand=True)
    dd.columns = new_month_feature
    dd = dd.fillna(0)
    cost_month_pd = pd.merge(dd, dangan_pd, on='newID')
    # 少了一列，加上
    cost_month_pd.insert(loc=len(new_month_feature)+1, column='1_date', value=0)
    cost_month_pd['newID'] = cost_month_pd['newID'].astype('str')
    user = np.array(cost_month_pd[cost_month_pd['newID'] == id], dtype=np.int64).tolist()

    for j in range(17, 0, -1):
        if user[0][j] != 0:
            cost_month_np_new = [user[0][0]] + user[0][19:] + user[0][j + 1:19] + user[0][1:j + 1]  # 换位置
            user[0] = cost_month_np_new
            break
    # 变成差值
    for j in range(4, 22):
        before = 0 if j == 4 else user[0][j - 1]
        user[0].append(user[0][j] - before)
    user_array = np.array(user,dtype=np.int64)
    regressor = joblib.load(BASE_DIR+'/model/payment_date_model.m')
    print("------------- predict date------- : ")
    important = [1,2,3] + [i for i in range(22,39)]
    predictions = regressor.predict(user_array[:,important]) # 得到预测结果
    # print(predictions)
    # 转为时间序列
    true_time = (int(predictions[0]) + user_array[0, 20])*60*60*24
    timeA = time.localtime(true_time)
    time_str = time.strftime('%Y/%m/%d', timeA)
    return time_str
if __name__ == '__main__':
    user_id = '1700001'
    print(predict_payment_cost(user_id))
    print(predict_payment_date(user_id))
    # train()
