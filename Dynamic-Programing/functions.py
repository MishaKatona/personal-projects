# -*- coding: utf-8 -*-

import csv
import math

# Formats the csv file that is the coppy of the xls file and returns an other csv


# Reads and formats the data form all_data csv file
def read_data(file_name="All_data.csv"):
    all_data = []
    
    # reads the data into all_data list
    with open(file_name) as file:
        data = csv.reader(file)
        for line in data:
            all_data.append(line)
        file.close()
        
    # get the data for each of the 3 planes form all_data (i forgot what prp is supposed to be) 
    prp = [[float(y) for y in x] for x in all_data[45:55]]
        
    # creat a dictionary for the planes and thir charachteristics
    ac = {}
    for i in range(3):
        ac[i+1] = {"speed":prp[0][i], "seats":prp[1][i], "TAT":prp[2][i],
                         "range":prp[3][i], "rwr":prp[4][i], "lease":prp[5][i],
                         "fixed_o_c":prp[6][i], "time_c":prp[7][i], "fuel_c":prp[8][i],
                         "fleet":prp[9][i]}
        
    # get the demand form A1 and dist values from the all_data list
    demand = [[int(y[:-2]) for y in x] for x in all_data[0:20]]
    dist = [[int(y) for y in x] for x in all_data[24:44]]
    
    # creat a dictionary that has the runway lengths and the hourly demand
    loc = {}
    for i in range(20):
        loc[i] = {"rwl":int(all_data[22][i][:-2])}
        
    for i in range(56,76):
        loc[i-56].update({"h_d":[float(x) for x in all_data[i][1:]]})
        
    # creat a compliance matrix that shows how long it take a plane to go form airport to airport
    # It appends 1 for cases where it stays (as opposed to 0 for flights it cannot make)
    ac_comp = []
    for ac_type in range(1,4):
        ac_m = []
        for loc1 in range(20):
            row = []
            for loc2 in range(20):
                if ac[ac_type]["rwr"] <= loc[loc1]["rwl"] and ac[ac_type]["rwr"] <= loc[loc2]["rwl"] and \
                ac[ac_type]["range"] > dist[loc1][loc2] and loc1 != loc2:
                    # the time it flies x 10 (as this time is given in hours) + the TAT /6 as tat is given in min
                    # + half an hour from the assigment 30 / 6 = 5
                    time = (dist[loc1][loc2]/ac[ac_type]["speed"])*10 + ac[ac_type]["TAT"]/6 + 5 
                    row.append(math.ceil(time))
                elif loc1 == loc2:
                    row.append(1)
                else:
                    row.append(0)
            ac_m.append(row)
        ac_comp.append(ac_m)
        
    # Creats a matrix for each plane where the possible profit for each route is added
    ac_profit = []
    for ac_type in range(1,4):
        ac_m = []
        for loc1 in range(20):
            row = []
            for loc2 in range(20):
                if ac[ac_type]["rwr"] <= loc[loc1]["rwl"] and ac[ac_type]["rwr"] <= loc[loc2]["rwl"] and \
                ac[ac_type]["range"] > dist[loc1][loc2] and loc1 != loc2:
                    # check the function to see what it returns
                    row.append(profit(ac_type,loc1,loc2,dist,ac))
                else:
                    row.append(0)
            ac_m.append(row)
        ac_profit.append(ac_m)
    
    # returns the demand from A1, a dictionary with runway lengts and hourly demand,
    # compliance matrix for each plane that gives how long it takes to get form one place to another,
    # a matrix that gives the profit for each ac, and a dictionary for each ac
    return demand, loc, ac_comp, ac_profit, ac, dist


# converts the given hourly demand float and the demand form A1 to hourly demands
def h_demands(demand,loc):
    tot_demands = []
    
    for t in range(24):
        time = []
        for i in range(20):
            row = []
            for j in range(20):
                dem = loc[i]["h_d"][t]
    
                row.append(int(dem*demand[i][j]))
            time.append(row)
        tot_demands.append(time)
        
    return tot_demands

# takes the hourly demand and takes into account the +1,0,-1,-2 hours demand that is captured
# for each hour, so it gives the maximum number of people that are willing to fly at that time
def tot_h_dems(h_demand):
    tot_demands = []
    
    for t in range(24):
        time = []
        for i in range(20):
            row = []
            for j in range(20):
                if i == 0 or j == 0:
                    dem = h_demand[t][i][j] # take current hour into account
                    if t >= 2 and t <= 24:
                        dem += h_demand[t-2][i][j] # take hour -2 into account
                    if t >= 1 and t <= 24:
                        dem += h_demand[t-1][i][j] # take hour -1 into account
                    if t <= 22:
                        dem += h_demand[t+1][i][j] # take hour +1 into account
                else:
                    dem = 0
    
                row.append(int(dem))
            time.append(row)
        tot_demands.append(time)
        
    return tot_demands

                
# returns a tuple with the revenue and the cost (the revenue is per passenger)
def profit(ac_type,loc1,loc2,dist,ac):
    # as london is our hub (which is 1st in the list) the 1st item is 0.7 which is the 
    # 30% cost decrease from assigment one
    cost = [0.7] + [1]*19
    # cost of flying is given by the fixed cost, time cost and fuel cost times 0.7 for hub and 1 for non-hub
    c = (ac[ac_type]["fixed_o_c"] + (dist[loc1][loc2] / ac[ac_type]["speed"]) * ac[ac_type]["time_c"] +
          dist[loc1][loc2]*ac[ac_type]["fuel_c"]*(1.42/1.5))*cost[loc1]*cost[loc2]
    r = (5.9*(dist[loc1][loc2]**(-0.76))+0.043)*dist[loc1][loc2]
