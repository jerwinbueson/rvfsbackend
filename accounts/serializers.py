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