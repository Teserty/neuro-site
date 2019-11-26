ARRAY_SIZE = 10


def convert_to_vector(symptoms):
    array = [0]*ARRAY_SIZE
    for i in symptoms:
        r = symptom_in_data(i)
        if r != -1:
            array[r] = 1
    return array


def symptom_in_data(symptom):
    index = 0
    for i in data:
        if symptom == i:
            print(i)
            return index
        index += 1
    return -1


data = [
    "pain",
    "mood",
    "temperature",
    "backache",
    "fever",
    "pain in the neck"
]