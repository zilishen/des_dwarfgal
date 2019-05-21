from sklearn.cluster import DBSCAN
import numpy as np
import pandas as pd

df = pd.read_csv('des_dr1_g_i_small_box_hpix_4.csv')
result_dir = './pair_dist_results/'
dbscan_dir = './dbscan_results/'

unique_pixels = np.unique(df['pix'])

for pix in unique_pixels:
  n_clusters_tot = 0
  pix_ra_dec_label = {}
  pix_clustercenter = {}
 
  square_dist_hvs = np.load(result_dir+'pair_dist_hp4_{}.npy'.format(pix))
  radius_d = 10./60. #in degrees
  radius_r = radius_d*np.pi/180. #in radians
  db = DBSCAN(eps=radius_r, min_samples=10, metric='precomputed').fit(square_dist_hvs)

  n_clusters_ = len(set(db.labels_)) - (1 if -1 in db.labels_ else 0)
  print('Estimated number of clusters: %d' % n_clusters_)
  labels = db.labels_
  n_clusters_tot += n_clusters_

  if n_clusters_ > 0:
    np.save(dbscan_dir+'dbscan_hp4_{}'.format(pix),labels)
