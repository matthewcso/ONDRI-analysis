# %%
import ants
import numpy as np
from utils.extract_metrics import extract_metrics_from_map
import pandas as pd
import os
from utils.load_scalar import image_read_rotation, load_scalar
from utils.asegStats_to_df import asegStats_to_df
from utils.texturemap import *
# %%
new_paths = ['outputs', 'outputs/example_pictures']
FLAIR_path = 'data/FLAIR_standardized' 

for path in new_paths:
    if not os.path.exists(path):
        os.makedirs(path)

clinical_df = pd.read_csv('data/summary/ONDRI_summary.csv')
clinical_df = clinical_df[clinical_df['COHORT']!= 'VCI']
clinical_df = clinical_df[~pd.isna(clinical_df['NII_FILENAME_T1'])]

# %%
row = clinical_df.iloc[1]
print(row)

# %%
atlas = ants.image_read('atlas/mni_icbm152_nlin_sym_09c_t2_csfnull.nii.gz')
atlas_labels = ants.image_read('atlas/mni_icbm152_nlin_sym_09c_CerebrA_nifti/mni_icbm152_CerebrA_tal_nlin_sym_09c.nii')
# %%
all_rows = []

img_path = '%s/%s' % (FLAIR_path, row['STANDARDIZED_NII'])

img_path = 'data/FLAIR_standardized/%s' % row['STANDARDIZED_NII']

img0 = image_read_rotation(img_path, transpose=[1,0,2])

if os.path.exists('data/mask/%s' % row['MASK_NII']):
    img_mask = image_read_rotation('data/mask/%s' % row['MASK_NII'], transpose=[1,0,2])
else: 
    img_mask = image_read_rotation('data/hdbet_mask/%s' % row['STANDARDIZED_NII'].replace('.nii.gz', '_mask.nii.gz'), transpose=[1,0,2])

if not img_mask.shape == img0.shape:
    img_mask = ants.pad_image(img_mask, shape=img0.shape)

atlas_based_labels = image_read_rotation('outputs/registration_labels/%s' % row['STANDARDIZED_NII'], flip=True)
csf_labels = image_read_rotation('outputs/csf_segmentation/%s' % row['STANDARDIZED_NII'], flip=True)
t1 = ants.image_read('outputs/fastsurfer/scratch/sub-OND01BYC1009_ses-01SE01MR_run-1_T1w/mri/orig.mgz')
t1_labels = ants.image_read('outputs/fastsurfer/scratch/sub-OND01BYC1009_ses-01SE01MR_run-1_T1w/mri/aparc.DKTatlas+aseg.deep.mgz')
t1_labels_flairspace = ants.image_read('outputs/registration_labels_t1/sub-OND01BYC1009_ses-01SE01MR_run-1_FLAIR_time0.nii.gz')
# %%
f = 9
img0.plot(overlay_cmap='tab20',  slices=[25], axis=2, figsize=f)
img0[img_mask == 0] = 0
img0.plot(overlay_cmap='tab20', slices=[25], axis=2, figsize=f)
img0.plot(overlay=atlas_based_labels, overlay_cmap='tab20', slices=[25], overlay_alpha=0.5, axis=2, figsize=f)
img0.plot(overlay=csf_labels, overlay_cmap='tab20', slices=[25], overlay_alpha=0.5, axis=2, figsize=f)
mad = apply_slicewise(img0.numpy(), MAD)

ants.from_numpy(mad).plot(slices=[25], axis=2, figsize=f)

t1.plot(overlay_cmap='tab20',  slices=[160], axis=2, figsize=f)
t1.plot(overlay=t1_labels, overlay_cmap='tab20', slices=[160], overlay_alpha=0.25, axis=2, figsize=f)
img0.plot(overlay=t1_labels_flairspace, overlay_cmap='tab20', slices=[25], overlay_alpha=0.25, axis=2, figsize=f)




# %%