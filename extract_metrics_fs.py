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
new_paths = ['outputs', 'outputs/metrics_ondri_fs']
FLAIR_path = 'data/FLAIR_standardized' 

for path in new_paths:
    if not os.path.exists(path):
        os.makedirs(path)

clinical_df = pd.read_csv('data/summary/ONDRI_summary.csv')
clinical_df = clinical_df[clinical_df['COHORT']!= 'VCI']
clinical_df = clinical_df[~pd.isna(clinical_df['NII_FILENAME_T1'])]

# %%
label_details = asegStats_to_df('utils/sample_fs.txt')
label_dict = dict(zip(label_details['SegId'], label_details['StructName']))


# %%
all_rows = []
# %%
for i, row in clinical_df.iterrows():
    print(i)
    metrics_filename = 'outputs/metrics_ondri_fs/%s.csv' % row['SUBJECT']
    # standard labels
    try:


        # if os.path.exists(metrics_filename):
        #     continue
        img_path = '%s/%s' % (FLAIR_path, row['STANDARDIZED_NII'])
        
        img_path = 'data/FLAIR_standardized/%s' % row['STANDARDIZED_NII']
        
        img0 = image_read_rotation(img_path, transpose=[1,0,2])

        if os.path.exists('data/mask/%s' % row['MASK_NII']):
            img_mask = image_read_rotation('data/mask/%s' % row['MASK_NII'], transpose=[1,0,2])
        else: 
            img_mask = image_read_rotation('data/hdbet_mask/%s' % row['STANDARDIZED_NII'].replace('.nii.gz', '_mask.nii.gz'), transpose=[1,0,2])

        if not img_mask.shape == img0.shape:
            img_mask = ants.pad_image(img_mask, shape=img0.shape)



        t1_labels_path = 'outputs/registration_labels_t1/%s' % row['STANDARDIZED_NII']
        
        labels_pt = ants.image_read(t1_labels_path)
        # img0.plot(overlay=labels_pt,overlay_cmap='tab20', nslices=10, overlay_alpha=0.5, axis=2, figsize=3, )
        

        labels_pt = labels_pt.numpy()
        img_mask = img_mask.numpy()

        img0 = img0.numpy()
        img0[img_mask == 0] = 0
        labels_pt[img_mask==0] = 0

        mii = apply_slicewise(img0, MII)
        mad = apply_slicewise(img0, MAD)

        new_row = extract_metrics_from_map(img0, labels_pt, label_dict, mii, mad)
        new_row['TBV-voxel'] = np.sum(img_mask==1)
        pd.DataFrame(new_row).to_csv(metrics_filename, index=False, header=True)
        all_rows.append(new_row)


    except Exception:
        print('Error in %s' % metrics_filename)
# %%