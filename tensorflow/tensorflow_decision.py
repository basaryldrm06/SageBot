import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd

def predict(file_path, dataObj):
    try:
        df = pd.read_csv(file_path)

        if df.empty:
            raise ValueError("No data in csv file")

        columns = ["date", "price", "macd_12", "macd_26", "ema_100", "rsi_6"]
        for i in range(0, 15):
            columns.extend([
                f"opening_{i}", f"closing_{i}",
                f"min_{i}", f"max_{i}"
            ])

        X = df[columns].values
        y = df['state'].values

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = Sequential()
        model.add(Dense(32, activation='relu', input_dim=X_train.shape[1]))
        model.add(Dense(1, activation='sigmoid'))

        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

        model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.2)

        _, test_acc = model.evaluate(X_test, y_test)

        def predict(indicatorDataObj):
            features = [indicatorDataObj.date, indicatorDataObj.price, 
                        indicatorDataObj.macd_12, indicatorDataObj.macd_26, 
                        indicatorDataObj.ema_100, indicatorDataObj.rsi_6]
            for bar in indicatorDataObj.bar_list:
                for element in bar: 
                    features.append(element)

            new_data = np.array([features])
            predictions = model.predict(new_data)

            predictions = np.where(predictions > 0.5, "LONG", "SHORT")
            return predictions

        prediction = predict(dataObj)
        return test_acc, prediction

    except Exception as e:
        print(f"WARNING: {e}")
        return None, "LONG"
