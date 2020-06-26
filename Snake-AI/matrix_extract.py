# -*- coding: utf-8 -*-

def matrix_info(matrix,travel,side_len):
    food_pos = None
    for numy, y in enumerate(matrix):
        for numx, val in enumerate(y):
            if val == 1:
                head_pos = (numy,numx)
            elif val == -1:
                food_pos = (numy,numx)
                
    if not food_pos:
        food_pos = head_pos
                
    if head_pos[0] == 0:
        head_n = 1
    else:
        head_n = matrix[head_pos[0]-1][head_pos[1]]
    
    if head_pos[1] == side_len-1:
        head_e = 1
    else:
        head_e = matrix[head_pos[0]][head_pos[1]+1]
        
    if head_pos[0] == side_len-1:
        head_s = 1
    else:
        head_s = matrix[head_pos[0]+1][head_pos[1]]
        
    if head_pos[1] == 0:
        head_w = 1
    else:
        head_w = matrix[head_pos[0]][head_pos[1]-1]
        
    soround = [head_n, head_e, head_s, head_w]
    
    soround = soround[travel:] + soround[:travel]
    
    soround.pop(2)
    
    for i in range(len(soround)):
        if soround[i] > 0:
            soround[i] = 1
        else:
            soround[i] = 0
            
    y_food_dist = 0 if head_pos[0] == food_pos[0] else (head_pos[0] - food_pos[0])/abs(head_pos[0] - food_pos[0])
    x_food_dist = 0 if head_pos[1] == food_pos[1] else (head_pos[1] - food_pos[1])/abs(head_pos[1] - food_pos[1])
    
    if travel == 0:
        f_food_dist = y_food_dist
        s_food_dist = x_food_dist
    elif travel == 1:
        f_food_dist = x_food_dist
        s_food_dist = y_food_dist
    elif travel == 2:
        f_food_dist = -y_food_dist
        s_food_dist = -x_food_dist
    elif travel == 3:
        f_food_dist = -x_food_dist
        s_food_dist = -y_food_dist
    
    return [f_food_dist,s_food_dist]+soround
    

#additional
def extra():
    if head_pos[0] <= 1:
        head_n2 = 1
    else:
        head_n2 = matrix[head_pos[0]-2][head_pos[1]]
    
    if head_pos[1] >= side_len-2:
        head_e2 = 1
    else:
        head_e2 = matrix[head_pos[0]][head_pos[1]+2]
        
    if head_pos[0] >= side_len-2:
        head_s2 = 1
    else:
        head_s2 = matrix[head_pos[0]+2][head_pos[1]]
        
    if head_pos[1] <= 1:
        head_w2 = 1
    else:
        head_w2 = matrix[head_pos[0]][head_pos[1]-2]
    
    
    
    soround = [head_n, head_n2, head_e, head_e2, head_s, head_s2, head_w, head_w2]
    
    soround = soround[travel*2:] + soround[:travel*2]
    
    soround.pop(4)
    soround.pop(5)
    