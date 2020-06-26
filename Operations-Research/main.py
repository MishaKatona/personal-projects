# -*- coding: utf-8 -*-

from gurobipy import *
import numpy as np
from data_reader import read_data
from gen_ac import flight_gen_normal

#creat model
m = Model("Bay Assignment")

#read data
dist, comp, ac_type, bays = read_data()
ba = sorted(bays)
    
flight = flight_gen_normal(100)

#Funcitons to convert hours,minutes to minutes + buffer times 
def time(lst):
    return int(lst[0]*60 + lst[1])

def times(lst, early_buffer, late_buffer):
    for i in range(len(lst)):
        lst[i][5] = time(lst[i][5]) - early_buffer
        lst[i][6] = time(lst[i][6]) + late_buffer
    return lst

# Convert and sort by arrival time
flight = times(flight,15,30)
flight = sorted(flight,key =lambda x: x[-3])

# Add the N/A bay to the model
bays.append("N/A")
dist["N/A"] = {'A': '1000', 'B': '1000', 'C': '1000', 'D': '1000'}
comp["N/A"] = {'H': 1, 'G': 1, 'F': 1, 'E': 1, 'D': 1, 'C': 1, 'B': 1, 'A': 1}

#Generating decision variables
ac_d_var = []
for i in range(len(flight)):
    flight_lst = []

    for k in bays:
        preference = flight[i][1]
        preference_l = flight[i][4]
        #creat binary decision variable for each palne and bay that includes the distance walked for passengers 
        flight_lst.append(m.addVar(vtype=GRB.BINARY, obj= int(dist[k][preference])*flight[i][-1]+ int(dist[k][preference_l])*flight[i][-1],name="{0}-{1}".format(k,flight[i][0][3:])))
    ac_d_var.append(flight_lst)

#Generating constraints
bay_comp = []
for i in range(len(flight)):
    bay_comp_lst = []
    for k in range(len(bays)):
        # Each plane can only go to gates that it fits in
        bay_comp_lst.append(m.addConstr(comp[bays[k]][ac_type[flight[i][2]]] >= ac_d_var[i][k]))
    # Each plane must be in a bay
    bay_comp_lst.append(m.addConstr(quicksum(ac_d_var[i][k] for k in range(len(bays))) == 1))
    bay_comp.append(bay_comp_lst)


for i in range(len(flight)):
    lst = []
    lst2 = []
    for o in range(len(flight)):
        # Find aircaft that are at the airport at the same time as the current ac
        if flight[i][5] <= flight[o][6] and flight[i][5] >= flight[o][5]:
            lst.append(ac_d_var[o])
        # Find big ac that are at the airport at the same time
        big = ["H","G","F"]
        if ac_type[flight[o][2]] in big and i!=o and flight[i][5] <= flight[o][6] and flight[i][6] >= flight[o][5]:
            lst2.append(ac_d_var[o])
            
    bay_comp2 = []
    for k in range(len(bays)-1):
        if len(lst) > 1:
            # For ac that are at the airport at the same time dont assign to same gate
            bay_comp2.append(m.addConstr(quicksum(lst[i][k] for i in range(len(lst))) <= 1))
        
    if lst2:
        # Only one big ac for gates 7,8 and 9,10 or 2 small planes
        for u in range(len(lst2)):
            bay_comp2.append(m.addConstr(lst2[u][8] + ac_d_var[i][12] <= 1))
            bay_comp2.append(m.addConstr(lst2[u][12] + ac_d_var[i][8] <= 1))
            bay_comp2.append(m.addConstr(lst2[u][4] + ac_d_var[i][28] <= 1))
            bay_comp2.append(m.addConstr(lst2[u][28] + ac_d_var[i][4] <= 1))
        

#Optimize model
m.update()
#m.write("MCF_Model.lp")
m.optimize()

def h_m(time):
    hour = time//60
    minutes = time % 60
    return [hour,minutes]
    
#Status
status = m.status

if status == GRB.Status.UNBOUNDED:
    print('The model cannot be solved because it is unbounded')

elif status == GRB.Status.OPTIMAL or True:
    f_objective = m.objVal
    print('***** RESULTS ******')
    print('\nObjective Function Value: \t %g' % f_objective)

elif status != GRB.Status.INF_OR_UNBD and status != GRB.Status.INFEASIBLE:
    print('Optimization was stopped with status %d' % status)

#Print solutions
print()
print("Flight allocation:----------------------------------")
print()
for i in range(len(flight)):
    for k in range(len(bays)):
        if ac_d_var[i][k].X >0:
            print(flight[i][0],h_m(flight[i][-3]),"-",h_m(flight[i][-2]), ' to ', bays[k])#,ac_type[flight[i][2]], "-----" ,flight[i][1],flight[i][4])
count = 0
for i in range(len(flight)):
    for k in range(len(bays)):
        if ac_d_var[i][k].X >0 and bays[k] == "N/A":
            count += 1
print(count)
        






