from sklearn.cluster import DBSCAN
import numpy as np
import pandas as pd

df = pd.read_csv('des_dr1_g_i_small_box_hpix_4.csv')
result_dir = './pair_dist_results/'

unique_pixels = np.unique(df['pix'])

#start a loop here
n_clusters_tot = 0
pix_ra_dec_label = {}
pix_clustercenter = {}
current_pix = 151
 
square_dist_hvs = np.load(result_dir+'pair_dist_hp4_{}.npy'.format(current_pix))
radius_d = 10./60. #in degrees
radius_r = radius_d*np.pi/180. #in radians
db = DBSCAN(eps=radius_r, min_samples=10, metric='precomputed').fit(square_dist_hvs)

core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(db.labels_)) - (1 if -1 in db.labels_ else 0)
print('Estimated number of clusters: %d' % n_clusters_)
    #print('Estimated number of noise points: %d' % n_noise_)
    #n_noise_ = list(labels).count(-1)
labels = db.labels_
n_clusters_tot += n_clusters_

if n_clusters_ > 0:
  unique_labels = np.unique(db.labels_)
  core_samples_center = np.zeros((len(unique_labels)-1,2))
  for j in np.arange(len(unique_labels)):
      if ~(unique_labels[j] == -1):
          class_member_mask = (labels == unique_labels[j])
          xy = X[class_member_mask & core_samples_mask]
          xy = xy*180.0/np.pi
          core_samples_center[j,:] = np.mean(xy, axis=0)
  print(core_samples_center)
