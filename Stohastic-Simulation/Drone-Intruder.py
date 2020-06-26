# -*- coding: utf-8 -*-

import random
import numpy as np
import matplotlib.pyplot as plt

# The key in the dictionary is the current room, and the value is the list of possible adjacent rooms
rooms = {1:[2], 2:[1,3], 3:[2,4,7], 4:[3,5], 5:[4,6,7,10], 6:[5,9], 7:[3,5,8], 8:[7,9], 9:[6,8], 10:[5]}

# Given the current room it chooses with equal probability an other room form the possible adjacent rooms
def path(current):
    lst = rooms[current]
    rand = random.random()
    for i in range(len(lst)):
        if rand <= (i+1)/len(lst):
            return lst[i]

# Given the current room it finds the time the intruder will spend in the room
def intruder_time(room):
    rand_num = random.random()
    return -(1 / np.sqrt((room+1)/10) ) * np.log(rand_num)

# When both parties move in a random manner, this function finds the times the intruder is found
def found_time(num_runs):
    found_time = []
    
    for i in range(num_runs):
        drone_pos = [7] # Drone starts in room 7
        intruder_pos = [9] # intruder starts in room 9
        
        t = 0 # Continous time counter for the intruder
        int_t = 0 # Intiger time counter for the drone
        found = False
        
        while not found: # Continue the simulation while the intruder is not found
            move_time = intruder_time(intruder_pos[-1]) # Find the time it takes for the intruder to move from the current room
            t += move_time
            
            while int(t) > int_t: # If the intruder waits in a room long enough then the drone will move a number of times before the intruder moves
                drone_pos.append(path(drone_pos[-1]))
                int_t += 1
                if drone_pos[-1] == intruder_pos[-1]: # If found break the while loop
                    found = True
                    found_time.append(int_t)
                    break
                
            if not found: # If not found by the drone move
                intruder_pos.append(path(intruder_pos[-1]))
                if drone_pos[-1] == intruder_pos[-1]: # If found break the while loop 
                        found = True
                        found_time.append(t)
        
    # Plot the histogram of being found
    plt.hist(found_time,bins=55, range=(0,55), density=True)
    plt.xlabel('Minutes')
    plt.ylabel('Probability')
    plt.title('Probability of the intruder being found by the drone ')
    plt.show()
    
    # Retrun the list of found times and its mean
    return found_time,np.mean(found_time)
    
# Finds the distribution of rooms the drone is in for each time point
def time_prob(num_runs):
    rooms_count = [[0]*10 for p in range(181)] # Set up for a counter ( for each room for each time point (180 min))
    
    for i in range(num_runs):
        drone_pos = 7
        rooms_count[0][6] += 1
        for o in range(1,181):
            drone_pos = path(drone_pos)
            rooms_count[o][drone_pos-1] += 1 # Add one to wherever the drone is for each time point
    
    # Return the probability of being in a room for each time point
    return np.array(rooms_count)/num_runs

# Generates the best path for the intruder, it moves at the same rate as the drone
# Used to find the best path, but best path now has a hard coded path so this function is redundant
def best_path():
    pos = [9,6,5,4,3,2,1] # The longest possible route where the intruder cannot be found
    for i in range(7,181):
        if i % 2 == 0: # Alternate between room 1 and 2 untill time runs out
            pos.append(1)
        else:
            pos.append(2)  
    # Retrun the path to be followed by the intruder
    return pos

# Finds the time untill the intruder is found if the best path is followed
def found_time_inteligent(num_runs,b_path):
    found_time = []
    
    for i in range(num_runs):
        drone_pos = 7
        
        # The drone moves through the rooms randomly and if its position is the same as the intruder then it found him
        for o in range(181):
            if drone_pos == b_path[o]:
                found_time.append(o)
                break
            drone_pos = path(drone_pos)
        
    
    # Plot the histogram of the time untill being found
    plt.hist(found_time,bins=180, range=(0,180), density=True, color = (1,0.4,0.4))
    plt.show()
    
    # Return the list of times untill being found, and the mean time
    return found_time,np.mean(found_time)


found_lst_r,found_mean_r = found_time(100000)
array = time_prob(100000) # this line creats the 180x10 array for where the drone is 
b_path = best_path()
#found_lst, found_mean_smart = found_time_inteligent(100000,b_path)
#print("not found %",(1-len(found_lst)/100000)*100)





    