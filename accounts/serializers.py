import base64
import imghdr
import os.path

from django.conf import settings
from django.contrib.auth.hashers import make_password
from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model
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


class UserSerializers(ModelSerializer):

    def create(self, validated_data):
        validated_data.pop("image_type")
        validated_data.pop("is_image_uploaded")
        return User_Model.objects.create_user(**validated_data, is_active=True)

    def update(self, instance, validated_data):
        instance = super(UserSerializers, self).update(instance, validated_data)
        instance.email = validated_data.get('first_name')
        instance.first_name = validated_data.get('first_name')
        instance.last_name = validated_data.get('last_name')
        instance.date_of_birth = validated_data.get('date_of_birth')
        instance.address = validated_data.get('address')
        instance.city = validated_data.get('city')
        instance.country = validated_data.get('country')
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])

        if validated_data['is_image_uploaded']:
            instance.image = os.path.join(settings.AZURE_BLOB_URL, instance.username + "_" + str(instance.id) + '.' + validated_data['image_type'])
        instance.save()
        return instance

    def validate(self, attrs):

        if 'image' in attrs and attrs['image'] != "":
            # Split the base64 string to get the content type and data
            header, encoded = attrs['image'].split(',', 1)

            decoded_data = base64.b64decode(encoded)

            attrs['image_type'] = header.split(';')[0].split('/')[1]
            attrs['is_image_uploaded'] = True

        return attrs



    class Meta:
        model = User_Model
        fields = '__all__'

