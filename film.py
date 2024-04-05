#1.读取数据
import pandas as pd
import numpy as  np
import matplotlib.pyplot as plt
#读取文件(url usecols)
df=pd.read_csv('./movie_metadata.csv',usecols=[0,1,2,3,4,5,6,7,8,9,10,11,13,15,27])#文件名 列名可以用下标表示
#2.清洗数据
'''df.shape
df.count()#每一列非空数量
df.isna().sum#每一列空值
df.describe()#数据描述 数值类型的数据'''
#df.info()#数据信息 包含上面所有 浏览数据

data=df.dropna(how='any')#去掉空值 简单粗暴
#dropna删除空值  how指定形式  any只要有一个空这一行就删除
#how=all 这一行全部为空，被删除

#3.分析数据
#1.电影发展趋势 与时间有关系
def year_four(x):
    #print(x)
    #print(type(x))
    if int(x)>=27 and int(x)<=99:
        return '19'+x
    else:
        return '20'+x
# data['title_year'] 类型有问题
#data['year'] = data['title_year'].apply(lambda x:x[5:])#取出年
data['newyear'] = data['title_year'].apply(lambda x:x[5:]).apply(year_four)
#1历年来电影趋势 按照年份分组
move_year_count = data.groupby('newyear')['movie_title'].count()
#数据绘图

plt.figure(figsize=(20,8),dpi=80)
move_year_count.plot()
plt.savefig('move_year_count.png')
#plt.show()
#2历年来电影票房走势
move_year_gross = data.groupby('newyear')['gross'].sum()
plt.figure(figsize=(20,8),dpi=80)
move_year_gross.plot()
plt.savefig('move_year_gross.png')
#plt.show()
#各个国家电影数
country_years_count=data.groupby('country')['movie_title'].count()
country_years_count.sort_values(ascending=False)
#电影时长
move_duration=data.duration
plt.figure(figsize=(20,8),dpi=100)
#直方图
#组距
distance=5
#组数
group_number=int((max(move_duration)-min(move_duration))/distance)
#绘图
plt.hist(move_duration,bins=group_number)
#x轴刻度
plt.xticks(range(int(min(move_duration)),int(max(move_duration)))[::10])#每五个显示一个标签 （刻度 ，值）
plt.grid(linestyle='--',alpha=0.5)#网络
plt.savefig('move_duration.png')
#plt.show()
#电影类型
#准备一个dataframe 拆开数据 （类别，票房）
genre_data = pd.DataFrame(columns=['genre','gross'])
#读取data数据
for i ,row_data in data.iterrows():#suoyin shuju iterrows迭代器 按照行读取
#使用split把类型分割
    genres = row_data['genres'].split('|')
    #2.2 记录列表长度
    n_genres=len(genres)
    #2.3构建空字典 保存类型票房
    dict_obj={}
    dict_obj['genre'] =genres
    dict_obj['gross'] = [row_data['gross']] * n_genres
    #2.4字典转换成dataframe
    genre_df=pd.DataFrame(dict_obj)
    #2.存储
    genre_data=genre_data._append(genre_df)
print(genre_data)
#生成csv文件
genre_data.to_csv('genre_data.csv',index=None)
##按照类型分类 查看个数
genre_count = genre_data.groupby('genre').size()
plt.figure(figsize=(15,10))
genre_count.plot(kind='barh')
plt.savefig('genre_count.png')

#类别票房
genre_gross = genre_data.groupby('genre')['gross'].sum()/10000
plt.figure(figsize=(15,10))
genre_gross.plot(kind='barh')
plt.savefig('genre_gross.png')
#plt.show()
#盈利
data['profit']=data.gross-data.budget
group_director_profit = data.groupby('director_name')['profit'].sum()/10000
group_director_profit.sort_values(ascending=False)
print(group_director_profit)
#平均分最高的导演前二十个
director_mean = data.groupby('director_name')['imdb_score'].mean()
director_mean_20 =director_mean.sort_values(ascending=False)[:10]
plt.figure(figsize=(18,10))
director_mean_20.plot(kind='barh')
plt.savefig('director_mean_20.png')
