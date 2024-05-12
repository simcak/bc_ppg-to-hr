import numpy as np
import matplotlib.pyplot as plt

"""
    plot the signal with the detected peaks
    it is called only when there is a significant diff between our and ref peaks
    (handled by if condition in HR_and_peakCount() function)
"""
def figure_ppg_with_peaks(data, peaksPositions, ppg_signal):
    time_axis = np.arange(len(ppg_signal)) / data['fs']

    # figure
    plt.figure(figsize=(10, 4))
    plt.plot(time_axis, ppg_signal, label='PPG Signal')
    plt.scatter(time_axis[peaksPositions], ppg_signal[peaksPositions], color='red', label='Detected Peaks')
    if data['refLocs'] is not 0:
        plt.scatter(time_axis[data['refLocs']], ppg_signal[data['refLocs']], marker='x', color='blue', label='Reference Peaks')
    plt.title(f'PPG Signal with Detected Peaks in: {data["ID"]}')
    plt.xlabel('Time [seconds]')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.show()

"""
    plot the HR over time for one signal
"""
def figure_HR_in_time(data, peaksPositions, rate):
    # Calculating our HR
    time_of_peaks = peaksPositions / data['fs']
    heart_rates = 60.0 / np.diff(time_of_peaks)

    # NeuroKit HR = rate
    # time_rate = np.linspace(0, len(data['ppg']) / data['fs'], len(rate))
    
    # Reference HR
    ref_peak_times = [loc / data['fs'] for loc in data['refLocs']]
    ref_heard_rates = 60.0 / np.diff(ref_peak_times)
    
    # figure
    plt.figure(figsize=(10, 4))
    plt.title(f'Heart Rate Over Time in: {data["name"]}')
    plt.plot(time_of_peaks[1:], heart_rates, label='Detected HR', color='red')
    plt.plot(ref_peak_times[1:], ref_heard_rates, label='Reference HR', color='blue')
    # plt.plot(time_rate, rate, label='NeuroKit HR', color='green')
    plt.xlabel('Time [seconds]')
    plt.ylabel('Heart Rate [BPM]')
    plt.legend()
    plt.show()

"""
    print out the results into simple table in the console
"""
def print_what_is_on_input(name, ref_locs_len, peaks_len, Our_HR, Ref_HR, HR_diff, peak_diff):
    # print out the results into simple table
    print(f"for {name}:")
    print(f"Average HR:            |{Our_HR:.2f} BPM")
    print(f"Reference HR:          |{Ref_HR:.2f} BPM")
    print(f"Detected our peaks:    |{peaks_len} peaks")
    print(f"Detected ref peaks:    |{ref_locs_len} peaks")
    print('- - - - - - - - - - - - - - - - - - - - - - - - - - -')
    print(f"Diff of HR: {HR_diff:.2f} BPM and diff of peaks: {peak_diff} peaks")
    print('-----------------------------------------------------')

"""
    this prints the confusion matrix in a nice table, into the console
"""
def print_confusion_matrix(confusion_matrix):
    width = 50
    table = "   |\tFN \t|\tFP \t|\tTP \t|\n"
    table += "-" * width + "\n"

    for i, (fn, fp, tp) in enumerate(confusion_matrix, start=1):
        table += f"{i} |\t{fn:2d} \t|\t{fp:2d} \t|\t{tp:2d} \t|\n"
    
    table += "-" * width + "\n"
    table += f"   |\t{sum([fn for fn, _, _ in confusion_matrix]):2d} \t|\t{sum([fp for _, fp, _ in confusion_matrix]):2d} \t|\t{sum([tp for _, _, tp in confusion_matrix]):2d} \t|\n"
    print(table)

"""
    - plot the cleaned PPG signal with detected peaks 
    - plot HR over time
"""
def figure_HR(rate):
    plt.figure(figsize=(10, 4))
    plt.plot(rate, label='Heart Rate', color='r')
    plt.legend()
    plt.title('Heart Rate from PPG')
    plt.xlabel('Sample Index')
    plt.ylabel('Heart Rate [BPM]')
    plt.show()
