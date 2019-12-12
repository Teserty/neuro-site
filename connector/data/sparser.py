#Not for Server

#Only to make data


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


from connector.data.readydata import data2
def make_dialog():

    data_symptoms_to_ills = {}
    data_ills_to_symptoms = {}
    for i in data2:
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
    for ill in ills:
        for s in dict_ills.get(ill):
            if s_dict.get(s):
                value = s_dict.get(s)+1
                s_dict.update({s: value})
                if value > max:
                    max = value
            else:
                s_dict.update({s: 1})
    for i, y in s_dict.items():
        if y == max and i not in symptoms:
            s_advice.append(i)
    return s_advice


from connector.data.readydata import data as ready_data


def make_advert_with_text(text):
    symp = []
    text = text.lower()
    for i in ready_data:
        if i in text:
            symp.append(i)
    print(symp)
    return make_advert(symp)

def test():
    pass
    #print(make_dialog())
    #print(make_advert_with_text("Fatigue"))

if __name__ == "__main__":
    test()