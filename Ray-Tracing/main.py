# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw
from math import sqrt,cos,sin,pi



screen = (500,500) #x,y
camera = (0,0,0) #x,y,z

sphere_center = (0,500,0)
sphere_radious = 200

light_r = 500

steps = 3
cir = 2*pi/steps
light_steps = []

for p in range(steps):
    step = [500*cos(cir*p),0,500*sin(cir*p)]
    light_steps.append(step)
#light_steps = [[500,100,1000]]
    
#print("*"*100)
print()

for l in range(steps):
    print("*", sep='', end='', flush=True)
    
    light = light_steps[l]
    light_mag = sqrt(sum([x**2 for x in light]))
    
    
    img = Image.new('RGB', screen, color=(50,50,50))    
    idraw = ImageDraw.Draw(img)
    
    points = []
    for i in range(screen[0]):
        for o in range(screen[1]):
            if sqrt((i-(screen[0]/2))**2 + (o-(screen[1]/2))**2) < sphere_radious:
                y = sqrt(sphere_radious**2 - (i-(screen[0]/2))**2 - (o-(screen[1]/2))**2)
                point = [i-(screen[0]/2),sphere_center[1]-y,o-(screen[1]/2)]
                
                d = [x-y for [x,y] in zip(point,light)]
                n = [x-y for [x,y] in zip(point,sphere_center)]
                n_norm = [x/sqrt(sum([x**2 for x in n])) for x in n]
                dot = sum([x*y for [x,y] in zip(d,n_norm)])
                r = [x - 2 * dot*y for [x,y] in zip(d,n_norm)]
                
                n_dot = sum([x*y for [x,y] in zip(r,point)])
                cos = n_dot/(sqrt(sum([x**2 for x in r]))*sqrt(sum([x**2 for x in point])))
                multi = 1 - (cos+1)/2
                idraw.point((i,o),(0,0,int(multi*255)))
    
    
    
    for i in range(0):
        idraw.point((250,i),(0,0,i))
        idraw.point((251,i),(0,0,i))
        idraw.point((252,i),(0,0,i))
    
     
    img.show()
    #name = str(l)+".png"
    #img.save(name,"PNG")