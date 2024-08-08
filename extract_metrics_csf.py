# %%
import ants
import numpy as np
from utils.extract_metrics import extract_metrics_from_map
import pandas as pd
import os
from utils.load_scalar import image_read_rotation, load_scalar

from utils.texturemap import *
# %%
new_paths = ['outputs', 'outputs/metrics_ondri_noncsf']
FLAIR_path = 'data/FLAIR_standardized' 

for path in new_paths:
    if not os.path.exists(path):
        os.makedirs(path)

clinical_df = pd.read_csv('data/summary/ONDRI_summary.csv')
clinical_df = clinical_df[clinical_df['COHORT']!= 'VCI']

#
label_dict = {0: 'Brain', 1: 'CSF'}
# %%
all_rows = []
# %%
for i, row in clinical_df.iterrows():
    # standard labels
    print(i)
    metrics_filename = 'outputs/metrics_ondri_noncsf/%s.csv' % row['SUBJECT']

    if os.path.exists(metrics_filename):
        continue

    try:
        img_path = '%s/%s' % (FLAIR_path, row['STANDARDIZED_NII'])
        img_path = 'outputs/rotation_images/%s' % row['STANDARDIZED_NII']
        
        img0 = image_read_rotation(img_path, k=0)

        if os.path.exists('data/mask/%s' % row['MASK_NII']):
            img_mask = image_read_rotation('data/mask/%s' % row['MASK_NII'], k=1)
        else: 
            img_mask = image_read_rotation('data/hdbet_mask/%s' % row['STANDARDIZED_NII'].replace('.nii.gz', '_mask.nii.gz'), k=1)

        if not img_mask.shape == img0.shape:
            img_mask = ants.pad_image(img_mask, shape=img0.shape)

        img_csf = ants.image_read('outputs/csf_segmentation/%s' % row['STANDARDIZED_NII'])

        img_mask = img_mask.numpy()
        img_csf = img_csf.numpy()
        img0 = img0.numpy()
        img0[img_mask == 0] = 0


        mii = apply_slicewise(img0, MII)
        mad = apply_slicewise(img0, MAD)

        new_row = extract_metrics_from_map(img0, img_csf, label_dict, mii, mad)
        new_row['TBV-voxel'] = np.sum(img_mask==1)
        pd.DataFrame(new_row).to_csv(metrics_filename, index=False, header=True)
        all_rows.append(new_row)
    except Exception:
        print('Error in %s' % metrics_filename)


# %%