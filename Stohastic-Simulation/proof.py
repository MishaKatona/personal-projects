# -*- coding: utf-8 -*-

import random
import numpy as np

def pick_e(mu):
    rand_num = random.random()
    return -(1/mu)*np.log(rand_num)

num1 = []
num2 = []
for i in range(10000):
    x = []
    for o in range(25):
        x.append(pick_e(1))
    num1.append(min(x))
    z = pick_e(25)
    num2.append(z)

print(np.mean(num1))
print(np.mean(num2))