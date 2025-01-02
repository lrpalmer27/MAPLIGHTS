import os
from datetime import datetime, timedelta
import numpy as np
import pandas as pd 
import cv2
import imageio 

debugging=True

#folder locations
video_name='MakeBuildTimelapse/PhysicalBuildTimelapse.mp4'
image_folder=os.path.join(os.getcwd(),r'MakeBuildTimelapse\.PicturesFromPi')

#get picture names and put them in correct order!
allPics=os.listdir(image_folder)

if debugging:
    print(allPics)

### --------------------------------- make timelapse here ----------------------------------
frame = cv2.imread(os.path.join(image_folder, allPics[0]))
height, width, layers = frame.shape
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video = cv2.VideoWriter(video_name, fourcc=fourcc, fps=5, frameSize=(width,height))

#image text things
font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 1
color = (0, 0, 255) #red in BGR
org=(int((width/2)-250),int(50))
thickness=2

for image in allPics:
    if debugging: 
        print(f'image:{image}')
    img=cv2.imread(os.path.join(image_folder, image))
    imgWtxt=cv2.putText(img,f'{image}',org,font,fontScale,color,thickness)
    if debugging:
        None
        # cv2.imshow('tester', img) 
    video.write(imgWtxt)

cv2.destroyAllWindows()
video.release()

print('Done')