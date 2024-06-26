from scipy.signal import find_peaks, butter, filtfilt
import os
import numpy as np
import mypackage.print_out as po
import mypackage.SeP as sep
import mypackage.loot_data as ld
import mypackage.hr_and_peaks as hr
import mypackage.neuroKit2 as mnk

## 🥇 SET THE PATH TO THE DIRECTORY WITH THE FILES 🥈 ##
## 🥇 CAPNOBASE 🥇 ##
directory_path = './sources/capnobase/'                 # path to the directory with the files
files = os.listdir(directory_path)                      # listdir is listing all files in the directory
samples = [f for f in files[:] if f.endswith('.mat')]     # filtering out non-MAT files

## 🥈 BUT_PPG 🥈 ##
# BUT_PPG_path = './sources/BUT_PPG.mat'
# samples = [i for i in range(0, 48)]

"""
    here we decide what to print out
    its printing crossroad :)
    three dots are here, because we can commend all lines
"""
def choose_what_to_print(data, peaks, sample, Our_HR, Ref_HR, HR_diff, peak_diff, cleaned_ppg, rate):
    ## 📊 GOOD FOR CAPNOBASE DATASET 📊 ##
    po.print_what_is_on_input(sample, len(data['refLocs']), len(peaks), Our_HR, Ref_HR, HR_diff, peak_diff)
    
    # if (peak_diff >= 10):
        # po.figure_ppg_with_peaks(data, peaks, cleaned_ppg)
        # po.figure_ppg_with_peaks(data, peaks, data['ppg'])
        # po.figure_HR(rate)
        # po.figure_HR_in_time(data, peaks, rate)

    print(f"file: {sample}\nOur HR: {Our_HR:.2f} BPM \nRef HR: {Ref_HR:.2f} BPM")

    ## 📊 GOOD FOR BUT_PPG DATASET 📊 ##
    # po.figure_ppg_with_peaks(data, peaks, data['ppg'])
    # po.print_what_is_on_input(sample + 1, ref_locs_len=None, peaks_len=len(peaks), Our_HR=Our_HR, Ref_HR=Ref_HR, HR_diff=HR_diff, peak_diff=None)
    ...

"""
    Main function
    we iterate over all files in the directory
    - load data from file
    - find peaks (here we use scipy.signal.find_peaks plus our own peak finder)
    - calculate HR and peak count
    - print out our and ref HR for each file (optional)
    - print out the confusion matrix (optional)
    - calculate Se and Pp of our algorithm
"""
def __main__():    
    confusion_matrix = []
    tolerance_in_ms = 100
    peak_diff_v, cleaned_ppg_v, rate_v = 0, 0, 0

    for sample in samples:
        # # 🧨 CHOOSE THE DATA ARSENAL 🧨 ##
        data = ld.loot_data_from_capnobase(directory_path, sample)
        # data = ld.loot_data_from_BUT_PPG(BUT_PPG_path, sample)

        # # 🧨 CHOOSE THE PEAK-FINDING WEAPON 🧨 ##
        peaks, rate_v, cleaned_ppg_v = mnk.neuroKit2(data)
        # peaks, _ = find_peaks(data['ppg'], distance=data['fs']/2)
        # ZFR peak finder is defined and coded in Matlab
        # filtered_signal = bandpass_filter(data['ppg'], 0.5, 4.0, 30, 5)  # Adjust these values as needed
        # peaks = moving_window(data['ppg'], data['fs'])

        ## 🧮 CHOOSE THE HEART-RATE CALCULATOR 🧮 ##
        Our_HR, Ref_HR, HR_diff, peak_diff_v = hr.HR_and_peakCount(data, peaks, sample)
        # Our_HR, Ref_HR, HR_diff = hr.HR_and_peakCount_BUT_PPG(data, peaks)

        ## 🤔 CAN WE CALCULATE CONFUSION MATRIX? 🤔 ##
        FN, FP, TP = sep.confusion_matrix_calc(peaks, data['refLocs'], round(tolerance_in_ms * data['fs']/1000))
        confusion_matrix.append((FN, FP, TP))

        ## 🚏 PRINTING CROSSROAD 🚀 ##
        choose_what_to_print(data, peaks, sample, Our_HR, Ref_HR, HR_diff, peak_diff=peak_diff_v, cleaned_ppg=cleaned_ppg_v, rate=rate_v)
    
    ## 😵‍💫 PRINT CONFUSION MATRIX AT THE END 😵‍💫 ##
    po.print_confusion_matrix(confusion_matrix)
    Se, Pp = sep.calculate_Se_Pp(confusion_matrix)
    F1_score = sep.calculate_F1_score(Se, Pp)
    print (f"Se:  {Se:.3f}% \nPp:  {Pp:.3f}% \nF1:  {F1_score:.3f}%\n")

if __name__ == '__main__':
    __main__()
