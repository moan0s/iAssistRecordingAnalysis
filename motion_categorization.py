import argparse
import pandas as pd
import numpy as np
import h5py
from matplotlib import pyplot as plt


def load(filepath: str):
    return h5py.File(filepath, 'r')


def draw(acceleration, velocity, velocity2, timestamps):
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4)

    ax1.set_ylabel("Acceleration")
    ax1.plot(acceleration[0])
    ax1.plot(acceleration[1])
    ax1.plot(acceleration[2])

    ax2.plot(velocity[0])
    ax2.plot(velocity[1])
    ax2.plot(velocity[2])

    ax3.plot(velocity2[0])
    ax3.plot(velocity2[1])
    ax3.plot(velocity2[2])

    steps = np.diff(timestamps)
    ax4.set_ylabel("Derivative of Acceleration")
    ax4.plot(np.diff(acceleration[0])/steps, label="X")
    ax4.plot(np.diff(acceleration[1])/steps, label="X")
    ax4.plot(np.diff(acceleration[2])/steps, label="X")
    ax4.legend(loc='upper center', shadow=True, fontsize='x-large')
    plt.show()


def calculate_position(acceleration_data, timestamps, initial_position=(0, 0, 0), initial_velocity=(0, 0, 0)):
    position = np.transpose(np.array(initial_position, ndmin=2))
    velocity = np.transpose(np.array(initial_velocity, ndmin=2))

    for i in range(1, acceleration_data.shape[1]):
        step = timestamps[i] - timestamps[i - 1]
        acceleration = acceleration_data[:, i]

        new_velocity = velocity[:, -1] + acceleration * step
        velocity = np.column_stack((velocity, new_velocity))

        new_position = position[:, -1] + new_velocity * step
        position = np.column_stack((position, new_position))

    return velocity, position


def cli():
    parser = argparse.ArgumentParser(description='View a h5 file containing motion tracker data')
    parser.add_argument('-i', '--input', help="The file to load")
    args = parser.parse_args()
    data = load(args.input)
    acceleration = data["Sensors"]["FOREARM_R"]["Accelerometer"]
    timestamps = np.arange(acceleration.shape[1]) / 80
    velocity, position = calculate_position(acceleration, timestamps)
    acceleration_corrected = np.array((acceleration[0] - np.mean(acceleration[0]), acceleration[1] - np.mean(acceleration[1]),
                              acceleration[2] - np.mean(acceleration[2])))
    velocity2, position2 = calculate_position(acceleration_corrected, timestamps)
    draw(acceleration, velocity, velocity2, timestamps)


if __name__ == "__main__":
    cli()
