# 测试集和训练集数据重组
import numpy as np
import pandas as pd
import random
# test_path = '../test_dataset/month.csv'
# train_path = '../training_dataset/month.csv'
# save_path = 'data/train_month.csv'
#
# test_data = pd.read_csv(test_path)
# train_data = pd.read_csv(train_path)
#
# save_data = pd.concat([test_data, train_data])
#
# save_data.to_csv(save_path, index=0)

# # 去除某些行
# path = 'data/test_date.csv'
# data = pd.read_csv(path)
# save_data = data[['id','rq','kwh']]
# save_data.to_csv(path, index=0)



# # 生成缴费金额
# path = 'data/train_month.csv'
# data = pd.read_csv(path)
# data['cost'] = data['pq_f']*1.0911+ data['pq_g']*0.3647 + data['pq_p']*0.6805
#
# # 加一些干扰值，以多交到100为至
#
# for i in range(len(data)):
#     k = random()
#     if k > 0.5:
#         data.iloc[i,-1] += (k-0.5)*100      # random在0--1之间
#     data.iloc[i,-1] += random() * 50
#
# data.to_csv(path, index=0)


# 生成缴费日期
path = 'data/test/test_month.csv'
save_path = 'data/test/test_cost_month.csv'
data = pd.read_csv(path)
data = np.array(data)  # 先将数据框转换为数组
data_list = data.tolist()  # 其次转换为列表

date = ['01','02','03','04','05','06','07','08','09']   # 30个数
for i in range(10,31):
    date.append(str(i))

new_data = []
# 每个用户都是有22个月份的数据
for i in range(len(data_list)):
    if i%22 != 0 :
        continue
    else:
        flame = data_list[i:i+22]
        # 生成随机切分序列
        split_list = []
        current_start = 0
        while current_start<22:
            k = random.randint(1, 3)
            if current_start+k<22:
                split_list.append(k)
                current_start += k
            else:
                split_list.append(22-current_start)
                break
        start = 0
        for len in split_list:
            data_flame = flame[start:(start+len)]
            current_id = str(int(data_flame[0][0]))
            current_date = str(int(data_flame[-1][1]))[0:4] +'/'+ str(int(data_flame[-1][1]))[4:] + '/'+date[random.randint(0, 29)]
            current_cost = 0
            for k in data_flame:
                current_cost += k[-1]
            current_list = [current_id, current_date, int(current_cost)]
            start = start+len
            new_data.append(current_list)

new_data_csv = pd.DataFrame(columns=['id','payment_date', 'payment_cost'], data=new_data)
new_data_csv.to_csv(save_path, index=False)