import numpy as np


def get_raw_data():
    # TODO: Move to config
    csv_file = "data/symptoms.csv"

    raw_data = []
    f = open(csv_file)

    for row in f:
        raw_data.append(row.strip("\n").split(",", 1))

    return raw_data


def create_dict():
    # Create set of diseases
    disease_set = set()
    symptom_set = set()
    for i in get_raw_data():
        disease_set.add(i[0])
        symptom_set.add(i[1])

    # Save  dictionaries
    disease_set = np.array(list(disease_set))
    d_dict = open("data/diseases.dict", "w")
    for i in disease_set:
        d_dict.write("{}\n".format(i))

    symptom_set = np.array(list(symptom_set))
    s_dict = open("data/symptoms.dict", "w")
    for i in symptom_set:
        s_dict.write("{}\n".format(i))

    d_dict.close()
    s_dict.close()

    return len(disease_set), len(symptom_set)


def get_clean_data():
    diseases = []
    symptoms = []

    d_dict = open("data/diseases.dict")
    for line in d_dict:
        diseases.append(line.strip("\n"))

    s_dict = open("data/symptoms.dict")
    for line in s_dict:
        symptoms.append(line.strip("\n"))

    # print(symptoms)

    text = np.zeros((len(diseases), len(symptoms)))
    labels = np.zeros((len(diseases)))

    for i in get_raw_data():
        # Create row with length of total diseases
        # Set el of row with id of disease to 1
        id = diseases.index(i[0])
        labels[id] = id

    for i in get_raw_data():
        # Create row with length of total symptoms
        # Set el of row with id of disease to 1
        idD = diseases.index(i[0])
        idS = symptoms.index(i[1])
        text[idD][idS] = 1

    return np.array(text), np.array(labels)


if __name__ == '__main__':
    create_dict()
    text, labels = get_clean_data()
    print(text)
    print(labels)


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


def get_disease(index):
    diseases = []
    d_dict = open("data/diseases.dict")
    for line in d_dict:
        diseases.append(line.strip("\n"))

    return diseases[index]
