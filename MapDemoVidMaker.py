"""
this file is intended to combine all digital map representation photos into a video for demonstration purposes only
"""

import os
from datetime import datetime, timedelta
import numpy as np
import pandas as pd 
import cv2
import imageio  

debugging=0

if __name__=="__main__":
    ## ------------------------------- Generate list of files --------------------------------------
    ## logic duplicated from the timelapse generator file logic so that they'll match identically without having to
    ## read and sort filenames in the folder. This approach assumes none of the files have been moved or renamed or are in a temp (unaccessible) state
       
    if True: #objective of this statement is to make a timelapse of the sun rising across NA (finer resolution, less time)
        TimePeriodStart=datetime(2024,12,19,11,0,0)
        samples2gen=240
        TimeLength=timedelta(hours=14)
    if False: #objective of this statement is to make a timelapse of the tempertures across the whole day (coarser resolution, more time)
        TimePeriodStart=datetime(2024,12,19,0,0,0)
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
    
    
    ## ----------------------------------- save pictures together into a video -----------------------------------------------
    # from: https://stackoverflow.com/questions/44947505/how-to-make-a-movie-out-of-images-in-python
       
    image_folder = '.AllDigitalMapShots'
    video_name = '.AllDigitalMapShots/Video.mp4' # saves file as mp4

    images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape
    
    saveMP4=True
    if saveMP4: #save as mp4
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video = cv2.VideoWriter(video_name, fourcc=fourcc, fps=5, frameSize=(width,height))

        for image in images:
            video.write(cv2.imread(os.path.join(image_folder, image)))
    
        cv2.destroyAllWindows()
        video.release()
    
    saveGIF=False  
    if saveGIF: #save as mp4
        gifName = '.AllDigitalMapShots/TimelapseGIF.gif' # saves file as gif
        imagesList=[]
        for image in images: 
            imagesList.append(imageio.imread(os.path.join(image_folder,image)))
        imageio.mimsave(gifName, imagesList)
        
        cv2.destroyAllWindows()
    
    
    
            
        
        
        