import sys
import numpy as np


class HiddenLayer:
    def __init__(self, inputDimension, outputDimension):
        self.parameter = dict()
        # x-size is the input dimension while y-size is the output dimension. The values are set with normalized
        # distribution between 0 to 0.1
        self.parameter['Weight'] = np.random.normal(0, 0.1, size=(inputDimension, outputDimension))
        self.parameter['Bias'] = np.random.normal(0, 0.1, size=(1, outputDimension))
        self.gradient = dict()
        self.gradient['Weight'] = np.zeros((inputDimension, outputDimension))
        self.gradient['Bias'] = np.zeros((1, outputDimension))

    def forward(self, inputArray):
        forwardOutput = np.dot(inputArray, self.parameter['Weight']) + self.parameter['Bias']
        return forwardOutput

    def backward(self, inputArray, gradient):
        self.gradient['Weight'] = np.dot(inputArray.transpose(), gradient)
        self.gradient['Bias'] = np.sum(gradient, axis=0)
        backwardOutput = np.dot(gradient, self.parameter['Weight'].transpose())
        return backwardOutput


class sigmoid:

    def sigmoidFunc(self, x):
        return 1 / (1 + np.exp(-x))

    def forward(self, inputArray):
        forwardOutput = self.sigmoidFunc(inputArray)
        return forwardOutput

    def backward(self, inputArray, gradient):
        derivative = self.sigmoidFunc(inputArray) * (1 - self.sigmoidFunc(inputArray))
        # only do the element-wise multiply
        backwardOutput = np.multiply(gradient, derivative)
        return backwardOutput


def Gradient(system, learningRate):
    for layerName, layer in system.items():
        if hasattr(layer, 'parameter'):
            for key, value in layer.parameter.items():
                layer.parameter[key] -= learningRate * layer.gradient[key]
    return system


def predictLabel(x):
    if x.shape[1] == 1:
        return (x > 0).astype(float)
    else:
        return np.argmax(x, axis=1).astype(float).reshape((x.shape[0], -1))


class Data:
    def __init__(self, image, label):
        self.image = image
        self.label = label
        self.imageNum, self.dim = self.image.shape

    def batch(self, dataIndex):
        batchImage = np.zeros((len(dataIndex), self.dim))
        batchLabel = np.zeros((len(dataIndex), 1))
        for i in range(len(dataIndex)):
            batchImage[i] = self.image[dataIndex[i]]
            batchLabel[i] = self.label[dataIndex[i]]
        return batchImage, batchLabel


class DataTest:
    def __init__(self, image):
        self.image = image
        self.sampleNum, self.dim = self.image.shape

    def batch(self, dataIndex):
        batchImage = np.zeros((len(dataIndex), self.dim))
        for i in range(len(dataIndex)):
            batchImage[i] = self.image[dataIndex[i]]
        return batchImage


class Loss:

    def __init__(self):
        self.encodedLabel = None
        self.logit = None
        self.sumExp = None
        self.probability = None

    def forward(self, inputArray, labelArray):
        # flatten the array
        self.encodedLabel = np.zeros(inputArray.shape).reshape(-1)
        self.encodedLabel[
            labelArray.astype(int).reshape(-1) + np.arange(inputArray.shape[0]) * inputArray.shape[1]] = 1.0
        self.encodedLabel = self.encodedLabel.reshape(inputArray.shape)

        self.logit = inputArray - np.amax(inputArray, axis=1, keepdims=True)
        self.sumExp = np.sum(np.exp(self.logit), axis=1, keepdims=True)
        self.probability = np.exp(self.logit) / self.sumExp

        forwardOutput = -np.sum(np.multiply(self.encodedLabel, self.logit - np.log(self.sumExp))) / inputArray.shape[
            0]

        return forwardOutput

    def backward(self, inputArray, labelArray):
        backwardOutput = -(self.encodedLabel - self.probability) / inputArray.shape[0]
        return backwardOutput


def main():
    Layer1Num = 1000
    Layer2Num = 100
    Epoch = 20
    learningRate = 0.02
    step_learning_damp = 10
    batchSize = 5

    file1 = "train_image.csv"
    file2 = "train_label.csv"
    file3 = "test_image.csv"
    train_image = np.genfromtxt(file1, delimiter=',')
    train_label = np.genfromtxt(file2, delimiter=',')
    test_image = np.genfromtxt(file3, delimiter=',')

    N_sample, dim = train_image.shape
    Test_num, test_dim = test_image.shape

    train_data = Data(train_image, train_label)
    test_data = DataTest(test_image)

    system = dict()

    system['Layer1'] = HiddenLayer(dim, Layer1Num)
    system['act'] = sigmoid()
    system['Layer2'] = HiddenLayer(Layer1Num, Layer2Num)
    system['Output'] = HiddenLayer(Layer2Num, 10)
    system['loss'] = Loss()

    momentum = dict()
    for layerName, layer in system.items():
        if hasattr(layer, 'parameter'):
            for key, value in layer.parameter.items():
                momentum[layerName + key] = np.zeros(layer.gradient[key].shape)
    for epoch in range(Epoch):
        if (epoch % step_learning_damp == 0) and (epoch != 0):
            # damping the learning rate to reach the minimum
            learningRate = learningRate * 0.2

        index = np.random.permutation(N_sample)

        set_number = int(np.floor(N_sample / batchSize))
        for i in range(set_number):
            inputArray, labelArray = train_data.batch(index[i * batchSize:(i + 1) * batchSize])
            # forward
            Layer1 = system['Layer1'].forward(inputArray)
            actionLayer1 = system['act'].forward(Layer1)
            Layer2 = system['Layer2'].forward(actionLayer1)
            actionLayer2 = system['act'].forward(Layer2)
            finalLayer = system['Output'].forward(actionLayer2)
            loss = system['loss'].forward(finalLayer, labelArray)

            gradFinalLayer = system['loss'].backward(finalLayer, labelArray)
            gradAction2 = system['Output'].backward(actionLayer2, gradFinalLayer)
            gradLayer2 = system['act'].backward(Layer2, gradAction2)
            gradAction1 = system['Layer2'].backward(actionLayer1, gradLayer2)
            gradLayer1 = system['act'].backward(Layer1, gradAction1)
            grad_input = system['Layer1'].backward(inputArray, gradLayer1)
            system = Gradient(system, learningRate)

        test_predict = np.zeros((Test_num, 1))
        set_number_test = int(np.floor(Test_num / batchSize))
        for i in range(set_number_test):
            inputArray = test_data.batch(np.arange(i * batchSize, (i + 1) * batchSize))
            Layer1 = system['Layer1'].forward(inputArray)
            actionLayer1 = system['act'].forward(Layer1)
            Layer2 = system['Layer2'].forward(actionLayer1)
            actionLayer2 = system['act'].forward(Layer2)
            finalLayer = system['Output'].forward(actionLayer2)

            test_predict[i * batchSize: (i + 1) * batchSize] = predictLabel(finalLayer).astype(int)

    np.savetxt("test_predictions.csv", test_predict, fmt='%i')


main()
