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

    def __init__(self, layer_sizes, act_func=Sigmoid, weights=None, biases=None):
        """Constructor of the Network.

        Constructor has two options of generating new Network objects.

        Default and 'enforced' version is the initialization with random weights
        and biases. This option needs exact specification of 'layer_sizes' parameter.
        Parameter 'layer_sizes' should be a list containing amounts of neurons present
        in corresponding network layers.
        Ex. [5, 10, 2] represents network where input layer has 5 neurons, hidden layer 10 and output layer 2.

        Second option is to initialize and pass 'weights' and 'biases' parameters.
        They correspond to matrices of weights and biases used for forward propagation.
        Weights and biases should be passed in form of python list.

        :parameter layer_sizes - list containing number of neurons present in each layer.
        :parameter act_func - function used for activation in each neuron.
        :parameter weights - list containing matrices of weights present in each layer.
        :parameter biases - list containing arrays of biases present in each layer.

        :returns new Network object.
        """
        self.act_func_ = act_func
        self.biases_ = [2*np.random.random(i) - 1 for i in layer_sizes[1:]] if biases is None else biases
        self.weights_ = [np.random.normal(loc=0, scale=(1 / np.sqrt(layer_sizes[0])), size=(j, i))
                         for j, i in zip(layer_sizes[1:], layer_sizes[:-1])] if weights is None else weights

    def __add__(self, other):
        """Adds two Networks in terms of weights and biases.

        Operator '+' used on Network will apply addition on each matrix of weights and
        array of biases.

        :parameter other - other Network used for addition.

        :returns new Network object being the result of addition.
        """
        res_weights_ = [w_s + w_o for w_s, w_o in zip(self.weights_, other.weights_)]
        res_biases_ = [b_s + b_o for b_s, b_o in zip(self.biases_, other.biases_)]

        return Network([0], Sigmoid, res_weights_, res_biases_)

    def __truediv__(self, val):
        """Divides Network weights and biases by 'val' value.

        Operator '/' will apply division bo 'val' value on each element of
        weights matrices and biases array.

        :parameter val - value be which the Network 'insides' will be divided. Val must be numerical value.

        :returns new Network object being the result of division.
        """
        res_weights_ = [w / val for w in self.weights_]
        res_biases_ = [b / val for b in self.biases_]

        return Network([0], Sigmoid, res_weights_, res_biases_)

    def feed_forward(self, a):

        for w, b in zip(self.weights_, self.biases_):
            z = np.dot(a, w.T) + b                   # Next layer weighted input.
            a = self.act_func_.activate(z)           # Next layer activation.

        return a

    def predict(self, x):
        return self.feed_forward(x) >= 0.5

    def crossover(self, other):
        """Function generating new Network.

        Function implements averaging crossover with ranks.
        It means that for each of parents there exists a special
        rank (lets call them r1 and r2) where r1 + r2 = 1.
        The final result of recombination will be:
            (parent1*r1 + parent2*r2) / 2   where '+' and '*' signs mean applying regular arithmetic expression
                                            to gens of parents (in Network gens are weights and biases).

        :param other - second parent used for recombination.

        :returns new Network which is the result of crossover.
        """
        eta = np.random.uniform()
        ex_one = self / (1 / eta)
        ex_two = other / (1 / (1 - eta))

        return (ex_two + ex_one) / 2

    def mutate(self, eta):
        """Function performing mutation of a Network.

        Function performs regular mutation on a network.
        For each weight and bias present in the network random value is generated
        (values have standard normal distribution). This random value is then being
        added to corresponding weights or bias with respect to strength of the mutation eta.
        Final result is:
                w_new = w_old + random_val*eta

        :parameter eta - strength of the mutation.

        :returns new Network object being the result of the mutation.
        """
        mutation_w = [w + eta * np.random.standard_normal(size=w.shape) * np.random.choice([0, 1], size=w.shape)
                      for w in self.weights_]
        mutation_b = [b + eta * np.random.standard_normal(size=b.shape) * np.random.choice([0, 1], size=b.shape)
                      for b in self.biases_]

        return Network([0], Sigmoid, weights=mutation_w, biases=mutation_b)
