from rest_framework import serializers
from .models import User, Order


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['email', 'password', 'is_verified']


    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance


class VerifyAccountSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()

class OrderSerializer(serializers.Serializer):
    email = serializers.EmailField()


class OrderCompleteSerializer(serializers.Serializer):
    email = serializers.EmailField()
    bike_id = serializers.IntegerField()
    end_station_id = serializers.IntegerField()

        

