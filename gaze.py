import argparse
import pandas as pd
from matplotlib import pyplot as plt


def load(filepath: str):
    return pd.read_csv(filepath)


def draw(data):
    plt.plot(data["gaze_x"], data["gaze_y"], 'ro')
    plt.show()


def cli():
    parser = argparse.ArgumentParser(description='View a csv file containing gaze data')
    parser.add_argument('-i', '--input', help="The file to load")
    args = parser.parse_args()
    data = load(args.input)

    draw(data)


if __name__ == "__main__":
    cli()
