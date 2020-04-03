"""
Utils for describers
"""

from typing import List, Optional

import numpy as np


class Stats:
    """
    Calculate the stats of a list of values.
    This is particularly helpful when you want to convert
    lists of values of different lengths to uniform length
    for machine learning purposes.

    supported
    """

    @staticmethod
    def max(data: List[float]) -> float:
        """
        Max of value
        Args:
            data (list): list of float data

        Returns: maximum value

        """
        return np.max(data)

    @staticmethod
    def min(data: List[float]) -> float:
        """
        min of value
        Args:
            data (list): list of float data

        Returns: minimum value

        """
        return np.min(data)

    @staticmethod
    def range(data: List[float]) -> float:
        """
        Range of values
        Args:
            data (list): list of float data

        Returns: range of values, i.e., max - min

        """
        return Stats.max(data) - Stats.min(data)

    @staticmethod
    def moment(data: List[float],
               weights: Optional[List[float]] = None,
               order: Optional[int] = None,
               max_order: Optional[int] = None):
        """
        Moment of probability mass function

        order = 1 means weighted mean
        order = 2 means standard deviation
        order > 2 corresponds to higher order moment to
            the 1./order power

        Args:
            data (list): list of float data
            weights (list or None): weights for each data points
            order (int): moment order
            max_order (int): if set, it will overwrite order

        Returns: float or list of floats

        """
        # check if only a single value should be output
        if max_order is None:
            single = True
        else:
            single = False

        if weights is None:
            weights = [1.0] * len(data)

        if max_order is not None:
            orders = list(range(1, max_order + 1))
        else:
            orders = [order or 1]

        stats = [_root_moment(data, weights, i) for i in orders]

        if not single:
            return stats
        return stats[0]

    @staticmethod
    def mean(data: List[float],
             weights: Optional[List[float]] = None) -> float:
        """
        Weighted average

        Args:
            data (list): list of float data
            weights (list or None): weights for each data point

        Returns: average value

        """
        return Stats.moment(data, weights=weights, order=1)

    @staticmethod
    def std(data: List[float],
            weights: Optional[List[float]] = None) -> float:
        """
        Standard deviation

        Args:
            data (list): list of float data
            weights (list or None): weights for each data point

        Returns: Standard deviation

        """

        return Stats.moment(data, weights=weights, order=2)

    @staticmethod
    def skewness(data: List[float],
                 weights: Optional[List[float]] = None) -> float:
        """
        Skewness of the distribution

        Args:
            data (list): list of float data
            weights (list or None): weights for each data point

        Returns: Skewness of the distribution

        """
        third = Stats.moment(data, weights=weights, order=3)
        std = Stats.std(data, weights=weights)
        return third ** 3 / std ** 3

    @staticmethod
    def kurtosis(data: List[float],
                 weights: Optional[List[float]] = None) -> float:
        """
        Kurtosis of the distribution

        Args:
            data (list): list of float data
            weights (list or None): weights for each data point

        Returns: Kurtosis of the distribution

        """
        fourth = Stats.moment(data, weights=weights, order=4)
        std = Stats.std(data, weights=weights)
        return fourth ** 4 / std ** 4


def _root_moment(data, weights, order) -> float:
    """
    Auxilliary function to compute moment

    Args:
        data (list): list of float data
        weights (list or None): weights for each data point
        order (int): order of moment

    Returns:

    """
    weights_sum = np.sum(weights)
    pmf = np.array(weights) / weights_sum
    mean = 0.0

    if order > 1:
        mean = np.mean(data)

    moment = sum([(i - mean) ** order * j for
                  i, j in zip(data, pmf)])

    return moment ** (1. / order)