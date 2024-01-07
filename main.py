from binance.client import Client
from binanceAPI.position_utilities import enter_long, enter_short
from config import api_key, secret_key
from indicators.fetch_all_indicators import fetch_all_indicators
from data.io_utilities import print_with_color, calculateWR
from time import sleep
from data.data_functions import save_position, save_result
from tensorflow.tensorflow_decision import predict
import copy

# Binance API initialization
client = Client(api_key, secret_key)

# Global Variables
csv_path_position = "./data/sagebot_dataset.csv"
csv_path_result = "./data/sagebot_result.csv"
data_objects = [None, None]
on_long = False
on_short = False
tp_price = 0
sl_price = 0
prediction = None
tp_count = 0
sl_count = 0

# Global Functions
def close_position(isTP):
    global on_long
    global on_short
    global tp_count
    global sl_count
    global data_objects
    global prediction
    global csv_path_position
    global csv_path_result

    state = "" 
    
    if (on_long and isTP) or (on_short and (not isTP)): 
        state = "LONG"
    elif (on_long and (not isTP)) or (on_short and isTP):
        state = "SHORT"

    save_position(csv_path_position, state, data_objects[0])
    save_result(csv_path_result, data_objects[0].date, state, prediction)

    on_long = False
    on_short = False

    if isTP:
        print_with_color("green", "Position closed with TP")
        print_with_color("yellow", "TP: " + str(tp_count), + " SL: " + 
              str(sl_count) + " win-rate" + calculateWR(tp_count, sl_count))
    else:
        print_with_color("red", "Position closed with SL")
        print_with_color("yellow", "TP: " + str(tp_count), + " SL: " + 
            str(sl_count) + " win-rate" + calculateWR(tp_count, sl_count))
        
print_with_color("cyan", "SageBot is running...")

while True:
    try:
        sleep(10)
        data_objects[1] = fetch_all_indicators(client)

        if not (on_long or on_short):
            data_objects[0] = copy.deepcopy(data_objects[1])
            prediction = predict(csv_path_position, data_objects[0])
            if prediction == "LONG":
                tp_price, sl_price = enter_long(client)
                on_long = True
            elif prediction == "SHORT":
                tp_price, sl_price = enter_short(client)
                on_short = True
            print_with_color("yellow", "\nEntered " + prediction + " Current: " + 
                             data_objects[0].price + " TP_PRICE: " + tp_price + 
                             " SL_PRICE: " + sl_price)
        else:
            if (on_long and  data_objects[1].price > tp_price) or \
                  (on_short and data_objects[1].price < tp_price):
                close_position(True)
            elif (on_long and data_objects[1].price < sl_price) or \
                  (on_short and data_objects[1].price > sl_price):
                close_position(False)

    except Exception as e:
        error_message = str(e)
        print_with_color("yellow", error_message)