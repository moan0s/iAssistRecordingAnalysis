import h5py
import pandas as pd
from iAssistADL_analysis.tools import samples_lost
import numpy as np


def get_xsense_data(base_recording_path: str):
    data = h5py.File(f"{base_recording_path}/xsense.h5", 'r')
    return data


def get_zed_data(base_recording_path: str):
    data = h5py.File(f"{base_recording_path}/zed2i_skeleton3d.h5", 'r')
    return data


def get_gaze_data(base_recording_path: str):
    data = pd.read_csv(f"{base_recording_path}/gaze.csv")
    return data

def get_xsense_timestamps(base_recording_path: str, sensor: str, ts_type: str = "sensor"):
    data = get_xsense_data(base_recording_path)
    if ts_type == "sensor":
        return data["Sensors"][sensor]["Timestamp_Sensor"][0]
    else:
        return data["Sensors"][sensor]["Timestamp_Processing"][0]

def get_xsense_seqIDs(base_recording_path: str, sensor: str):
    data = get_xsense_data(base_recording_path)
    return data["Sensors"][sensor]["SeqID"][0]

def get_zed_timestamps(base_recording_path: str, ts_type: str = "sensor"):
    data = get_zed_data(base_recording_path)
    if ts_type == "sensor":
        return data["Timestamps"]["Timestamp_Sensor"][0]
    else:
        return data["Timestamps"]["Timestamp_Processing"][0]

def get_gaze_timestamps(base_recording_path: str, ts_type: str = "sensor"):
    data = get_gaze_data(base_recording_path)
    if ts_type == "sensor":
        return list(data["gaze_sensor_timestamps"])
    else:
        return list(data["gaze_processing_timestamps"])

if __name__ == "__main__":
    subject = "Test"
    session = "Completeness"
    recording = "1"
    base_data_path = "/home/moanos/Nextcloud/Masterarbeit/recordings/"
    recording_base_path = f"{base_data_path}/{subject}/{session}/{recording}"
    print("XSENSE")
    for sensor in ["FOREARM_R", "HAND_R", "STERNUM", "UPPER_ARM_R"]:
        sensor_timestamps = get_xsense_timestamps(recording_base_path, sensor)
        processing_timestamps = get_xsense_timestamps(recording_base_path, sensor, "processing")
        seqIDs = get_xsense_seqIDs(recording_base_path, sensor, "processing")
        time_diff_to_processing = processing_timestamps-sensor_timestamps
        samples_lost_abs, samples_lost_percentage = samples_lost(sensor_timestamps)
        effective_sampling_frequency = len(sensor_timestamps) / (sensor_timestamps[-1] - sensor_timestamps[0])
        print(f"For {sensor} {samples_lost_abs} datums seem to be lost which equates to {samples_lost_percentage * 100:.3}%.")
        print(f"The sampling frequency overall was {effective_sampling_frequency:.4}Hz")
        print(f"The average delay to processing was {np.mean(time_diff_to_processing)*1000:.3}ms")

    print("\nZED")
    sensor_timestamps = get_zed_timestamps(recording_base_path)
    processing_timestamps = get_zed_timestamps(recording_base_path, "processing")
    time_diff_to_processing = processing_timestamps - sensor_timestamps
    samples_lost_abs, samples_lost_percentage = samples_lost(sensor_timestamps)
    effective_sampling_frequency = len(sensor_timestamps) / (sensor_timestamps[-1] - sensor_timestamps[0])
    print(f"For ZED3D {samples_lost_abs} datums seem to be lost which equates to {samples_lost_percentage * 100:.3}%.")
    print(f"The sampling frequency overall was {effective_sampling_frequency:.4}Hz")
    print(f"The average delay to processing was {np.mean(time_diff_to_processing)*1000:.3}ms")

    print("\nPUPIL")
    sensor_timestamps = get_gaze_timestamps(recording_base_path)
    processing_timestamps = get_gaze_timestamps(recording_base_path, "processing")
    time_diff_to_processing = np.array(processing_timestamps) - sensor_timestamps
    samples_lost_abs, samples_lost_percentage = samples_lost(sensor_timestamps)
    effective_sampling_frequency = len(sensor_timestamps) / (sensor_timestamps[-1] - sensor_timestamps[0])
    print(f"For gaze data {samples_lost_abs} datums seem to be lost which equates to {samples_lost_percentage * 100:.3}%.")
    print(f"The sampling frequency overall was {effective_sampling_frequency:.4}Hz")
    print(f"The average delay to processing was {np.mean(time_diff_to_processing)*1000}ms")
