# -*- coding: utf-8 -*-

import funct
import matplotlib.pyplot as plt
from data_reader import read_data

dist, comp, ac_type, bays = read_data()

bays.append("N/A")
dist["N/A"] = {'A': '1000', 'B': '1000', 'C': '1000', 'D': '1000'}
comp["N/A"] = {'H': 1, 'G': 1, 'F': 1, 'E': 1, 'D': 1, 'C': 1, 'B': 1, 'A': 1}

#data,runs = funct.read_sim_data("Outputnormal.csv")
#data_u,runs_u = funct.read_sim_data("Outputuniform.csv")

#data,runs = funct.read_sim_data("Outputbuffern.csv")
#data_u,runs_u = funct.read_sim_data("Outputbufferu.csv")
data,runs = funct.read_sim_data("Output_freq.csv")
print("done reading")

walk_n = []
walk_u = []
na_n = []
na_u = []

for i in range(len(data)):
    lst = data[i]

    walk, na_ac, ac_count = funct.type_count(lst,dist)
    
    na,na_frac = funct.num_NA(lst)
    avg_lst,avg_walked = funct.avg_walk(lst,dist)
    n_lst = funct.remove_NA(lst)
    walk, na_ac, ac_count = funct.type_count(lst,dist)
    avg_lst_nn,avg_walked_nn = funct.avg_walk(n_lst,dist)
    walk_n.append(walk)
    na_n.append(sum(na)/250)
    
#for i in range(len(data_u)):
#    lst = data_u[i]
#
#    walk, na_ac, ac_count = funct.type_count(lst,dist)
#    
#    na,na_frac = funct.num_NA(lst)
#    avg_lst,avg_walked = funct.avg_walk(lst,dist)
#    n_lst = funct.remove_NA(lst)
#    avg_lst_nn,avg_walked_nn = funct.avg_walk(n_lst,dist)
#    walk_u.append(avg_lst_nn)
#    na_u.append(sum(na)/250)


xaxes = "Plane type"
yaxes = "Walk Distance"
titles = ["Uniform Aircraft generation frequency","Custom Aircraft generation frequency"]
types = ["A","B","C","D","E","F","G","H"]

f,a = plt.subplots(2,1)
a = a.ravel()
for idx,ax in enumerate(a):
    ax.bar(types, walk_n[idx])
    ax.set_title(titles[idx])
    ax.set_xlabel(xaxes)
    ax.set_ylabel(yaxes)
plt.tight_layout()


#dat = [walk_u,walk_n] 
#xaxes = "Buffer times"
#yaxes = "Average Walking Distance [m]"
#titles = ["Uniform arrival distribution","Normal arrival distribution"]
#types = ["5-10","15-30","20-45"]
#
#
#f,a = plt.subplots(1,2)
#a = a.ravel()
#for idx,ax in enumerate(a):
#    ax.boxplot(dat[idx],labels=types)
#    ax.set_title(titles[idx])
#    ax.set_ylim([0,50])
#    ax.set_xlabel(xaxes)
#    ax.set_ylabel(yaxes)
#plt.tight_layout()

#dat = [walk_u,walk_n] 
#xaxes = "Number of Aircraft"
#yaxes = "Average Walking Distance [m]"
#titles = ["Uniform arrival distribution","Normal arrival distribution"]
#types = [75,100,125,150,175,200]
#
#
#f,a = plt.subplots(1,2)
#a = a.ravel()
#for idx,ax in enumerate(a):
#    ax.boxplot(dat[idx],labels=types)
#    ax.set_title(titles[idx])
#    ax.set_ylim([0,350])
#    ax.set_xlabel(xaxes)
#    ax.set_ylabel(yaxes)
#plt.tight_layout()



#xaxes = "Plane type"
#yaxes = "Walk Distance"
#titles = [str(x[2])+" planes with uniform distribution" for x in runs_u]
#types = ["A","B","C","D","E","F","G","H"]
##info = []
##for i in range(len(na_n)):
##    info.append([(x/y)*100 for [x,y] in zip(na_n[i],count_n[i])])
#
#f,a = plt.subplots(5,1)
#a = a.ravel()
#for idx,ax in enumerate(a):
#    ax.bar(types, na_n[idx])
#    ax.set_title(titles[idx])
#    #ax.set_xlabel(xaxes)
#    ax.set_ylabel(yaxes)
#plt.tight_layout()




#plt.figure()
#plt.hist(avg_lst,bins=50,range=(0,50), density=True, alpha = 0.5)
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