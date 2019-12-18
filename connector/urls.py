from django.urls import path
from connector import views

urlpatterns = [
    path('', views.dialog_view, name="dialog")
]
