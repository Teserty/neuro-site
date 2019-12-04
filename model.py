from tensorflow.python.keras import Sequential
from tensorflow.python.keras.layers import Dense, Dropout

def init_model(_in, _out):
    print(_in)
    print(_out)
    model = Sequential([
        Dense(100, activation='sigmoid', input_shape=(_in,)),
        Dropout(0.1),
        # Dense(100, activation='relu'),
        # Dropout(0.1),
        Dense(_out, activation='softmax'),
    ])

    return model
