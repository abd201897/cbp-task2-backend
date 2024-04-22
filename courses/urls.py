from django.urls import path

from courses.views import get_courses_list, get_course_modules

urlpatterns = [
    # ### Course List API's
    path('get_courses_list', get_courses_list, name='get_courses_list'),
    path('get_course_modules', get_course_modules, name='get_course_modules'),
]