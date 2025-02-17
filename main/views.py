import json
import os
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from main.software_cup.model.cross_multi import predict_month,predict_date
from main.software_cup.predict_payment.predict_payment_date import predict_payment_cost,predict_payment_date
all=[]
thisall=[]

def kmeanspage(request):#聚类界面
    # dic={'thisall':thisall[:30]}
    return render(request, 'tables8.html')

def WKpage(request):#疑似挖矿用户
    wlist=[[1707729, 0, 380, 480.0, '2014/1/21 0:00', 120, '2014/1/21 0:00'], [1712779, 0, 380, 580.0, '2013/9/22 0:00', 120, '2013/9/22 0:00'], [1713497, 0, 380, 522.2, '2015/5/22 15:02', 120, '2015/5/22 15:02'], [1717792, 0, 380, 550.0, '2015/6/19 17:15', 120, '2015/6/19 17:15'], [1718230, 0, 10000, 160.0, '2007/12/25 9:08', 12, '2021/1/31 0:00'], [1718500, 0, 380, 500.0, '2014/2/27 12:39', 12, '2014/2/27 12:39'], [1718506, 0, 380, 480.0, '2019/8/27 11:00', 120, '2019/8/27 11:00'], [1718510, 0, 380, 165.0, '2008/11/14 9:47', 24, '2018/5/31 0:00'], [1718511, 0, 10000, 800.0, '2009/1/8 0:00', 12, '2021/3/31 0:00'], [1718513, 0, 10000, 800.0, '2009/1/8 0:00', 12, '2021/6/30 0:00'], [1718516, 0, 380, 264.0, '2009/12/31 0:00', 24, '2019/1/31 0:00'], [1718527, 0, 380, 250.0, '2014/3/25 9:41', 120, '2014/3/25 9:41'], [1718543, 0, 380, 99.0, '2016/9/27 10:57', 120, '2016/9/27 10:57'], [1718768, 0, 380, 198.0, '2017/10/16 9:45', 120, '2017/10/16 9:45'], [1718791, 0, 380, 264.0, '2009/6/1 0:00', 12, '2021/10/31 0:00'], [1718797, 0, 380, 99.0, '2010/12/28 0:00', 60, '2010/12/28 0:00'], [1718807, 0, 380, 66.0, '2016/9/27 10:57', 120, '2016/9/27 10:57'], [1718836, 3, 380, 165.0, '2013/1/8 0:00', 24, '2019/1/28 0:00'], [1719059, 0, 380, 197.0, '2013/8/21 0:00', 120, '2013/8/21 0:00'], [1719072, 0, 380, 250.0, '2015/2/9 10:57', 120, '2015/2/9 10:57']]
    zz = {'wlist': wlist}
    return render(request,'tables9.html',zz)

def t9inner(request):
    return render(request, 't9inner.html')
def nextMonth(request):#预测下个月的缴费
    return render(request,'tables10.html')
def t10inner(request):
    return render(request, 't10inner.html')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(BASE_DIR,'main','alluse.csv'),'r',encoding='utf8')as f:
    all=f.readlines()
for i in all:
    op=i.strip('\n').split(',')
    op[2]=round(float(op[2]), 1)
    thisall.append(op)

def relax(request):
    return render(request,'tables4.html')

def searcha(request):#输入id后 调用多预测
    uid = json.loads(request.body.decode('utf-8')).get('uid')
    print(uid)
    d1,d2=predict_date(uid) # 前100天的用电量，类型: list;  后8天的用电量， 类型: list  d1就包括俩
    m0, m2=predict_month(uid) # 前18个月用电量，类型: list;  后4个月用电量， 类型: list
    money=predict_payment_cost(uid)
    date=predict_payment_date(uid)
    m1=[float(val) for val in m2]
    print(m1)
    # return JsonResponse({'d1':d2,"m1":m1,})
    return JsonResponse({'d1':d2,"m1":m1,"money":str(money),"date":str(date)})

def dashboard(request):#查询界面
    return render(request, 'tables7.html')

def search(request):#输入id后 调用查询
    uid = json.loads(request.body.decode('utf-8')).get('uid')
    print(uid)
    d1,d2=predict_date(uid) # 前100天的用电量，类型: list;  后8天的用电量， 类型: list  d1就包括俩
    m0, m2=predict_month(uid) # 前18个月用电量，类型: list;  后4个月用电量， 类型: list
    m1=[float(val) for val in m0]
    print(m1)
    return JsonResponse({'d1':d1[:-8],"m1":m1[:-4]})

def t7inner(request):
    return render(request, 't7inner.html')

def index(request):
    return render(request, 'newnewindex.html')




def dash(request):#默认界面
    zz={'thisall':thisall[:100]}
    return render(request, 'tables5.html', zz)

def okk():
    uid='1700001'
    money=predict_payment_cost(uid)# 113 用户最后一个月的缴费金额
    date=predict_payment_date(uid)
    print(money,date)



if __name__ == '__main__':
    okk()