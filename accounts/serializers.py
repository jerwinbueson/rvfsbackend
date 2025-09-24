from rest_framework import serializers
from .models import CustomUser


class UserInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id',
            'email',
            'first_name',
            'middle_name',
            'last_name',
            'date_of_birth',
            'phone_number',
            'image',
            'is_active',
            'is_staff',
            'last_login',
            
        ]
        read_only_fields = ['id', 'is_active', 'is_staff', 'last_login']
        extra_kwargs = {
            'image': {'required': False, 'allow_null': True}
        }
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Add full URL for the image if it exists
        if instance.image:
            request = self.context.get('request')
            if request is not None:
                representation['image'] = request.build_absolute_uri(instance.image.url)
        return representation

class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        min_length=8,
        error_messages={
            'min_length': 'Password must be at least 8 characters long.'
        }
    )
    
    class Meta:
        model = CustomUser
        fields = [
            'id',
            'email',
            'password',
            'first_name',
            'middle_name',
            'last_name',
            'date_of_birth',
            'phone_number',
            'image',
            'is_active',
            'is_staff',
            'last_login',
            'company',
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'is_active': {'read_only': True},
            'is_staff': {'read_only': True},
            'last_login': {'read_only': True},
        }
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user