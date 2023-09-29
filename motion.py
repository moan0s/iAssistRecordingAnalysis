import argparse
import pandas as pd
import h5py
from matplotlib import pyplot as plt


def load(filepath: str):
    return h5py.File(filepath, 'r')


def draw(data):
    mtw_sensor_id = 0
    sensor_0 = data["Sensors"]["FOREARM_R"]
    fig, (ax1, ax2, ax3) = plt.subplots(3)

    ax1.set_ylabel("Acceleration")
    ax1.plot(sensor_0["Accelerometer"][0])
    ax1.plot(sensor_0["Accelerometer"][1])
    ax1.plot(sensor_0["Accelerometer"][2])

    ax2.set_ylabel("Orientation (deg)")
    ax2.plot(sensor_0["Orientation"][0])
    ax2.plot(sensor_0["Orientation"][1])
    ax2.plot(sensor_0["Orientation"][2])

    ax3.set_ylabel("Angular velocity")
    ax3.plot(sensor_0["Gyroscope"][0])
    ax3.plot(sensor_0["Gyroscope"][1])
    ax3.plot(sensor_0["Gyroscope"][2])
    plt.show()


def cli():
    parser = argparse.ArgumentParser(description='View a h5 file containing motion tracker data')
    parser.add_argument('-i', '--input', help="The file to load")
    args = parser.parse_args()
    data = load(args.input)

    draw(data)


if __name__ == "__main__":
    cli()
