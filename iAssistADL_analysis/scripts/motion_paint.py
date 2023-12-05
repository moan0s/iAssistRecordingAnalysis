import argparse
import pandas as pd
import numpy as np
import h5py
import matplotlib
from matplotlib import pyplot as plt
from numpy.fft import fft


def load(filepath: str):
    return h5py.File(filepath, 'r')

def _plot_xsense_data(ax1, data, mtw_sensor_id, timestamps):
    sampling_rate = 60  # For plotting we assume a sampling_rate of 80
    ax1.clear()  # Clear the canvas.
    ax1.set_ylabel("Acceleration")
    ax1.plot(timestamps, data[0])
    ax1.plot(timestamps, data[1])
    ax1.plot(timestamps, data[2])

def paint_xsense_plot(data, timestamps):
    fig, ax1 = plt.subplots(1)
    for i in range(0, data.shape[1]-600):
        _plot_xsense_data(ax1, data[:,i:i+600], 1, timestamps[i:i+600])
        fig.canvas.draw()
        fig.canvas.flush_events()


from matplotlib.figure import Figure



xsense_sensor = "HAND_R"
base_path = "/home/moanos/Nextcloud/Masterarbeit/recordings/Recording/1"
xsense_path = f"{base_path}/xsense.h5"
event_path = f"{base_path}/events.csv"
data_acc = load(xsense_path)
hand_acceleration = data_acc["Sensors"][xsense_sensor]["Accelerometer"]
timestamps = data_acc["Sensors"][xsense_sensor]["Timestamp"][0]
paint_xsense_plot(hand_acceleration, timestamps)
