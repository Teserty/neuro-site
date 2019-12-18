#Not for Server

#Only to make data
def new_get_symptoms_dict():
    dict = open("../../data/Training.csv")
    symptoms = []
    data = []
    for i in dict:
        if len(symptoms) < 1:
            s = i.split(",")
            for y in s:
                y = y.replace("_", " ")
                symptoms.append(y)
        else:
            c = 0
            words = i.split(",")
            key = words[-1]
            for word in words:
                if word == "0" or word == "1":
                    c += 1
                    if word == "1":
                        line = key.replace("\n", "") +","+symptoms[c].replace("\n", "")
                        data.append(line)
            #print(key)
    data = list(set(data))
    #print(data)

    return data


def get_symptoms_dict():
    dict = open("dialog-s.csv")
    data = []
    for i in dict:
        data.append(i.replace("\n", ""))
    print(data)
    return data


def get_symptopms():
    dict = open("symptoms.csv")
    data = []
    for i in dict:
        for s in i.split("\n"):
            data.append(s)

    while data.count("") > 0:
        data.remove("")
    print(data)
    return data
####


from connector.data.readydata import data3
def make_dialog():

    data_symptoms_to_ills = {}
    data_ills_to_symptoms = {}
    for i in data3:
        i = i.replace("\n", "").lower().split(",")
        x = i[0]
        y = i[1]
        if data_symptoms_to_ills.get(y):
            sympts = data_symptoms_to_ills.get(y)
            sympts.append(x)
        else:
            data_symptoms_to_ills.update({y: list([x])})
        if data_ills_to_symptoms.get(x):
            ills = data_ills_to_symptoms.get(x)
            ills.append(y)
        else:
            data_ills_to_symptoms.update({x: list([y])})
    return data_symptoms_to_ills, data_ills_to_symptoms


def make_advert(symptoms):
    dict_symptoms, dict_ills = make_dialog()
    ills = []
    for i in symptoms:
        if ills:
            ills = [y for y in dict_symptoms.get(i) if y in ills]
        else:
            ills = dict_symptoms.get(i)
    #print(ills)
    s_advice = []
    s_dict = {}
    max = 0
    if type(ills) == None:
        return -1
    for ill in ills:
        for s in dict_ills.get(ill):
            if s_dict.get(s):
                value = s_dict.get(s)+1
                s_dict.update({s: value})
                if value > max:
                    max = value
            else:
                s_dict.update({s: 1})
    #print(s_dict)
    for i, y in s_dict.items():
        if i not in symptoms:
            s_advice.append(i)
    return s_advice


from connector.data.readydata import data as ready_data


def make_advert_with_text(text):
    symp = []
    text = text.lower()
    for i in ready_data:
        if i in text:
            symp.append(i)
    #print(symp)
    return make_advert(symp)


if __name__ == "__main__":
    #print(new_get_symptoms_dict())
    print(make_advert_with_text("joint pain"))
