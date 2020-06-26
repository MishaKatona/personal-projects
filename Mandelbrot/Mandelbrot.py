# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw
from mytools import pbf,pal

pale = pal()


s = 800
s2 = int(s/2)
s4 = int(s/4)

sxn = -int((2*s)/3)
sxp = int(s/3)+1
syn = -s2
syp = s2 + 1


img = Image.new('P', (s,s), )
img.putpalette(pale)    
idraw = ImageDraw.Draw(img)

for r in range(sxn,sxp):
    pbf(r-sxn,s)
    for i in range(syn,syp):
        point = complex(r/(s/3),i/(s/3))
        x = 0
        for u in range(255,-1,-1):
            if abs(x) > 2:
                break
            x = x**2 + point 
        #idraw.point((r+(square/2),i-syn),(c,100,c))
        idraw.point((r-sxn,i-syn),u)

 
img.show()
img.save("mandelbrotf.bmp") # BEFORE RUNNING MAKE SURE FILE DOES NOT GET OVER WRITTEN

