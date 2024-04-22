from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response

from courses.models import Module
from courses.serializers import ModuleSerializer
from utils.handlers.request_handlers import DRHandler

DR_handler = DRHandler()

# Create your views here.


@DR_handler.public_rest_call(allowed_methods=['GET'])
def get_module_detail(request):
    try:
        pk = request.GET.get('id', None)
        if pk and type(int(pk)) is int:
            module = Module.objects.get(pk=pk)
            serializer = ModuleSerializer(module)
            return Response(data=serializer.data)
        else:
            raise KeyError('`id` of type `int` cannot be empty.')
    except Module.DoesNotExist:
        return Response(data={
            'message': 'Module does not exist.'
        }, status=status.HTTP_404_NOT_FOUND)
    except KeyError as ke:
        return Response(data={
            'message': str(ke)
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as ex:
        return Response(data={
            'message': str(ex)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
