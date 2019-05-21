import sys
import numpy as np
import pandas as pd
from scipy.spatial import cKDTree
from scipy.spatial.distance import pdist, squareform
import subprocess as sp
import multiprocessing as mp
import operator
import os
import random

i = int(sys.argv[1])
result_dir = './pair_dist_results'

def angular_separation_hvs(x1,x2):
    """
    Modified from astropy.coordinates.angle_utilities 
    Angular separation between two points on a sphere.
    Parameters
    ----------
    x1, x2: array of float Longitude and latitude in radians.
    each array needs to have two columns, lon(RA)(lambda) and lat(dec)(phi)
    Returns
    -------
    angular separation: float in radians.
    Notes
    -----
    The angular separation is calculated using the Haversine formula [1]_,
    which is computationally less expensive than
    Vincenty, but is not stable at antipodes.
    .. [1] https://en.wikipedia.org/wiki/Great-circle_distance
    """
    ssqrdlat = np.sin(0.5*(x2[1] - x1[1]))**2
    ssqrdlon = np.sin(0.5*(x2[0] - x1[0]))**2
    clat1 = np.cos(x1[1])
    clat2 = np.cos(x2[1])
    
    return 2*np.arcsin(np.sqrt(ssqrdlat + clat1*clat2*ssqrdlon))
    
df = pd.read_csv('des_dr1_g_i_small_box_hpix_4.csv')

unique_pixels = np.unique(df['pix'])

add_pix, = np.where(df['pix'] == i)
ra_rad = df['ra'][add_pix].values*np.pi/180.0
dec_rad = df['dec'][add_pix].values*np.pi/180.0
X = np.column_stack((ra_rad,dec_rad))

import time
print('Pixel # {} started'.format(i))
t0 = time.time()
dist_hvs = pdist(X,angular_separation_hvs)
t1 = time.time()
square_dist_hvs = squareform(dist_hvs) # DBscan expects square dist. matrix, so this is crucial

np.save(result_dir+'/pair_dist_hp4_{}'.format(i),square_dist_hvs)
print('Finished pixel #{} with {} stars in {} seconds'.format(i,X.shape[0],t1-t0))
