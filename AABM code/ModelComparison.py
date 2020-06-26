#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 11:25:27 2020

@author: rgraas
"""
## This code includes: 
## - Model comparison
## - Statistical tests
import main_v4 as m
import random
import time
import demandv2 as dem
from run_logic import main_loop, gen_agents
import time as times
import numpy as np
import pickle
import matplotlib.pyplot as plt


#################################################################################
#### Weights 
#################################################################################
weights = [[[0.0634853790759966, 0.3826631587772218, 0.4236892177490603, 0.680122907121363, -0.38080911000385087, -0.73690859211672], [-0.31650536528538664, 0.3874503286068779, -0.3162025181115611, -0.3936277470768178, -0.6481598761886045, -0.8783291123349619], [-0.893443951407238, 0.3989718813011005, -0.5272413735899104, 0.016572026921704425, 0.12465361092423644, 0.7668775566296966], [0.6556762764034014, -0.3167333434428461, 0.3671292382698861, 0.6968427053466459, 0.6368106165518448, 0.9934321159953097], [-0.5268961516752413, 0.3950922005177131, 0.1100550398062386, 0.036855820961868346, 0.563665514240641, -0.2881709164574042], [-0.4604978968258273, -0.2969697898342727, -0.47137927700800075, 0.13765653605153405, -0.14476059524923657, 0.5851145774071143]], [[0.4650045968877172, -0.7707814669066964, 0.6028881446525505, -0.12607709144563573, 0.8688328653428452, -0.8083145909718426], [-0.4468392175174398, 0.29807823966013647, -0.5487025463120678, -0.2726424143189814, 0.8883702967305729, -0.8201511186481316], [0.5030736662744866, -0.6760608055424113, -0.6264260550658982, 0.1425712025848354, 1.0287320643053395, 0.3920834391558954], [0.6128306840837996, 0.3486096977765456, -0.04002784455646724, 0.3501650987283062, 0.3438546979329242, -0.9158808923599959], [-0.08017295431060756, 0.22116336641581547, -0.7215368955769328, -0.042621189211460964, 0.8426923258227728, 0.01408743235482196], [0.4981108664465199, -0.5218048863091018, 0.2416199021459151, -0.8452094929707066, 0.4652829695127596, 0.09399777535415232]], [[-1.0659412151364254, -0.6648826282729361, 0.2172803361380946, 0.150453431661844, -0.4013924835795414, 0.2508877400407376], [-0.592177727783264, 0.09546095099414398, 0.634169671695582, -0.8864200839766729, 0.34035215875931435, 0.5749509039851726], [-0.2040139938940626, -0.2541654432657413, -0.9047441708960184, -0.13963452192428205, 0.8911286025714387, 0.09255233706659571], [-0.024091608506800588, -0.36081201591273504, -0.35879936642529, 0.3507951387359783, 0.6418403121066141, 0.4783015273056136]], [[-0.22710748738960929, -0.6318054336247805, -0.828223374000665, 0.34595290772562715]], [[0.14899970125755835, 0.8362313418645488, -0.3710336362400688, -0.21498922377947705, -0.470196929993951, 0.22073403591915763, -0.39793660534768627, -0.3496054186302523, 0.34667773121312623, -0.3583768051635505, -0.007095575142562538, 0.8987615240446614, -0.0005058854834270043, 0.98813616677188, 1.124796722093522, -0.32571743636542916, -0.17580636537189864, -0.010327358384964347, 0.9861115479780318, 0.5705700709535082, -0.9390895310960459, -0.6529715741626314]]]
weights = [np.array(x) for x in weights]

#################################################################################
#### Restaurant Locations
#################################################################################
np.random.seed(1)
rest_loc = []
for i in range(20):
    rest_loc.append(dem.mapGenerator(gridSize=(1000,1000), spawn_prob=False, peakCoordinates = False))
np.random.seed(None)
# resttest = np.random.rand(3)

#################################################################################
#### Simulation Function
#################################################################################
def run_sim(runs, ticks, num_drones, num_restaurants, demandRate, rest_loc, learning_weights):
    
    size = (1000,1000)
    
    rest_loc = rest_loc[0:num_restaurants]
    
    overall_util = []
    avg_util = []
    delivery_time = []
    jobs_completed = []
    for i in range(runs):
        drones, restaurants, chargers, jobs_na = gen_agents(size=size, d_input=num_drones, r_input=rest_loc, c_input=False, num_pre_dem=int(num_drones/2), peak_loc=False)
        
        jobs_a = []
        # jobs_na = []
        jobs_c = []
        
        ## RUN SIMULATION
        t = 0
        run = True
        while run:
            jobs_na, jobs_a, jobs_c, slow = main_loop(drones, restaurants, chargers, jobs_a, jobs_na, jobs_c, t, spawn_prob=demandRate, size=size, peak_loc=False, learning_weights=learning_weights)
            t += 1
            if t == ticks:
                run = False
        
        ## UTILISATION
        utilisation = []
        for d in drones:
            utilisation.append(d.utilised_counter/ticks)
        overall_util.append(utilisation)
        avg_util.append(np.average(utilisation))
        
        ## DELIVERY TIME
        jobType = [] 
        jobs_all = jobs_c + jobs_na + jobs_a
        for job in jobs_all:
            if job.complete_time < 1000:
                if job.deliveryStart == 0:
                    jobType.append(ticks - job.complete_time)
                else:
                    jobType.append(job.deliveryStart - job.complete_time)
        
        delivery_time.append(np.average(jobType))
        
        ## JOBS COMPLETED / PERCENTAGE UNASSIGNED
        jobs_completed.append(len(jobs_c))
        perc_na = len(jobs_na)/(len(jobs_a) + len(jobs_c) + len(jobs_na))
    
    return overall_util, avg_util, delivery_time, jobs_completed, perc_na

#################################################################################
#### Model Comparison
#################################################################################
from scipy.stats import normaltest, ttest_rel, wilcoxon
runs       = 200
drones_ref = 12
rest_ref   = 8
order_ref  = 0.2

s = times.time()
# Generate data frome baseline model
dataBaseline = run_sim(runs, 1000, drones_ref, rest_ref, order_ref, rest_loc, learning_weights = False)
utiBaseline = np.array(dataBaseline[1])
deltimeBaseline = np.array(dataBaseline[2])
kpiBaseline = (utiBaseline / deltimeBaseline) 
jobsC_Baseline = np.array(dataBaseline[3])
print('runtime =', times.time()-s)

# Generate data frome Learning model
dataLearningModel = run_sim(runs, 1000, drones_ref, rest_ref, order_ref, rest_loc, learning_weights = weights) 
utiLearningModel = np.array(dataLearningModel[1])
deltimeLearningModel = np.array(dataLearningModel[2])
kpiLearningModel = (utiLearningModel / deltimeLearningModel) 
jobsC_Learning = np.array(dataLearningModel[3])
print('runtime =', times.time()-s)

## Plot BoxPlots
data1 = [kpiBaseline, kpiLearningModel]
data2 = [utiBaseline, utiLearningModel]
data3 = [deltimeBaseline, deltimeLearningModel]
font = 18
labelsize = 12
fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
plt.subplots_adjust(left=0.08, right=0.92, top=0.8, bottom=0.2, wspace=0.275, hspace=0.11)

fig.suptitle("Model Comparison", fontsize=font, y=0.87)

bp1 = ax1.boxplot(data1, patch_artist = True)
ax1.set_xticklabels(["Baseline", "Final Model"], fontsize=font)
ax1.set_ylabel("KPI", fontsize=font)
ax1.tick_params(labelsize=labelsize)
ax1.set_ylim(0,0.015)

bp2 = ax2.boxplot(data2, patch_artist = True)
ax2.set_xticklabels(["Baseline", "Final Model"], fontsize=font)
ax2.set_ylabel("Utilisation", fontsize=font)
ax2.tick_params(labelsize=labelsize)
ax2.set_ylim(0,0.8)


bp3 = ax3.boxplot(data3, patch_artist = True)
ax3.set_xticklabels(["Baseline", "Final Model"], fontsize=font)
ax3.set_ylabel("Delivery Delay", fontsize=font)
ax3.tick_params(labelsize=labelsize)
ax3.set_ylim(0,180)


color = ['dodgerblue' , 'royalblue']
for element in ['boxes', 'whiskers', 'fliers', 'means', 'medians', 'caps']:
    plt.setp(bp1[element], color=color[1])
    plt.setp(bp2[element], color=color[1])
    plt.setp(bp3[element], color=color[1])

for patch in bp1['boxes']:
    patch.set(facecolor=color[0]) 

for patch in bp2['boxes']:
    patch.set(facecolor=color[0]) 
    
for patch in bp3['boxes']:
    patch.set(facecolor=color[0])
    
    
data = [data1, data2, data3]

# Check whether the differences are Normality distributed
for i in data:
    stat, p = normaltest(i[0] - i[1])
    #print('Statistics=%.3f, p=%.3f' % (stat, p))
    
    alpha = 0.05 #significance level
    if p > alpha:
        normal = True
        print('Sample looks Gaussian (fail to reject H0) with p =', p)
        
    else:
        normal = False
        print('Sample does not look Gaussian (reject H0) with p =', p)
        
    print()
            
    ## Statistical Test to compare both distributions
    if normal == True:                  # T-test when data is normally distributed
        
        ttest = ttest_rel(i[0], i[1])
        pvalue = ttest[1]
        sig_threshold = 0.05
        
        print("===================================================================")
        print("T-Test H0: No difference between the means of the distributions")
        print("===================================================================")
    
        if pvalue < sig_threshold:
            print("Reject H0: means are significantly different with p-value =", pvalue)
        else:
            print("Accept H0: means are equal with p-value =", pvalue)
        print()
        print()
    else:
        
        print("===================================================================")
        print("Wilcoxon Test H0: No difference between the means of the distributions")
        print("===================================================================")
        wil = wilcoxon(i[0], i[1])
        pvalue = wil[1]
        sig_threshold = 0.05
        if pvalue < sig_threshold:
            print("Reject H0: means are significantly different with p-value =", pvalue)
        else:
            print("Accept H0: means are equal with p-value =", pvalue)
            
        print("===================================================================")
        print()
        print()