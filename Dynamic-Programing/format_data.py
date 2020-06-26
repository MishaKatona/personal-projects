# -*- coding: utf-8 -*-

import xlrd
import csv
import numpy as np


# Converts the xlx workbook into one csv file 

workbook = xlrd.open_workbook('AE4423_Ass2_APO.xlsx')
old_workbook = xlrd.open_workbook('AE4423_Datasheets.xls')


all_data = []

worksheet = old_workbook.sheet_by_index(24) # check if it is group 24 or if im fucing up
# getting 2014 deamnd
for o in range(12,32):
    row = []
    for p in range(2,22):
        row.append(worksheet.cell(o,p).value)
    all_data.append(row)
all_data.append([])

# get dist and runway data
worksheet = workbook.sheet_by_index(0)

for o in range(1,5):
    row = []
    for p in range(1,21):
        row.append(worksheet.cell(o,p).value)
    all_data.append(row)
all_data.append([])

# convert the lat and lng values into distance matrix
lat = all_data[-4]
long = all_data[-3]

# remove the lat and long values from the all_data lst
all_data.pop(-3)
all_data.pop(-3)

def rad(deg):
    return (np.pi * deg) / 180

def dist(lat_i,long_i,lat_j,long_j):
    lat_i = rad(lat_i)
    long_i = rad(long_i)
    lat_j = rad(lat_j)
    long_j = rad(long_j)
    first_t = np.sin( (lat_i - lat_j)/ 2 )**2
    second_t = np.cos(lat_i) * np.cos(lat_j) * np.sin( (long_i - long_j)/ 2 ) **2
    arc = 2 * np.arcsin( np.sqrt( first_t + second_t ) )
    return round(6371*arc,1)


for i in range(len(lat)):
    row = []
    for o in range(len(long)):
        row.append(int(dist(lat[i],long[i],lat[o],long[o])))
    all_data.append(row)
all_data.append([])


# get the plane data
worksheet = workbook.sheet_by_index(1)

for o in range(1,11):
    row = []
    for p in range(1,4):
        row.append(worksheet.cell(o,p).value)
    all_data.append(row)
all_data.append([])

# get the hourly demand data
worksheet = workbook.sheet_by_index(2)

for o in range(2,22):
    row = []
    for p in range(2,27):
        row.append(worksheet.cell(o,p).value)
    all_data.append(row)


# write it to a more convinient csv file
with open('All_data.csv', 'w+', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(all_data)