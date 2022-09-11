from django.urls import path

from . import views

urlpatterns = [
    path('transact', views.Transact.as_view()),
    path('balance', views.ShowBalance.as_view()),
    path('history', views.HistorySuccesfullTransact.as_view()),
]