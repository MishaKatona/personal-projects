# -*- coding: utf-8 -*-

# Import a library of functions called 'pygame'
import pygame
import pygame.freetype 
import random

    
# Initialize the game engine
pygame.init()
font = pygame.font.Font(None, 28)
font2 = pygame.font.Font(None, 82)
 
# Define the colors we will use in RGB format
black = (0, 0, 0)
white = (255, 255, 255)
blue = (65,105,225)
red = (220,20,60)


# Set the height and width of the screen
size = [600, 600]
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("Snake")

 
# Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()

# Set up patrix for snake and food
p_size = 30
matrix = []
for i in range(int(size[1]/p_size)):
    matrix.append([0]*int(size[0]/p_size))
    
matrix[5][5] = 1
matrix[4][5] = 2
matrix[3][5] = 3
matrix[2][5] = 4
    
travel = 2
direction = 0

score = 4
play_side = int(size[1]/p_size)
play_area = play_side**2

#make scree white
screen.fill(white)
play = False
game = True

matrix[8][8] = -1
pygame.draw.rect(screen,blue,[8*p_size,8*p_size,p_size,p_size])
food = True
food_counter = 0
food_num = 0

for numy, y in enumerate(matrix):
    for numx, val in enumerate(y):
        if val == 1:
            pygame.draw.rect(screen,red,[numx*p_size,numy*p_size,p_size,p_size])
        if val > 1:
            pygame.draw.rect(screen,black,[numx*p_size,numy*p_size,p_size,p_size])
 
while not done:
 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                direction = -1
                play = True
            elif event.key == pygame.K_RIGHT:
                direction = 1
                play = True
                
    text = font.render("SCORE: "+str(score), True, (0,0,0))
    pygame.draw.rect(screen,white,[10,10,110,18])
    screen.blit(text,(10, 10))

    if play and game:
        
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
                        pygame.draw.rect(screen,black,[numx*p_size,numy*p_size,p_size,p_size])
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
                            pygame.draw.rect(screen,red,[numx*p_size,(numy-1)*p_size,p_size,p_size])
                        elif travel == 2:
                            if matrix[numy+1][numx] == -1:
                                score += 1
                                food = False
                            elif matrix[numy+1][numx] > 0 and matrix[numy+1][numx] < score:
                                game = False
                                break
                            matrix[numy+1][numx] = 1
                            pygame.draw.rect(screen,red,[numx*p_size,(numy+1)*p_size,p_size,p_size])
                        elif travel == 1:
                            if matrix[numy][numx+1] == -1:
                                score += 1
                                food = False
                            elif matrix[numy][numx+1] > 0 and matrix[numy][numx+1] < score:
                                game = False
                                break
                            matrix[numy][numx+1] = 1
                            pygame.draw.rect(screen,red,[(numx+1)*p_size,numy*p_size,p_size,p_size])
                        elif travel == 3:
                            if matrix[numy][numx-1] == -1:
                                score += 1
                                food = False
                            elif matrix[numy][numx-1] > 0 and matrix[numy][numx-1] < score:
                                game = False
                                break
                            matrix[numy][numx-1] = 1
                            pygame.draw.rect(screen,red,[(numx-1)*p_size,numy*p_size,p_size,p_size])
                        traveled = True
                    elif matrix[numy][numx]+1 > score:
                        pygame.draw.rect(screen,white,[numx*p_size,numy*p_size,p_size,p_size])
                        matrix[numy][numx] = 0
                    elif val > 1:
                        matrix[numy][numx] += 1
                elif food_num == food_counter and food == False:
                    matrix[numy][numx] = -1
                    pygame.draw.rect(screen,blue,[numx*p_size,numy*p_size,p_size,p_size])
                    food = True
                    
    if not game:
        end_text = font2.render("GAME OVER "+str(score), True, (0,0,0))
        pygame.draw.rect(screen,red,[60,250,480,100])
        screen.blit(end_text,(size[0]/2 - end_text.get_width() // 2, size[0]/2 - end_text.get_height() // 2))


    pygame.display.flip()
    clock.tick(6)
 
pygame.quit()