import numpy as np
import math


class BMFLC():
    """ FLC filter class

    Attributes
    ----------
    n : int
        Number of harmonics
    X : ndarray
        Reference input vector
    W : ndarray
        Weights
    V : ndarray
        Angular  frequencies
    mu : float
        Adaptive filter gain
    f0 : float
        Starting frequency
    dF : float
        Frequrncey step
    """

    def __init__(self, mu=0.01, fmin=3, fmax=9, dF=0.1):
        """
        Parameters
        ----------
        n : int
            Number of harmonics
        mu : float
            Adaptive filter gain
        f0 : float
            Starting frequency
        """

        self.n = int((fmax - fmin) / dF) + 1
        self.mu = mu
        self.fmax = fmax
        self.fmin = fmin
        self.X = np.zeros(shape=(2, self.n))
        self.W = np.zeros(shape=(2, self.n))
        self.V = np.array(np.zeros([self.n]))
        self.estimatedFrequency = 0

        for i in range(self.n):
            self.V[i] = 2 * math.pi * (self.fmin + dF * i)

    def update(self, k, s):
        """ BMFLC filter

        Parameters
        ----------
        k : float
            Time instant
        s : float
            Reference signal

        Returns
        -------
        y : float
            Estimated signal
        """
        for i in range(self.n):
            self.X[0][i] = math.sin(self.V[i] * k)
            self.X[1][i] = math.cos(self.V[i] * k)

        y = np.dot(np.transpose(self.W[0]), self.X[0]) + np.dot(np.transpose(self.W[1]), self.X[1])

        err = s - y

        # Update weights
        for i in range(self.n):
            self.W[0][i] += 2 * self.mu * self.X[0][i] * err
            self.W[1][i] += 2 * self.mu * self.X[1][i] * err

        a = 0
        b = 0
        vest = 0

        for i in range(self.n):
            a += (self.W[0][i] ** 2 + self.W[1][i] ** 2) * self.V[i]
            b += self.W[0][i] ** 2 + self.W[1][i] ** 2
        vest += a / b

        self.estimatedFrequency = vest / (2 * math.pi)

        return y


class FLCWrapper:
    """Wraps a generic FLC"""

    def __init__(self, classifier=None):
        """initialize Ringbuffer class

        Parameters
        ----------
        classifier : object
            classifier

        Returns
        -------

        """
        if classifier is None:
            classifier = BMFLC(mu=0.01, fmin=3, fmax=10, dF=0.4)
        self.classifier = classifier


    def estimate(self, timestamps, data):
        estimated_signal = []
        estimated_freq = []
        for idx, timestamp in enumerate(timestamps):
            est = self.classifier.update(timestamp, data[idx])
            estimated_signal.append(est)
            estimated_freq.append(self.classifier.estimatedFrequency)
        return estimated_signal, estimated_freq

    def process(self, timestamp, sample):
        """ stream data and classify

        Parameters
        ----------

        Returns
        -------
        estimated_signal : array
            array with reconstructed signal

        estimated_freq : array
            array with estimated frequencies

        """

        estimated_signal = self.classifier.BMFLC(timestamp, sample)
        estimated_freq = self.classifier.estimatedFrequency

        return estimated_signal, estimated_freq
