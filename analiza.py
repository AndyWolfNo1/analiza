import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math as math
import datetime
import os, sys

path = 'nc_clear/'
plt.style.use('fivethirtyeight')
plt.rc('xtick', direction='out', color='gray')
plt.rc('ytick', direction='out', color='gray')


def take_list(path):
    dirs = os.listdir(path)
    list_name = []
    for i in dirs:
        list_name.append(i.replace('.csv', ''))
    return list_name


class MyFrameObj:
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.data = self.take_data()
        self.data['year'] = self.data['year'].astype('category')
        self.vol_sum = self.data['Wolumen'].sum()
        self.year_count = self.data['year'].value_counts()
        self.year_category_list = self.list_sort_by_category_year()

    def __repr__(self):
        return self.name

    def take_data(self):
        url = self.path+self.name+'.csv'
        data = pd.read_csv(url)
        del data['Unnamed: 0']
        return data

    def year(self, year):
        data = self.data
        try:
            group = data.groupby(by="year")
            group_y = group.get_group(year)
            return group_y
        except:
            return 'NaN'

    def list_sort_by_category_year(self):
        year_list = []
        for i in self.year_count.index:
            year_list.append(i)
        year_list.sort()
        return year_list

    def take_group_year(self):
        bufor = []
        for i in self.year_category_list:
            data = self.year(i)
            bufor.append(data)
        return bufor

    def show_plt_year(self):
        sum_list = []
        groups = self.take_group_year()
        for i in range(len(self.year_category_list)):
            sum_list.append(groups[i]['Wolumen'].sum()/1000000)
        plt.plot(self.year_category_list, sum_list)
        plt.title('Boruta')
        plt.xlabel('Rok')
        plt.ylabel('obr [mln szt]')
        plt.show()
        
    
def list_obj(path):
    list_name = take_list(path)
    list_obj = []
    for i in list_name:
        obj = MyFrameObj(i, path)
        list_obj.append(obj)
    return list_obj
      

def file_sum_wol(path):
    list_ob = list_obj(path)
    title = 'Name,Suma Wol,LenS,Start'
    with open('sum_wolumen.txt', 'a') as file:
        file.write(title)
        file.write('\n')
    for i in range(len(list_ob)):
        data = list_ob[i].name + ',' + str(list_ob[i].data['Wolumen'].sum()) + ',' + str(len(str(list_ob[i].data['Wolumen'].sum()))) + ',' + str(list_ob[i].data['year'].min())
        with open('sum_wolumen.txt', 'a') as file:
            file.write(data)
            file.write('\n')
    return "Powodzenie"


p2b = MyFrameObj('p2b', path)
lps = MyFrameObj('lps', path)
bru = MyFrameObj('bru', path)

##list_name = take_list(path)
##list_ob = list_obj(path)
##res = list_ob
##liczba = list_ob[1].data['Wolumen'].sum()
