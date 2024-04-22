from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from courses.models import Course, Module
from courses.serializers import CourseSerializer, ModuleSerializer
from utils.handlers.request_handlers import DRHandler

DR_handler = DRHandler()

# Create your views here.


@DR_handler.public_rest_call(allowed_methods=['GET'])
def get_courses_list(request):
    paginator = PageNumberPagination()
    paginator.page_size = 10  # Set the number of items per page
    courses = Course.objects.all()
    result_page = paginator.paginate_queryset(courses, request)
    serializer = CourseSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@DR_handler.public_rest_call(allowed_methods=['GET'])
def get_course_modules(request):
    course_id = request.GET.get('id', None)
    if course_id and type(int(course_id)) == int:
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Set the number of items per page
        course_ = Course.objects.filter(id=course_id)
        result_page = paginator.paginate_queryset(course_, request)
        serializer = CourseSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    else:
        return Response(data={
            'message': '`course_id` of type int be provided.'
        }, status=status.HTTP_400_BAD_REQUEST)


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
