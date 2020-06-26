# -*- coding: utf-8 -*-

# This code reads the csv file that is produced by final_run and provides some 
# Heat maps for the analisys

import csv
import numpy as np

def convert(val):
    try:
        return int(val)
    except:
        try:
            return float(val)
        except:
            try:     
                val = val[1:-1]
                val = val.split(",")
                return (float(val[0]),float(val[1]))
            except:
                None
         
            
         
def read_AABM_csv(file_name):
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        
        all_data = {"jobs_not_assigned":{}, "jobs_assigned":{}, "jobs_completed":{}, "drones":{}}
    
        last_run_num = None
        last_type = False
        lst = []
        for idx,row in enumerate(csv_reader):
            if row == []:
                if lst:
                    all_data[last_type][last_run_num] = lst
                    lst = []
                last_run_num = None
                continue
            if idx == 0:
                sim_settings = {"size":convert(row[0]), "num_runs":convert(row[1]), "sim_length":convert(row[2]), "spaw_rate":convert(row[3])}
                continue
            
            if last_run_num == None:
                last_run_num = convert(row[0])
            elif len(row) == 1:
                if lst:
                    all_data[last_type][last_run_num] = lst
                    lst = []
                elif row[0] in all_data and last_type != row[0] and last_type != False:
                    all_data[last_type][last_run_num] = []
                last_type = row[0]
            else:
                lst.append([convert(x) for x in row])
    return all_data, sim_settings
            
        
        
file_name_def = 'AABM_default.csv'
file_name_nn = 'AABM_NN.csv'      

data_d, sim_settings_d = read_AABM_csv(file_name_def)
data_nn, sim_settings_nn = read_AABM_csv(file_name_nn)


comp_jobs_d = []

for i in range(sim_settings_d["num_runs"]):
    comp_jobs_d += data_d["jobs_completed"][i]
    comp_jobs_d += data_d["jobs_not_assigned"][i]
    comp_jobs_d += data_d["jobs_assigned"][i]
    

comp_jobs_nn = []

for i in range(sim_settings_nn["num_runs"]):
    comp_jobs_nn += data_nn["jobs_completed"][i]
    comp_jobs_nn += data_nn["jobs_not_assigned"][i]
    comp_jobs_nn += data_nn["jobs_assigned"][i]

locations_d = [x[3] for x in comp_jobs_d]
delays_d = [x[2]-x[1] if x[2] != 0 else sim_settings_d["sim_length"] - x[1] for x in comp_jobs_d]

locations_nn = [x[3] for x in comp_jobs_nn]
delays_nn = [x[2]-x[1] if x[2] != 0 else sim_settings_nn["sim_length"] - x[1] for x in comp_jobs_nn]



def data_for_heatmap(heat_size,data_size,loc,val):
    data_size = [int(data_size[0]),int(data_size[1])]
    array = []
    for i in range(heat_size[0]):
        row = []
        for o in range(heat_size[1]):
            row.append([0,0])
        array.append(row)
    
    for idx, l in enumerate(loc):
        x = int(l[0]/data_size[0]*heat_size[0])
        y = int(l[1]/data_size[1]*heat_size[1])
        array[x][y][0] += val[idx]
        array[x][y][1] += 1
        
    for i in range(heat_size[0]):
        for o in range(heat_size[1]):
            if array[i][o][1] != 0:
                array[i][o] =   array[i][o][0] / array[i][o][1]#
            else:
                array[i][o] = 0
        
    for i in array:
        i.reverse()
        
    array.reverse()
    
    labelx = [x if x%heat_size[0] == 0 else " " for x in range(0,data_size[0],int(data_size[0]/heat_size[1]))]
    labely = [x if x%heat_size[1] == 0 else " " for x in range(0,data_size[1],int(data_size[1]/heat_size[1]))]
    
    return array, labelx, labely

array_lst_d, labelx_d, labely_d = data_for_heatmap([25,25],sim_settings_d["size"],locations_d,delays_d)
array_lst_nn, labelx_nn, labely_nn = data_for_heatmap([25,25],sim_settings_nn["size"],locations_nn,delays_nn)


array_d = np.array(array_lst_d)
array_nn = np.array(array_lst_nn)
array_dif = array_nn - array_d

def convert_(val):
    if val > 10:
        return 1
    if val < -10:
        return -1
    return 0



myfunc_vec = np.vectorize(convert_)

array_dif = myfunc_vec(array_dif)

import matplotlib.pyplot as plt
import seaborn as sns

fig = plt.subplot(1,3,1)
sns.heatmap(array_d, linewidth=0, xticklabels=labelx_d,yticklabels=labely_d)
fig.scatter([300/40,450/40,700/40,550/40],[300/40,400/40,500/40,700/40],marker='+', s=100, color='white')
plt.title("Average Delay by customer \n location (baseline)")


fig = plt.subplot(1,3,2)
sns.heatmap(array_nn, linewidth=0, xticklabels=labelx_nn,yticklabels=labely_nn)
fig.scatter([300/40,450/40,700/40,550/40],[300/40,400/40,500/40,700/40],marker='+', s=100, color='white')
plt.title("Average Delay by customer \n location (final)")


fig = plt.subplot(1,3,3)
sns.heatmap(array_dif, linewidth=0, xticklabels=labelx_d,yticklabels=labely_d, cmap = "RdBu_r")
fig.scatter([300/40,450/40,700/40,550/40],[300/40,400/40,500/40,700/40],marker='+', s=100, color='black')

#plt.title("Difference between average delays")
plt.title("Demand density map used for simulation")
plt.rcParams.update({'font.size': 14})


plt.show()















