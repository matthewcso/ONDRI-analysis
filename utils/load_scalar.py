from pymatreader import read_mat
import nibabel as nib
import warnings
import numpy as np
import ants

def load_scalar(file_path, index_strs, rot90=0, flip=False, debug=False):
  with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    mat = read_mat(file_path)


    for index_str in index_strs:
        if debug:
            print(mat.keys())
        mat = mat[index_str]

    mat = mat.astype('float32')
    mat = np.rot90(mat, k=rot90, axes=(0,1))
    if flip:
        mat = np.flip(mat, axis=0)

    return mat

def image_read_rotation(path, k=0, transpose=[0, 1, 2], flip=False, index_strs=[]):
    if path.endswith('.nii.gz'):
        dt = nib.load(path).get_fdata()
        dt = np.rot90(dt, k=k)
        if flip:
            dt = np.flip(dt, axis=0)
        if transpose != [0, 1, 2]:
            dt = np.transpose(dt, transpose)
            
    elif path.endswith('.mat'):
        dt = load_scalar(path, index_strs, rot90=k, flip=flip)
    return ants.from_numpy(dt)

