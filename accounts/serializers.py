import base64
import os.path

from django.conf import settings
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ParseError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

User_Model = get_user_model()


class JWTObtainTokenPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        # ...

        return token


class JWTTokenView(TokenObtainPairView):
    serializer_class = JWTObtainTokenPairSerializer


class UserSerializers(serializers.ModelSerializer):
    password = serializers.CharField(allow_blank=True, )
    image = serializers.CharField(allow_blank=True)

    def create(self, validated_data):
        validated_data.pop("image_type")
        validated_data.pop("is_image_uploaded")
        return User_Model.objects.create_user(**validated_data, is_active=True)

    def update(self, instance, validated_data):
        # instance = super(UserSerializers, self).update(instance, validated_data)
        instance.first_name = validated_data.get('first_name')
        instance.last_name = validated_data.get('last_name')
        instance.date_of_birth = validated_data.get('date_of_birth')
        instance.address = validated_data.get('address')
        instance.city = validated_data.get('city')
        instance.country = validated_data.get('country')
        if 'password' in validated_data and validated_data['password'] != '':
            instance.set_password(validated_data['password'])
        else:
            validated_data.pop('password')

        if 'email' in validated_data and validated_data['email'] == '':
            validated_data.pop('email')
        else:
            instance.email = validated_data.get('email')

        if 'image' in validated_data and validated_data['image'] == '':
            validated_data.pop('image')
        else:
            instance.image = validated_data.get('image')

        # if validated_data['is_image_uploaded']:
        #     instance.image = os.path.join(settings.AZURE_BLOB_URL,
        #                                   instance.username + "_" + str(instance.id) + '.' + validated_data[
        #                                       'image_type'])
        instance.save()
        return instance

    def validate(self, attrs):
        try:
            if 'image' in attrs and attrs['image'] != "":
                # Split the base64 string to get the content type and data
                header, encoded = attrs['image'].split(',', 1)

                decoded_data = base64.b64decode(encoded)

                attrs['image_type'] = header.split(';')[0].split('/')[1]
                attrs['is_image_uploaded'] = True
        except Exception as ex:
            raise serializers.ValidationError(detail='`image` This field is of base64encoded string.')

        return attrs

    def to_representation(self, instance):
        data = super(UserSerializers, self).to_representation(instance)

        if 'password' in data:
            data.pop('password')
        data.pop('date_joined')

        return data

    class Meta:
        model = User_Model
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'user_permissions': {'write_only': True},
            'groups': {'write_only': True}
        }
