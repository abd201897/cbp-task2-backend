from django.urls import path
from .views import *

urlpatterns = [

    path('get_module_detail', get_module_detail, name='get_module_detail'),
]