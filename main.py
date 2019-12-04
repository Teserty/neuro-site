import numpy as np
import os
import random

import tensorflow as tf
from tensorflow.python.keras.models import load_model
from tensorflow.python.keras.optimizers import Adam

import model
import parser2


def train():
    # TODO: Move this to config
    test_ratio = 1 / 4

    # Receiving clean data arrays here
    print("Parsing data...")
    train_text, train_lbls, test_text, test_lbls, len1, len2 = parser2.get_clean_data()

    # Shuffle data for more plain distribution

    print(test_text.shape)
    print(test_lbls.shape)
    print(train_text.shape)
    print(train_lbls.shape)

    # TODO: Move this to config
    print("Compiling model...")
    # Init optimizer, loss function and metrics
    optimizer = Adam(lr=0.1)
    loss = 'sparse_categorical_crossentropy'
    metrics = ['accuracy']  # ['categorical_accuracy']

    m = model.init_model(len1, len2)
    m.compile(optimizer=optimizer, loss=loss, metrics=metrics)

    # TODO: Move this to config
    print("Establishing checkpoints...")
    checkpoint_path = "training/cp.ckpt"

    # Train model with new callback
    print("Training model...")
    fit = m.fit(train_text,
                train_lbls,
                epochs=5,
                validation_data=(test_text, test_lbls))  # Pass callback to training

    # valuate = m.evaluate(test_text, test_lbls)

    m.save(f'training/model.h5')

    print('Training complete:')
    print(fit.history)
    print("Accuracy: {}".format(fit.history['val_accuracy'][-1]))
    print("Loss: {}".format(fit.history['val_loss'][-1]))


def predict(val):
    # TODO: Load dictionary
    # TODO: Tokenize input
    #s = val.lower()
    #s = s.replace('_', '')
    #symptoms = s.split(",")
    #tok = parser2.tokenize(symptoms)
    # TODO: Predict
    m = load_model(f'training/model.h5')
    unique, counts = np.unique(val, return_counts=True)
    #print(val)
    print(dict(zip(unique, counts)))
    #print(tok)
    #print(np.array(tok))

    result = m.predict(val.reshape(1, val.shape[0]))

    results_num = 3

    top_results = []
    i = 0
    while i < results_num:
        top_results.append((int(result.max() * 100), parser2.get_disease(result.argmax())))
        result[0][result.argmax()] = 0
        i += 1
    return top_results


def f1():
    train_text, train_lbls, test_text, test_lbls, len1, len2 = parser2.get_clean_data()
    text = train_text # + test_text
    lbls = train_lbls # + test_lbls
    m = load_model(f'training/model.h5')

    lens = np.zeros((len2,))
    for i in lbls:
        lens[i] += 1

    # 4 arrays for recall and precision calculations
    relevant = lens  # симптомы для конкретной болезни
    true_positives = np.zeros((len2,))  # симптомы для конкретной болезни, выбранные нейронкой
    false_positives = np.zeros((len2,))  # симптомы не принадлежащие конкретной болезни, выбранные нейронкой

    if text.shape[0] == lbls.shape[0]:
        for i in range(text.shape[0]):
            res = np.array(m.predict(text[i].reshape(1, text[i].shape[0])))
            if res.argmax() == lbls[i]:
                true_positives[res.argmax()] += 1
            else:
                false_positives[res.argmax()] += 1
    else:
        raise Exception("Labels and messages arrays have different sizes")

    print(relevant)
    print(true_positives)
    print(false_positives)

    precision = np.zeros((len2,))
    recall = np.zeros((len2,))
    f = np.zeros((len2,))
    for i in range(len2):
        # Сколько выбранных сообщений правильны?
        if false_positives[i] > 0:
            precision[i] = true_positives[i] / (true_positives[i] + false_positives[i])

        # Сколько правильных сообщений выбрано?
        recall[i] = true_positives[i] / relevant[i]

        # F-measure для каждого отдельного человека
        if precision[i] > 0 and recall[i] > 0:
            f[i] = 2 * precision[i] * recall[i] / (precision[i] + recall[i])

    return f.mean()


if __name__ == '__main__':
    # train()
    print(f1())
    # print(predict())
