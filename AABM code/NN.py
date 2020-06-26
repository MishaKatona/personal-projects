# -*- coding: utf-8 -*-

# This file is responible for all learning related functions, the neural network
# The evolutionary algorith and all its necesarry functions, as well as the 
# PWA (positive weight augmentation which boosts weights along a gradient)

import numpy as np
import random

# this gives the resposnse of a preceptron to the sum of inputs (maps -inf,inf to -1,1)
def sigmund(value):
    return ((1/(1 + np.exp(-value)))*2)-1


# This takes the input vector and weights list (weights list contains a list of 2d matrexies that describe how its conected)
def NN(weights, inputs): # each row represents the weight to each of the preceptrons
    biases = weights[-1][0]
    bias_idx = 0
    for idx,w in enumerate(weights[:-1]):
        bias_end_idx = bias_idx + w.shape[0]
        inputs = sigmund(np.dot(w,inputs)-biases[bias_idx:bias_end_idx])
        bias_idx = bias_end_idx
    return inputs

# from this point on its the evulutionary network

# Takes all the weights and with a certain probability it will add or substract a random amount that is between -mut_amm,mut_amm
def rand_mutation(flat_weights, mutation_rate, muation_ammount):
    for fw in flat_weights:
        done = False
        mutation_index = 0
        while not done:
            mutation_index += int(np.random.exponential(mutation_rate))
            if mutation_index >= len(fw):
                done = True
                break
            fw[mutation_index] += (random.random()*muation_ammount*2)-muation_ammount
    return flat_weights

# Basically cross mutation
# Takes the scores and "mates" more sucesfull "agents" more frequently than ones with low scores
# it swaps random parts of their weights between the "mom" and "dad" to creat two offsprings
def death_roulette(weights, sim_scores):
    min_score = min(sim_scores)
    max_score = max(sim_scores)
    accum_scores = [0]
    for score in sim_scores:
        accum_scores.append(score+accum_scores[-1]-(0.3*min_score))
    
    tot_score = accum_scores[-1]
    new_weights = []
    while len(new_weights)+2 < len(weights):
        dad_score = random.random()*tot_score
        mom_score = random.random()*tot_score
        
        for idx, s in enumerate(accum_scores):
            if s >= dad_score:
                dad = weights[idx-1]
                break
        
        for idx, s in enumerate(accum_scores):
            if s >= mom_score:
                mom = weights[idx-1]
                break
            
        len_weight = len(weights[0])
        cut1 = random.randint(0, len_weight-2)
        cut2 = random.randint(cut1, len_weight-1)
        
        dad_cut = dad[cut1:cut2]
        mom_cut = mom[cut1:cut2]
        
        dad = np.concatenate([dad[0:cut1],mom_cut,dad[cut2:]])
        mom = np.concatenate([mom[0:cut1],dad_cut,mom[cut2:]])
        
        new_weights.append(dad)
        new_weights.append(mom)
     
    new_weights.append(weights[sim_scores.index(max_score)])
    new_weights.append(weights[sim_scores.index(max_score)])
        
    if len(new_weights) > len(weights):
        new_weights.pop(-1)
        
    return new_weights

# takes the weights and flattens them down to a 1d array so that I can do the random mutation and the cross "breeding" easily
def flatten_concat(weights):
    flat_weights = []
    for w in weights:
        lst = [x.flatten() for x in w]
        flat = np.concatenate(lst)
        flat_weights.append(flat)
    return flat_weights

# takes the flat weights and turns it back into a list of numpy arrays        
def unflatten(weights,shape):
    out = []
    for w in weights:
        weight = []
        idx = 0
        for s in shape:
            lenght = s[0]*s[1] + idx
            weight.append(w[idx:lenght].reshape(s))
            idx += s[0]*s[1]
        out.append(weight)
    return out

# main loop of the evulutionary learning
def darwin_was_right(weights, sim_scores, mutation_rate):

    matrix = weights[0]
    shape = []
    for m in matrix:
        shape.append(m.shape)
        
    flat_weights = flatten_concat(weights)
    
    new_weights = death_roulette(flat_weights, sim_scores)
    
    final_weights = rand_mutation(new_weights,mutation_rate,0.3)
    
    return unflatten(final_weights, shape)

def return_best(weights,scores):
    best = (0,0)
    for idx,s in enumerate(scores):
        if s >= best[0]:
            best = (s,idx)
            
    return weights[best[1]],best[0]
        
    
