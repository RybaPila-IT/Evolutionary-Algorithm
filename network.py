import numpy as np


class Sigmoid:
    """Class representing sigmoid activation function.
    Sigmoid class implements popular logistic function called sigmoid function.
    Sigmoid function for argument z is specified as follows:
        1 + / (1 + e ^ (-z))
    """

    @staticmethod
    def activate(z):
        """Sigmoid activation function.
        Sigmoid activation function for arg z is given as:
            1 + / (1 + e ^ (-z))
        """
        return 1 / (1 + np.exp(-z))


class Network:

    @staticmethod
    def set_seed(seed=1):
        np.random.seed(seed)

    def __init__(self, layer_sizes, act_func=Sigmoid):
        self.layers_num = len(layer_sizes)
        self.act_func = act_func
        self.biases = [np.random.random(i) for i in layer_sizes[1:]]
        self.weights = [np.random.normal(loc=0, scale=(1 / np.sqrt(layer_sizes[0])), size=(j, i))
                        for j, i in zip(layer_sizes[1:], layer_sizes[:-1])]

    def feed_forward(self, a):

        for w, b in zip(self.weights, self.biases):
            z = np.dot(a, w.T) + b                  # Next layer weighted input.
            a = self.act_func.activate(z)           # Next layer activation.

        return a

    def predict(self, x):
        return self.feed_forward(x) >= 0.5
