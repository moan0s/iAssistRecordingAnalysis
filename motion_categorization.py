import argparse
import pandas as pd
import numpy as np
import h5py
from matplotlib import pyplot as plt


def load(filepath: str):
    return h5py.File(filepath, 'r')


def draw(acceleration, velocity, velocity2):
    fig, (ax1, ax2, ax3) = plt.subplots(3)

    ax1.set_ylabel("Acceleration")
    ax1.plot(acceleration[0])
    ax1.plot(acceleration[1])
    ax1.plot(acceleration[2])

    ax2.plot(velocity[:,0])
    ax2.plot(velocity[:,1])
    ax2.plot(velocity[:,2])

    ax3.plot(velocity2[:,0])
    ax3.plot(velocity2[:,1])
    ax3.plot(velocity2[:,2])
    plt.show()


def calculate_position(acceleration_data, timestamps, initial_position=(0, 0, 0), initial_velocity=(0, 0, 0)):
    position = np.array([initial_position,])
    velocity = np.array([initial_velocity,])

    for i in range(1, acceleration_data.shape[1]):
        print(i)
        step = timestamps[i] - timestamps[i - 1]
        acceleration = acceleration_data[:, i]

        idx = 0
        new_velocity = velocity[-1] + acceleration * step
        velocity = np.vstack((velocity, new_velocity))

        new_position = position[-1] + velocity[i-1] * step
        position = np.vstack((position, new_position))

    return velocity, position


def cli():
    parser = argparse.ArgumentParser(description='View a h5 file containing motion tracker data')
    parser.add_argument('-i', '--input', help="The file to load")
    args = parser.parse_args()
    data = load(args.input)
    acceleration = data["Sensors"]["FOREARM_R"]["Accelerometer"]
    timestamps = np.arange(acceleration.shape[1]) / 80
    velocity, position = calculate_position(acceleration, timestamps)
    acceleration2 = np.array((acceleration[0]-np.mean(acceleration[0]), acceleration[1]-np.mean(acceleration[1]), acceleration[2]-np.mean(acceleration[2])))
    velocity2, position2 = calculate_position(acceleration2, timestamps)
    draw(acceleration, velocity, velocity2)


if __name__ == "__main__":
    cli()
