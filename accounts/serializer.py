from rest_framework import serializers
from .models import User,Driver_Documents
import re


class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = (
            'phone_number',
            'full_name',
            'email',
            'password',
            'password2'
        )
        extra_kwargs = {
            'password':{'write_only':True},
        }
    def create(self, validated_data):
        del validated_data['password2']
        return User.objects.create_user(**validated_data)

    def create_driver(self,validate_data):
        user = User.objects.create_user(
            phone_number=validate_data['phone_number'],
            full_name=validate_data['full_name'],
            email=validate_data['email'],
            password=validate_data['password']
        )
        user.is_driver = True
        user.save()
        return user


    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        return data

    def validate_phone_number(self,value):
        if not re.fullmatch(r'\d{11}', value):
            raise serializers.ValidationError('Please enter a valid 11-digit phone number.')
        return value

    def validate_email(self,value):
        valid_email = ['@gmail.com','@email.com','@yahoo.com']
        if not any(value.endswith(domain) for domain in valid_email):
            raise serializers.ValidationError(
                {'email':'Email must be from a valid domain, such as @gmail.com or @email.com.'}
            )
        return value

class DriverDocumentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Driver_Documents
        fields = (
            'license_number',
            'license_expiry',
            'health_card_number',
            'health_card_expiry',
        )
    def create(self, validated_data, request):
        user = User.objects.get(pk=request.user.id)
        return Driver_Documents.objects.create(
            user_id=user,
            license_number=validated_data['license_number'],
            license_expiry=validated_data['license_expiry'],
            health_card_number=validated_data['health_card_number'],
            health_card_expiry=validated_data['health_card_expiry'],
        )


