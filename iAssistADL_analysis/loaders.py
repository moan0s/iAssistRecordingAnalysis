import h5py
import pandas as pd
def get_xsense_data(base_recording_path: str):
    data = h5py.File(f"{base_recording_path}/xsense.h5", 'r')
    return data


def get_zed_skeleton3d_data(base_recording_path: str):
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

def get_zed_timestamps(base_recording_path: str, ts_type: str = "sensor", tracked_object=None):
    data = get_zed_skeleton3d_data(base_recording_path)
    if tracked_object is None:
        skeleton = list(data["Skeletons"].keys())[0]
    else:
        skeleton = tracked_object
    sensor_timestamps = data["Skeletons"][skeleton]["Timestamps"]["Timestamp_Sensor"][0]
    processing_timestamps = data["Skeletons"][skeleton]["Timestamps"]["Timestamp_Processing"][0]
    if ts_type == "sensor":
        return sensor_timestamps
    else:
        return processing_timestamps

def get_gaze_timestamps(base_recording_path: str, ts_type: str = "sensor"):
    data = get_gaze_data(base_recording_path)
    if ts_type == "sensor":
        return list(data["gaze_sensor_timestamps"])
    else:
        return list(data["gaze_processing_timestamps"])
