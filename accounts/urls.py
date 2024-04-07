from django.urls import path, include
from .views import *
urlpatterns = [
    # path('login', login, name='login'),
    path('add_user', add_user, name='add_user'),
    path('update_user', update_user, name='update_user'),
    path('get_user', get_user, name='get_user'),

]
