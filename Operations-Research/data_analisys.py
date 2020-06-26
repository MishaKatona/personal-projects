# -*- coding: utf-8 -*-

from data_reader import read_data
from main_function import bay_assigment
from mytools import pbf
import csv
import time

dist, comp, ac_type, bays = read_data()

all_data = []

bays.append("N/A")
dist["N/A"] = {'A': '1000', 'B': '1000', 'C': '1000', 'D': '1000'}
comp["N/A"] = {'H': 1, 'G': 1, 'F': 1, 'E': 1, 'D': 1, 'C': 1, 'B': 1, 'A': 1}

start = time.time()
lst = []
obj = []
runs = 250
num_planes = 150
distro_type = "u"
for i in range(runs):
    pbf(i,runs,"gurobi solves for bay assigment")
    x = bay_assigment(dist,comp,ac_type,bays,num_planes,distro_type)
    obj.append(x[1])
    lst.append(x[0])
    
t_diff = round(time.time() - start,3)

all_data.append([t_diff,runs,num_planes,distro_type])
all_data += lst
all_data.append(["end"])

#walk, na_ac, ac_count = type_count(lst,dist)
#
#na,na_frac = num_NA(lst)
#avg_lst,avg_walked = avg_walk(lst,dist)
#n_lst = remove_NA(lst)
#avg_lst_nn,avg_walked_nn = avg_walk(n_lst,dist)

#plt.figure()
#plt.hist(avg_lst_nn,bins=20,range=(0,55), density=True)
#plt.xlabel('Walking distance')
#plt.ylabel('probability')
#plt.title('average waling distance without N/A bays')
#
#plt.figure()
#plt.hist(na, density=True)
#plt.xlabel('number NA')
#plt.ylabel('probability')
#plt.title('number of NA assigments')
#plt.show()




with open('Output_freq.csv', 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(all_data)





