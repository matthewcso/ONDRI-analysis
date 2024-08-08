import numpy as np
def create_label_dict(clinical_sheet):
    counts = clinical_sheet['Diagnosis'].value_counts()
    numeric_encodings = np.arange(len(counts))
    label_dict = dict(zip(counts.index, numeric_encodings))
    return label_dict

