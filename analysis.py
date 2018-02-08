import numpy as np


# TODO get performance in up, down, sideways trends
# TODO get performance in high, med, low volatility


def get_accuracy(output, tolerance=0.5):
    if output:
        diff = np.abs(output['truth']['out'] - output['result']['out']) < tolerance
        correct = diff.sum()
        total = len(diff)
        return correct / total


def get_average_distance(output):
    if output:
        diff = np.abs(output['truth']['out'] - output['result']['out'])
        total_diff = diff.sum()
        total = len(diff)
        return total_diff / total