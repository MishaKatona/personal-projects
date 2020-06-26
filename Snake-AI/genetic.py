# -*- coding: utf-8 -*-

from snake_AI import snake
import random


def iteration(weights,runs,wait,side_len=10):
    fitnes = []
    scores = []
    for w in weights:
        fit = []
        avg_score = []
        for run in range(runs):
            count, score = snake(w,wait,side_len)
            avg_score.append(score)
            if score < 5:
                fit.append(-250 + count) # change to adjust how much it dislikes dying early
            else:
                fit.append(score*150 - count) # change to adjust reward
        fitnes.append(min(fit))
        scores.append(min(avg_score))
    return fitnes,scores

def index_(list1):
    rand = random.random()
    for i in range(len(list1)):
        if list1[i] >= rand:
            return i

def cross(weights,fitnes):
    weight1 = weights[index_(fitnes)]
    weight2 = weights[index_(fitnes)]
    
    first = random.randint(0,len(fitnes)-2)
    last = random.randint(first+1,len(fitnes))
    
    return weight1[:first] + weight2[first:last] + weight1[last:]
    
def evolution(weights,fitnes):
    
    minim = min(fitnes)
    fitnes = [x-minim for x in fitnes] #removes the lowest scoring by making it 0
    c = sum(fitnes)
    if c == 0:
        fitnes = [1/len(fitnes) for x in fitnes]
    else:
        fitnes = [x/c for x in fitnes]
    num = 0
    for i in range(len(fitnes)):
        num += fitnes[i]
        fitnes[i] = num
    crosses = random.randint(int(len(fitnes)*0.70),len(fitnes)-5)
    out = []
    max_index = fitnes.index(max(fitnes))
    out.append(weights[max_index]) #takes best of the pop and saves it
    for i in range(len(fitnes)-crosses-1): #takes random num and rulet wheel saves them
        out.append(weights[index_(fitnes)])
    for i in range(crosses):
        out.append(cross(weights,fitnes))
        
    for i in range(len(fitnes)):
        for o in range(len(weights[1])):
            r = random.randint(0,150) # change for mutation chance
            if r < 2:
                out[i][o] +=  random.randint(-2,2)*0.2 # change this for mutation amount
    out[0] = weights[max_index]
    return out

def init(pop,weight_interval,mid_layer=5): 
    weights = []
    num_conections = (2 + 5) * mid_layer # change this to adjust how many nodes there are in first and last layer
    for i in range(pop):
        weight = []
        for o in range(num_conections):
            weight.append((random.random()*(weight_interval[1]-weight_interval[0]))+weight_interval[0])
        weights.append(weight)
    
    return weights
        

            
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    
    
    