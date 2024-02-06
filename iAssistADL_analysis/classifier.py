import numpy as np
import math

class PowerEstimator():
    def __init__(self):
        self.power = 0
        self.last_datum = 0
        self.coefficient = 0.9
    def update(self, datum):
        self.power = self.power*self.coefficient+abs(self.last_datum-datum)
        self.last_datum = datum
        return self.power

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

class BMFLC_Kalman():
    """
    FLC filter class

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
    fmin : float
        Minimum frequency
    fmax : float
        Maximum frequency
    dF : float
        Frequrncey step
    R : float
        measurement noise
    Q : float
        system noise
    P : float
        covariance weight

    """

    def __init__(self, fmin=3, fmax=9, dF=0.1, R=0.01, Q=0.01, P=0.01):
        """
        Parameters
        ----------
        n : int
            Number of harmonics
        f0 : float
            Starting frequency
        """

        self.n = int((fmax - fmin) / dF) + 1
        self.fmax = fmax
        self.fmin = fmin
        self.X = np.zeros(shape=(1, self.n * 2 + 1))
        self.X[0][-1] = 1
        self.W = np.zeros(shape=(1, self.n * 2 + 1))
        self.V = np.array(np.zeros([self.n + 1]))
        self.estimatedFrequency = 0
        # Kalman stuff
        self.P = np.identity(self.n * 2 + 1) * P  # Covariance Matrix
        self.K = np.zeros(shape=(self.n * 2 + 1, 1))  # Kalman gain
        self.R = np.array([[R]])  # measurement noise covariance

        self.Q = np.eye(self.n * 2 + 1) * Q  # process noise covariance

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
            self.X[0][i + self.n] = math.cos(self.V[i] * k)

        y = np.dot(np.transpose(self.W[0][0:self.n]), self.X[0][0:self.n]) + np.dot(np.transpose(self.W[0][self.n:]),
                                                                                    self.X[0][self.n:])

        # Update weights Kalman

        # Compute Kalman gain K = P * H^T * (H * P * H^T + R)^-1
        S = np.dot(np.dot(self.X, self.P), np.transpose(self.X)) + self.R
        S_inv = S ** -1
        self.K = np.dot(np.dot(self.P, np.transpose(self.X)), S_inv)

        # Update the BMFLC weights?
        newW0 = np.dot(self.K, (s - np.dot(np.transpose(self.X[0]), self.W[0])))
        self.W[0] += newW0.flatten()

        # Update correlation matrix
        self.P = np.dot((np.identity(len(self.K)) - np.dot(self.K, self.X)), self.P) + self.Q

        I = self.W[0][-1]
        T = y - I

        a = 0
        b = 0
        vest = 0

        for i in range(self.n):
            a += (self.W[0][i] ** 2 + self.W[0][i + self.n] ** 2) * self.V[i]
            b += self.W[0][i] ** 2 + self.W[0][i + self.n] ** 2
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
        self.power_estimator = PowerEstimator()


    def estimate(self, timestamps, data):
        estimated_signal = []
        estimated_freq = []
        estimated_power = []
        for idx, timestamp in enumerate(timestamps):
            signal, freq, power = self.process(timestamp, data[idx])
            estimated_signal.append(signal)
            estimated_freq.append(freq)
            estimated_power.append(power)
        return estimated_signal, estimated_freq, estimated_power

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

        estimated_signal = self.classifier.update(timestamp, sample)
        estimated_freq = self.classifier.estimatedFrequency
        estimated_power =  self.power_estimator.update(estimated_signal)

        return estimated_signal, estimated_freq, estimated_power

