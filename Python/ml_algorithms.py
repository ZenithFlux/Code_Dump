import numpy as np
import matplotlib.pyplot as mpl

'''
Linear and Logistic Regression algorithms (without regularization):-
feature_count - No. of independent variables.

Attributes:-
learning_rate - Set or change the learning rate of the algorithm.

Methods-
1- predict - Predict values based on provided features X.
2- cost - Find cost corresponding to features X and outputs Y.
3- train - Train the algorithm using features X and outputs Y.

Parameters of Methods-
X - Features. This should always be a 2D array, even if there is only one row.
Y - Outputs. This should always be a 1D array. (Consisting of only 0 and 1 in case of Logistic Regression)
'''
class LinearRegressor:
    def __init__(self, feature_count: int, learning_rate: float):
        self.learning_rate = learning_rate
        self.theta = np.zeros(feature_count + 1)
        
    def predict(self, X):
        X = np.insert(X, 0, 1, axis = 1)
        return np.dot(X, self.theta)
    
    def cost(self, X, Y):
        X = np.insert(X, 0, 1, axis = 1)
        m = X.shape[0]
        E = np.dot(X, self.theta) - Y
        return (1/m) * np.dot(E, E)
        
    def train(self, X, Y, iterations: int):
        dot = np.dot
        tp = np.transpose
        
        X = np.insert(X, 0, 1, axis = 1)
        alpha = self.learning_rate
        theta = self.theta
        m = X.shape[0]
        
        for _ in range(0, iterations):
            theta = theta - (alpha/m) * dot( tp(X), dot(X, theta)-Y )
            
        self.theta = theta
      
        
class LogisticRegressor:
    def __init__(self, feature_count: int, learning_rate: float):
        self.learning_rate = learning_rate
        self.theta = np.zeros(feature_count + 1)
        
    def predict(self, X):
        X = np.insert(X, 0, 1, axis = 1)
        return np.round(sig(np.dot(X, self.theta)))
    
    def cost(self, X, Y):
        dot = np.dot
        log = np.log
        
        X = np.insert(X, 0, 1, axis = 1)
        m = X.shape[0]
        Y = np.array(Y)
        H = sig(dot(X, self.theta))
        return (-1/m) * (dot(Y, log(H)) + dot((1-Y), log(1-H)))
        
    def train(self, X, Y, iterations: int):
        dot = np.dot
        tp = np.transpose
        
        X = np.insert(X, 0, 1, axis = 1)
        Y = np.array(Y)
        alpha = self.learning_rate
        theta = self.theta
        m = X.shape[0]
        
        for _ in range(0, iterations):
            H = sig(dot(X, theta))
            theta = theta - (alpha/m) * dot( tp(X), H - Y )
            
        self.theta = theta
  
        
'''
Linear Support Vector Machine (SVM without Kernal Trick):-
feature_count - No. of independent variables.

Attributes:-
learning_rate - Set or change the learning rate of the algorithm.
regularization_constant - Set or change the regularization constant of the algorithm.

Methods-
1- predict - Predict values based on provided features X.
2- cost - Find cost corresponding to features X and outputs Y.
3- train - Train the algorithm using features X and outputs Y.

Parameters of Methods-
X - Features. This should always be a 2D array, even if there is only one row.
Y - Outputs. This should always be a 1D array. (only 1 or -1 as values)
'''
class SVM:
    def __init__(self, feature_count: int, learning_rate: float, regularization_constant: float):
        self.learning_rate = learning_rate
        self.reg_const = regularization_constant
        self.W = np.zeros(feature_count)
        self.b = 0
        
    def predict(self, X):
        return sign( np.dot(X, self.W) + self.b )
    
    def cost(self, X, Y):
        Reg = self.reg_const * sum(self.W**2)
        Y = np.array(Y)
        X = np.array(X)
        H = Y * (np.dot(X, self.W) + self.b)
        n = X.shape[0]
        return Reg + (1/n)*sum(np.maximum(0, 1 - H))
    
    def train(self, X, Y, iterations: int):
        alpha = self.learning_rate
        lmda = self.reg_const
        W = self.W
        Y = np.array(Y)
        X = np.array(X)
            
        for _ in range(0, iterations):
            for i in range(0, X.shape[0]):
                if Y[i] * (np.dot(X[i], W) + self.b) >= 1:
                    W = W - alpha*lmda*W
                    self.b = self.b - alpha*lmda*self.b
                     
                else:
                    W = W - alpha*( lmda*W - Y[i] * X[i])
                    self.b = self.b - alpha*( lmda*self.b - Y[i])
            
        self.W = W
        
    @property
    def regularization_constant(self):
        return self.reg_const
    
    @regularization_constant.setter
    def regularization_constant(self, value):
        self.reg_const = value
  
  
# ------ Micro Functions --------  
        
# Sigmoid Function
def sig(x):
    return 1 / (1 + np.exp(-x))

# Positive and zero -> 1, Negative -> 0
def sign(x):
    x = np.sign(x)
    x[x==0] = 1
    return x



# ------------------------ Testing Area ---------------------------

class Test:
    def linearReg():
        X = [[1,2,3],[2,3,1],[10,10,10],[3,10,20],[1,1,2],[11,15,16],[20,13,5],[89,50,79],[17,67,89],[23,43,63]]
        Y = [2, 11, 30, -4, 1, 35, 69, 170, 57, 49]
        # y = 2*x[0]+3*x[1]-2*x[2]
        
        lr = LinearRegressor(3, 0.0005)
        lr.train(X, Y, 10000)
        print("Theta values after training- ", lr.theta)
        print("Predicting training data-    ", lr.predict(X))
        print("Cost- ", lr.cost(X, Y))
    
    def logisticReg():
        # lr = LogisticRegressor(4, 0.0065)
        # lr.train(X, Y, 10000)
        # print("Theta values after training- ", lr.theta)
        # print("Predicting training data-    ", lr.predict(X))
        # print("Cost- ", lr.cost(X, Y))
        pass

    def svm():
        # X = np.array([[randint(80, 130), randint(10, 60)] for _ in range(0, 20)] + [[randint(10, 60), randint(80, 130)] for _ in range(0, 20)])
        X = ([[83, 55], [111, 47], [82, 28], [82, 20], [120, 60], [93, 28], [107, 26], [97, 14], [123, 39], [101, 60], [92, 16], [88, 10], 
            [103, 39], [112, 22], [113, 39], [103, 24], [93, 19], [107, 47], [104, 11], [87, 32], [45, 121], [20, 120], [18, 83], 
            [27, 125], [45, 128], [19, 108], [60, 102], [59, 83], [14, 103], [48, 127], [24, 87], [59, 96], [12, 127], [51, 101], 
            [28, 96], [58, 108], [57, 97], [46, 119], [33, 116], [12, 115]])

        Y = [-1 for _ in range(0, 20)] + [1 for _ in range(0, 20)]
        X = np.array(X)
        mpl.scatter(X[:,0], X[:,1])

        svm = SVM(2, 0.04, 0.006)
        svm.train(X, Y, 10000)
        print(svm.predict(X))
        print(svm.cost(X, Y))
        
        x = [0, 130]
        y = [(-svm.W[0]*i - svm.b)/svm.W[1] for i in x]
        y1 = [(-svm.W[0]*i - svm.b + 1)/svm.W[1] for i in x]
        y2 = [(-svm.W[0]*i - svm.b - 1)/svm.W[1] for i in x]
        mpl.plot(x, y, 'k')
        mpl.plot(x, y1, '--')
        mpl.plot(x, y2, '--')
        mpl.show()
        
if __name__ == '__main__':
    Test.svm()