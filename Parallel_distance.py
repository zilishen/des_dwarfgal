import sys
import numpy as np
import subprocess as sp
import multiprocessing as mp
import pandas as pd
import time 

df = pd.read_csv('des_dr1_g_i_small_box_hpix_4.csv')

unique_pixels = np.unique(df['pix'])
process_list = []

for p in unique_pixels:
  command = 'python Stellar_density_pair_dist.py {}'.format(p) 
  process = sp.Popen(command,shell=True)
  process_list.append(process)

AllDone = False    ### boolean flag denoting if all are done
while (not AllDone):
  time.sleep(10)
  process_state = np.array([p.poll() for p in process_list])
  if (np.count_nonzero(process_state == None) == 0): 
    AllDone = True
