import numpy as np

"""
    Calculate the HR and the difference between our HR and the reference HR
    - optionally we can print out the results
    - optionally we can plot the HR over time
"""
def HR_and_peakCount(data, peaksPositions, name):
    # Calculating our HR
    time_of_peaks = peaksPositions / data['fs']         # finding WHEN (in seconds) the peaks occur
    heart_rates = 60.0 / np.diff(time_of_peaks)         # calculating the HR from the time differences between peaks
    Our_HR = np.mean(heart_rates)
    # Reference HR
    ref_peak_times = [loc / data['fs'] for loc in data['refLocs']]
    ref_heard_rates = 60.0 / np.diff(ref_peak_times)
    Ref_HR = np.mean(ref_heard_rates)
    # DIFF
    HR_diff = abs(Our_HR - Ref_HR)
    peak_diff = abs(len(peaksPositions) - len(data['refLocs']))

    return Our_HR, Ref_HR, HR_diff, peak_diff
