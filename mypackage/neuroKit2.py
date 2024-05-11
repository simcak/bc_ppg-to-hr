import neurokit2 as nk
import numpy as np

"""
    use of neuroKit2
    GitHub: https://github.com/peterhcharlton/NeuroKit
    
    returns cleaned_ppg, rate, peaks
    cleaned_ppg: cleaned PPG signal
    rate: heart rate = UNNECESSARY, because we calculate it ourselves in HR_and_peakCount (it is just for comparison + its smoothed)
    peaks: list indicates the location (index) of the peaks
"""
def neuroKit2(data):
    ppg_signal = data['ppg']
    fs = data['fs']

    # Process the PPG signal
    signals, info = nk.ppg_process(ppg_signal, sampling_rate=fs)

    # Extract clean PPG, heart rate, and peak locations as lists
    cleaned_ppg = signals['PPG_Clean']
    rate = signals['PPG_Rate']
    peak_table = signals['PPG_Peaks'] == 1  # The 'PPG_Peaks' column in the signals DataFrame indicates the location of the peaks. Peaks are marked with 1 (peak) and 0 (no peak)

    # here we convert the pandas series to numpy arrays
    cleaned_ppg_array = cleaned_ppg.values
    rate_array = rate.values
    peak_arr = np.array([i for i, value in enumerate(peak_table) if value == 1])    # Find the indices of the peaks

    return peak_arr, rate_array, cleaned_ppg_array
