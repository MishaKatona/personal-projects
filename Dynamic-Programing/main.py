# -*- coding: utf-8 -*-

from functions import read_data, h_demands, h_profits, tot_profits, find_next, update_demand, block_time, tot_h_dems, plot_help, kpis
import time

# current asumptions im usure about
# - planes must leave the hub in the morning and get back to the hub before the end of the day
# ( does each ac need to leave and get back form the hub ?)
# - currently all routes can be used, not only the ones including the hub 
# (not that it matters as all routes only use routes with the hub)

# have fun with checking it and have a nice holidays, and well done for finishing up the last assigment in time 

s = time.time()

# get all the necessary info for the main loop
demand, loc, comp, ac_prof, ac, dist = read_data()

# get the hourly demand 
h_demand = h_demands(demand,loc)


# set up the while loop and the final list to which the answer is stored
final_paths = []
profitable = True

# main loop of the code, it will run until run out of planes or no more planes are profitable
while profitable:
    
    # gets total demand for each hour (+1,0,-1,2)
    tot_h_dem = tot_h_dems(h_demand)
    
    # gets the current still not assigned fleet available
    planes = []
    for i in ac:
        planes.append(ac[i]["fleet"])
    
    # if there are planes of a certain type left then use them 
    ac_types = []
    for i in range(len(planes)):
        if planes[i]:
            ac_types.append(i+1)
    
    # initialising the best path
    b_path = {'prof': 0, 'path': [1], "b_t":0, "ac":0, "fs":[]}
    
    # checking for all still availabe ac types
    for ac_type in ac_types:
    
        # for each ac the h_profit changes so its calculated here
        h_profit = h_profits(tot_h_dem, ac_prof, ac_type, ac)
        
        # Using h_profit convert it so that it uses the 6 min intervall
        profit = tot_profits(h_profit)
        
        # initialise a matrix of 240x20 which has a dictionary for each location that will
        # have the most profitable path to it
        paths = []
        for t in range(240):
            places = []
            for i in range(20):
                places.append({"prof":0, "path":[1]})
                if t == 0:
                    places[i]["path"] = [i]
            paths.append(places)
            
        # using the paths matrix update each node so that it has the most profitable path to it
        # for t (time)
        for t,i in enumerate(paths):
            # for o the current airport  
            for o,airport in enumerate(i):
                # get the current path to the airport
                c_path = airport["path"]
                # if the path to the current airport starts at london continue
                if c_path[0] == 0:
                    # find the airports that i can get to asap (no waiting) from the current location
                    nodes = find_next(o,comp,ac_type)
                    # for j the destination from the current airport
                    for j in nodes:
                        # if it will arive to the destination before end of day
                        # and its more profitable than previous paths to that location update the path to it
                        if t+j[1] < 240 and \
                        paths[t+j[1]][j[0]]["prof"] <= airport["prof"] + profit[t][o][j[0]]:
                                paths[t+j[1]][j[0]]["path"] = c_path + [j[0]]
                                paths[t+j[1]][j[0]]["prof"] = airport["prof"] + profit[t][o][j[0]]
        
        # once the best path is found take the lease cost from the revenue of the best path
        # and get the block time
        paths[239][0]["prof"] -= ac[ac_type]["lease"]
        prof_ac = paths[239][0]["prof"]
        b_time = block_time(paths,comp,ac_type,ac)
        
        # if the current best path is more profitable the paths of other types of ac then
        # replace the best path with the current one 
        # (this chosses which ac is most profitable to take currently)
        if prof_ac >= b_path['prof']:
            b_path['prof'] = round(paths[239][0]['prof'],1)
            b_path['path'] = paths[239][0]['path']
            b_path['b_t'] = b_time
            b_path["ac"] = ac_type
    
    # if the final best path is profitable after taking the lease out then add the best path
    # the the final paths list, and reduce the fleet of the used ac type
    if b_path["prof"] > 0:
        h_demand,fs = update_demand(h_demand, b_path["path"], comp, ac, ac_type)
        ac[b_path["ac"]]["fleet"] -= 1
        b_path["fs"] = fs
        final_paths.append(b_path)
    else:
        profitable = False
    # if at the start of the current loop there was only one ac then it was used up and no others are available
    if sum(planes) == 1:
        profitable = False
        
# total profit is the sum of all profits of final paths
t_p = 0
# print the profit, block time, ac type and flight schedule of each of the routes to be flown
for i in final_paths:
    print("route profit -",i["prof"],"  \tblock time -",i["b_t"],"\tac type -",i["ac"])#,"flight schedule",i["fs"])
    print()
    t_p += i["prof"]

print()
print(round(time.time()-s,2),"seconds")
print()
print("total profit",round(t_p,1))
   

import matplotlib.pyplot as plt 

for o in range(1,4):
    plt.figure()
    for i in final_paths:
        t = [0]
        loc = [0,0]
        if i["ac"] == o:
            t,loc = plot_help(i["path"], comp, i["ac"])
            plt.plot(t,loc,"-o",alpha=0.6)
    plt.title("ac type {0}".format(o))
    plt.xlabel("time")
    plt.ylabel("location")
    plt.grid()
    plt.show()

ask, rpk, load, cask, rask, rrpk = kpis(final_paths, ac, dist, ac_prof)
print("ask",ask," rpk",rpk," load f",round(load,3)," cask",cask," rask",rask," rrpk",rrpk)


#old_ac = 3
#count = 0
##Return arrays as latex tables
#from tabulate import tabulate
#import numpy as np
#for i in final_paths:
#    if old_ac != i["ac"]:
#        count = 1
#    else:
#        count += 1
#    old_ac = i["ac"]
#
#    lst = []
#    for o in i["fs"]:
#        lst.append([o[0],o[1],o[2],o[3]])
#    flst = np.array(lst)
#    print("\\begin{table}[H]")
#    print("\centering")
#    print("\caption{{Flight schedule of ac type {0} plane {1}}}".format(i["ac"],count))
#    print(tabulate(flst, headers=["Departure Time","Departure","Destination","Passengers"], tablefmt="latex", stralign="center", numalign="center"))#, floatfmt=".0f"))
#    print("\end{table}")
#    print()
#    print()






    









