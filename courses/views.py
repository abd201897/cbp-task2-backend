from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from courses.models import Course
from courses.serializers import CourseSerializer
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