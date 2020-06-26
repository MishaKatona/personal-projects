# -*- coding: utf-8 -*-

import random
import numpy as np
import matplotlib.pyplot as plt

def pick_e(mu):
    rand_num = random.random()
    return -(1/mu)*np.log(rand_num)

num_drones = 5
nd = num_drones

w_d = {}
r_d = []

for i in range(num_drones):
    w_d[i] = pick_e(1)

times = [0]*(nd+1)
num_repair = []
repair_t = 0

t = 0
ot = 0
for i in range(100000):
    nxt_w = min(w_d.items(),key= lambda x: x[1], default=0)
    nxt_r = repair_t
    if nxt_w and (nxt_w[1] < nxt_r or not nxt_r):
        t = nxt_w[1]
        r_d.append(nxt_w[0])
        w_d.pop(nxt_w[0])
        if len(r_d) == 1:
            repair_t = t + pick_e(2)
    else:
        q = r_d.pop(0)
        t = nxt_r
        w_d[q] = t + pick_e(1)
        repair_t = t + pick_e(2)
        if len(r_d) == 0:
            repair_t = 0
    num_repair.append(len(r_d))
    times[len(r_d)] += t - ot
    ot = t
    
print(np.mean(num_repair))

ts = [round(x/t,5) for x in times]

array = [[0]*(nd+1) for x in range(nd+1)]
for i in range(nd+1):
    if i > 0:
        array[i][i-1] = 2
    array[i][i] = -(2 +1*(nd-i))
    if i == 0:
        array[i][i] = -(nd-i)
    if i < nd:
        array[i][i+1] = (nd-i)*1

x = np.array(array)

A=np.append(np.transpose(x),[[1]*(nd+1)],axis=0)
b=np.transpose(np.array([0]*(nd+1)+[1]))
y = np.linalg.solve(np.transpose(A).dot(A), np.transpose(A).dot(b))


print("occurence prob\t time sim\t stationary d\t difference")
for i in range(nd+1):
    print(i,":",num_repair.count(i)/100000,"\t",ts[i],"   \t",round(y[i],5),"   \t delta:",round(100*abs(ts[i]-y[i])/y[i],3),"%")

plt.plot(range(0,nd+1),ts,"o",color='red', alpha=0.5,label="MC sim")
plt.plot(range(0,nd+1),y,"o",color='blue', alpha=0.5,label="SD")
plt.legend()
plt.show()

        