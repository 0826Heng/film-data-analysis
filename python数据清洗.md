python数据清洗

数据清洗的方法：

# 重复值处理

## 检测重复值

pandas中的duplicated方法。

该方法返回的每一行的检验结果，及每一行返回一个布尔值

## 处理重复值

使用drop_duplicated方法进行去重

```sql
data = pd.read_excel('1.xlsx')#读取文件
# 判断是否存在重复观测
print('是否存在重复观测：',any(data.duplicated())
# 处理重复观测
data.drop_duplicates(inplace=True) # inplace=True时直接删除data中重复的数据
f = pd.ExcelWriter('2.xlsx')   # 创建文件对象
data.to_excel(f)                            # 将处理后的data写入新建的excel中
f.save()                                    # 保存文件
```

# 缺失值处理

## 检测缺失值

使用isnull检测是否为缺失值，返回布尔值

## 缺失值处理

### 删除法dropna

```sql
dropna(axis = 0, how = 'any', thresh = None)
## -------- 参数注释 -----------
# （1）axis = 0 表示删除行（记录）；axis = 1 表示删除列（变量）
# （2）how 参数可选值为 any 或 all, all 表示删除全有NaN的行
# （3）thresh 为整数类型，表示删除的条件，如thresh = 3，表示一行中至少有3个非NaN值时，才将其保留。
```

### 数据填充 fillna

```sql
fillna(value = None, method = None, axis = None, inplace = False)
# 其中value值除基本类型外，还可以使用字典，这样可以实现对不同的列填充不同的值。method表示采用的填补数据的方法，默认是None。
```

```sql
b1 = a.fillna(0)  							# 用 0 填补所有的缺失值
b2 = a.fillna(method = 'ffill') 			# 用前一行的值填补缺失值
b3 = a.fillna(method = 'bfill') 			# 用后一行的值填补，最后一行缺失值不处理	
b4 = a.fillna(value = {'gender':a.gender.mode()[0],'age':a.age.mean(),'income':a.income.median()})
## 性别使用众数替换 年龄使用均值替换 收入使用中位数替换
```

# 异常值处理

对于异常值的检测，一般采用两种方法，一种是标准差法，另一种是箱线图判别法

![](D:\Typora\数据分析\LF%7B1HPH$GB5(5ZXS)MD~J.png)

```sql
# =============================================
# 异常值检测
# =============================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
a = pd.read_csv('ISSN_Y_tot.csv')
a
#---------------------------------------------
plt.plot(a.counts)
plt.show()
#---------------------------------------------
mu = a.counts.mean()  # 计算黑子 个数年平均值
s = a.counts.std()    # 计算黑子个数标准差
print('标准差法异常值上限检测：',any(a.counts>mu+2*s))  # 输出： True
print('标准差法异常值下限检测：',any(a.counts<mu-2*s))  # 输出： False
#---------------------------------------------
Q1 = a.counts.quantile(0.25) # 计算下四分位数
Q3 = a.counts.quantile(0.75) # 计算上四分位数
IQR = Q3 - Q1
print("箱线图法异常值上限检测：",any(a.counts> Q3 + 1.5*IQR))  # 输出：  True
print("箱线图法异常值下限检测：",any(a.counts< Q1 - 1.5*IQR))  # 输出：  False
#---------------------------------------------
plt.style.use('ggplot')     # 设置绘图风格
a.counts.plot(kind = 'hist', bins = 30 , density = True)    # 绘制直方图
a.counts.plot(kind = 'kde')                                 # 绘制核密度曲线
plt.show()
# =============================================
#  异常值处理
# =============================================
print('异常值替换前的数据统计特征',a.counts.describe())
#---------------------------------------------
UB = Q3 + 1.5 * IQR;
st = a.counts[a.counts < UB].max()
print('判别异常值的上限临界值为：',UB)
print('用以替换异常值的数据为：',st)
#---------------------------------------------
a.loc[a.counts>UB,'counts'] = st      # 替换超过判别上限异常值
print('异常值替换后的数据特征\n',a.counts.describe())

```

