# 交叉验证+模型融合
# F:\\QQ\\a(1)\\main\\software_cup\\model\\   李昂电脑 相对路径调用有问题
# 基础工具
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import lightgbm as lgb
import xgboost as xgb
import os
from sklearn.model_selection import GridSearchCV, cross_val_score, StratifiedKFold, train_test_split, KFold

# 定义了一个统计函数，方便后续信息统计
def Sta_inf(data):
    print('_min', np.min(data))
    print('_max:', np.max(data))
    print('_mean', np.mean(data))
    print('_ptp', np.ptp(data))
    print('_std', np.std(data))
    print('_var', np.var(data))

# 定义xgb和lgb模型函数验证查看模型的参数效果
def build_model_xgb(X_train, y_train):
    models = []
    model = xgb.XGBRegressor(n_estimators=150, learning_rate=0.1, gamma=0, subsample=0.8, \
                             colsample_bytree=0.9, max_depth=7)  # , objective ='reg:squarederror'
    sk = KFold(n_splits=5, shuffle=True, random_state=0)  # 5折交叉验证方式
    for train_ind, val_ind in sk.split(X_train, y_train):
        train_x = X_train.iloc[train_ind].values
        train_y = y_train.iloc[train_ind]

        model.fit(train_x, train_y)
        models.append(model)
    return models


def build_model_lgb(x_train, y_train):
    estimator = lgb.LGBMRegressor(num_leaves=127, n_estimators=150)
    param_grid = {
        'learning_rate': [0.01, 0.05, 0.1, 0.2],
    }
    gbm = GridSearchCV(estimator, param_grid)
    gbm.fit(x_train, y_train)
    return gbm


def evaluation(predictions, y_test):     # X_test是test集的输入，y_test是test集的输出
    # 计算指标
    count_5 = 0
    Mape = 0
    for i in range(len(y_test)):
        if y_test[i] == 0:
            continue
        apei = abs(y_test[i] - predictions[i]) / y_test[i]
        Mape += apei
        if apei <= 0.1:
            count_5 += 1
    Mape = Mape / len(y_test)
    count_acc = count_5 / len(y_test)
    accarucy5 = 0.2 * (1 - Mape) + 0.8 * count_acc

    print("Mape: ", Mape)
    print("Testing Accuracy5 : ", count_acc)
    print("Le: ", accarucy5)


def predict_kfold(models, x_val, fold):
    test = np.zeros((x_val.shape[0], 1))  # 设置测试集，输出矩阵。每一组数据输出：[0,0,0,0]以概率值填入
    for model in models:
        pred_xgb = model.predict(x_val)
        pred_xgb = pred_xgb.reshape(-1, 1)
        test += pred_xgb
    # 预测值
    sub_Weighted = test / fold

    return sub_Weighted
#
def train():
    data_pd = pd.read_csv('../data/train/train_date_result.csv').fillna(-1)
    # 输出数据的大小信息
    print('data shape:', data_pd.shape)

    for i in range(8,0,-1): # 4,3,2,1    # month 4 data 8
        # 选择特征列（手动选取）
        train = data_pd.iloc[:, 1:-i]
        label = data_pd.iloc[:, -i]  # 倒数第4个月   倒数8天

        # 切分数据集
        X_data, X_test, y_data, y_test = train_test_split(train, label, test_size=0.2, random_state=0)
        print('X train shape:', X_data.shape)
        print('X test shape:', X_test.shape)
        # 切分验证集
        X_train, X_val, y_train, y_val = train_test_split(X_data, y_data, test_size=0.2, random_state=0)
        print("----------start to train----------", i)
     # ----- lgb -------
        print('Train lgb...')
        model_lgb = build_model_lgb(X_train, y_train)
        # 在验证集上的指标
        val_lgb = model_lgb.predict(X_val)
        evaluation(val_lgb, np.array(y_val))
        # 保存模型
        joblib.dump(model_lgb, "elec_date_lgb_model_last_" + str(i) + ".m")   #elec_date_model_last_
    # ----- xgb -------
        print('Train xgb...')
        model_xgbs = build_model_xgb(X_train, y_train)  # k个模型
        val_xgb = predict_kfold(model_xgbs, X_val, 5)
        evaluation(val_xgb, np.array(y_val))
        # 保存模型
        for j, model_xgb in enumerate(model_xgbs):
            joblib.dump(model_xgb, "elec_date_xgb_model_last_" + str(i) +'_'+str(j) + ".m")  # elec_date_model_last_



