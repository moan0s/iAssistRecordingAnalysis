import pytest
import time
import random
from iAssistADL_analysis.tools import samples_lost


def _generate_unix_timestamps(num_timestamps, sampling_frequency, jitter_coefficient, num_lost_datums=0):
    """
    Generates artificial unix timestamps with jitter and a defined number of lost datums
    """
    timestamps = []
    base_time = time.time()
    base_time_between_samples = 1 / sampling_frequency
    absolute_jitter = base_time_between_samples*jitter_coefficient

    for i in range(num_timestamps):
        timestamp = base_time + i * base_time_between_samples + random.uniform(-absolute_jitter, absolute_jitter)
        timestamps.append(timestamp)

    for i in range(0, num_lost_datums):
        idx = random.randint(1, len(timestamps) - 1)
        timestamps.pop(idx)

    return timestamps


def test_missed_datums():
    # Generates unix timestamps with 120 hz and a jitter of 1/3 of the period
    num_dropped_datums = 12
    timestamps = _generate_unix_timestamps(100, 120, 1 / (120 * 3), num_dropped_datums)
    num_samples_lost, percentage_samples_lost = samples_lost(timestamps)
    assert num_samples_lost == num_dropped_datums
