import numpy as np

from parser2 import get_disease, get_raw_data, get_symptom


def get_max_symptom(disease_index):
    raw_data = get_raw_data()

    disease = get_disease(disease_index)

    sum_vec = np.zeros((len(raw_data[0]) - 1,))

    for i in raw_data[1:]:
        if i[-1] == disease:
            j = np.array(i[0:-1])
            j = j.astype(int)
            sum_vec += j

    print(sum_vec)

    for i in range(len(sum_vec)):
        if sum_vec[i] > 0:
            print("{} - {}".format(get_symptom(i), sum_vec[i]))


def get_symptoms_sum_vec():
    raw_data = get_raw_data()

    sum_vec = np.zeros((len(raw_data[0]) - 1,))

    for i in raw_data[1:]:
        j = np.array(i[0:-1])
        j = j.astype(int)
        sum_vec += j

    # print(sum_vec)

    min_symptoms = []

    for i in range(len(sum_vec)):
        if sum_vec[i] in range(108, 121):
            min_symptoms.append(i)
            print("{} - {}".format(get_symptom(i), sum_vec[i]))

    print(min_symptoms)

    return min_symptoms


def get_disease_by_solo_symptom(symptom_index):
    raw_data = get_raw_data()
    min_symptoms = get_symptoms_sum_vec()

    if symptom_index >= len(raw_data) - 1:
        return "Sorry, there are no diseases with this symptom in our database"

    for i in raw_data[1:]:
        if i[symptom_index] != 0:
            if symptom_index in min_symptoms:
                return i[-1]
            else:
                return "Couldn't unambiguously identify the disease, too little information"


# def reduce_synonyms_and_tokenize():

if __name__ == '__main__':
    # get_max_symptom(0)
    # get_symptoms_sum_vec()
    print(get_disease_by_solo_symptom(4))
