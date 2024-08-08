from utils.texturemap import *
from scipy.stats import skew, kurtosis
import numpy as np
import pandas as pd
import ants


def extract_metrics_from_map(img, labels_ptx, total_lookup, mii_all, mad_all):
    columns = []
    col_names = []

    for x in total_lookup.keys():
        col_values = [np.nan for _ in range(7)]
        if len(img[labels_ptx==x]) != 0:
            nvox = np.sum(labels_ptx==x)

            mean = np.mean(img[labels_ptx==x])
            std = np.std(img[labels_ptx==x])
            skewness = skew(img[labels_ptx==x])
            kurt = kurtosis(img[labels_ptx==x])

            mii = np.nanmean(mii_all[labels_ptx==x])
            mad = np.nanmean(mad_all[labels_ptx==x])
            col_values = [mad, mii, std, skewness, kurt, mean, nvox]        

        col_types = ['MAD', 'MII', 'std', 'skewness', 'kurtosis', 'mean', 'nvox']
        for ic, _ in enumerate(col_types):
            col_names.append('%s_%s' % (col_types[ic], total_lookup[x]))
            columns.append(col_values[ic])


    row = pd.concat([pd.Series(columns, index=col_names)], axis=1).T

    return row
