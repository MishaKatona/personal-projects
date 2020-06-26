# -*- coding: utf-8 -*-

# This file is responsible for the learning, it contains the main loop as well 
# As the evolutionary algorithm and the PWA, the code outputs the best performing
# Weight list for a given fitness function 

# The final weights are stored in the lst_weights list

import run_logic as rl
import NN
import mytools
import time
import matplotlib.pyplot as plt

# Input parameters
size = (1000,1000)
num_iterations = 50
pop_count = 5
sim_lenght = 1000
NN_shape = [(5,6),(5,5),(1,5)] # (out,in)
spawn_prob = 0.15
threshold   = (0.1,15,0.5) #mean, sumdiff, score 
boost       = 1.05
percentageBoost = 0.1



weightsOld  = 0
scoresOld   = 0

weights = NN.gen_weights(pop_count,NN_shape)

x,y,z = [0],[0],[0]

plt.ion()
ax = plt.gca()
plt.title("Model performance during learning")
plt.xlabel("Number of runs")
plt.ylabel("Model performance")
plt.rcParams.update({'font.size': 14})
xmax = 5
ymax = 1
plt.xlim(0, xmax)
plt.ylim(0, ymax)
line, = ax.plot(x, y, "ro-",)
line2, = ax.plot(x,z,"bo-")
best = [0,0]

#storing for Didier 
# weightLst = [] 
# scoresLst = []

for i in range(num_iterations):
    mytools.pbf(i,num_iterations)
    scores = []
    jobs_not_comp = 0
    
    fin = 0
    
    for p in range(pop_count):
                  
      
        jobs_a = []
        jobs_c = [] 
        
        drones, restaurants, chargers, jobs_na = rl.gen_agents(size,7,[[300,300],[450,400],[700,500],[550,700]],False,9,False)
        t = 0
        run = True
        while run:

            jobs_na, jobs_a, jobs_c, slow = rl.main_loop(drones, restaurants, chargers, jobs_a, jobs_na, jobs_c, t, spawn_prob, size, False, weights[p])
            
            if slow:
                run = False
                break

            t += 1
            if t == sim_lenght:
                run = False
            
        if t == sim_lenght:
            utilisation = []
            delay = []
            for d in drones:
                utilisation.append(d.utilised_counter/sim_lenght)
                delay.append(d.order_delay)
            utilisation = sum(utilisation)
            delay = sum(delay)
        else:
            utilisation = 0
            delay = 10000000000
            
        delay_jna = sum([sim_lenght - x.complete_time for x in jobs_na])
        delay_ja = sum([sim_lenght - x.complete_time for x in jobs_a])
        
        fin += len(jobs_na+jobs_a)
        
                
        
        # Definition of the fitness function
        scores.append(1/(delay + delay_ja + delay_jna + 10)*10000)
        #scores.append(utilisation*100/7 + 1/(delay + delay_ja + delay_jna)*200000)
    
    best_w = NN.return_best(weights,scores)
    if best_w[1] >= best[1] and i > num_iterations/2:
        best = best_w
        
    #here i first boost the high scoring weights. then subset into darwin was right
    if i != 0:
        idxChange, weightsBoost, weightsNoBoost, scoresNoBoost,shapeCurrent = NN.weightBoosterv2(scoresOld, scores, weights, weightsOld, threshold,boost,percentageBoost)
    else:
        weightsNoBoost  = weights
        scoresNoBoost   = scores 
        
    weightsNoBoost     = NN.darwin_was_right(weightsNoBoost, scoresNoBoost, 80)
    
    if i != 0: 
        weights      = NN.merging(idxChange, weightsNoBoost,weightsBoost,shapeCurrent)
    else:
        weights = weightsNoBoost
        


    weightsOld = weights
    scoresOld  = scores
    
    max_score = max(scores)
    avg_score = sum(scores)/len(scores)


    xmax+=1
    x.append(x[-1]+1)
    y.append(max_score)
    z.append(avg_score)

    if y[-1]+1 > ymax:
        ymax = y[-1]+1
    plt.xlim(0, xmax)
    plt.ylim(0, ymax)
    line.set_ydata(y)
    line.set_xdata(x)
    line2.set_ydata(z)
    line2.set_xdata(x)
    plt.draw()
    plt.pause(0.1)
    
lst_weights = []
for i in best[0]:
    lst_weights.append(i.tolist())
    

        
        
            
