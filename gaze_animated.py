import matplotlib.pyplot as plt
import numpy as np
import argparse

from matplotlib.animation import FuncAnimation
import pandas as pd
from time import sleep

# Fixing random state for reproducibility
np.random.seed(19680801)

def load(filepath: str):
    return pd.read_csv(filepath)

parser = argparse.ArgumentParser(description='View a csv file containing gaze data')
parser.add_argument('-i', '--input', help="The file to load")
args = parser.parse_args()
data = load(args.input)

# Create new Figure and an Axes which fills it.
fig = plt.figure(figsize=(7, 7))
ax = fig.add_axes([0, 0, 1, 1], frameon=False)
ax.set_xlim(0, int(max(data["gaze_x"]))), ax.set_xticks([])
ax.set_ylim(0, int(max(data["gaze_y"]))), ax.set_yticks([])

# Create rain data
n_drops = 50
drops = np.zeros(n_drops, dtype=[('position', float, (2,)),
                                 ('size',     float),
                                 ('color',    float, (4,))])


# Construct the scatter which we will update during animation
# as the raindrops develop.
scat = ax.scatter(data["gaze_x"][:50], data["gaze_y"][:50],
                  s=drops['size'], lw=0.5, edgecolors=drops['color'],
                  facecolors='none')


def update(frame_number):
    # Get an index which we can use to re-spawn the oldest raindrop.
    current_index = frame_number % n_drops

    # Make all colors more transparent as time progresses.
    drops['color'][:, 3] -= 1.0 / len(drops)
    drops['color'][:, 3] = np.clip(drops['color'][:, 3], 0, 1)

    # Make all circles bigger.
    drops['size'] -= 1

    try:
        drops['position'][current_index] = (data["gaze_x"][frame_number], data["gaze_y"][frame_number])
    except KeyError:
        print("Showed everything")
        exit()
    drops['size'][current_index] = 50
    drops['color'][current_index] = (0, 0, 0, 1)



    # Update the scatter collection, with the new colors, sizes and positions.
    scat.set_edgecolors(drops['color'])
    scat.set_sizes(drops['size'])
    scat.set_offsets(drops['position'])
    sleep(0.03)


# Construct the animation, using the update function as the animation director.
animation = FuncAnimation(fig, update, interval=10, save_count=100)
plt.show()
