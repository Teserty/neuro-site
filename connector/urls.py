from django.urls import path
from connector import views

urlpatterns = [
    path('', views.test),
    path('feedback', views.post_feedback),
    path('dialog', views.dialog)
]
