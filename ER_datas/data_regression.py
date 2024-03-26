from ER_apis.crawler import DakPlayerCrawler
from sklearn.linear_model import LinearRegression

# import statsmodels.api as sm
import numpy as np
import matplotlib.pyplot as plt


class MMRRegression:
    def __init__(self, player_name, season):
        self.c = DakPlayerCrawler(player_name, season)
        self.c.crawling_mmr_change()
        mmr_change = self.c.datas["MMR"]
        self.data = np.array(mmr_change, dtype=float)
        self.model_module = ""

    # scikit-learn
    def linear_regression_sklearn(self):
        X = np.arange(len(self.data)).reshape(-1, 1)
        Y = self.data
        self.model = LinearRegression().fit(X, Y)
        self.model_module = "sklearn"

    """
    #statsmodels 
    def linear_regression_sm(self, add_constant:bool=True):
        self.df = pd.DataFrame({'X':list(range(len(self.data))),'Y':self.data})
        #Y = self.df['Y']
        #X = self.df['X']
        X = list(range(29))
        Y = self.data
        print(self.data)
        self.model = sm.OLS(Y, X)
        result = self.model.fit()
        #print(result.summary())
    """

    def print_model(self):
        print(self.model)

    def print_plot(self):
        if self.model_module == "":
            return print("Model Not fitted")
        X = np.arange(len(self.data))
        plt.scatter(X, self.data, label="Data")
        X = X.reshape(-1, 1)
        Y = self.model.predict(X).reshape(-1, 1)
        plt.plot(X, Y, color="blue", label=self.model_module)
        plt.xlabel("X")
        plt.ylabel("y")
        plt.title("Linear Regression with OLS({0})".format(self.model_module))
        plt.legend()
        plt.show()

    def predict_mmr(self, predict_mmr):
        if self.model_module == "":
            return print("Model Not fitted")
        predicted_game = -1
        if self.model_module == "sklearn":
            coef = self.model.coef_[0]
            bias = self.model.intercept_
            predicted_game = (predict_mmr - bias) / coef
        return predicted_game
