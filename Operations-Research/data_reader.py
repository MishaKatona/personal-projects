# -*- coding: utf-8 -*-

def read_data():
    
    with open("data.txt") as file:
        data = file.read()
        
    data = data.replace("\n"," ")    
    data = data.split("  ")
    
    for i in range(len(data)):
        data[i] = data[i].split(" ")
    
    bay_dist = data[:3]
    bay_compliance = data[3:]
    
    bays = bay_dist[1][::2]
    add_bays = bay_dist[1][1::2]
    
    
    bay_distances = {}
    for i in range(len(bays)):
        bay_distances[bays[i]] = {"A":add_bays[i], "B":bay_dist[2][i*3],
                                  "C":bay_dist[2][i*3+1], "D":bay_dist[2][i*3+2]}
        
    bays_comp = bay_compliance[9][::2]
    comp = [[int(y) for y in x] for x in bay_compliance[9][1::2]]
    
    compliance = {}
    for i in range(len(bays_comp)):
        compliance[bays_comp[i]] = {}
        for o in range(len(comp[0])):
            compliance[bays_comp[i]].update({bay_compliance[0][o+2]:comp[i][o]})
            
    ac_type = {}
    for i in range(1,9):
        for o in range(len(bay_compliance[i])):
            ac_type[bay_compliance[i][o]] = bay_compliance[0][i+1]
            
    keys_dist = set(bay_distances.keys())
    keys_comp = set(compliance.keys())
    sec = keys_dist & keys_comp
    
    out1 = {}
    for key in bay_distances:
        if key in sec:
            out1[key] = bay_distances[key]
    
    out2 = {}
    for key in compliance:
        if key in sec:
            out2[key] = compliance[key]
        
            
    return out1, out2, ac_type, list(sec)

#dist, comp, ac_type, sort = read_data()


    
    
