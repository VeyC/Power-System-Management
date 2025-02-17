# 给出前几月的用电量，用前18个月的用电量预测后4个月的用电量, 训练集用于训练，测试集用于测试
# 给出前几日的用电量，用前100天的用电量预测后8天的用电量，训练集用于训练，测试集用于测试
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import numpy as np
import joblib


def evaluation(regressor, predictions, X_test, y_test):     # X_test是test集的输入，y_test是test集的输出
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
    print("R^2: ", regressor.score(X_test, y_test))
    print("Testing Accuracy5 : ", count_acc)
    print("Le: ", accarucy5)


def train():
    """
    function: 模型训练用，不用于外部接口
    """
    # path = '../data/train_month_result.csv'
    path = '../data/train_date_result.csv'
    # 回归器
    regressor = RandomForestRegressor(
        n_estimators=160,
        bootstrap=True,
        oob_score=False,
        n_jobs=3,
        random_state=0,
        max_depth=27
    )

    # 加载数据集
    data_pd = pd.read_csv(path)
    data_pd = data_pd.fillna(0)

    for i in range(8, 0, -1):  # 4,3,2,1    # month 4 data 8
        train = np.array(data_pd.iloc[:, 1:-i])
        label = np.array(data_pd.iloc[:, -i])  # 倒数第4个月   倒数8天

        # 切分数据集
        X_train, X_test, y_train, y_test = train_test_split(train, label, test_size=0.2, random_state=0)
        print("----------start to train----------", i)
        regressor.fit(X_train, y_train)  # 训练数据
        predictions = regressor.predict(X_test)  # 得到预测结果
        # 保存模型
        joblib.dump(regressor, "elec_date_model_last_" + str(i) + ".m")
        # 评测指标
        evaluation(regressor, predictions, X_test, y_test)


def test():
    """
    function: 模型测试用，不用于外部接口
    """
    # path = '../data/test_month_result.csv'
    path = '../data/test_date_result.csv'
    # 加载数据集
    data_pd = pd.read_csv(path)
    data_pd = data_pd.fillna(0)
    predict_pd = data_pd.iloc[:, 0:-8]  # 不取后4列      # month -4 date -8
    for i in range(8, 0, -1):  # 4,3,2,1     # month 4 date 8
        test = np.array(predict_pd.iloc[:, 1:])
        regressor = joblib.load("elec_date_model_last_" + str(i) + ".m")
        predictions = regressor.predict(test)  # 得到预测结果
        print("------------- predict month : ", 101+8-i)
        evaluation(regressor, predictions, test, np.array(data_pd.iloc[:,-i]))
        # name = str(23-i)+'_pg_z'
        name = str(109-i)
        # predict_pd[name] = predictions    # 添加在尾列
        predict_pd.insert(loc=len(predict_pd.columns), column=name, value=np.around(predictions,decimals=2))

    predict_pd.to_csv('../data/test_date_predict.csv',index=0)


def predict_month(id:str):
    """
    function: 输入用户的id,返回用户后4个月的用电量，外部接口
    """
    path = '../data/test_month_result.csv'
    data = pd.read_csv(path)
    data = data.fillna(0)
    data['ID'] = data['ID'].astype('str')
    user_before = np.array(data[data['ID']==id].iloc[:, 1:-4]).tolist()
    user = user_before.copy()
    user_list = []
    for i in range(4,0,-1):
        user_array = np.array(user)
        regressor = joblib.load("elec_model_last_" + str(i) + ".m")
        print("------------- predict month : ", 101 + 8 - i)
        predictions = regressor.predict(user_array).astype('int')  # 得到预测结果
        user_list.extend(predictions)
        user[0].extend(predictions)

    return user_before[0], user_list


def predict_date(id:str):
    """
        function: 输入用户的id,返回用户后8天的用电量，外部接口
    """
    path = '../data/test_date_result.csv'
    data = pd.read_csv(path)
    data = data.fillna(0)
    data['ID'] = data['ID'].astype('str')
    user_before = np.array(data[data['ID'] == id].iloc[:, 1:-8]).tolist()
    user = user_before.copy()
    user_list = []
    for i in range(8, 0, -1):
        user_array = np.array(user)
        regressor = joblib.load("elec_date_model_last_" + str(i) + ".m")
        print("------------- predict date : ", 101 + 8 - i)
        predictions = np.round(regressor.predict(user_array), decimals=2) # 得到预测结果
        user_list.extend(predictions)
        user[0].extend(predictions)

    return user_before[0], user_list

if __name__ == '__main__':
    user_id = '179404030'
    predict_date(user_id)