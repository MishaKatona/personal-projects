# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 14:40:11 2019

@author: kater
"""
from data_reader import read_data
dist, comp, ac_type, bays = read_data()   
import random
import numpy as np

ac_types = []    
for key in ac_type:
    ac_types.append(key)
    
ac_types.sort()
ac_passengers = [160, 320, 45, 70, 170, 170, 170, 170, 520, 350, 350, 350, 280, 280, 110, 100, 80]
ac_num = list(zip(ac_types,ac_passengers))

ac_pax1 = []

for i in range(len(ac_passengers)):
    x = 1/(ac_passengers[i]+100)
    ac_pax1.append(x)
acpaxtot = sum(ac_pax1)

ac_pax2 = []
for i in range(len(ac_pax1)):
    ac_pax2.append(round(sum(ac_pax1[:i+1]),3))


def flight_gen_normal(n_flights):
    
    def actypes():
        y = random.random()*acpaxtot
        for i in range(len(ac_pax2)):
            if y < ac_pax2[i]:
                x = i + 1
                break
        ac = ac_types[x-1]
        pax = ac_passengers[x-1]
        return ac, pax
        
    def flightnumber():
        x = random.randint(0,900)
        arrival = 'KLM' + str(x)
        departing = 'KLM' +str(x+1)
        return arrival, departing
    
    def gates():
        gates = ['A', 'B', 'C', 'D']
        arrivalgate = gates[random.randint(0,3)]
        departinggate = gates[random.randint(0,3)]
        return arrivalgate, departinggate
        
    def times():
        y = random.randint(0,3)
        arrivalhour = np.random.normal(8+y*4,1)
        arrivalminute = random.randint(0,11)*5
        departinghour = arrivalhour + random.randint(1,2)
        departingminute = random.randint(0,11)*5
        return int(arrivalhour), arrivalminute, int(departinghour), departingminute
    
    flights = []
    for i in range(n_flights):
        x = flightnumber()
        t = times()
        y = actypes()
        flights.append([x[0], gates()[0], y[0], x[1], gates()[1], [t[0], t[1]], [t[2], t[3]], y[1]])
        
    return flights
        

def flight_gen_uni(n_flights):    
    def actypes():
        x = random.randint(0,16) + 1
        ac = ac_types[x-1]
        pax = ac_passengers[x-1]
        return ac, pax
        
    def flightnumber():
        x = random.randint(0,900)
        arrival = 'KLM' + str(x)
        departing = 'KLM' +str(x+1)
        return arrival, departing
    
    def gates():
        gates = ['A', 'B', 'C', 'D']
        arrivalgate = gates[random.randint(0,3)]
        departinggate = gates[random.randint(0,3)]
        return arrivalgate, departinggate
        
    def times():
        arrivalhour = 8 + random.randint(0,12)
        arrivalminute = random.randint(0,11)*5
        departinghour = arrivalhour + random.randint(1,2)
        departingminute = random.randint(0,11)*5
        return arrivalhour, arrivalminute, departinghour, departingminute
    
    flights = []
    for i in range(n_flights):
        x = flightnumber()
        t = times()
        y = actypes()
        flights.append([x[0], gates()[0], y[0], x[1], gates()[1], [t[0], t[1]], [t[2], t[3]], y[1]])
        
    return flights
        