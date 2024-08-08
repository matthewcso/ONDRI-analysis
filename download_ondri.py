# %%
# %%
import os
from utils.gdrive_utils import *
import pandas as pd
import os



# # %%
drive = authenticate("credentials.txt")




# %%
id_NeuroMRI_DB2 = '0AP8L6d0wygnpUk9PVA'
id_ONDRI_FLAIR_STANDARDIZED = '1cET9JM582DARlJQsaOcP5gmS8YF5oa5c' 
id_MASK = '1DVo3-eAYo18cVk5Bn8WPVcG94eZ5EA-C'
id_WML = '1EoqnZHBmOE557hL5tf-IpNBegDuHgnaV'
id_ONDRI_T1_NII = '1VwQt1qSXzcRnyj3GXkwg7_KNGNViJL4m'
id_ONDRI_FLAIR_NONSTANDARDIZED = '1z_Tuz_oj4ipv26jAKj1ipbpQI4yMN64q'

flair_standardized_file_list = list_folder(id_ONDRI_FLAIR_STANDARDIZED, drive)
flair_nonstandardized_file_list = list_folder(id_ONDRI_FLAIR_NONSTANDARDIZED, drive)
t1_file_list = list_folder(id_ONDRI_T1_NII, drive)
mask_file_list = list_folder(id_MASK, drive)
wml_file_list = list_folder(id_WML, drive)


# %%
flair_summary = pd.read_excel('data/summary/OND01_FLAIR_Summary.xlsx')
t1_summary = pd.read_excel('data/summary/OND01_T1_Summary.xlsx')
merged = flair_summary[['SUBJECT', 'NII_FILENAME', 'MAT_FILENAME', 'COHORT', 'VISIT']]
# merged['COHORT'] = merged['COHORT_FLAIR'].combine_first(merged['COHORT_T1'])
# merged = merged.drop(columns=['COHORT_FLAIR', 'COHORT_T1'])
merged['SUBJECT'] = [x.replace('_', '') for x in merged['SUBJECT']]



# %%

df = pd.DataFrame()
titles = [x['title'] for x in flair_standardized_file_list]
df['SUBJECT'] = [x[4:16] for x in titles]
df['VISIT'] = [int(x[21:23]) for x in titles]
df['STANDARDIZED_NII'] = titles

merged = pd.merge(df, merged,  how='outer', on=['SUBJECT', 'VISIT'])
merged = merged[~pd.isna(merged['STANDARDIZED_NII'])]


# %%

df = pd.DataFrame()
titles = [x['title'] for x in mask_file_list]
df['SUBJECT'] = [x[4:16] for x in titles]
df['VISIT'] = [int(x[21:23]) for x in titles]
df['MASK_NII'] = titles

merged = pd.merge(df, merged,  how='outer', on=['SUBJECT', 'VISIT'])



# %%

df = pd.DataFrame()
titles = [x['title'] for x in wml_file_list]
df['SUBJECT'] = [x[4:16] for x in titles]
df['VISIT'] = [int(x[21:23]) for x in titles]
df['WML_NII'] = titles

merged = pd.merge(df, merged,  how='outer', on=['SUBJECT', 'VISIT'])

# %%
df = pd.DataFrame()
titles = [x['title'] for x in t1_file_list]
df['SUBJECT'] = [x[4:16] for x in titles]
df['VISIT'] = [int(x[21:23]) for x in titles]
df['NII_FILENAME_T1'] = titles

merged = pd.merge(df, merged,  how='outer', on=['SUBJECT', 'VISIT'])




# %%
merged = merged.sort_values('VISIT').groupby('SUBJECT').first().reset_index()


# %%
merged = merged.drop(columns=['NII_FILENAME', 'MAT_FILENAME'])

# %% 

merged = pd.merge(merged, t1_summary[['SUBJECT', 'VISIT', 'COHORT']], how='outer', on=['SUBJECT', 'VISIT'], suffixes=('_FLAIR', '_T1'))
merged['COHORT'] = merged['COHORT_FLAIR'].combine_first(merged['COHORT_T1'])
merged['COHORT'][pd.isna(merged['COHORT'])] = 'HC'

 # %%
merged = merged[~pd.isna(merged['STANDARDIZED_NII'])]

# %%
merged.to_csv('data/summary/ONDRI_summary.csv', index=False)

# %%

t1_files_selected = list(filter(lambda x: x['title'] in merged['NII_FILENAME_T1'].values, t1_file_list))
mask_files_selected = list(filter(lambda x: x['title'] in merged['MASK_NII'].values, mask_file_list))
wml_files_selected = list(filter(lambda x: x['title'] in merged['WML_NII'].values, wml_file_list))
flair_standardized_files_selected = list(filter(lambda x: x['title'] in merged['STANDARDIZED_NII'].values, flair_standardized_file_list))

download_multiple_gdrive(t1_files_selected, 'data/T1/')
print('Completed T1!')

download_multiple_gdrive(flair_standardized_files_selected, 'data/FLAIR_standardized/')
print('Completed FLAIR!')

download_multiple_gdrive(mask_files_selected, 'data/mask/')
print('Completed Mask!')

download_multiple_gdrive(wml_files_selected, 'data/WML/')
print('Completed Mask!')


