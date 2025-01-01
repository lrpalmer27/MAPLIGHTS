import pandas as pd
import os 

keepers=pd.read_pickle(os.path.join(os.getcwd(),'cDATA.pkl'))

print(keepers.head)
print(keepers.shape)

nRows=keepers.shape[0]

for L in range(0,keepers.shape[0]):
    print('long',keepers['Longitude'][L])