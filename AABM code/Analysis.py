#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 17:16:12 2020

@author: rgraas
"""
## This code includes: 
## - Define coefficient of variation
## - Local sensitiviy analyis plots + Tornado Diagram
import main_v4 as m
import random
import time
import demandv2 as dem
from run_logic import main_loop, gen_agents
import time as times
import numpy as np
import pickle
import matplotlib.pyplot as plt

# with open('COV', 'rb') as f:
#     COV_data = pickle.load(f)

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

###############################################################################
## Coefficient of Variation
###############################################################################
from scipy.stats import variation
import matplotlib.pyplot as plt

s = times.time()
runs = 1000
data1 = run_sim(runs, 1000, 20, 8, 0.20, rest_loc, learning_weights = weights)
utilisation = np.array(data1[1])
delaytime   = np.array(data1[2])
KPI         = utilisation / delaytime

runs_list   = list(range(2, runs+1)) 
cov_list    = []
for i in range(1,len(KPI)):
    cov = variation(KPI[:i+1])
    cov_list.append(cov)
    
data2 = run_sim(runs, 1000, 20, 8, 0.20, rest_loc, learning_weights = weights)
utilisation = np.array(data2[1])
delaytime   = np.array(data2[2])
KPI2        = utilisation / delaytime

runs_list2   = list(range(2, runs+1)) 
cov_list2    = []
for i in range(1,len(KPI2)):
    cov2 = variation(KPI2[:i+1])
    cov_list2.append(cov2)

data3 = run_sim(runs, 1000, 20, 8, 0.20, rest_loc, learning_weights = weights)
utilisation = np.array(data3[1])
delaytime   = np.array(data3[2])
KPI3         = utilisation / delaytime

runs_list3   = list(range(2, runs+1)) 
cov_list3    = []
for i in range(1,len(KPI3)):
    cov3 = variation(KPI3[:i+1])
    cov_list3.append(cov3)

with open('COV', 'rb') as f:
    mydata = pickle.load(f)


print("Run time =", times.time()-s)
cov_list = COV_data[0]
cov_list2 = COV_data[1]
cov_list3 = COV_data[2]

plt.plot(runs_list, cov_list, color='navy')
plt.plot(runs_list, cov_list2, color='blue')
plt.plot(runs_list, cov_list3, color='dodgerblue')


line1 = 1.1 * 0.6 * np.ones(999)
line2 = 0.9 * 0.6 * np.ones(999)
plt.plot(runs_list, line1, '--', color='black')
plt.plot(runs_list, line2, '--', color='black')

plt.grid()
plt.title("Coefficient of variation with increasing number of runs", fontsize=20)
plt.xlabel("Number of runs", fontsize=20)
plt.ylabel("Coefficient of variation", fontsize=20)
plt.tick_params(labelsize=16)

plt.xlim(0,600)
plt.show()
       
################################################################################
### Tornado Diagram
################################################################################


run1 = run_sim(200, 1000, 25, 8, 0.2, rest_loc, learning_weights = weights)
base_final = np.mean(np.array(run1[1]) / np.array(run1[2]))
run2 = run_sim(200, 1000, 25, 8, 0.2, rest_loc, learning_weights = False)
base_base = np.mean(np.array(run2[1]) / np.array(run2[2]))

        
s = times.time()
# Varying the Drones        
bDrone10d = run_sim(200, 1000, 22, 8, 0.2, rest_loc, learning_weights = False)
KPI_bDrone10d = np.mean(np.array(bDrone10d[1]) / np.array(bDrone10d[2]))
fDrone10d = run_sim(200, 1000, 22, 8, 0.2, rest_loc, learning_weights = weights)
KPI_fDrone10d = np.mean(np.array(fDrone10d[1]) / np.array(fDrone10d[2]))
print(times.time() - s)

bDrone10i = run_sim(200, 1000, 28, 8, 0.2, rest_loc, learning_weights = False)
KPI_bDrone10i = np.mean(np.array(bDrone10i[1]) / np.array(bDrone10i[2]))
fDrone10i = run_sim(200, 1000, 28, 8, 0.2, rest_loc, learning_weights = weights)
KPI_fDrone10i = np.mean(np.array(fDrone10i[1]) / np.array(fDrone10i[2]))
print(times.time() - s)

# Varying the restaurants
bRest10d = run_sim(200, 1000, 25, 7, 0.2, rest_loc, learning_weights = False)
KPI_bRest10d = np.mean(np.array(bRest10d[1]) / np.array(bRest10d[2]))
fRest10d = run_sim(200, 1000, 25, 7, 0.2, rest_loc, learning_weights = weights)
KPI_fRest10d = np.mean(np.array(fRest10d[1]) / np.array(fRest10d[2]))
print(times.time() - s)

bRest10i = run_sim(200, 1000, 25, 9, 0.2, rest_loc, learning_weights = False)
KPI_bRest10i = np.mean(np.array(bRest10i[1]) / np.array(bRest10i[2]))
fRest10i = run_sim(200, 1000, 25, 9, 0.2, rest_loc, learning_weights = weights)
KPI_fRest10i = np.mean(np.array(fRest10i[1]) / np.array(fRest10i[2]))
print(times.time() - s)

# Varying the order frequency
bOF10d = run_sim(200, 1000, 25, 8, 0.18, rest_loc, learning_weights = False)
KPI_bOF10d = np.mean(np.array(bOF10d[1]) / np.array(bOF10d[2]))
fOF10d = run_sim(200, 1000, 25, 8, 0.18, rest_loc, learning_weights = weights)
KPI_fOF10d = np.mean(np.array(fOF10d[1]) / np.array(fOF10d[2]))
print(times.time() - s)

bOF10i = run_sim(200, 1000, 25, 8, 0.22, rest_loc, learning_weights = False)
KPI_bOF10i = np.mean(np.array(bOF10i[1]) / np.array(bOF10i[2]))
fOF10i = run_sim(200, 1000, 25, 8, 0.22, rest_loc, learning_weights = weights)
KPI_fOF10i = np.mean(np.array(fOF10i[1]) / np.array(fOF10i[2]))
print(times.time() - s)

tornado_drone_base  = [KPI_bDrone10d, KPI_bDrone10i]
tornado_drone_final = [KPI_fDrone10d, KPI_fDrone10i]

tornado_rest_base   = [KPI_bRest10d, KPI_bRest10i]
tornado_rest_final  = [KPI_fRest10d, KPI_fRest10i]

tornado_of_base     = [KPI_bOF10d, KPI_bOF10i]
tornado_of_final    = [KPI_fOF10d, KPI_fOF10i]

## Tornado Diagram (Summarise SA)
## The following parameters are being varied 
variables = [
    'Drones',
    'Order frequency',
    'Restaurants'
]

base = base_base

lows = np.array([
    np.min(tornado_drone_base),
    np.min(tornado_of_base),
    np.min(tornado_rest_base)
])


highs = np.array([
    np.max(tornado_drone_base),
    np.max(tornado_of_base),
    np.max(tornado_rest_base)
])

#
################################################################################
# The actual drawing part

# The y position for each variable
ys = range(len(highs))[::-1]  # top to bottom
plt.subplots_adjust(top=0.88,
bottom=0.11,
left=0.17,
right=0.83,
hspace=0.2,
wspace=0.2)
# Plot the bars, one by one
for y, low, high in zip(ys, lows, highs):
    # The width of the 'low' and 'high' pieces
    low_width = base - low
    high_width = high - base

    # Each bar is a "broken" horizontal bar chart
    plt.broken_barh(
        [(low, low_width), (base, high_width)],
        (y - 0.4, 0.8),
        facecolors=['white', 'pink'],  # Try different colors if you like
        edgecolors=['black', 'black'],
        linewidth=1,
    )

font=20
labelsize=12
# Draw a vertical line down the middle
plt.axvline(base, color='black')

# Position the x-axis on the top, hide all the other spines (=axis lines)
axes = plt.gca()  # (gca = get current axes)
axes.spines['left'].set_visible(False)
axes.spines['right'].set_visible(False)
axes.spines['bottom'].set_visible(False)
axes.xaxis.set_ticks_position('top')

# Make the y-axis display the variables
plt.yticks(ys, variables, fontsize=font)
plt.xticks(fontsize=labelsize)

# Set the portion of the x- and y-axes to show
plt.xlim(0, 0.3)
plt.ylim(-1, len(variables))
plt.title("Tornado Diagram (KPI of baseline model)", fontsize=font)

print("Base Model with Reference KPI =", base_base )
print("Drones (-10% ; +10%) = ",KPI_bDrone10d, ';', KPI_bDrone10i)
print("Rest (-10% ; +10%) = ",KPI_bRest10d,';',  KPI_bRest10i)
print("Order (-10% ; +10%) = ",KPI_bOF10d,';',  KPI_bOF10i)
print()
print("Final Model with Reference KPI =", base_final )
print("Drones (-10% ; +10%) = ",KPI_fDrone10d, ';',  KPI_fDrone10i)
print("Rest (-10% ; +10%) = ",  KPI_fRest10d, ';' , KPI_fRest10i)
print("Order (-10% ; +10%) = ", KPI_fOF10d,  ';' ,  KPI_fOF10i)



#################################################################################
#### LSA Plots
#################################################################################
#runs      = 200
#drone_ref = 25
#rest_ref  = 8
#of_ref    = 0.20
#
## Vary the parameters as follows
#drones = list(range(5, 46, 2))
#rest   = list(range(5, 13, 1))
#order  = [p/100 for p in range(10, 42, 5)]
#
#s = times.time()
## Varying the number of drones
#lst_uti_drone       = []
#lst_deltime_drone   = []
#lst_kpi_drone       = []
#lst_jobsC_drone     = []
#
#lst_uti_drone_base     = []
#lst_deltime_drone_base = []
#lst_kpi_drone_base     = []
#lst_jobsC_drone_base   = []
#
#for drone in drones:
#    print("#Drones =", drone)
#    run_drone       = run_sim(runs, 1000, drone, rest_ref, of_ref, rest_loc, learning_weights = weights)
#    uti_drone       = np.array(run_drone[1])
#    deltime_drone   = np.array(run_drone[2])
#    kpi_drone       = np.mean(uti_drone/deltime_drone)
#    jobsC_drone     = np.array(run_drone[3])
#    lst_uti_drone.append(np.mean(uti_drone))
#    lst_deltime_drone.append(np.mean(deltime_drone))
#    lst_jobsC_drone.append(np.mean(jobsC_drone))
#    lst_kpi_drone.append(kpi_drone)
#    
#    run_drone_base       = run_sim(runs, 1000, drone, rest_ref, of_ref, rest_loc, learning_weights = False)
#    uti_drone_base       = np.array(run_drone_base[1])
#    deltime_drone_base   = np.array(run_drone_base[2])
#    kpi_drone_base       = np.mean(uti_drone_base/deltime_drone_base)
#    jobsC_drone_base     = np.array(run_drone_base[3])
#    lst_uti_drone_base.append(np.mean(uti_drone_base))
#    lst_deltime_drone_base.append(np.mean(deltime_drone_base))
#    lst_jobsC_drone_base.append(np.mean(jobsC_drone_base))
#    lst_kpi_drone_base.append(kpi_drone_base)
#
#print("Run time =", (times.time() - s) / 60, "minutes")
#
### Varying the number of restaurants
#lst_uti_rest        = []
#lst_deltime_rest    = []
#lst_kpi_rest        = []
#lst_jobsC_rest      = []
#
#lst_uti_rest_base     = []
#lst_deltime_rest_base = []
#lst_kpi_rest_base     = []
#lst_jobsC_rest_base   = []
#
#for r in rest:
#    print("#Restaurants =", r)
#    run_rest        = run_sim(runs, 1000, drone_ref, r, of_ref, rest_loc, learning_weights = weights)
#    uti_rest        = np.array(run_rest[1])
#    deltime_rest    = np.array(run_rest[2])
#    kpi_rest        = np.mean(uti_rest/deltime_rest)
#    jobsC_rest      = np.array(run_rest[3])
#    lst_uti_rest.append(np.mean(uti_rest))
#    lst_deltime_rest.append(np.mean(deltime_rest))
#    lst_kpi_rest.append(kpi_rest)
#    lst_jobsC_rest.append(np.mean(jobsC_rest))
#    
#    run_rest_base       = run_sim(runs, 1000, drone, r, of_ref, rest_loc, learning_weights = False)
#    uti_rest_base       = np.array(run_rest_base[1])
#    deltime_rest_base   = np.array(run_rest_base[2])
#    kpi_rest_base       = np.mean(uti_rest_base/deltime_rest_base)
#    jobsC_rest_base     = np.array(run_rest_base[3])
#    lst_uti_rest_base.append(np.mean(uti_rest_base))
#    lst_deltime_rest_base.append(np.mean(deltime_rest_base))
#    lst_jobsC_rest_base.append(np.mean(jobsC_rest_base))
#    lst_kpi_rest_base.append(kpi_rest_base)
#
#print("Run time =", (times.time() - s) / 60, "minutes")
#
## Varying the order frequency
#lst_uti_of          = []
#lst_deltime_of      = []
#lst_kpi_of          = []
#lst_jobsC_of        = []
#
#lst_uti_of_base          = []
#lst_deltime_of_base      = []
#lst_kpi_of_base          = []
#lst_jobsC_of_base        = []
#
#for o in order:
#    print("Order Frequency =", o)
#    run_of          = run_sim(runs, 1000, drone_ref, rest_ref, o, rest_loc, learning_weights = weights)
#    uti_of          = np.array(run_of[1])
#    deltime_of      = np.array(run_of[2])
#    kpi_of          = np.mean(uti_of/deltime_of)
#    jobsC_of        = np.array(run_of[3])
#    lst_uti_of.append(np.mean(uti_of))
#    lst_deltime_of.append(np.mean(deltime_of))
#    lst_kpi_of.append(kpi_of)
#    lst_jobsC_of.append(np.mean(jobsC_of))
#    
#    run_of_base       = run_sim(runs, 1000, drone, rest_ref, o, rest_loc, learning_weights = False)
#    uti_of_base       = np.array(run_of_base[1])
#    deltime_of_base   = np.array(run_of_base[2])
#    kpi_of_base       = np.mean(uti_of_base/deltime_of_base)
#    jobsC_of_base     = np.array(run_of_base[3])
#    lst_uti_of_base.append(np.mean(uti_of_base))
#    lst_deltime_of_base.append(np.mean(deltime_of_base))
#    lst_jobsC_of_base.append(np.mean(jobsC_of_base))
#    lst_kpi_of_base.append(kpi_of_base)
#    
#
#print("Total run time =", (times.time() - s) / 60, "minutes")
#        
#### Plotting the results
#col = ['royalblue', 'dodgerblue']
#mark = ['o', 'x']
#labelsize=12
#font=18
#### Drones
#fig1, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4)
#plt.subplots_adjust(top=0.9,
#bottom=0.44,
#left=0.065,
#right=0.95,
#hspace=0.2,
#wspace=0.33)
#
#fig1.suptitle("Varying the number of drones", y=0.95, fontsize=font)
#
#ax1.plot(drones, lst_kpi_drone, marker = mark[0], color = col[0], label = 'Final model')
#ax1.plot(drones, lst_kpi_drone_base, marker = mark[1], color = col[1], label = 'Baseline')
#ax1.set_xlabel("Number of drones", fontsize=font)
#ax1.set_ylabel("KPI", fontsize=font)
#ax1.tick_params(labelsize=labelsize)
#
#ax2.plot(drones, lst_uti_drone, marker = mark[0], color = col[0], label = 'Final model')
#ax2.plot(drones, lst_uti_drone_base, marker = mark[1], color = col[1], label = 'Baseline')
#ax2.set_xlabel("Number of drones", fontsize=font)
#ax2.set_ylabel("Utilisation", fontsize=font)
#ax2.tick_params(labelsize=labelsize)
#
#        
#ax3.plot(drones, lst_deltime_drone, marker = mark[0], color = col[0], label = 'Final model')
#ax3.plot(drones, lst_deltime_drone_base, marker = mark[1], color = col[1], label = 'Baseline')
#ax3.set_xlabel("Number of drones", fontsize=font)
#ax3.set_ylabel("Delivery Delay", fontsize=font)
#ax3.tick_params(labelsize=labelsize)
#
#ax4.plot(drones, lst_jobsC_drone, marker = mark[0], color = col[0], label = 'Final model')
#ax4.plot(drones, lst_jobsC_drone_base, marker = mark[1], color = col[1], label = 'Baseline')
#ax4.set_xlabel("Number of drones", fontsize=font)
#ax4.set_ylabel("Number of completed jobs", fontsize=font)
#ax4.tick_params(labelsize=labelsize)
#
#
#handles, labels = ax1.get_legend_handles_labels()
#fig1.legend(handles, labels, loc='upper right', fontsize=labelsize)
#       
#### Restaurants
#fig2, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4)
#plt.subplots_adjust(top=0.9,
#bottom=0.44,
#left=0.065,
#right=0.95,
#hspace=0.2,
#wspace=0.33)
#
#fig2.suptitle("Varying the number of restaurants", y=0.95, fontsize=font)
#
#ax1.plot(rest, lst_kpi_rest, marker = mark[0], color = col[0], label = 'Final model')
#ax1.plot(rest, lst_kpi_rest_base, marker = mark[1], color = col[1], label = 'Baseline')
#ax1.set_xlabel("Number of restaurants", fontsize=font)
#ax1.set_ylabel("KPI", fontsize=font)
#ax1.tick_params(labelsize=labelsize)
#    
#ax2.plot(rest, lst_uti_rest, marker = mark[0], color = col[0], label = 'Final model')
#ax2.plot(rest, lst_uti_rest_base, marker = mark[1], color = col[1], label = 'Baseline')
#ax2.set_xlabel("Number of restaurants", fontsize=font)
#ax2.set_ylabel("Utilisation", fontsize=font)
#ax2.tick_params(labelsize=labelsize)
#     
#ax3.plot(rest, lst_deltime_rest, marker = mark[0], color = col[0], label = 'Final model')
#ax3.plot(rest, lst_deltime_rest_base, marker = mark[1], color = col[1], label = 'Baseline')
#ax3.set_xlabel("Number of restaurants", fontsize=font)
#ax3.set_ylabel("Delivery Delay", fontsize=font)
#ax3.tick_params(labelsize=labelsize)
#
#ax4.plot(rest, lst_jobsC_rest, marker = mark[0], color = col[0], label = 'Final model')
#ax4.plot(rest, lst_jobsC_rest_base, marker = mark[1], color = col[1], label = 'Baseline')
#ax4.set_xlabel("Number of restaurants", fontsize=font)
#ax4.set_ylabel("Number of completed jobs", fontsize=font)
#ax4.tick_params(labelsize=labelsize)
#
#handles, labels = ax1.get_legend_handles_labels()
#fig2.legend(handles, labels, loc='upper right', fontsize=labelsize)
##        
##### Order frequency
#fig3, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4)
#plt.subplots_adjust(top=0.9,
#bottom=0.44,
#left=0.065,
#right=0.95,
#hspace=0.2,
#wspace=0.33)
#
#fig3.suptitle("Varying the order frequency", y=0.95, fontsize=font)
#
#ax1.plot(order, lst_kpi_of, marker = mark[0], color = col[0], label = 'Final model')
#ax1.plot(order, lst_kpi_of_base, marker = mark[1], color = col[1], label = 'Baseline')
#ax1.set_xlabel("Order frequency", fontsize=font)
#ax1.set_ylabel("KPI", fontsize=font)
#ax1.tick_params(labelsize=labelsize)
#    
#ax2.plot(order, lst_uti_of, marker = mark[0], color = col[0], label = 'Final model')
#ax2.plot(order, lst_uti_of_base, marker = mark[1], color = col[1], label = 'Baseline')
#ax2.set_xlabel("Order frequency", fontsize=font)
#ax2.set_ylabel("Utilisation", fontsize=font)
#ax2.tick_params(labelsize=labelsize)
#
#        
#ax3.plot(order, lst_deltime_of, marker = mark[0], color = col[0], label = 'Final model')
#ax3.plot(order, lst_deltime_of_base, marker = mark[1], color = col[1], label = 'Baseline')
#ax3.set_xlabel("Order frequency", fontsize=font)
#ax3.set_ylabel("Delivery Delay", fontsize=font)
#ax3.tick_params(labelsize=labelsize)
#
#
#ax4.plot(order, lst_jobsC_of, marker = mark[0], color = col[0], label = 'Final model')
#ax4.plot(order, lst_jobsC_of_base, marker = mark[1], color = col[1], label = 'Baseline')
#ax4.set_xlabel("Order frequency", fontsize=font)
#ax4.set_ylabel("Number of completed jobs", fontsize=font)
#ax4.tick_params(labelsize=labelsize)
#
#
#handles, labels = ax1.get_legend_handles_labels()
#fig3.legend(handles, labels, loc='upper right', fontsize=labelsize)
##    
    



