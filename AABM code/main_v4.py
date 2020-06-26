# -*- coding: utf-8 -*-

# Main code for the simulatoin, here the drones, jobs, resturants are defined
# As well as their interactions, as well as the score generation for both the neural network
# And the simple model along with the hungarian algorithm that finds the optimum allocation

import math
import random
import numpy as np
from scipy.optimize import linear_sum_assignment
import NN

# Drone class is resposible for moving the drone agent as well as setting/ changing
# The jobs that it is assigned form the hungarian algorithm
class drone(object):
    
    vel = 20
    bat_drain = 0.5
    bat_charge = 0.5
    startChargeThreshold = 100
    tot_range = (100/bat_drain)*vel
    
    def __init__(self, loc, drone_id):
        self.loc = loc
        self.drone_id = drone_id
        self.battery = 100
        self.job = 0
        self.move = []
        self.move_count = 0
        self.order_delay = 0
        self.utilised_counter = 0
        self.chargeThreshold = self.startChargeThreshold

    
    def dist(self, dest):
        sq = (self.loc[0]-dest[0])**2 + (self.loc[1]-dest[1])**2
        return math.sqrt(sq)
        
    def find_move_to_goal(self):
        x = self.job.wp[0] - self.loc[0]
        y = self.job.wp[1] - self.loc[1]
        g_ang = math.atan2(x,y)
        self.move = [self.vel * math.sin(g_ang),self.vel * math.cos(g_ang)]
        self.move_count = int((self.dist(self.job.wp) / self.vel) + 1) # this is so that if the required steps are 7.8 it will require 8
        
    def find_battery_range(self):
        return (self.battery / self.bat_drain ) * self.vel
    
    def set_job(self, job):
        self.job = job
        self.job.assign_job(self.drone_id)
        self.find_move_to_goal()
        
    def set_charger(self,charger):
        self.job = charger
        self.find_move_to_goal()
                        
    def move_to_goal(self,time,chargers):
        if self.job:
            if self.move_count == 0:
                self.loc[0] = self.job.wp[0]
                self.loc[1] = self.job.wp[1]
                if self.job.job_type == 1:
                    if self.job.update_job(time):
                        self.order_delay += time - self.job.complete_time
                        self.find_move_to_goal()
                    if self.job.state == 3:
                        self.job = 0
                elif self.job.job_type == 2:
                    if self.battery*10 < 1000:
                        self.battery += self.bat_charge
                        self.utilised_counter += 1                        
                    else:
                        self.job = 0
            elif self.battery >= 0:
                self.loc[0] += self.move[0]
                self.loc[1] += self.move[1]
                self.move_count -= 1
                self.battery -= self.bat_drain
                if self.job.state == 2:
                    self.utilised_counter += 1
        else:
            self.move_to_charger(chargers)
            
            
    def closest_charger(self,chargers):
        #find closest charger; chargers is a list of all available chargers
        closestCharge = (10000, False)
        for i in chargers:
            distToCharge = self.dist(i.wp)
            if distToCharge < closestCharge[0]:
                closestCharge = (distToCharge,i)
                
        return closestCharge 
    
    def move_to_charger(self,chargers):
        closestCharge = self.closest_charger(chargers)        
        #range of battery 
        battRange = self.find_battery_range()
        #check how much battery range is left if drone moves to closest charging station
        rangeLeft = battRange - closestCharge[0]
        
        #if range is below certain treshold than find and move to charger
        if rangeLeft < self.chargeThreshold: 
            self.chargeThreshold = self.startChargeThreshold
            self.set_charger(closestCharge[1])
        elif self.chargeThreshold: 
            self.chargeThreshold += 50
 
# Charger class just saves the location of the chargers that are initially set               
class charge(object):

    def __init__(self,loc):
        self.wp = loc
        self.job_type = 2
        self.state = 4
        
# The job object is the jobs that individual custumers require to be completed
# This inclueds the location of the resturant as well as the custumer, the class
# Is also responsible to change the state of the job as it gets assigned, the order
# Picked up, and then delivered
class job(object):
    
    @staticmethod
    def find_distance(loc1, loc2):
        sq = (loc1[0]-loc2[0])**2 + (loc1[1]-loc2[1])**2
        return math.sqrt(sq)
        
    def __init__(self, cust_loc, resturant, order_time, prep_time, cust_to_charg):
        self.cust_loc = cust_loc
        self.resturant = resturant
        self.order_time = order_time
        self.prep_time = prep_time
        self.cust_to_charg = cust_to_charg 
        self.rest_to_cust = self.find_distance(resturant.loc, cust_loc)
        self.wp = [resturant.loc[0],resturant.loc[1]]
        self.state = 0
        self.job_type = 1
        self.complete_time = 0
        self.deliveryStart = 0 #added for KPI delivery time
        self.deliveryTime = 0 #added for KPI delivery time
        self.resturant.add_order(self)
        
    def assign_job(self,drone_id):
        self.state = 1
        self.drone_id = drone_id
        
    def update_job(self,time):
        if self.state == 1 and self.complete_time <= time:
            self.wp[0] = self.cust_loc[0]
            self.wp[1] = self.cust_loc[1]
            self.state = 2
            self.deliveryStart = time #added for KPI delivery time, time its ready for pickup
            return True
        elif self.state == 2:
            self.state = 3
            self.deliveryTime = time - self.deliveryStart #added for KPI delivery time, time at which job is completed - time it was ready for pickup
            return False
        return False
    
    def is_job_possible(self, drone):
        drone_rest = self.find_distance(drone.loc,  self.resturant.loc)
        drone_range = drone.find_battery_range()
        tot_dist = drone_rest + self.rest_to_cust + self.cust_to_charg
        if tot_dist + 25 >= drone_range:
            return False, False
        return drone_rest + self.rest_to_cust, drone_rest

