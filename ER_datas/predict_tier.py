import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from keras.layers import Dense, LSTM
from keras.models import Sequential
from ER_datas.data_class import User


class Predict_Tier:
    def __init__(self, player_name, season):
        self.c = User(player_name, season)
        self.mmrBefore = None

    def get_mmr_data(self):
        self.mmrBefore = self.c.user_data["MMR"]
        print(self.mmrBefore)

    def LSTM(self):
        if self.mmrBefore is None:
            self.get_mmr_data()
            print("a")
        mmrBefore_x_train = []
        mmrBefore_y_train = []
        seq_length = 5
        size = len(self.mmrBefore)

        for i in range(size - 6 * seq_length):
            mmrBefore_x_train.append(self.mmrBefore[i : i + seq_length])
            mmrBefore_y_train.append(self.mmrBefore[i + seq_length])

        mmrBefore_x_train = np.array(mmrBefore_x_train)
        mmrBefore_y_train = np.array(mmrBefore_y_train)

        scaler = MinMaxScaler()
        mmrBefore_x_train_scaler = scaler.fit_transform(
            mmrBefore_x_train.reshape(-1, 1)
        )
        mmrBefore_y_train_scaler = scaler.fit_transform(
            mmrBefore_y_train.reshape(-1, 1)
        )

        model = Sequential()
        model.add(LSTM(100, activation="relu", input_shape=(seq_length, 1)))
        model.add(Dense(1))
        model.compile(optimizer="adam", loss="mse")
        model.summary()
        model.fit(
            mmrBefore_x_train_scaler.reshape(-1, seq_length, 1),
            mmrBefore_y_train_scaler,
            epochs=100,
            batch_size=16,
        )

        new_mmrBefore = np.array(self.mmrBefore[size - 6 * seq_length :])
        new_mmrBefore_scaler = scaler.transform(new_mmrBefore.reshape(-1, 1))
        predict_tier_scaler = model.predict(
            new_mmrBefore_scaler.reshape(-1, seq_length, 1)
        )
        predict_tier = scaler.inverse_transform(predict_tier_scaler).flatten()

        print(predict_tier)

        plt.plot(
            range(seq_length, len(self.mmrBefore)),
            self.mmrBefore[seq_length:],
            label="Original Data",
        )
        plt.plot(
            range(len(self.mmrBefore), len(predict_tier) + len(self.mmrBefore)),
            predict_tier,
            label="Predicted Data",
        )

        plt.legend()
        plt.show()
