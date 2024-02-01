import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from iAssistADL_analysis.loaders import *
from iAssistADL_analysis.classifier import FLCWrapper, BMFLC


def plot_stuff(timestamps, real_signal, estimated_signal, estimated_freq, event_timestamps=None):

    real_signal = np.array(real_signal)
    real_signal[np.isnan(real_signal)] = 0
    """ pca if multiple sensors? 
    pca = PCA(n_components=1)
    pca_dat = pca.fit_transform(real_signal)
    pca_dat = np.reshape(pca_dat,[len(pca_dat),])
    """
    frame_rate = 60
    w = 6.
    freqs = np.linspace(1, frame_rate/3, 120)
    widths = w*frame_rate / (2*freqs*np.pi)
    cwtmatr = signal.cwt(real_signal, signal.morlet2, widths,w=w)

    fig, axs = plt.subplots(nrows=2)
    ax1 = axs[0]
    ax2 = axs[1]

    ax1.set_title("Frequency Analysis")

    ax1.pcolormesh(timestamps, freqs, np.abs(cwtmatr), cmap='viridis', shading='gouraud')
    ax1.plot(timestamps,estimated_freq,color='r', label='Estimated Frequency')
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Frequency (Hz)')
    ax1.legend()

    ax2.plot(timestamps, real_signal,color='b', label='Real Signal')
    ax2.plot(timestamps, estimated_signal, color='y', label='Estimated Signal')
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Signal')
    ax2.legend()

    if event_timestamps is not None:
        for event_timestamp in event_timestamps:
            ax1.axvline(event_timestamp, color="pink", label="Point reached")
            ax2.axvline(event_timestamp, color="pink", label="Point reached")

    fig.tight_layout()
    plt.show()

def find_timestamp_idx(time, timestamps):
    for idx, timestamp in enumerate(timestamps):
        if timestamp >= time:
            return idx

def cut(cutting_range, timestamps, signals):
    cut_signals = []
    timestamp_idx_start = find_timestamp_idx(cutting_range[0], timestamps)
    timestamp_idx_end = find_timestamp_idx(cutting_range[1], timestamps)

    for signal in signals:
        cut_signals.append(signal[timestamp_idx_start:timestamp_idx_end])
    return timestamps[timestamp_idx_start:timestamp_idx_end], cut_signals

if __name__ == "__main__":
    subject = "BRAD-3115"
    session = "1"
    recording = "2"
    sensor = "HAND_R" # FOREARM_R HAND_R
    use_real_time_estimation = False

    base_data_path = "/home/moanos/software/Compsense/recordings"
    recording_base_path = f"{base_data_path}/{subject}/{session}/{recording}"

    display_range = (5,9) # Timestamp in seconds from beginning
    # 1706265098.245
    event_timestamps = np.array([1706265099.111, 1706265100.178, 1706265100.9117, 1706265101.9119])


    sensor_timestamps = get_xsense_timestamps(recording_base_path, sensor)
    event_timestamps = event_timestamps-sensor_timestamps[0]
    sensor_timestamps = sensor_timestamps-sensor_timestamps[0]

    xsense = get_xsense_data(recording_base_path)
    real_signal = xsense["Sensors"][sensor]["Accelerometer"][0] # Selects the x-axis of the given sensor

    if use_real_time_estimation:
        estimated_signal = xsense["Sensors"][sensor]["Estimated_Signal"][0]
        estimated_freq = xsense["Sensors"][sensor]["Estimated_Frequency"][0]
    else:
        classifier = BMFLC(mu=0.01, fmin=2, fmax=10, dF=0.5)
        classification_wrapper = FLCWrapper(classifier)
        estimated_signal, estimated_freq = classification_wrapper.estimate(sensor_timestamps, real_signal)
    sensor_timestamps, (real_signal, estimated_signal, estimated_freq) = cut(display_range, sensor_timestamps, (real_signal, estimated_signal, estimated_freq))

    plot_stuff(sensor_timestamps, real_signal, estimated_signal, estimated_freq, event_timestamps)
    

    
