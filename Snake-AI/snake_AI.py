#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 14 15:06:01 2019

@author: Misa
"""
import random
from matrix_extract import matrix_info
from AI_neural_net import MLP



def snake(weights,wait,side_len):
        
    matrix = []
    for i in range(side_len):
        matrix.append([0]*side_len)
        
    matrix[5][5] = 1
    matrix[4][5] = 2
    matrix[3][5] = 3
    matrix[2][5] = 4
        
    travel = 2
    direction = 0
    
    score = 4
    play_side = side_len
    play_area = play_side**2
    
    game = True
    
    matrix[8][8] = -1
    food = True
    food_counter = 0
    food_num = 0
    
    wait_c = 0
    count = 0
    
    
    while game:
        count += 1
        
        wait_c += 1
        if wait_c > wait:
            game = False
            
        ai_input = matrix_info(matrix,travel,side_len)
        left,right = MLP(weights,ai_input)
        
        
        if left == 1 and left > right:
            direction = -1
        elif right == 1 and right > left:
            direction = 1
        elif right == 1 and left == 1:
            direction = 0
        
        
        if food == False:
            food_num = random.randint(0,play_area-score)
            food_counter = 0
    
        n_travel = travel + direction
        if n_travel == -1:
            travel = 3
        elif n_travel == 4:
            travel = 0
        else:
            travel = n_travel
        
        direction = 0
        traveled = False
    
        for numy, y in enumerate(matrix):
            for numx, val in enumerate(y):
                food_counter += 1
                if val != 0:
                    if val == 1 and not traveled:
                        matrix[numy][numx] = 2
                        if numy == play_side-1 and travel == 2 or numy == 0 and travel == 0 or numx == 0 and travel == 3 or numx == play_side-1 and travel == 1:
                            game = False
                            break
                        if travel == 0:
                            if matrix[numy-1][numx] == -1:
                                score += 1
                                food = False
                            elif matrix[numy-1][numx] > 0 and matrix[numy-1][numx] < score:
                                game = False
                                break
                            matrix[numy-1][numx] = 1
                        elif travel == 2:
                            if matrix[numy+1][numx] == -1:
                                score += 1
                                food = False
                            elif matrix[numy+1][numx] > 0 and matrix[numy+1][numx] < score:
                                game = False
                                break
                            matrix[numy+1][numx] = 1
                        elif travel == 1:
                            if matrix[numy][numx+1] == -1:
                                score += 1
                                food = False
                            elif matrix[numy][numx+1] > 0 and matrix[numy][numx+1] < score:
                                game = False
                                break
                            matrix[numy][numx+1] = 1
                        elif travel == 3:
                            if matrix[numy][numx-1] == -1:
                                score += 1
                                food = False
                            elif matrix[numy][numx-1] > 0 and matrix[numy][numx-1] < score:
                                game = False
                                break
                            matrix[numy][numx-1] = 1
                        traveled = True
                    elif matrix[numy][numx]+1 > score:
                        matrix[numy][numx] = 0
                    elif val > 1:
                        matrix[numy][numx] += 1
                elif food_num == food_counter and food == False:
                    matrix[numy][numx] = -1
                    food = True
                    wait_c = 0
                    
    return count,score
                    
                    
