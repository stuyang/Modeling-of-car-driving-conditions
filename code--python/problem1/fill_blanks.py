"""
填补数据文件中的缺失数据
返回至结果数据文件夹中
注： 需要分析得到切割/插值的时间阈值大小
"""

from TimeSeriesProcess import fill_data
import pandas as pd


df1 = pd.read_excel('..\\data\\原始数据\\文件1.xlsx', encoding='utf8')
df1_fill = fill_data(df1, 10)
df1_fill.to_excel('..\\data\\结果数据文件\\1_fill.xlsx', encoding='utf-8')

df2 = pd.read_excel('..\\data\\原始数据\\文件2.xlsx', encoding='utf8')
df2_fill = fill_data(df2, 10)
df2_fill.to_excel('..\\data\\结果数据文件\\2_fill.xlsx', encoding='utf-8')

df3 = pd.read_excel('..\\data\\原始数据\\文件3.xlsx', encoding='utf8')
df3_fill = fill_data(df3, 10)
df3_fill.to_excel('..\\data\\结果数据文件\\3_fill.xlsx', encoding='utf-8')
