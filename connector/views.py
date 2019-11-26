from django.shortcuts import render
from connector.utils.forNLP import *
from connector.utils.symptoms_defs import *
from connector.models import *
from django.shortcuts import redirect
from connector.utils.connect_with_neuro import *
from django.http import JsonResponse


def test(request):
    if request.method == "GET":
        return render(request, "mainpage.html")
    if request.method == "POST":
        text = request.POST.get("text")

        dialog = Dialog.objects.create()
        dialog.user_text = text

        array = work_with_text(text)
        array = convert_to_vector(array)
        # Add neuro
        f_res = get_data(array)

        dialog.result = f_res
        dialog.save()
        return render(request, "mainpage.html",
                      {"result": array, "withResult": True, "f_res": f_res, "id": dialog.id}
                      )


def post_feedback(request):
    if request.method == "POST":
        id = request.POST.get("id")
        is_good_result = request.POST.get("is_good")
        dialog = Dialog.objects.get(id=id)
        is_good_result = (is_good_result == "good")
        dialog.is_good_result = is_good_result
        dialog.save()
    return redirect("/")


# Dialog: Send sympoms to user to check correction. Also give some sympoms, if them are in the same


from django.views.decorators.csrf import csrf_exempt
from connector.models import NewDialog
import json

# 0 - пользователь написал нам свои жалобы
# 1 - пользователь оценил наш анализ текста (проверил правильность симтомов) (2 или 3)
# 2 - пользователю непонравился наш анализ и он написал его сам
# 3 - пользователь согласился с нами
# 4 - пользователь получил наш ответ и оценивает его


def dialog(request):
    if request.method == "POST":
        #print(request.POST.get("id"))
        dialog = NewDialog.objects.get(id=request.POST.get("id"))
        if(dialog.stage == 0):

            array = work_with_text(request.POST.get("text"))
            array = convert_to_vector(array)

            dialog.user_text += "\n" + request.POST.get("text")
            mystring = ""
            for digit in array:
                mystring += str(digit)
            dialog.our_text += "\n" + mystring
            dialog.result = array
            dialog.stage = 1
            dialog.save()
            return render(request, "dialog.html", {"neuro_text": array, "id": dialog.id})
        if(dialog.stage == 1):
            if(request.POST.get("text") == ("Y" or "Yes" or "yes")):
                dialog.stage = 3

                result = "Wait"
                #dialog.result
                dialog.save()
                #return render(request, "dialog.html", {"neuro_text": result, "id": dialog.id})
            else:
                dialog.stage = 2
                text = "Send again"
                dialog.save()
                return render(request, "dialog.html", {"neuro_text": text, "id": dialog.id})
        if(dialog.stage == 2):
            array = convert_to_vector(request.POST.get("text"))

            dialog.user_text += "\n" + request.POST.get("text")
            mystring = ""
            for digit in array:
                mystring += " "+ str(digit)
            dialog.our_text += "\n" + mystring
            dialog.result = array
            dialog.stage = 3
            dialog.save()

            return render(request, "dialog.html", {"neuro_text": mystring, "id": dialog.id})
        if(dialog.stage == 3):
            #neuro
            f_res = get_data(dialog.result)
            dialog.stage = 4
            dialog.save()
            return render(request, "dialog.html", {"neuro_text": f_res, "id": dialog.id})
        if(dialog.stage == 4):
            if(request.POST.get("text") == "Good"):
                dialog.is_good_result = True
            else:
                dialog.is_good_result = False
            return render(request, "dialog.html", {"neuro_text": "Ok", "id": dialog.id})


    else:
        dialog = NewDialog.objects.create()
        dialog.save()
        return render(request, "dialog.html", {"id": dialog.id})

