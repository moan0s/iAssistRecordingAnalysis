import numpy as np
def diff_between_samples(samples):
    time_diffs = [samples[i + 1] - samples[i] for i in range(len(samples) - 1)]
    return time_diffs

def samples_lost(timestamps: list):
    """"
    Based on timestamps this funtion determines the number of datums lost
    """

    time_diffs = diff_between_samples(timestamps)
    median_deviation_time_diffs = np.median(time_diffs)
    std_deviation_time_diffs = np.std(time_diffs)

    number_samples_lost = 0
    for diff in time_diffs:
        if abs(diff - median_deviation_time_diffs) > std_deviation_time_diffs*2:
            number_samples_lost_in_diff = round(diff / median_deviation_time_diffs)-1
            number_samples_lost = number_samples_lost + number_samples_lost_in_diff

    percentage_samples_lost = number_samples_lost/len(time_diffs)
    return number_samples_lost, percentage_samples_lost

def jumps(seqIDS: list):
    """"
    Based on seqIDS this funtion determines all jumps
    """

    diffs = diff_between_samples(seqIDS)
    jump_list = []
    for diff in diffs:
        if diff > 1:
            jump_list.append(diff)
    return jump_list
