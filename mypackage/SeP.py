import numpy as np

"""
    Sensitivity and Positive Predictivity
"""
def confusion_matrix_calc(peaks, ref_peaks, tolerance):
    FN = 0
    FP = 0
    TP = 0

    for peak in peaks:
        pom = [ref for ref in ref_peaks if abs(peak - ref) <= tolerance]
        if not pom:
            FP += 1

    for peak in ref_peaks:
        pom = [q for q in peaks if abs(peak - q) <= tolerance]
        if not pom:
            FN += 1
        elif pom:
            TP += 1
            if len(pom) >= 2:
                FP += len(pom) - 1

    if not ref_peaks:
        TP = 0
        FP = 0
        FN = 0

    return FN, FP, TP

def calculate_Se_Pp(confusion_matrix):
    Se = np.sum(np.array([tp for _, _, tp in confusion_matrix])) / (np.sum(np.array([tp for _, _, tp in confusion_matrix])) + np.sum(np.array([fn for fn, _, _ in confusion_matrix])))
    Pp = np.sum(np.array([tp for _, _, tp in confusion_matrix])) / (np.sum(np.array([tp for _, _, tp in confusion_matrix])) + np.sum(np.array([fp for _, fp, _ in confusion_matrix])))
    
    return Se * 100, Pp * 100