import argparse
import pandas as pd
import numpy as np
import h5py
import matplotlib
from matplotlib import pyplot as plt
from numpy.fft import fft


def load(filepath: str):
    return h5py.File(filepath, 'r')



def draw(acceleration, accelleration_ts, time_diffs, event_ts):
    fig, (ax1, ax2) = plt.subplots(2)

    ax1.set_ylabel("Acceleration")
    ax1.plot(accelleration_ts, acceleration[0])
    ax1.plot(accelleration_ts, acceleration[1])
    ax1.plot(accelleration_ts, acceleration[2])
    for ts in event_ts:
        print(ts)
        ax1.axvline(ts)

    ax2.set_ylabel("Time diffs")
    ax2.plot(time_diffs)

    plt.show()

def value_diffs(list_to_diff, scale=1):
    """
    Calculates the difference between items in a list
    
    Returns a list with len(list_to_diff)-1 objects
    """
    diffs = [(j-i)*scale for i, j in zip(list_to_diff[:-1], list_to_diff[1:])]
    return diffs



def cli():
    xsense_sensor = "UPPER_ARM_R"
    base_path = "/home/moanos/Nextcloud/Masterarbeit/recordings/sync/14"
    xsense_path = f"{base_path}/xsense.h5"
    event_path = f"{base_path}/events.csv"
    data_acc = load(xsense_path)
    hand_acceleration = data_acc["Sensors"][xsense_sensor]["Accelerometer"]
    hand_timestamps = data_acc["Sensors"][xsense_sensor]["Timestamp"][0]/1_000_000
    canonical_start = hand_timestamps[0]
    hand_timestamps = hand_timestamps-canonical_start
    time_diffs_ms = value_diffs(hand_timestamps, 1000)
    print(f"Time diffs. Mean {np.mean(time_diffs_ms):.6}, Std {np.std(time_diffs_ms):.6}")
    print(f"Min: {min(time_diffs_ms)}, Max: {max(time_diffs_ms):.6}")
    
    len([diff for diff in time_diffs_ms if diff > 9])
    
    try:
        events = pd.read_csv(event_path)
        event_ts = events.timestamp
        event_ts = event_ts-canonical_start
    
        draw(hand_acceleration, hand_timestamps, time_diffs_ms, event_ts)
    except FileNotFoundError:
        draw(hand_acceleration, hand_timestamps, time_diffs_ms, [0])


if __name__ == "__main__":
    cli()
