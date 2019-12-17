import numpy as np


def get_raw_data(test=False):
    # TODO: Move to config
    if test:
        csv_file = "data/Testing.csv"
    else:
        csv_file = "data/Training.csv"
    raw_data = []
    f = open(csv_file)

    for row in f:
        raw_data.append(row.strip("\n").split(","))

    return raw_data


def create_dict():
    raw_data = get_raw_data()

    # Create set of diseases
    disease_set = []
    symptom_set = []
    symptoms = raw_data[0]
    symptoms.pop()  # Remove "prognosis" from symptoms
    for i in symptoms:
        symptom_set.append(i)

    for i in raw_data[1:]:
        if i[-1] not in disease_set:
            disease_set.append(i[-1])

    # Save  dictionaries
    disease_set = np.array(list(disease_set))
    d_dict = open("data/diseases.dict", "w")
    for i in disease_set:
        d_dict.write("{}\n".format(i))

    symptom_set = np.array(list(symptom_set))
    s_dict = open("data/symptoms.dict", "w")
    for i in symptom_set:
        s = i.lower()
        s = s.replace('_', '')
        s_dict.write("{}\n".format(s))

    d_dict.close()
    s_dict.close()

    return len(disease_set), len(symptom_set)


def get_clean_data():
    diseases = []
    symptoms = []

    d_dict = open("data/diseases.dict")
    for line in d_dict:
        diseases.append(line.strip("\n"))

    tr_labels = []
    tr_text = []

    ts_labels = []
    ts_text = []

    for i in get_raw_data()[1:]:
        tr_labels.append(diseases.index(i[-1]))
        i.pop()
        tr_text.append(i)

    for i in get_raw_data(test=True)[1:]:
        ts_labels.append(diseases.index(i[-1]))
        i.pop()
        ts_text.append(i)

    return np.array(tr_text).astype('float32'), np.array(tr_labels), np.array(ts_text).astype('float32'), np.array(
        ts_labels), len(tr_text[0]), len(diseases)


def tokenize(val):
    symptoms = []
    s_dict = open("data/symptoms.dict")
    for line in s_dict:
        symptoms.append(line.strip("\n"))

    tok = np.zeros(len(symptoms))

    for v in val:
        if v in symptoms:
            tok[symptoms.index(v)] = 1

    return tok


def get_symptom(index):
    symptoms = []
    s_dict = open("data/symptoms.dict")
    for line in s_dict:
        symptoms.append(line.strip("\n"))

    return symptoms[index]


def get_disease(index):
    diseases = []
    d_dict = open("data/diseases.dict")
    for line in d_dict:
        diseases.append(line.strip("\n"))

    return diseases[index]


if __name__ == '__main__':
    create_dict()
    print(get_clean_data())