#    if r * ac[ac_type]["seats"] - c < 0:
#        return 0
    return [round(r,2),round(c,2)]

# returns an hourly profit matrix for an ac type for each possible route
def h_profits(h_demand,ac_profit,ac_type,ac):
    prof = []
    for i in range(len(h_demand)):
        lst = []
        for o in range(20):
            row = []
            for j in range(20):
                # get the profit, cost tuple
                x = ac_profit[ac_type-1][o][j]
                # get the total demand for that hour
                dem = h_demand[i][o][j]
                # if demand is larger than the capacity then demand is set to the number of seats
                if dem >= ac[ac_type]["seats"]:
                    dem = ac[ac_type]["seats"]
                # if profit tuple isnt 0 (so its profitable) then set revenue to the
                # number of seats used * profit/passenger - cost
                if x:
                    revenue = round(x[0]*dem - x[1],2)
                # return 0 if not profitable (could also mean staying in place)
                else:
                    revenue = 0.0
                # if the number of people is not enough to make it profitable return empty string
                # gives slight performance improvement (if commented then unprofitable routes are also considered)
#                if revenue < 0:
#                    revenue = ""
                row.append(revenue)
            lst.append(row)
        prof.append(lst)
    return prof
            
# find the next possible destinations and how long it will take to get there
def find_next(current,comp,ac_type):
    # -1 is needed because then comp list starts at 0 but first ac starts at 1
    lst = comp[ac_type-1]
    options = []
    # if the hub then all possible locations are available
    if current == 0:  
        for o in range(len(lst[current])):
            if lst[current][o]:
                # destination, time to destination
                options.append((o,lst[current][o]))
    # if not the hub the only destination is the hub
    else:
        options.append((0,lst[current][0]))
    return options
    
# simple function that gets the profit of a route given the current location, destination and time
def get_prof(h_profit, dtime, current, destination):
    dtime = int(dtime/10)
    return h_profit[dtime][current][destination]

# turns the hourly profits into  per 6 min profits 
def tot_profits(h_profit):
    
    all_nodes = []
    for t in range(240):
        matrix = []
        for i in range(20):
            row = []
            for o in range(20):
                x = get_prof(h_profit, t, i, o)
                row.append(x)
            matrix.append(row)
        all_nodes.append(matrix)
        
    return all_nodes

# update the hourly demand (not tot)
def update_demand(h_demand, path, comp, ac, ac_type):
    # get the flight schedule (fs) for the best path
    fs = []
    past = 0
    t = -1
    for i in path:
        # if the current location is the same as the past step then it did not move
        # so add one to the time (still on the 6 min intervall)
        if i == past:
            t += 1
        else:
            fs.append([t,past,i])
            t += comp[ac_type-1][past][i]
            past = i
    
    # using the flight schedule substract the number of people flying on a route
    # taking into account the +1,0,-1,-2 demands
    ts = [0,-1,1,-2]
    for i in fs:
        removed = 0
        seats = ac[ac_type]["seats"]
        t = int(i[0]/10)
        for o in ts:
            # if the number of seats still availabe is larger than the demand
            # remove the demand from that hour and decrease the available seats
            if seats >= h_demand[t+o][i[1]][i[2]]:
                seats -= h_demand[t+o][i[1]][i[2]]
                removed += h_demand[t+o][i[1]][i[2]]
                h_demand[t+o][i[1]][i[2]] = 0
            # if the demand is more than the number of seats 
            # substract the last availabe seats from the demand and stop
            else:
                h_demand[t+o][i[1]][i[2]] -= int(seats)
                removed += int(seats)
                break
        i.append(removed)
        
    #retunr the new hourly demand after the best flight and the flight schedule of it
    return h_demand, fs

# get the block time that the ac spends in the air because of the (min 6 hour requirement)
def block_time(paths,comp,ac_type,ac):
    flight_t = 0
    past = 0
    for i in paths[239][0]["path"]:
        if i != past:
            flight_t += comp[ac_type-1][past][i] - math.ceil(ac[ac_type]["TAT"]/6)# include this if part c is part of block time + 5)
            past = i
    return flight_t

# helper function for the plotting
def plot_help(path, comp, ac_type):
    
    times = [0]
    pos = [0]
    past = 0
    t = -1
    for i in path:
        # if the current location is the same as the past step then it did not move
        # so add one to the time (still on the 6 min intervall)
        if i == past:
            t += 1
        else:
            if times[-1]+1 != t:    
                times.append(t)
                pos.append(past)
            t += comp[ac_type-1][past][i]
            times.append(t)
            pos.append(i)
            past = i
    times.append(239)
    pos.append(0)
    return times, pos

def kpis(final_paths, ac, dist, ac_prof):
    ask, rpk, num_p, num_s, tot_c, tot_p = 0, 0, 0, 0, 0, 0
    for i in final_paths:
        for o in i["fs"]:
            d = dist[o[1]][o[2]]
            seats = ac[i["ac"]]["seats"]
            used = o[3]
            ask += d*seats
            rpk += d*used
            num_p += used
            num_s += seats
            tot_c += ac_prof[i["ac"]-1][o[1]][o[2]][1]
        tot_c += ac[i["ac"]]["lease"]
        tot_p += i["prof"]
    cask = tot_c/ask
    rask = (tot_p+tot_c)/ask
    rrpk = (tot_p+tot_c)/rpk
        
    return ask,rpk,num_p/num_s,cask,round(rask,4),round(rrpk,4)
            
            
    
    








