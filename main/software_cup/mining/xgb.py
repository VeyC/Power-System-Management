import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

def get_suspected_user_id(K=30):
    # 加载数据集
    valdme = 'F:\QQ\\a(1)\main\software_cup\\'
    train_data = pd.read_csv(valdme+'data/train/train_Result_dangan.csv')
    test_data = pd.read_csv(valdme+'data/test/test_Result_dangan.csv')
    new_test_data = pd.read_csv(valdme+'data/test/new_test_dangan1.csv')

    train = train_data.iloc[:,1:-1]
    label = train_data.iloc[:,-1]
    test = test_data.iloc[:,1:-1]
    ids = test_data['id'].values.tolist()
    x_train, x_test, y_train, y_test = train_test_split(train,
                                                        label,
                                                        test_size = 0.2,
                                                        random_state = 33)
    ### fit model for train data
    model = XGBClassifier(learning_rate=0.1,
                          n_estimators=120,         # 树的个数--1000棵树建立xgboost
                          num_class=2,
                          max_depth=20,               # 树的深度
                          min_child_weight = 1,      # 叶子节点最小权重
                          gamma=0.,                  # 惩罚项中叶子结点个数前的参数
                          objective='multi:softmax', # 指定损失函数
                           random_state=27            # 随机数
                          )
    model.fit(x_train, y_train,
              eval_set = [(x_test,y_test)],
              eval_metric = "mlogloss",
              early_stopping_rounds = 10,
              verbose = True)

    pred = model.predict(test)

    # print(pred)
    res = model.predict_proba(test).tolist()
    # print('res：',res)
    for i in range(len(res)):
        res[i] = [ids[i]] + res[i]
    # print('**res：', res)
    res.sort(key=lambda x: x[2],reverse=True)   # 按predict 1 排序
    print('***res：', res[0:20] )
    suspected_user_id = [ res[i][0] for i in range(K) ]
    print(suspected_user_id)
    # 修改id后的连接
    # new_suspected_user_id = new_test_data[new_test_data['id'].isin(suspected_user_id)]['newID'].astype('int').tolist()
    new_suspected_user_id = new_test_data[new_test_data['id'].isin(suspected_user_id)]['newID'].astype('int').tolist()
    new_suspected_user_id1 = new_test_data[new_test_data['id'].isin(suspected_user_id)]['elec_type_name'].tolist()
    new_suspected_user_id2 = new_test_data[new_test_data['id'].isin(suspected_user_id)]['volt_name'].tolist()
    new_suspected_user_id3 = new_test_data[new_test_data['id'].isin(suspected_user_id)]['contract_cap'].tolist()
    new_suspected_user_id5 = new_test_data[new_test_data['id'].isin(suspected_user_id)]['build_date'].tolist()
    new_suspected_user_id6 = new_test_data[new_test_data['id'].isin(suspected_user_id)]['chk_cycle'].tolist()
    new_suspected_user_id7 = new_test_data[new_test_data['id'].isin(suspected_user_id)]['last_chk_date'].tolist()
    ppp=[]

    for i in range(len(new_suspected_user_id)):
        pp = []
        pp.append(new_suspected_user_id[i])
        pp.append(new_suspected_user_id1[i])
        pp.append(new_suspected_user_id2[i])
        pp.append(new_suspected_user_id3[i])
        pp.append(new_suspected_user_id5[i])
        pp.append(new_suspected_user_id6[i])
        pp.append(new_suspected_user_id7[i])
        ppp.append(pp)
    print(ppp)
    return new_suspected_user_id


if __name__ == '__main__':

    # 返回前30个疑似用户, 预测了320个，可以K取值为[1，320]
    # -----320个应该是固定的  取前几名而已
    get_suspected_user_id(K=20)