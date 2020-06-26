# -*- coding: utf-8 -*-

from gurobipy import *
import numpy as np
#from data_reader import read_data
from gen_ac import flight_gen_normal, flight_gen_uni

#dist, comp, ac_type, bays = read_data()

def bay_assigment(dist,comp,ac_type,bays,num_planes,gen_type):
    
    if gen_type == "u":
        flight = flight_gen_normal(num_planes)
    if gen_type == "n":
        flight = flight_gen_uni(num_planes)
   
    m = Model("Bay Assignment")
    
    def time(lst):
        return int(lst[0]*60 + lst[1])
    
    def times(lst, early_buffer, late_buffer):
        for i in range(len(lst)):
            lst[i][5] = time(lst[i][5]) - early_buffer
            lst[i][6] = time(lst[i][6]) + late_buffer
        return lst

    flight = times(flight,15,30)
    flight = sorted(flight,key =lambda x: x[-3])
    final = [x for x in flight]
    
    ac_d_var = []
    for i in range(len(flight)):
        flight_lst = []
    
        for k in bays:
            preference = flight[i][1]
            preference_l = flight[i][4]
            flight_lst.append(m.addVar(vtype=GRB.BINARY, obj= int(dist[k][preference])*flight[i][-1]+ int(dist[k][preference_l])*flight[i][-1]))
        ac_d_var.append(flight_lst)
    
    bay_comp = []
    for i in range(len(flight)):
        bay_comp_lst = []
        for k in range(len(bays)):
            bay_comp_lst.append(m.addConstr(comp[bays[k]][ac_type[flight[i][2]]] >= ac_d_var[i][k]))
        bay_comp_lst.append(m.addConstr(quicksum(ac_d_var[i][k] for k in range(len(bays))) == 1))
        bay_comp.append(bay_comp_lst)
    
    
    for i in range(len(flight)):
        lst = []
        lst2 = []
        for o in range(len(flight)):
            if flight[i][5] <= flight[o][6] and flight[i][5] >= flight[o][5]:
                lst.append(ac_d_var[o])
            big = ["H","G","F"]
            if ac_type[flight[o][2]] in big and i!=o and flight[i][5] <= flight[o][6] and flight[i][6] >= flight[o][5]:
                lst2.append(ac_d_var[o])
                
        bay_comp2 = []
        for k in range(len(bays)-1):
            if len(lst) > 1:
                bay_comp2.append(m.addConstr(quicksum(lst[i][k] for i in range(len(lst))) <= 1))
            
        if lst2:
    
            for u in range(len(lst2)):
                bay_comp2.append(m.addConstr(lst2[u][14] + ac_d_var[i][23] <= 1))
                bay_comp2.append(m.addConstr(lst2[u][23] + ac_d_var[i][14] <= 1))
                bay_comp2.append(m.addConstr(lst2[u][22] + ac_d_var[i][28] <= 1))
                bay_comp2.append(m.addConstr(lst2[u][28] + ac_d_var[i][22] <= 1))
            
    
    m.setParam( 'OutputFlag', False )
    m.update()    
    m.optimize()
    
    
    for i in range(len(flight)):
        final[i] = final[i][1:]
        final[i].pop(2)
        final[i][1] = ac_type[final[i][1]]
        for k in range(len(bays)):
            if ac_d_var[i][k].X >0:
                final[i].append(bays[k])
                
    return final,m.objVal
