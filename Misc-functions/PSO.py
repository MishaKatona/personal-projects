# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import random
import math
import mytools

def PSO(function,num_particles,num_iterations,dimention_limits):
    momentum = 0.85
    social_individual = 0.9
    social_increase = 0.005
    factor = 0.15
    dimention = len(dimention_limits)
    particles=[]
    if not particles:
        for o in range(num_particles):
            particle = []
            for p in dimention_limits:
                val = random.random() * (p[1] - p[0]) + p[0]
                particle.append(val)
            particle += [0] * dimention
            particle.append([])
            particle.append(0)
            particles.append(particle)
            
    plt.ion()
    ax = plt.gca()
    plt.xlim(dimention_limits[0])
    plt.ylim(dimention_limits[1])
    line, = ax.plot([x[0] for x in particles], [x[1] for x in particles], "yo")
    
    best = []
    
    
    for i in range(num_iterations):
        mytools.pbf(i,num_iterations)
        social_individual -= social_increase
        
        for particle in particles:
            val = function(particle[:dimention])
            particle[-1] = val
            if not particle[-2] or val > particle[-2][-1]:
                particle[-2] = particle[:dimention]+[val]
            if not best or best[-1] < val:
                best = particle[:dimention]+[val]

        best_a = np.array(best[:-1])
        for particle in particles:
            current_a = np.array(particle[:dimention])
            ind_best_a = np.array(particle[-2][:-1])
            best_v_a =  current_a - best_a 
            ind_best_v_a = ind_best_a - current_a 
            new_v = (best_v_a * (social_individual-1) + ind_best_v_a * (social_individual))*factor + momentum * np.array((particle[dimention:-2]))
            particle[dimention:-2] = list(new_v)
            pos_a = np.array(particle[:dimention])
            particle[:dimention] = list(pos_a + new_v)
            
        line.set_ydata([x[1] for x in particles])
        line.set_xdata([x[0] for x in particles])
        plt.draw()
        plt.pause(0.01)
        
        #if i > num_iterations - num_particles + 5:
        #    particles.pop(random.randint(0,len(particles)-1))
            
    #e = time.time()
        
    #print(best,"---",comp,"----",len(particles))
    #print(e-s, "for ",comp, " calculations")
    return best[:-1]

def func(lst):
    return abs(math.sin(lst[1]*lst[0]))*(1-abs(lst[0]*lst[1]))


x = PSO(func,100,200,[[-2,2],[-2,2]])
print(func(x))














