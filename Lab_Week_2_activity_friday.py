# -*- coding: utf-8 -*-
"""Lab1-Activity-Friday.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zljxBC_eFtyHRA1GXUsB6qsM0GOJo9_j
"""

a = 5

b = 10

print(a)

a*b

a/b

a + b

a - b

c = a*b
print(c)

d = 5.0

print(d)

type(a)

type(d)

print('Hello World!')

a = 'Hello World!'
print(a)

print(c)

len(a)

len(c)

a[2]

b = '5.0'

type(b)

int(b)

int(5.0)

list1 = [2,3,1,5,4,6]

print(list1)

type(list1)

list1*4

len(list1)

list1[1]

print(list1)

list1[1:5]

list1[1:-1]

list1[-2]

list2 = [list1,a,b,c,d]
print(list2)

tuple1 = (3,2,4,5,6)

list1[2] = 10
print(list1)

tuple1[2] = 10

import numpy as np

arr1 = np.array(list1)
print(arr1)

arr2 = np.array([1,2,3,4,5,6])

arr3 = arr1*5
print(arr3)

arr1+arr2

type(arr1)

arr1.dtype

arr4 = np.array([1,1,3.0,2,5.0])
print(arr4)

arr4.dtype

np.array(list2)

np.array([1,'1'])

import pandas as pd

dict1 = {'Name': ['Rob','Bob','Bill','Will'],
        'Age':[20,18,19,21],
        'Year':[1,2,1,4]}

dict1['Name']

df = pd.DataFrame(dict1)

print(df)

display(df)

df1 = df.set_index('Name')

display(df1)

df1.loc['Rob']

df1['Year']

url = 'https://dl.dropboxusercontent.com/s/tc6s7f6xl05kwzh/etch_roof.csv?dl=1'

data = pd.read_csv(url)

display(data)

data.min()

data_sub = data.loc[:,'deviceTime_local':'cpm']
display(data_sub)

import matplotlib.pyplot as plt

type(data['cpm'].tolist())

plt.plot(data['cpm'])
plt.show()

display(data_sub)

mask = (data_sub['deviceTime_local'] > '2022-01-01 00:00:00-08:00') & \
    (data_sub['deviceTime_local'] < '2022-03-01 00:00:00-08:00')

data_cut = data_sub[mask]
display(data_cut)

plt.plot(data_sub['deviceTime_unix'],data_sub['cpm'])
plt.ylabel('Counts-per-minute')
plt.xlabel('Time [epoch]')
plt.show()

plt.hist(data_sub[data_sub['cpm']<30]['cpm'],bins=35)
plt.show()

start_time = data['deviceTime_unix'][0]
print(start_time)

interval = 24*3600
stop_time = start_time + interval
mask = (data['deviceTime_unix'] >= start_time) & (data['deviceTime_unix'] < stop_time)
data_day = data[mask]
display(data_day)
#day_average = data_day

day_ave = data_day['cpm'].mean()
print(day_ave)

final_time = data['deviceTime_unix'].iloc[-1]
print(final_time)

start_time = data['deviceTime_unix'][0]
final_time = data['deviceTime_unix'].iloc[-1]
interval = 24*3600
total_time = int((final_time - start_time)/interval)
daily_aves = []
for i in range(total_time):
    stop_time = start_time + interval
    mask = (data['deviceTime_unix'] >= start_time) & (data['deviceTime_unix'] < stop_time)
    data_day = data[mask]
    day_ave = np.mean(data_day['cpm'])
    daily_aves.append(day_ave)
    start_time = stop_time

plt.plot(daily_aves)
plt.show()

def calc_ave(data):
    ave = np.mean(data['cpm'])
    return ave

calc_ave(data_cut)

print(ave)

