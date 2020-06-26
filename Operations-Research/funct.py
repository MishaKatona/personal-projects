import csv
import ast

def read_sim_data(file='Output.csv'):
    with open(file) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        all_data = []
        for row in readCSV:
            all_data.append(row)
    
    run_type = [all_data.pop(0)]
    
    
    data = []
    inter = []
    for i in range(len(all_data)):
        if len(all_data[i]) > 5:
            inter_data = []
            for o in range(len(all_data[i])):
                inter_data.append(ast.literal_eval(all_data[i][o]))
            inter.append(inter_data)
        elif len(all_data[i]) == 4 or len(all_data[i]) == 5:
            data.append(inter)
            inter = []
            run_type.append(all_data[i])
    else:
        data.append(inter)
        inter = []
    
    for i,val in enumerate(run_type):
        run_type[i] = [float(val[0]), int(val[1]), int(val[2]), val[3]]
    
    return data, run_type

def avg_walk(lst,dist):
    info = []
    for i in range(len(lst)):
        inf = []
        for o in lst[i]:
            inf.append([o[0],o[2],o[6],o[5]])
        info.append(inf)
        
    tot = []
    ppl = []
    for o in range(len(info)):
        t = 0
        p = 0
        for i in info[o]:
            t += (int(dist[i[2]][i[0]]) + int(dist[i[2]][i[1]])) * i[3]
            p += i[3]
        tot.append(t)
        ppl.append(p)
        
        avg = [x/y for [x,y] in zip(tot,ppl)]
        
    return avg,sum(tot)/sum(ppl)

def num_NA(lst):
    NA = []
    num = []
    for i in range(len(lst)):
        fl = 0
        nu = 0
        for o in lst[i]:
            nu += 1
            if o[6] == "N/A":
                fl += 1
        NA.append(fl)
        num.append(nu)
        
    return NA,[(x/y)*100 for [x,y] in zip(NA,num)]

def remove_NA(lst):
    new_lst = []
    for i in range(len(lst)):
        int_lst = []
        for o in lst[i]:
            if o[6] != "N/A":
                int_lst.append(o)
        new_lst.append(int_lst)
    return new_lst

def type_count(lst,dist):
    types = ["A","B","C","D","E","F","G","H"]
    walk = [0]*8
    NA = [0]*8
    count = [0]*8
    for i in lst:
        for o in i:
            for c,t in enumerate(types):
                if o[1] == t:
                    walk[c] += (int(dist[o[6]][o[0]]) + int(dist[o[6]][o[2]])) * o[5]
                    count[c] += o[5]
                    if o[6] == "N/A":
                        NA[c] += 1
    walk = [x/y for [x,y] in zip(walk,count)]
    return walk,NA,count        