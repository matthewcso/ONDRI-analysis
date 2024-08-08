# %%
# %%

import ants
import numpy as np
from utils.load_scalar import image_read_rotation, load_scalar
import pandas as pd
import os

# %%
if not os.path.exists('outputs/registration_labels_t1'):
    os.makedirs('outputs/registration_labels_t1')

if not os.path.exists('outputs/registration_images_t1'):
    os.makedirs('outputs/registration_images_t1')

if not os.path.exists('outputs/rotation_images_t1'):
    os.makedirs('outputs/rotation_images_t1')

# %%
clinical_df = pd.read_csv('data/summary/ONDRI_summary.csv')
clinical_df = clinical_df[clinical_df['COHORT']!= 'VCI']
clinical_df = clinical_df[~pd.isna(clinical_df['NII_FILENAME_T1'])]


# %%
# mask_loc = []
# # %%
# for i, row in clinical_df.iterrows():
#     print('Processing %s/%s: %s' % (str(i), str(len(clinical_df)), row['STANDARDIZED_NII']))
#     output_picture = 'outputs/registration_images_t1/%s'% row['STANDARDIZED_NII'].replace('.nii.gz', '.png')
#     # if os.path.exists(output_picture):
#     #     print('Already completed %s' % output_picture)
#     #     continue
    
#     img_path = 'data/FLAIR_standardized/%s' % row['STANDARDIZED_NII']
#     img0 = image_read_rotation(img_path, k=0)
#     img0 = ants.from_numpy(np.transpose(img0.numpy(), [1, 0, 2]))
#     img0.plot()
#     img0.to_filename('transpose.nii.gz')
#     raise Exception

# %%
mask_loc = []
# %%
for i, row in clinical_df.iterrows():

    print('Processing %s/%s: %s' % (str(i), str(len(clinical_df)), row['STANDARDIZED_NII']))
    output_picture = 'outputs/registration_images_t1/%s'% row['STANDARDIZED_NII'].replace('.nii.gz', '.png')
    if os.path.exists(output_picture):
        print('Already completed %s' % output_picture)
        continue
    
    img_path = 'data/FLAIR_standardized/%s' % row['STANDARDIZED_NII']
    img0 = image_read_rotation(img_path, transpose=[1, 0, 2], k=0, flip=False)

    if os.path.exists('data/mask/%s' % row['MASK_NII']):
        img_mask = image_read_rotation('data/mask/%s' % row['MASK_NII'],  transpose=[1, 0, 2], k=0, flip=False)
        mask_loc.append('data/mask/%s' % row['MASK_NII'])
    else: 
        img_mask = image_read_rotation('data/hdbet_mask/%s' % row['STANDARDIZED_NII'].replace('.nii.gz', '_mask.nii.gz'),  transpose=[1, 0, 2], k=0, flip=False)
        mask_loc.append('data/mask/%s' % row['STANDARDIZED_NII'].replace('.nii.gz', '_mask.nii.gz'))


    if not img_mask.shape == img0.shape:
        img_mask = ants.pad_image(ants.from_numpy(img_mask), shape=img0.shape).numpy()
    img_brain = img0.copy()
    img_brain[img_mask == 0] = 0

    t1_path = 'outputs/fastsurfer/scratch/%s/mri/orig.mgz' % row['NII_FILENAME_T1'].replace('.nii.gz', '')
    t1_mask_path = 'outputs/fastsurfer/scratch/%s/mri/mask.mgz' % row['NII_FILENAME_T1'].replace('.nii.gz', '')
    t1_labels_path = 'outputs/fastsurfer/scratch/%s/mri/aparc.DKTatlas+aseg.deep.mgz' % row['NII_FILENAME_T1'].replace('.nii.gz', '')
    if not os.path.exists(t1_path) or not os.path.exists(t1_mask_path) or not os.path.exists(t1_labels_path):
        print('Missing T1 files for %s' % row['STANDARDIZED_NII'])
        continue
    # converting to/from numpy seems to mess with the orientation information for T1s. I wonder if this is the underlying issue with image flip
    img_t1 = ants.image_read(t1_path)
    img_t1_mask = ants.image_read(t1_mask_path)
    img_t1_brain = img_t1.copy()
    img_t1_brain[img_t1_mask == 0] = 0
    t1_labels = ants.image_read(t1_labels_path)


    # img0.plot()
    # img_t1_brain.plot()

    try:
        registration = ants.registration(fixed=img_brain, moving=img_t1_brain, type_of_transform='SyN')
    
        registered_labels = ants.apply_transforms(fixed=img0, moving=t1_labels, transformlist=registration['fwdtransforms'], interpolator='genericLabel')

        registered_labels[img_mask == 0] = 0
        registered_labels.to_file('outputs/registration_labels_t1/%s'% row['STANDARDIZED_NII'])
        img0.to_file('outputs/rotation_images_t1/%s'% row['STANDARDIZED_NII'])

        img0.plot(overlay=registered_labels, overlay_cmap='tab20', nslices=6, overlay_alpha=0.5, axis=2, figsize=3, filename='outputs/registration_images_t1/%s'% row['STANDARDIZED_NII'].replace('.nii.gz', '.png'))

    except RuntimeError:
        print('Error in registration for %s' % row['STANDARDIZED_NII'])
        continue



# %%
# seg.plot(overlay=registered_labels, overlay_cmap='tab20', nslices=6, overlay_alpha=0.5, axis=2, figsize=3, filename='outputs/registration_images/segmentation.png')


