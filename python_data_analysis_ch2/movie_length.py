import pandas as pd

if __name__ == '__main__':
    #读取用户数据
    unames = ['user_id','gender','age','occupation','zip']
    users = pd.read_table('./ch02/movielens/users.dat',sep ='::',header=None,names=unames,engine='python')
    #print(users.head())

    #读取电影数据
    mnames = ['movie_id','title','genres']
    movies = pd.read_table('./ch02/movielens/movies.dat', sep='::', header=None, names=mnames,engine='python')
    #print(movies.head())

    # 读取评分数据
    rnames = ['user_id', 'movie_id', 'rating','timestamp']
    ratings = pd.read_table('./ch02/movielens/ratings.dat', sep='::', header=None, names=rnames,engine='python')
    #print(ratings.head())

    #用merge方法将三个表合并,先合并users和ratings，都含有user_id.所以行数相同。相同的列user_id自动合并为一行，即去掉一个重复行
    data = pd.merge(pd.merge(users,ratings),movies)
    #print(data.head())

    #根据年龄和性别计算某部电影的平均分----用到透视表方法：pivot_table
    #pivot_table生成的数据行键为每个电影的title，且结果里只包含gender，即有F和M两列，对rating按title进行分组，对每组数据在分别求其在F下和M下的均值
    mean_ratings = pd.pivot_table(data,values ='rating',index = 'title',columns = 'gender',aggfunc = 'mean')
    print(mean_ratings[:5])
    #gender                                F         M
    #title
    #$1,000,000 Duck (1971)              3.375000  2.761905
    #'Night Mother (1986)                3.388889  3.352941
    #'Til There Was You (1997)           2.675676  2.733333
    #'burbs, The (1989)                  2.793478  2.962085
    #...And Justice for All (1979)       3.828571  3.689024


    #针对data数据集，过滤到评分数据不够250条的数据
    rating_by_title = data.groupby('title').size()
    #print(type(rating_by_title))       #<class 'pandas.core.series.Series'>
    #print(rating_by_title[:10])
    active_titles = rating_by_title.index[rating_by_title>250]
    #print(type(active_titles))     #<class 'pandas.core.indexes.base.Index'>
    #print(active_titles)

    #在mean_ratings中取出满足评分数据不够250条的数据这个条件的行
    activate_ratings = mean_ratings.ix[active_titles]
    print(type(activate_ratings))
    print(activate_ratings)

    #找出女性最喜欢的电影----对mean_rating按F的值降序排列即可
    top_female_ratings = mean_ratings.sort_index(by='F',ascending=False)    #按diff从小到大排序
    print(top_female_ratings)

    #找出男性和女性分歧最大的电影---找出那行和女性对电影的评分的平均分差值最大的电影，所以增加一列，存储男性和女性对同一电影的评分的差值
    mean_ratings['diff'] = mean_ratings['M'] - mean_ratings['F']
    sorted_by_diff = mean_ratings.sort_index(by='diff')
    print(sorted_by_diff)

    #找出男性观众最喜欢的电影-----sorted_by_diff[::-1]将所有的行记录从下往上倒序
    top_male_raings = sorted_by_diff[::-1][:15]

    #不考虑性别找出分析最大的电影-----按电影title分组，求每组的方差，方差越大，分歧越大
    rating_std_by_title = data.groupby("title")['rating'].std()   #以什么做groupby，则index就为什么