def predict_date(id:str):
    """
        function: 输入用户的id,返回用户后8天的用电量，外部接口
    """
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(BASE_DIR,'data','test','new_test_date_result.csv')
    # path = 'F:\\QQ\\a(1)\\main\\software_cup\\data\\test\\new_test_date_result.csv'
    data = pd.read_csv(path)
    data = data.fillna(0)
    data['newID'] = data['newID'].astype('str')
    user_before = np.array(data[data['newID'] == id].iloc[:, 1:-8]).tolist()
    user = user_before.copy()
    user_list = []
    for i in range(8, 0, -1):
        user_array = np.array(user)
        lgb = joblib.load(os.path.join(BASE_DIR,'model','elec_date_lgb_model_last_'+ str(i) + ".m"))
        # lgb = joblib.load("F:\\QQ\\a(1)\\main\\software_cup\\model\\elec_date_lgb_model_last_" + str(i) + ".m")
        xgbs = []
        for j in range(5):
            xgbs.append(joblib.load(
                os.path.join(BASE_DIR,'model',"elec_date_xgb_model_last_" + str(i) +'_'+str(j) + ".m")))
            # xgbs.append(joblib.load("F:\\QQ\\a(1)\\main\\software_cup\\model\\elec_date_xgb_model_last_" + str(i) +'_'+str(j) + ".m"))
        print("------------- predict date : ", 101 + 8 - i)
        print('Predict lgb...')
        subA_lgb = lgb.predict(user_array)
        print('Predict xgb...')
        subA_xgb = predict_kfold(xgbs, user_array, 5)[0]
        sub_Weighted =  (subA_lgb + subA_xgb)/2  # 测试集
        predictions = np.round(sub_Weighted, decimals=2) # 得到预测结果
        user_list.extend(predictions)
        user[0].extend(predictions)

    return user_before[0], user_list


def predict_month(id:str):
    """
    function: 输入用户的id,返回用户后4个月的用电量，外部接口
    """
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(BASE_DIR, 'data', 'test', 'new_test_month_result.csv')
    # path = 'F:\\QQ\\a(1)\\main\\software_cup\\data\\test\\new_test_month_result.csv'
    data = pd.read_csv(path)
    data = data.fillna(0)
    data['newID'] = data['newID'].astype('str')
    user_before = np.array(data[data['newID'] == id].iloc[:, 1:-4]).tolist()
    user = user_before.copy()
    user_list = []
    for i in range(4, 0, -1):
        user_array = np.array(user)
        lgb = joblib.load(
            os.path.join(BASE_DIR, 'model', 'elec_month_lgb_model_last_' + str(i) + ".m"))
        # lgb = joblib.load("F:\\QQ\\a(1)\\main\\software_cup\\model\\elec_month_lgb_model_last_" + str(i) + ".m")
        xgbs = []
        for j in range(5):
            xgbs.append(joblib.load(
                os.path.join(BASE_DIR, 'model',
                             "elec_month_xgb_model_last_" + str(i) + '_' + str(j) + ".m")))
            # xgbs.append(joblib.load("F:\\QQ\\a(1)\\main\\software_cup\\model\\elec_month_xgb_model_last_" + str(i) +'_'+str(j) + ".m"))
        print("------------- predict month : ", 22 - i)
        print('Predict lgb...')
        subA_lgb = lgb.predict(user_array)
        print('Predict xgb...')
        subA_xgb = predict_kfold(xgbs, user_array, 5)[0]
        sub_Weighted =  (subA_lgb + subA_xgb)/2  # 测试集
        predictions = np.round(sub_Weighted, decimals=2) # 得到预测结果
        user_list.extend(predictions)
        user[0].extend(predictions)

    return user_before[0], user_list

if __name__=='__main__':
    user_id = '1700001'
    print(predict_month(user_id))

    # train()