import json

from collections import defaultdict,Counter
from pandas import DataFrame,Series
import pandas as pd
import numpy as np

#对各个时区的数量进行统计
def get_counts(sequence):
    counts = defaultdict(int)    #counts是一个字典，key为时区名称，value为时区数量
    for tz in sequence: 
        counts[tz] += 1
    return counts

#字典排序------获取数量前10的键值对
def top_counts(count_dict,n):
    value_key_pairs = [(v,k) for k,v in count_dict.items()]   #列表里的每个元素是一个元组
    value_key_pairs.sort()
    return value_key_pairs[-n:]


#Countre类排序-----获取数量前10的数据
def top_Counter_counts(count_dict,n):
    counts = Counter(count_dict)
    return counts.most_common(n)

def top_pandas_counts(records):
    frame = DataFrame(records)             #将一组字典对象转化为一个dataframe
    counts = frame['tz'].value_counts()
    return counts[:10]

#将数量排在前10的时区绘制成一张图，根据dataframe生成的series对象，利用matlibplot绘图
def counts_view(records,n):
    frame = DataFrame(records)
    clean_tz = frame['tz'].fillna("messing")   #将tz列的缺失值NA填充为messing
    clean_tz[clean_tz==''] = 'unknown'         #将空字符串填充为unknown，clean_tz[clean_tz=='']筛选出列里值为''的元素
    tz_counts= clean_tz.value_counts()
    
    view_counts = tz_counts[:n]
    ax = view_counts.plot(title='time_zone_statistics',kind='barh',rot=0)
    fig = ax.get_figure()   #用于保存图片
    fig.savefig('./picture/time_zone_statistics.png',bbox_inches = 'tight',dpi=200)  #dpi=200s使图片不会失真，bbox_inches = 'tight'时图片保存完整


            
if __name__ == "__main__":
    file = "./data/usagov_bitly_data2012-03-16-1331923249.txt"     #一行一个json串
    #print(open(file).readline())
    records = [json.loads(line) for  line in open(file)]   #列表推导式，对集合里的每个json line 转化为一个字典对象,相当于一行转化为一个字典对象
    #print(records[0])   #records是一组字典集合
    #print(records[0]['tz'])     

    #获取所有的时区记录

    time_zones = [rec['tz'] for rec in records if 'tz' in rec]  #将records中的所有tz的列转化为一个列表,作判空处理
    #print(time_zones[:10]) 
    counts = get_counts(time_zones)

    #获取时区数排在前10的数据
    top_counts = top_counts(counts,10)
    pandas_counts = top_pandas_counts(records)
    counters = top_Counter_counts(counts,10)

    #print(top_counts)
    #print(pandas_counts)
    #print(counters)

    #绘图
    counts_view(records,10)

    frame = DataFrame(records)
    results = Series([x.split()[0] for x in frame['a'].dropna()])   #将列表转化为series，x为列表里的每一个元素是frame[a]这一列(series)里的一个值，x.split()[0] 默认以空格切分，取第一个元素
   
    cframe = frame[frame['a'].notnull()]
    print(cframe)
    operation_system = np.where(cframe['a'].str.contains('Windows'),'Windows','Not Windows')  #np.where(condition, x, y),满足condition，输出x，不满足输出y
    #print(operation_system[:5])
    #print(type(operation_system[:5]))    #<class 'numpy.ndarray'>
    #根据operation对时区进行分组
    by_tz_os = cframe.groupby(['tz',operation_system])   #对cframe根据tz进行分组，分组结果只有window和 not window 连个值。根据operation进行分组
    by_tz_os_size = by_tz_os.size()   #<class 'pandas.core.series.Series'>，这个series的行index是tz和window的组合，即可认为时区和window或not 构成key，数量构成value
    print(by_tz_os_size)
    print(type(by_tz_os_size))
    print(by_tz_os_size[2])
    print(by_tz_os_size[0])
    agg_counts = by_tz_os.size().unstack().fillna(0)     #对每个组内的window和not window 进行计数，没有的nan值填0
    print(type(agg_counts))   #<class 'pandas.core.frame.DataFrame'>
    print(agg_counts)
    indexer = agg_counts.sum(1).argsort()    #agg_counts.sum(1) 对每一行的各个数求和，argsort()根据前面求得的和的大小从小到大排序，argsort函数返回的是数组值从小到大的索引值
    print(indexer[:10])
    print(type(indexer))                  #<class 'pandas.core.series.Series'>
    count_subset= agg_counts.take(indexer)[-10:]   #按照indexer的排序去最后10行，即取window+not window的值最大的10行
    print(count_subset)


  
  












    


