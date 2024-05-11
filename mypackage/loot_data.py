from sklearn.preprocessing import StandardScaler
import h5py
import numpy as np
from scipy.signal import resample

"""
    open .mat file and extract the data. than we:
    - ravel() the data to make it 1D
    - ravel()[0] to make it scalar
    - normalize the ppg signal
    - refLogs are reshaped from 2D pandas to 1D list of integers
    - if the sampling rate is higher than 100Hz, we downsample the signal, refLocs to 100Hz
    than we handel error cases
    if all good, we return the data in a dictionary
"""
def loot_data_from_file(directory_path, name):
    data_arr = {}
    scaler = StandardScaler()

    try:
        with h5py.File(directory_path + name, 'r') as file:
            data_arr['ppg'] = file['signal']['pleth']['y'][()].ravel()
            data_arr['ppg'] = (data_arr['ppg'] - np.min(data_arr['ppg'])) / (np.max(data_arr['ppg']) - np.min(data_arr['ppg']))	# normalize the ppg signal
            data_arr['ppg'] = scaler.fit_transform(data_arr['ppg'].reshape(-1, 1)).flatten()                      # standardize the ppg signal
            data_arr['age'] = file['meta']['subject']['age'][()].ravel()[0]
            data_arr['weight'] = file['meta']['subject']['weight'][()].ravel()[0]
            data_arr['fs'] = file['param']['samplingrate']['pleth'][()].ravel()[0]
            data_arr['name'] = name
            data_arr['refLocs'] = [int(val[0]) for val in file['labels']['pleth']['peak']['x'][()].tolist()]
        
            # Check if downsampling is needed
            if data_arr['fs'] > 100:
                our_dream_fs = 100
                num_points = int(len(data_arr['ppg']) * our_dream_fs / data_arr['fs'])   # Calculate the number of points after downsampling
                original_length = len(data_arr['ppg'])                                   # Store original length for refLocs calculation
                data_arr['ppg'] = resample(data_arr['ppg'], num_points)                  # Downsample the ppg signal to 100Hz
                data_arr['fs'] = our_dream_fs
                scaling_factor = num_points / original_length                            # Calculate the scaling factor for refLocs
                data_arr['refLocs'] = [int(loc * scaling_factor) for loc in data_arr['refLocs']]

    # if file not found, return None
    except IOError:
        print(f"Error: File {name} could not be opened.")
        return None
    # if data not found, return None
    except KeyError as e:
        print(f"Error: Missing expected data in {name}: {e}")
        return None
    
    return (data_arr)
