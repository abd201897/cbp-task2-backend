from django.urls import path
from .views import *

urlpatterns = [
    # ### Course List API's
    path('get_courses_list', get_courses_list, name='get_courses_list'),
    path('get_course_modules', get_course_modules, name='get_course_modules'),

    path('get_module_detail', get_module_detail, name='get_module_detail'),
]