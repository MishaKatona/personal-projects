# -*- coding: utf-8 -*-

def neuron(inputs,weights):
    tot = sum([x*y for [x,y] in zip(inputs,weights)])
    if tot > 0:
        return 1
    return 0
    

def MLP(weights,inputs):
    mid = int(len(weights)/7) # change this if num of input output changes
    mid_out = []
    final_out = []
    for i in range(0,len(weights)-2*mid,5): #change also
        mid_out.append(neuron(inputs,weights[i:i+5])) #change this also
    for o in range(len(weights)-2*mid,len(weights),mid):
        final_out.append(neuron(mid_out,weights[o:o+mid]))
    
    return final_out[0], final_out[1]
        

        
    