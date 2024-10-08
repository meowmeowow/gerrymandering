import cv2 
import itertools
import math
from enum import Enum 


class Color(Enum):
    PURPLE = 148
    ORANGE = 186

#from map.png get x,y,color of hexagons
img = cv2.imread('') 
  
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 

gray[gray == 0] = 255

_, threshold = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY) 
  #250 for map.png
  
contours, _ = cv2.findContours( 
    threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
  
i = 0
  

points =[]

id = 0

for contour in contours: 
    if i == 0: 
        i = 1
        continue
    
    approx = cv2.approxPolyDP( 
        contour, 0.01 * cv2.arcLength(contour, True), True) 
      
  
    M = cv2.moments(contour) 
    if M['m00'] != 0.0: 
        x = int(M['m10']/M['m00']) 
        y = int(M['m01']/M['m00']) 
  
    if len(approx) == 6:
        color = gray[y,x]

        points.append((x,y,color,id))

        id =id +1

#from points, find edges 

#point 1 id, point 2 id
edges = []
#point 1 id, color
colors = []

current = None
for point1, point2 in itertools.combinations(points, 2):
    #color
    if (current != point1):
        colors.append((point1[3],Color(point1[2]).name))
        current = point1



    dist= int(math.dist((point1[0],point1[1]),(point2[0],point2[1])))

    if(dist < 120 and dist > 90):
        #edge
        edges.append((point1[3],point2[3]))



colors.append((points[len(points)-1][3],Color(points[len(points)-1][2]).name))
       


# write to file
f = open("", "a")
f.write(str(edges)+'\n')
f.write(str(colors) + '\n')
f.write(str(points))
f.close() 



