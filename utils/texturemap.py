import numpy as np
from scipy.spatial.distance import cdist

def shift(array, offset, constant_values=0):
    """Returns copy of array shifted by offset, with fill using constant."""
    array = np.asarray(array)
    offset = np.atleast_1d(offset)
    assert len(offset) == array.ndim
    new_array = np.empty_like(array)

    def slice1(o):
        return slice(o, None) if o >= 0 else slice(0, o)

    new_array[tuple(slice1(o) for o in offset)] = (
        array[tuple(slice1(-o) for o in offset)])

    for axis, o in enumerate(offset):
        new_array[(slice(None),) * axis +
                (slice(0, o) if o >= 0 else slice(o, None),)] = constant_values

    return new_array


def MII(img):
    """
    Calculates the microstructural integrity index (MII) of an image.

    Args:
        img (numpy.ndarray): 2D image array
    
    Returns:
        lbp: the MII map of the image
    """

    # LBP is sum(s(I_p - I_c) * 2^P) where I_p is the intensity of the neighboring pixel 
    # and I_c is the intensity of the central pixel

    # [0, 1] left shift 1, [0, -1] right shift 1
    # [0, -1] up shift 1
    

    def s(x):
        # s(x)=1 when x > 0, 0 otherwise
        # and in this case, when NaN, also 0
        # (a NaN value wouldn't contribute to the sum anyway)
        return np.greater(x, 0)

    # neighboring is all I_p 
    central = img
    neighboring = []
    for shift_amt_x in [-1, 0, 1]:
        for shift_amt_y in [-1, 0, 1]:
            if not (shift_amt_x == 0 and shift_amt_y == 0):
                neighboring.append(shift(central, [shift_amt_x, shift_amt_y], constant_values=np.nan))
    neighboring = np.asarray(neighboring)

    # P is the number of neighboring pixels (valid non-NaN pixels)
    P = np.sum(~np.isnan(neighboring), axis=0)

    # we sum s(I_p - I_c) first, as 2**P is a constant for each pixel
    lbp = np.sum(s(neighboring - np.expand_dims(central, axis=0)), axis=0) * (2**P)
    return lbp

def MAD(img):
    central = img
    neighboring = []
    distances = []
    for shift_amt_x in [-1, 0, 1]:
        for shift_amt_y in [-1, 0, 1]:
            if not (shift_amt_x == 0 and shift_amt_y == 0):
                neighboring.append(shift(central, [shift_amt_x, shift_amt_y], constant_values=np.nan))
                distances.append(np.sqrt(shift_amt_x**2 + shift_amt_y**2))
    neighboring = np.asarray(neighboring)
    distances = np.asarray(distances)

    W = np.abs(neighboring - central)
    WU = W * np.expand_dims(np.expand_dims(distances, axis=-1), axis=-1)
    # don't have to consider central pixel as the distance will be 0, so W*U will be 0
    
    return np.nansum(WU, axis=0)




def apply_slicewise(img, fn):
    assert img.ndim == 3

    slice_maps_0 = []
    for i in range(img.shape[0]):
        slice_maps_0.append(np.expand_dims(fn(img[i, :, :]), axis=0))

    slice_maps_0 = np.concatenate(slice_maps_0, axis=0)
    

    slice_maps_1 = []
    for i in range(img.shape[1]):
        slice_maps_1.append(np.expand_dims(fn(img[:, i, :]), axis=1))

    slice_maps_1 = np.concatenate(slice_maps_1, axis=1)

    slice_maps_2 = []
    for i in range(img.shape[2]):
        slice_maps_2.append(np.expand_dims(fn(img[:, :, i]), axis=2))

    slice_maps_2 = np.concatenate(slice_maps_2, axis=2)

    aggregate_map = np.stack([slice_maps_0, slice_maps_1, slice_maps_2])
    aggregate_map = np.mean(aggregate_map, axis=0)
    #aggregate_map = slice_maps_2
    return aggregate_map

