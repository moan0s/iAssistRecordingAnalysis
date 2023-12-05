import numpy as np
def time_diff_between_samples(timestamps):
    time_diffs = [timestamps[i + 1] - timestamps[i] for i in range(len(timestamps) - 1)]
    return time_diffs

def samples_lost(timestamps: list):
    """"
    Based on timestamps this funtion determines the number of datums lost
    """

    time_diffs = time_diff_between_samples(timestamps)
    median_deviation_time_diffs = np.median(time_diffs)
    std_deviation_time_diffs = np.std(time_diffs)

    number_samples_lost = 0
    for diff in time_diffs:
        if abs(diff - median_deviation_time_diffs) > std_deviation_time_diffs*2:
            number_samples_lost_in_diff = round(diff / median_deviation_time_diffs)-1
            number_samples_lost = number_samples_lost + number_samples_lost_in_diff

    percentage_samples_lost = number_samples_lost/len(time_diffs)
    return number_samples_lost, percentage_samples_lost