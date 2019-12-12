def get_symptoms_dict():
    dict = open("dialog-s.csv")
    data = []
    for i in dict:
        data.append(i.replace("\n", ""))
    print(data)


get_symptoms_dict()