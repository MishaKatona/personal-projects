# -*- coding: utf-8 -*-

# The main testing file used to produced data that can be futher processed
# Either for the baseline model or the neural network

import run_logic as rl
import csv
from mytools import pbf
import numpy as np
import demandv2 as dem

np.random.seed(1)
rest_loc = []
for i in range(20):
    rest_loc.append(dem.mapGenerator(gridSize=(1000,1000), spawn_prob=False, peakCoordinates = False))
np.random.seed(None)

# if weights = False then the code will run wiht the default non-learning settings,
# otherwise if weigts is given then it will run the simulation with the neural network

weights = [[[0.0634853790759966, 0.3826631587772218, 0.4236892177490603, 0.680122907121363, -0.38080911000385087, -0.73690859211672], [-0.31650536528538664, 0.3874503286068779, -0.3162025181115611, -0.3936277470768178, -0.6481598761886045, -0.8783291123349619], [-0.893443951407238, 0.3989718813011005, -0.5272413735899104, 0.016572026921704425, 0.12465361092423644, 0.7668775566296966], [0.6556762764034014, -0.3167333434428461, 0.3671292382698861, 0.6968427053466459, 0.6368106165518448, 0.9934321159953097], [-0.5268961516752413, 0.3950922005177131, 0.1100550398062386, 0.036855820961868346, 0.563665514240641, -0.2881709164574042], [-0.4604978968258273, -0.2969697898342727, -0.47137927700800075, 0.13765653605153405, -0.14476059524923657, 0.5851145774071143]], [[0.4650045968877172, -0.7707814669066964, 0.6028881446525505, -0.12607709144563573, 0.8688328653428452, -0.8083145909718426], [-0.4468392175174398, 0.29807823966013647, -0.5487025463120678, -0.2726424143189814, 0.8883702967305729, -0.8201511186481316], [0.5030736662744866, -0.6760608055424113, -0.6264260550658982, 0.1425712025848354, 1.0287320643053395, 0.3920834391558954], [0.6128306840837996, 0.3486096977765456, -0.04002784455646724, 0.3501650987283062, 0.3438546979329242, -0.9158808923599959], [-0.08017295431060756, 0.22116336641581547, -0.7215368955769328, -0.042621189211460964, 0.8426923258227728, 0.01408743235482196], [0.4981108664465199, -0.5218048863091018, 0.2416199021459151, -0.8452094929707066, 0.4652829695127596, 0.09399777535415232]], [[-1.0659412151364254, -0.6648826282729361, 0.2172803361380946, 0.150453431661844, -0.4013924835795414, 0.2508877400407376], [-0.592177727783264, 0.09546095099414398, 0.634169671695582, -0.8864200839766729, 0.34035215875931435, 0.5749509039851726], [-0.2040139938940626, -0.2541654432657413, -0.9047441708960184, -0.13963452192428205, 0.8911286025714387, 0.09255233706659571], [-0.024091608506800588, -0.36081201591273504, -0.35879936642529, 0.3507951387359783, 0.6418403121066141, 0.4783015273056136]], [[-0.22710748738960929, -0.6318054336247805, -0.828223374000665, 0.34595290772562715]], [[0.14899970125755835, 0.8362313418645488, -0.3710336362400688, -0.21498922377947705, -0.470196929993951, 0.22073403591915763, -0.39793660534768627, -0.3496054186302523, 0.34667773121312623, -0.3583768051635505, -0.007095575142562538, 0.8987615240446614, -0.0005058854834270043, 0.98813616677188, 1.124796722093522, -0.32571743636542916, -0.17580636537189864, -0.010327358384964347, 0.9861115479780318, 0.5705700709535082, -0.9390895310960459, -0.6529715741626314]]]

weights = [np.array(x) for x in weights]    

#weights = False

size = (1000,1000) # dimension of the simulation (x,y)
num_runs = 250 # how many runs with one setting is needed
sim_lenght = 1000 # how many ticks should the simulation run for
spawn_prob = 0.16 # probability of a new demand occuring each tick

# the following parameters can either take a list of (x,y) tuples indicating the location
# or they can take a single intiger which determines how many it should place randomly
drones_init = 10 # number of drones
restaurants_init = [(300,300),(450,400),(700,500),(550,700)] # number of resturants
#restaurants_init = rest_loc[:8]
charger_init = False # number of chargers, if False then it places 2 in the middle 

orders_init = 5 # number of initial order to be generated at t = 0
peak_loc = False # peak location for the probabilities of spawing demand, list of (x,y) tuple
                 # if False then it will use default values


all_data = []
all_data.append([size,num_runs,sim_lenght,spawn_prob])
all_data.append([])
for i in range(num_runs):
    pbf(i,num_runs)
 
    drones, restaurants, chargers, jobs_na = rl.gen_agents(size,drones_init,restaurants_init,charger_init,orders_init,peak_loc)
    
    jobs_a = []
    jobs_c = []
    t = 0
    run = True
    
    while run:
        
        jobs_na, jobs_a, jobs_c, slow = rl.main_loop(drones, restaurants, chargers, jobs_a, jobs_na, jobs_c, t, spawn_prob, size, peak_loc, weights)
    
        t += 1
        if t == sim_lenght:
            run = False
    
    job_na_lst = []
    for job in jobs_na:
        job_na_lst.append([job.order_time, job.complete_time, job.deliveryStart, job.cust_loc, job.resturant.loc, job.rest_to_cust])
    
    job_a_lst = []
    for job in jobs_a:
        job_a_lst.append([job.order_time, job.complete_time, job.deliveryStart, job.cust_loc, job.resturant.loc, job.rest_to_cust])
        
    job_c_lst = []
    for job in jobs_c:
        job_c_lst.append([job.order_time, job.complete_time, job.deliveryStart, job.cust_loc, job.resturant.loc, job.rest_to_cust])
        
    drone_lst = []
    for drone in drones:
        drone_lst.append([drone.order_delay, drone.utilised_counter])
        
        
    all_data.append([i])
    all_data.append(["jobs_not_assigned"])
    all_data += job_na_lst
    all_data.append(["jobs_assigned"])
    all_data += job_a_lst
    all_data.append(["jobs_completed"])
    all_data += job_c_lst
    all_data.append(["drones"])
    all_data += drone_lst
    all_data.append([])
    
        

file_name = "AABM_"
if weights:
    file_name += "NN"
else:
    file_name += "default"
file_name += ".csv"

with open(file_name, mode='w',newline='') as data:
    data_writer = csv.writer(data, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)#csv.QUOTE_MINIMAL)
    
    for i in all_data:
        data_writer.writerow(i)