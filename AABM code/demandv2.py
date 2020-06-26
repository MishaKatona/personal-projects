# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 22:39:53 2020

@author: vande
"""

# This code generates the pseudorandom locations for the demand for the simulation
# Each tick with a probabilty it will return a location that is determied by 
# Normal distributions and uniform distributions

import numpy as np


def mapGenerator(gridSize, spawn_prob, peakCoordinates = False):
    if not peakCoordinates :
        peakCoordinates = [(350,350,10),(650,650,5)]

    if not spawn_prob:
        p = 1
    else:
        p = spawn_prob
        
    spawnOrNot  = np.random.binomial(1, p)
    # are we going to spawn
    if not spawnOrNot:
        order = False 
    else:          
        # draw first random variable for peak decision. Adding uniform distribution for 40% of the times 
        peakCoordinates     = np.array(peakCoordinates)
        strength            = peakCoordinates[:,-2]
        strength            = np.append(strength,(strength.sum()*2))    
        probabilities       = strength / strength.sum() 
        peakChoice          = np.random.choice(strength, p=probabilities)    
        
        # if draw from uniform distribution
        if peakChoice == strength[-1]:
            x_loc = np.random.uniform(0,gridSize[0])
            y_loc = np.random.uniform(0,gridSize[1])
        else:
            idx     = np.where(peakCoordinates == peakChoice)[0][0]  
            
            #random number: distance
            #dist = np.random.random() * variance
            
            dist = np.random.normal(160,70)
            
            if dist < 20 :
                dist = np.random.random() * 80
                
            #random number: which heading
            heading = np.random.random() * 2 * np.pi
        
            x_loc = peakCoordinates[idx][0] + (np.sin(heading)*dist)
            y_loc = peakCoordinates[idx][1] + (np.cos(heading)*dist) 
            
            #filter out the out of bounds
            if not 0 <= x_loc < gridSize[0]:
                x_loc = np.random.uniform(0,gridSize[0])
                y_loc = np.random.uniform(0,gridSize[1])
    
            if not 0 <= y_loc < gridSize[1]:
                x_loc = np.random.uniform(0,gridSize[0])
                y_loc = np.random.uniform(0,gridSize[1])
    
        order = x_loc,y_loc

    return (order)
    


