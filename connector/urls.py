from django.urls import path
from connector import views

urlpatterns = [
    path('', views.dialog_view),
    path('feedback', views.post_feedback),
    path('test', views.dialog_with_js)
]
