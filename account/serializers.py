from django.contrib.auth import get_user_model
from rest_framework import serializers, exceptions, validators
from django.contrib.auth.password_validation import validate_password
from rest_framework.serializers import ModelSerializer, Serializer
from core.serializers import BaseModelSerializer

User = get_user_model()


class UserSerializer(BaseModelSerializer):

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', "email", "username")


# class GroupSerializer(BaseModelSerializer):
#     user = UserSerializer()
#
#
# class UserBaseSerializer(Serializer):
#     id = serializers.IntegerField(read_only=True)
#     first_name = serializers.CharField(max_length=30, allow_blank=True, allow_null=True, )
#     last_name = serializers.CharField(max_length=50, allow_blank=True, allow_null=True, )
#     email = serializers.EmailField(
#         required=True,
#         validators=[
#             validators.UniqueValidator(queryset=User.objects.all(), ),
#         ]
#     )
#     password = serializers.CharField(write_only=True)
#
#     def validate_password(self, password):
#         if validate_password(password):
#             raise exceptions.ValidationError(detail="Пароль некоректний")
#         return password
#
#     def validate_first(self, email):
#         if email.enswith(("datawiz.io", "nieslse.com")):
#             raise exceptions.ValidationError(detail="Такі емейли недоступні")
#         return email
#
#     def validate(self, attrs):
#         attrs = super().validate(attrs)
#         return attrs
#
#     def create(self, validate_data):
#         return User.objects.create_user(**validate_data)
#
#     def update(self, instance, validated_data):
#         instance.__dict__.update(**validated_data)
#         instance.save()
#
#     class Meta:
#         model = User
