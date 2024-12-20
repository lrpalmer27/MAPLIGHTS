"""
this file is intended to combine all digital map representation photos into a video for demonstration purposes only
"""

import os
from datetime import datetime, timedelta
import numpy as np
import pandas as pd 
import cv2

debugging=0

if __name__=="__main__":
    ## ------------------------------- Generate list of files --------------------------------------
    
    TimePeriodStart=datetime(2024,12,19,0,0,0)
    TimeResolution=timedelta(minutes=15)
    samples2gen=int(24*60/15)
    TimeLength=timedelta(days=1)
    timespace=np.linspace(TimePeriodStart,TimePeriodStart+TimeLength,samples2gen)
    
    # Open time loop ---
    listofNames=[]
    for i in timespace:
        i=datetime.replace(i,second=0,microsecond=0)
        print(i)
        name=f'{i}'
        name=name.replace(':',' ')
        print(name) #for status checking
        
        listofNames.append(name)
    
    df=pd.DataFrame(listofNames)
    
    print(df)
    
    if debugging:
        df.to_csv('.AllDigitalMapShots/listofNames.csv')
        df.to_pickle('.AllDigitalMapShots/listofNames.pkl')
    
    
    ## ----------------------- save pictures together into a video ------------------------------------
    # from: https://stackoverflow.com/questions/44947505/how-to-make-a-movie-out-of-images-in-python
    image_folder = '.AllDigitalMapShots'
    video_name = '.AllDigitalMapShots/Video.avi'

    images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    video = cv2.VideoWriter(video_name, 0, 1, (width,height))

    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()
    video.release()
            
        
        
        