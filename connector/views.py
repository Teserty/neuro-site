from django.shortcuts import render
from connector.utils.forNLP import *
import numpy as np
from main import predict
from connector.models import NewDialog
from connector.data.readydata import *
from connector.data.sparser import *

from connector.data.readydata import data as symptoms


def gleb_blyad(text):
    array = set()
    for i in symptoms:
        for y in i.split(" "):
            if y in text and i not in text:
                array.add(i)
    array = list(array)
    return array


def dialog_view(request):
    if request.method == "POST":
        dialog = NewDialog.objects.get(id=request.POST.get("id"))
        if dialog.stage == 0:
            print(0)
            text = request.POST.get("text")
            text = text.replace(" ,", ",")
            text = text.lower()
            array = text.split(" ")
            array = lemmatize(array)
            new_text = ""
            for i in array:
                if new_text == "":
                    new_text = i
                else:
                    new_text = new_text + " " + i
            dialog.user_text += new_text
            if "end" in text or "finish" in text:
                dialog.stage = 1
                dialog.save()
                return dialog_view(request)
            print(text)
            dialog.save()
            array = make_advert_with_text(dialog.user_text)
            print(array)
            return render(request, "dialog.html",
                          {"OK": "hidden", "neuro_text": "Maybe you have some of this symptoms too? Please."
                                                         " Write 'end' or 'finish', if you finish", "id": dialog.id,
                           "hidden": "",
                           "hidden2": "hidden", "advice": array})
        elif dialog.stage == 1:
            print(1)
            text = dialog.user_text
            also = request.POST.get("text")
            text = text + " " + also
            tok = np.zeros(132)
            c = 0
            for i in data:
                if i in text:
                    tok[c] = 1
                c += 1
            if 1 in tok:
                array = predict(tok)
                print(array)
                dialog.user_text += "\n" + request.POST.get("text")
                mystring = ""
                for digit in array:
                    mystring += str(digit)
                dialog.our_text += "\n" + mystring
                dialog.result = array
                dialog.stage = 2
                dialog.save()
                return render(request, "dialog.html",
                              {"OK": "hidden", "neuro_text": "You seem to have:", "id": dialog.id, "hidden": "",
                               "pred": array})
            else:
                #TODO Реализовать страничку или выписать в существующую страничку когда
                # пользоваетль не ввел симптомы или мы их не нашли
                pass

        elif dialog.stage == 2:
            if request.POST.get("text") == "Good":
                dialog.is_good_result = True
            else:
                dialog.is_good_result = False
            dialog.save()
            return render(request, "dialog.html", {"OK": "", "id": dialog.id, "hidden": "hidden", "pred": ""})
    else:
        dialog = NewDialog.objects.create()
        dialog.save()
        return render(request, "dialog.html", {"id": dialog.id, "hidden": "hidden", "pred": "", "OK": "hidden"})