def gen_weights(pop,shape):
    weights = []
    for i in range(pop):
        weight = []
        num_biases = 0
        for s in shape:
            w = np.random.rand(s[0],s[1])
            weight.append((w*2)-1)
            num_biases += s[1]
        weight.append((np.random.rand(1,num_biases)*2)-1)
        weights.append(weight)
    return weights

def weightBooster(scoresOld, scoresCurrent, weightsCurrent, weightsOld, improveThreshold,boost):
    matrixCurrent = weightsCurrent[0]
    shapeCurrent = []
    for m in matrixCurrent:
        shapeCurrent.append(m.shape)   
    
    weightsCurrent  = flatten_concat(weightsCurrent)
    weightsOld      = flatten_concat(weightsOld)
    
    #replace all zero entries in scores with 0.1 (to avoid devision by zero)
    scoresOld = [0.1 if x == 0 else x for x in scoresOld]
    
    idxChange       = [True if (current_i-old_i)/old_i > improveThreshold else False for current_i, old_i in zip(scoresCurrent, scoresOld)]
    weightsDiff     = [boost*(current_i - old_i) for current_i,old_i in zip(weightsCurrent, weightsOld)]
    weightsBoost    = [current_i*boost for current_i, change_i in zip(weightsDiff,idxChange) if change_i == True]    
    
    #also make where the boosted weights are popped. Thist list will go into the evolutionary algorithm
    weightsNoBoost  = [current_i for current_i, change_i in zip(weightsCurrent,idxChange) if change_i == False]   
    scoresNoBoost   = [current_i for current_i, change_i in zip(scoresCurrent,idxChange) if change_i == False] 
    
    weightsNoBoost  = unflatten(weightsNoBoost,shapeCurrent)
    weightsBoost    = unflatten(weightsBoost,shapeCurrent)

    return idxChange, weightsBoost, weightsNoBoost, scoresNoBoost, shapeCurrent

def merging(idxChange, weightsNoBoost,weightsBoost,shapeCurrent):

    for idx,value in enumerate(idxChange):
        if value:
            weightsNoBoost.insert(idx, weightsBoost[0])
            weightsBoost.pop(0)
            
    return weightsNoBoost


def weightBoosterv2(scoresOld, scoresCurrent, weightsCurrent, weightsOld, threshold,boost,percentageBoost):
    matrixCurrent = weightsCurrent[0]
    shapeCurrent = []
    scoresTrue = [] 
    
    maxBoostCount = int(percentageBoost * len(weightsCurrent))
    if maxBoostCount == 0 :
        maxBoostCount = 1 
        
    for m in matrixCurrent:
        shapeCurrent.append(m.shape)   
    
    weightsCurrent  = flatten_concat(weightsCurrent)
    weightsOld      = flatten_concat(weightsOld)
    
    idxTrue       = [] 
    weightsBoost    = [] 
    for idx_c, (weight_c, scores_c) in enumerate(zip(weightsCurrent, scoresCurrent)):
        for idx_o, (weight_o, scores_o) in enumerate(zip(weightsOld, scoresOld)):
            
            meanDiff = np.mean(weight_c - weight_o)          
            sumDiff = np.sum(abs(weight_c - weight_o))
            scoreDiff = scores_c - scores_o
                
            if 0 < abs(meanDiff) < threshold[0] and abs(sumDiff) < threshold[1] and scoreDiff > threshold[2]:
                scoresTrue.append(scoreDiff)
                idxTrue.append(idx_c)
                weightsBoost.append(weight_c + ((weight_c - weight_o) * boost))

    #select the indices of the maxBoostCount highest scores. 
    if len(scoresTrue) >= maxBoostCount: 
        ind             = np.argpartition(scoresTrue, -maxBoostCount)[-maxBoostCount:]
    else: 
        ind = []
        
    weightsBoost    = [i for j, i in enumerate(weightsBoost) if j in ind] 
    idxTrue         = [i for j, i in enumerate(idxTrue) if j in ind] 

    weightsNoBoost  = [i for j, i in enumerate(weightsCurrent) if j not in idxTrue] 
    scoresNoBoost   =  [i for j, i in enumerate(scoresCurrent) if j not in idxTrue] 
    idxChange       = [True if j in idxTrue else False for j,i in enumerate(weightsCurrent)]

    weightsNoBoost  = unflatten(weightsNoBoost,shapeCurrent)
    weightsBoost    = unflatten(weightsBoost,shapeCurrent)

    return idxChange, weightsBoost, weightsNoBoost, scoresNoBoost, shapeCurrent