# The restaurant class keeps track of the locations of the restaurants as well
# As the earliest time that the next order can be copleted by
class restaurant(object):

    def __init__(self, loc):
        self.loc = loc
        self.next_start_time = 0
        
    def add_order(self, order):
        if self.next_start_time <= order.order_time:
            order.complete_time = order.order_time + order.prep_time
            self.next_start_time = order.complete_time
        else:
            order.complete_time = self.next_start_time + order.prep_time
            self.next_start_time = order.complete_time


#demand generation given a random location
def pick_restaurant(loc, restaurants, chargers):
    
    def dist(loc, dest):
        sq = (loc[0]-dest[0])**2 + (loc[1]-dest[1])**2
        return math.sqrt(sq)
    
    # finds closest charging station 
    best = 100000
    for dest in chargers:
        d = dist(loc, dest.wp)
        if d <= best:
            best = d
            
    dists = []
    val = 0
    for r in restaurants:
        cr_dist = dist(loc, r.loc) # because we want to pick the closer ones more ofter
        val += 1/((cr_dist+0.001)**1.5)
        dists.append(val)
        
    rand = random.random()*val
    for idx, d in enumerate(dists):
        if d >= rand:
            return restaurants[idx], best # returns resturant, and disntance from custumer to closest charger


# Generation of the simple scores matrix that describes the score of each drone 
# For each job, this gets fed into the hungarian matrix
def simpleScores(drones, naJobs, time):
    # drones is a list with all the drones that have not been assigned a task
    # naJobs is a list with all the jobs that have not been assigned yet
    
    scoreMatrix = np.ones((len(drones), len(naJobs)))
      
    for drone_idx, drone_val in enumerate(drones):
        for job_idx,job_val in enumerate(naJobs):
            dist, drone_rest = job_val.is_job_possible(drone_val)
            if not dist:
                score = 100000
            else:
                adjust = 1
                if time - job_val.complete_time > 0:
                    adjust = 1 + (time - job_val.complete_time)/10
                score = dist / adjust
            
            scoreMatrix[drone_idx,job_idx] = score
    #the higher the scores the worse       
    return scoreMatrix 

# Generation of the score matrix given the neural network and a set of weights and biases
# This gets fed into the hungarian algorithm
def NNscores(drones, naJobs, time, weigths,num_drones):
    scoreMatrix = np.ones((len(drones), len(naJobs)))
    
    for drone_idx, drone_val in enumerate(drones):
        for job_idx, job_val in enumerate(naJobs):
            dist, drone_rest = job_val.is_job_possible(drone_val)
            if dist:
                battery = drone_val.battery/100
                bat_req = dist/drone.tot_range
                #bat_req_to_charger = job_val.cust_to_charg/drone.tot_range
                time_to_order = ((drone_rest/drone_val.vel)+time - job_val.complete_time)/200
                is_charging = 0
                if drone_val.job and drone_val.job.job_type == 2:
                    is_charging = 1
                jobs_without_drone = len(naJobs)/50
                per_of_used_drones = len(drones)/num_drones
                inputs = [battery,bat_req,time_to_order,is_charging, jobs_without_drone,per_of_used_drones]
                NN_out = NN.NN(weigths, inputs)[0]
                
                # add an input that describes the distance, number of drones that could coplete the job
                # because their drop off is close to the restaurant 
                # but are still en route to their final drop off
                # This could let some drones take far away jobs
                
                
                if NN_out < 0:
                    score = 100000
                else:
                    score = NN_out
            else:
                score = 100000
                
            scoreMatrix[drone_idx,job_idx] = score
    
    return scoreMatrix 
        
# The hungian algorithm assigns the job to each drone that does not have a job
# By minimising the sum of the total scores from the score matrix, it outputs the assgiments
def hungarianMethod(bidMatrix):
    # bidMatrix: a m x n matrix where m is the number of agents and n the
    # number of not assigned tasks

    row_ind, col_ind = linear_sum_assignment(bidMatrix)
    return row_ind, col_ind
    
