from django.shortcuts import render
from connector.utils.forNLP import *
import numpy as np
from main import predict
from connector.models import NewDialog
from connector.data.readydata import *
from connector.data.sparser import *


def dialog_view(request):
    if request.method == "POST":
        dialog = NewDialog.objects.get(id=request.POST.get("id"))
        if dialog.stage == 0:
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
            dialog.user_text = new_text
            dialog.stage = 1
            dialog.save()
            array = make_advert_with_text(new_text)
            print(array)
            return render(request, "dialog.html",
                          {"OK": "hidden", "neuro_text": "Maybe you have some of this symptoms too?", "id": dialog.id, "hidden": "",
                           "hidden2": "hidden", "advice": array})
        elif dialog.stage == 1:
            text = dialog.user_text
            also = request.POST.get("text")
            tok = np.zeros(132)
            c = 0
            print(text)
            for i in data:
                if i in text:
                    tok[c] = 1
                c += 1

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