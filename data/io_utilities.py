import datetime
from termcolor import colored

def print_position_message(indicatorDataObj, position):
    print_with_color("yellow", "PRICE: " + str(indicatorDataObj.price) + 
          " MACD_12: " + str(indicatorDataObj.macd_12) + 
          " MACD_26: " + str(indicatorDataObj.macd_26) + 
          " EMA_100: " + str(indicatorDataObj.ema_100) + 
          " RSI_6: " + str(indicatorDataObj.rsi_6) + 
          " Position " + str(position))
    
def get_current_date_string(format="%Y-%m-%d %H:%M:%S"):
    current_date = datetime.datetime.now()
    date_string = current_date.strftime(format)
    return date_string

def print_with_color(color, text):
    colored_text = text
    if color.lower() == 'cyan':
        colored_text = colored(text, 'cyan')
    elif color.lower() == 'green':
        colored_text = colored(text, 'green')
    elif color.lower() == 'yellow':
        colored_text = colored(text, 'yellow')
    elif color.lower() == 'red':
        colored_text = colored(text, 'red')

    print(colored_text)

def calculateWR(tp_count, sl_count):
    total_trades = tp_count + sl_count

    if total_trades == 0:
        return "0.00%"

    win_rate = tp_count / total_trades
    win_rate_percentage = round(win_rate * 100, 2)

    return f"{win_rate_percentage}%"