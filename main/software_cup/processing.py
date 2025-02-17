# 用于将所有的用户的总用电量变成横栏

# 处理月份，合并数据
import pandas as pd


def process_month():
    path = '../B_testdataset/month.csv'
    month_data = pd.read_csv(path)
    # 添加新列，22月
    new_month_feature = []  # 为新生成的列取名
    for i in range(1, 23):
        new_month_feature.append(str(i) + '_pq_z')

    month_data = month_data[['id','pq_z']]
    month_data['m'] = month_data["pq_z"].astype("str")
    dd = month_data.groupby('id')['m'].agg('*'.join)
    dd = pd.DataFrame(data=dd)
    dd = dd['m'].str.split('*', expand=True)
    dd.columns = new_month_feature

    dd.to_csv('data/test/test_month_result.csv',index=1)  # 保存行索引



def process_date():
    path = '../B_testdataset/date.csv'
    date_data = pd.read_csv(path)
    # 添加新列，22月
    new_month_feature = []  # 为新生成的列取名
    for i in range(1, 109):   # 总共有108天
        new_month_feature.append(str(i))

    date_data = date_data[['id','kwh']]
    date_data['m'] = date_data["kwh"].astype("str")
    dd = date_data.groupby('id')['m'].agg('*'.join)
    dd = pd.DataFrame(data=dd)
    dd = dd['m'].str.split('*', expand=True)
    dd.columns = new_month_feature

    dd.to_csv('data/test/test_date_result.csv',index=1)  # 不保存行索引



def consist_date_month():
    month_path = 'data/test/test_month_result.csv'
    date_path = 'data/test/test_date_result.csv'
    month_pd = pd.read_csv(month_path)
    date_pd = pd.read_csv(date_path)

    ids = date_pd['ID'].to_numpy().tolist()
    common_month = month_pd[month_pd['ID'].isin(ids)]
    common_month.to_csv('data/test_month_result_new.csv',index=0)




# 将训练集和测试集的档案id, month, cost, dateid都进行修改
def change_user_id():
    month_path = 'data/test_month_result_new.csv'
    date_path = 'data/test/test_date_result.csv'
    month_pd = pd.read_csv(month_path)
    date_pd = pd.read_csv(date_path)
    user_id = 170000
    for i in range(len(month_pd)):
        month_pd.iloc[i,0] = str(user_id+i)
        date_pd.iloc[i,0] = str(user_id+i)

    month_pd.to_csv(month_path, index=0)
    date_pd.to_csv(date_path, index=0)


def change_user_id():
    """
    将user的id改为从1开始
    :return:
    """
    dangan_path = 'data/test/test_dangan.csv'
    cost_month_path = 'data/test/test_cost_month.csv'
    date_path = 'data/test/test_date_result.csv'
    month_path = 'data/test/test_month_result.csv'

    dangan_pd = pd.read_csv(dangan_path)
    cost_month_pd = pd.read_csv(cost_month_path)
    date_pd = pd.read_csv(date_path)
    month_pd = pd.read_csv(month_path)

    id_list = month_pd['id'].to_numpy().tolist()
    dangan_pd = dangan_pd[dangan_pd['id'].isin(id_list)]

    # insert new column 'player' as first column
    new_vals = []
    for i in range(len(dangan_pd)):
        new_vals.append(1700000 + i+1)
    dangan_pd.insert(loc=len(dangan_pd.columns), column='newID', value=new_vals)

    # 连接
    merge_dangan_date_pd = pd.merge(dangan_pd, date_pd, on='id')
    merge_dangan_month_pd = pd.merge(dangan_pd, month_pd, on='id')
    merge_dangan_cost_month = pd.merge(cost_month_pd, dangan_pd, left_on='id', right_on='id')

    new_date_pd = merge_dangan_date_pd.iloc[:,14:]
    new_month_pd = merge_dangan_month_pd.iloc[:,14:]
    new_cost_month_pd = merge_dangan_cost_month[['newID','payment_date', 'payment_cost']]

    # print(new_cost_month_pd.columns)
    # print(new_cost_month_pd)

    # 重新把保存
    dangan_pd.to_csv('data/test/new_test_dangan.csv',index=0)
    new_cost_month_pd.to_csv('data/test/new_test_cost_month.csv', index=0)
    new_month_pd.to_csv('data/test/new_test_month_result.csv',index=0)
    new_date_pd.to_csv('data/test/new_test_date_result.csv', index=0)


if __name__ == '__main__':
    change_user_id()
