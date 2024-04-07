import json

from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework.response import Response
from utils.handlers.request_handlers import DRHandler
from rest_framework.status import *
from .serializers import UserSerializers

UserModel = get_user_model()

DR_handler = DRHandler()
# Create your views here.


@DR_handler.public_rest_call(allowed_methods=['POST'])
def login(request):

    return Response(data={
        'user': request.user.username
    }, status=HTTP_200_OK)


@DR_handler.public_rest_call(allowed_methods=['POST'])
def add_user(request):
    serializer_ = ''
    data = json.loads(request.body)

    if data:
        serializer_ = UserSerializers(data=data, many=False)
        if serializer_.is_valid(raise_exception=True):
            serializer_.save()
            return Response(data={
                'message': "Student Registered!"
            }, status=HTTP_200_OK)
    return Response(data={
        'error': serializer_.errors
    }, status=HTTP_400_BAD_REQUEST)


@DR_handler.authenticate_rest_call(allowed_methods=['POST'])
def get_user(request):
    user_id = request.GET.get('user_id', None)

    if user_id:
        try:
            user_ = UserModel.objects.filter(id=user_id)
        except Exception as ex:
            return Response(data={
                'message': 'Invalid User'
            }, status=HTTP_400_BAD_REQUEST)
        serializer_ = UserSerializers(user_, many=True)
        return Response(data={
            'data': serializer_.data
        }, status=HTTP_200_OK)
    return Response(data={
        'error': '`user_id` can not be empty parameter!'
    }, status=HTTP_400_BAD_REQUEST)


@DR_handler.authenticate_rest_call(allowed_methods=['POST'])
def update_user(request):
    serializer_ = ''
    data = json.loads(request.body)

    if data:
        user_ = UserModel.objects.filter(username=data.get('username', None)).first()
        serializer_ = UserSerializers(user_, data=data)
        if serializer_.is_valid(raise_exception=True):
            serializer_.save()
            return Response(data={
                'message': "User Updated!"
            }, status=HTTP_200_OK)
    return Response(data={
        'error': serializer_.errors
    }, status=HTTP_400_BAD_REQUEST)