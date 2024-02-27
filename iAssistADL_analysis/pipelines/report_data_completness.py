from iAssistADL_analysis.tools import samples_lost, jumps
from bashplotlib.histogram import plot_hist
import numpy as np
from iAssistADL_analysis.loaders import *



if __name__ == "__main__":
    subject = "BRAD-1"
    session = "2"
    recording = "2"
    base_data_path = "/home/moanos/Nextcloud/Masterarbeit/recordings/"
    recording_base_path = f"{base_data_path}/{subject}/{session}/{recording}"
    print("XSENSE")
    for sensor in ["FOREARM_R", "HAND_R", "STERNUM", "UPPER_ARM_R"]:
        sensor_timestamps = get_xsense_timestamps(recording_base_path, sensor)
        processing_timestamps = get_xsense_timestamps(recording_base_path, sensor, "processing")
        seqIDs = get_xsense_seqIDs(recording_base_path, sensor)
        jump_list = jumps(seqIDs)
        time_diff_to_processing = processing_timestamps-sensor_timestamps
        samples_lost_abs, samples_lost_ratio = samples_lost(sensor_timestamps)
        effective_sampling_frequency = len(sensor_timestamps) / (sensor_timestamps[-1] - sensor_timestamps[0])
        print(f"For {sensor} {samples_lost_abs} datums seem to be lost which equates to {samples_lost_ratio * 100:.3}%.")
        print(f"The sampling frequency overall was {effective_sampling_frequency:.4}Hz")
        print(f"The average delay to processing was {np.mean(time_diff_to_processing)*1000:.3}ms")
        print(f"There were {len(jump_list)} jumps ({len(jump_list)/len(seqIDs)*100:.4}%) which jumped over {sum(jump_list)} datums")
        sensor_timestamp_diff = diff_between_samples(sensor_timestamps)
        print(f"The mean diff between samples was {np.mean(sensor_timestamp_diff)*1000}ms the std was {np.std(sensor_timestamp_diff)*1000}ms")
        try:
            plot_hist(jump_list)
        except ZeroDivisionError:
            pass

    print("\nZED")
    sensor_timestamps = get_zed_timestamps(recording_base_path)
    processing_timestamps = get_zed_timestamps(recording_base_path, "processing")
    time_diff_to_processing = processing_timestamps - sensor_timestamps
    samples_lost_abs, samples_lost_ratio = samples_lost(sensor_timestamps)
    effective_sampling_frequency = len(sensor_timestamps) / (sensor_timestamps[-1] - sensor_timestamps[0])
    print(f"For ZED3D {samples_lost_abs} datums seem to be lost which equates to {samples_lost_ratio * 100:.3}%.")
    print(f"The sampling frequency overall was {effective_sampling_frequency:.4}Hz")
    print(f"The average delay to processing was {np.mean(time_diff_to_processing)*1000:.3}ms")
    sensor_timestamp_diff = diff_between_samples(sensor_timestamps)
    print(f"The mean diff between samples was {np.mean(sensor_timestamp_diff)*1000}ms the std was {np.std(sensor_timestamp_diff)*1000}ms")

    print("\nPUPIL")
    sensor_timestamps = get_gaze_timestamps(recording_base_path)
    processing_timestamps = get_gaze_timestamps(recording_base_path, "processing")
    time_diff_to_processing = np.array(processing_timestamps) - sensor_timestamps
    samples_lost_abs, samples_lost_ratio = samples_lost(sensor_timestamps)
    effective_sampling_frequency = len(sensor_timestamps) / (sensor_timestamps[-1] - sensor_timestamps[0])
    sensor_timestamp_diff = diff_between_samples(sensor_timestamps)
    print(f"For gaze data {samples_lost_abs} datums seem to be lost which equates to {samples_lost_ratio * 100:.4}%.")
    print(f"The sampling frequency overall was {effective_sampling_frequency:.4}Hz")
    print(f"The average delay to processing was {np.mean(time_diff_to_processing)*1000}ms")
    print(f"The mean diff between samples was {np.mean(sensor_timestamp_diff)*1000}ms the std was {np.std(sensor_timestamp_diff)*1000}ms")
