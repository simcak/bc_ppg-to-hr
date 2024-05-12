from sklearn.preprocessing import StandardScaler
import h5py
import numpy as np
from scipy.signal import resample
import scipy.io

"""
    accual looting function, that extracts the data from the capnobase file
    here we:
    - extract the ppg signal, age, weight, fs, name and refLocs
    - ravel() the data to make it 1D
    - ravel()[0] to make it scalar
    - normalize the ppg signal
    - refLogs are reshaped from 2D pandas to 1D list of integers
"""
def accual_looting(capnobase_file, data_arr, scaler, sample):
    data_arr['ppg'] = capnobase_file['signal']['pleth']['y'][()].ravel()
    data_arr['ppg'] = (data_arr['ppg'] - np.min(data_arr['ppg'])) / (np.max(data_arr['ppg']) - np.min(data_arr['ppg']))	# normalize the ppg signal
    data_arr['ppg'] = scaler.fit_transform(data_arr['ppg'].reshape(-1, 1)).flatten()                      # standardize the ppg signal
    data_arr['age'] = capnobase_file['meta']['subject']['age'][()].ravel()[0]
    data_arr['weight'] = capnobase_file['meta']['subject']['weight'][()].ravel()[0]
    data_arr['fs'] = capnobase_file['param']['samplingrate']['pleth'][()].ravel()[0]
    data_arr['name'] = sample
    data_arr['refLocs'] = [int(val[0]) for val in capnobase_file['labels']['pleth']['peak']['x'][()].tolist()]

    return data_arr

"""
    resample the data to 100Hz
"""
def resample_data(data_arr):
    our_dream_fs = 100
    num_points = int(len(data_arr['ppg']) * our_dream_fs / data_arr['fs'])   # Calculate the number of points after downsampling
    original_length = len(data_arr['ppg'])                                   # Store original length for refLocs calculation
    data_arr['ppg'] = resample(data_arr['ppg'], num_points)                  # Downsample the ppg signal to 100Hz
    data_arr['fs'] = our_dream_fs
    scaling_factor = num_points / original_length                            # Calculate the scaling factor for refLocs
    data_arr['refLocs'] = [int(loc * scaling_factor) for loc in data_arr['refLocs']]

    return data_arr
    
"""
    * open .mat file and extract the data in accual_looting function.
    * If the sampling rate is higher than 100Hz, we downsample the signal, refLocs to 100Hz.
    * Than we handel error cases
    If all good, we return the data in a dictionary
    
    directory_path: str
    sample: str
"""
def loot_data_from_capnobase(directory_path, sample):
    data_arr = {}
    scaler = StandardScaler()

    try:
        with h5py.File(directory_path + sample, 'r') as capnobase_file:
            data_arr = accual_looting(capnobase_file, data_arr, scaler, sample)
            if data_arr['fs'] > 100:
                data_arr = resample_data(data_arr)

    # if capnobase_file not found, return None
    except IOError:
        print(f"Error: capnobase_file {sample} could not be opened.")
        return None
    # if data not found, return None
    except KeyError as e:
        print(f"Error: Missing expected data in {sample}: {e}")
        return None
    
    return (data_arr)

"""
    loat data from BUT_PPG.mat file

    BUT_PPG_path: str
    sample_num: int
    - line in the file that contains the ppg signal
"""

def loot_data_from_BUT_PPG(BUT_PPG_path, sample_num):
    data_arr = {}
    scaler = StandardScaler()

    try:
        BUT_file = scipy.io.loadmat(BUT_PPG_path)
        data_arr['ppg'] = BUT_file['BUT_PPG']['PPG'][0][0][sample_num]
        data_arr['fs'] = BUT_file['BUT_PPG']['PPG_fs'][0][0][0][0]
        data_arr['ID'] = sample_num
        data_arr['ref_HR'] = BUT_file['BUT_PPG']['HR'][0][0][sample_num][0]
        data_arr['Quality'] = BUT_file['BUT_PPG']['Quality'][0][0][sample_num][0]
        data_arr['refLocs'] = 0

    except IOError:
        print(f"Error: Line: {sample_num} could not be opened.")
        return None
    except KeyError as e:
        print(f"Error: Missing expected data on line: {sample_num}: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

    return data_arr
