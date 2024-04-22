from rest_framework import serializers
from .models import Module, Course, StudentModuleRegistration


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = '__all__'
        extra_kwargs = {
            'course_allowed': {'write_only': True},
        }


class CourseSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'

    def create(self, validated_data):
        modules_data = validated_data.pop('modules', [])
        course = Course.objects.create(**validated_data)
        for module_data in modules_data:
            Module.objects.create(course=course, **module_data)
        return course

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.code = validated_data.get('code', instance.code)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        # Update modules
        modules_data = validated_data.get('modules', [])
        existing_modules = {module.id: module for module in instance.modules.all()}
        for module_data in modules_data:
            module_id = module_data.get('id', None)
            if module_id:
                module_instance = existing_modules.pop(module_id, None)
                if module_instance:
                    module_instance.name = module_data.get('name', module_instance.name)
                    module_instance.code = module_data.get('code', module_instance.code)
                    module_instance.credit = module_data.get('credit', module_instance.credit)
                    module_instance.category = module_data.get('category', module_instance.category)
                    module_instance.description = module_data.get('description', module_instance.description)
                    module_instance.availability = module_data.get('availability', module_instance.availability)
                    module_instance.save()
                else:
                    Module.objects.create(course=instance, **module_data)
            else:
                Module.objects.create(course=instance, **module_data)

        # Delete removed modules
        for module in existing_modules.values():
            module.delete()

        return instance


class StudentModuleRegistrationSerializer(serializers.ModelSerializer):
    # modules = ModuleSerializer(many=True, read_only=True)
    modules = serializers.SerializerMethodField('get_modules', allow_null=False, read_only=True)

    def get_modules(self, obj):
        if hasattr(obj, 'module'):
            module_ = Module.objects.get(id=obj.module.id)
            module_serializer = ModuleSerializer(module_)
            return module_serializer.data
        return []

    class Meta:
        model = StudentModuleRegistration
        fields = ['id', 'student', 'module', 'modules']
        extra_kwargs = {
            'student': {'write_only': True},
        }