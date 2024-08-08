import pandas as pd
import os
import numpy as np

# -------------------------------------------------------------------------------------------------------
def load_ondri_data(include_flair=False):
    # load ONDRI data
    ondri_master = pd.read_csv('ondri_master_t1_and_flair.csv')
    ondri_master = ondri_master.rename(columns={'COHORT_T1':'DIAGNOSIS'})

    # Volume metrics
    volume_df = pd.read_csv('ONDRI_volume_features.csv')
    volume_df = volume_df.drop(columns=['COHORT_T1'])
    vol_cols = list(filter(lambda x: x not in ['DIAGNOSIS', 'TBV-voxel', 'SUBJECT'], volume_df.columns))
    volume_df[vol_cols] = volume_df[vol_cols]/np.expand_dims(volume_df['TBV-voxel'], axis=-1)

    # FLAIR metrics
    if include_flair:
        all_metric_dfs = []
        seg_folders = ['segmentation/metrics_ondri_fs/', 'segmentation/metrics_ondri_fs_simplified/', 'segmentation/metrics_ondri_fs_ctx/']
        for seg_folder in seg_folders:
            metric_df = []
            seg_files = os.listdir(seg_folder)
            for file in seg_files:
                metric_df.append(pd.read_csv(seg_folder + file))

            metric_df = pd.concat(metric_df)
            metric_df['SUBJECT'] = [x.split('.')[:-1][0] for x in seg_files]
            if 'TBV-voxel' in metric_df.columns:
                metric_df = metric_df.drop(columns=['TBV-voxel'])
            
            metric_df = metric_df[list(filter(lambda x: ('nvox' not in x) and 'CC' not in x, metric_df.columns))]
                
            metric_df = metric_df.dropna(axis=1, how='all')
            all_metric_dfs.append(metric_df)

        metric_df = all_metric_dfs[0]
        for metric_df_ in all_metric_dfs[1:]:
            metric_df = pd.merge(metric_df, metric_df_, on='SUBJECT')

        failed_ondri = ['BYC_1012','BYC_3009', 'EBH_1012', 'CAM_1026', 'CAM_1030', 'LHS_2001', 'LHS_2004', 'LHS_2005', 'LHS_4018', 'PKH_1021','LHS_4022', 'EBH_3001', 'EBH_3006', 'TOH_4025', 'TOH_4035', 'TOH_4040',
                        'TOH_4024']
        failed_ondri = ['OND01_' + x for x in failed_ondri]
        metric_df = metric_df[~metric_df['SUBJECT'].isin(failed_ondri)]

    # -------------------------------------------------------------------------------------------------------
    ondri_merged = pd.merge(ondri_master[['SUBJECT', 'DIAGNOSIS']], volume_df, on='SUBJECT', how='inner')

    if include_flair:
        ondri_merged = pd.merge(ondri_merged, metric_df, on='SUBJECT', how='inner')
        
    print(ondri_merged['DIAGNOSIS'].value_counts())

    return ondri_merged


def load_ondri_data_t1(include_flair=False):
    # load ONDRI data
    ondri_master = pd.read_csv('ondri_master_t1_and_flair.csv')
    ondri_master = ondri_master.rename(columns={'COHORT_T1':'DIAGNOSIS'})

    # Volume metrics
    volume_df = pd.read_csv('ONDRI_volume_features.csv')
    volume_df = volume_df.drop(columns=['COHORT_T1'])
    vol_cols = list(filter(lambda x: x not in ['DIAGNOSIS', 'TBV-voxel', 'SUBJECT'], volume_df.columns))
    volume_df[vol_cols] = volume_df[vol_cols]/np.expand_dims(volume_df['TBV-voxel'], axis=-1)

    # FLAIR metrics
    if include_flair:
        all_metric_dfs = []
        seg_folders = ['segmentation/metrics_ondri_fs_t1/', 'segmentation/metrics_ondri_fs_simplified_t1/', 'segmentation/metrics_ondri_fs_ctx_t1/']
        for seg_folder in seg_folders:
            metric_df = []
            seg_files = os.listdir(seg_folder)
            for file in seg_files:
                metric_df.append(pd.read_csv(seg_folder + file))

            metric_df = pd.concat(metric_df)
            metric_df['SUBJECT'] = [x.split('.')[:-1][0] for x in seg_files]
            if 'TBV-voxel' in metric_df.columns:
                metric_df = metric_df.drop(columns=['TBV-voxel'])
            
            metric_df = metric_df[list(filter(lambda x: ('nvox' not in x) and 'CC' not in x, metric_df.columns))]
                
            metric_df = metric_df.dropna(axis=1, how='all')
            all_metric_dfs.append(metric_df)

        metric_df = all_metric_dfs[0]
        for metric_df_ in all_metric_dfs[1:]:
            metric_df = pd.merge(metric_df, metric_df_, on='SUBJECT')

        failed_ondri = ['BYC_1012','BYC_3009', 'EBH_1012', 'CAM_1026', 'CAM_1030', 'LHS_2001', 'LHS_2004', 'LHS_2005', 'LHS_4018', 'PKH_1021','LHS_4022', 'EBH_3001', 'EBH_3006', 'TOH_4025', 'TOH_4035', 'TOH_4040',
                        'TOH_4024']
        failed_ondri = ['OND01_' + x for x in failed_ondri]
        metric_df = metric_df[~metric_df['SUBJECT'].isin(failed_ondri)]

    # -------------------------------------------------------------------------------------------------------
    ondri_merged = pd.merge(ondri_master[['SUBJECT', 'DIAGNOSIS']], volume_df, on='SUBJECT', how='inner')

    if include_flair:
        ondri_merged = pd.merge(ondri_merged, metric_df, on='SUBJECT', how='inner')
        
    print(ondri_merged['DIAGNOSIS'].value_counts())

    return ondri_merged