from django.urls import path
from . import views

urlpatterns= [
    path('',views.get),
    path('journal/',views.create_journal),
]