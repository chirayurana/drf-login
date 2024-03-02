from rest_framework import serializers
from account.models import MyUser

class UserRegistrationSerializer(serializers.ModelSerializer):
    #We are writing this because we need to confirm our password field in Registration Request
    password2 = serializers.CharField(style={'input_type':'password'}
                                      , write_only=True)
    class Meta:
        model = MyUser
        fields=['email','name','password','password2','tc']
        extra_kwargs={
            'password':{'write_only':True}
        }

    #Validating Password and Confirm Password while Registration
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        #If password and confirm password doesnt match
        if password != password2:
            raise serializers.ValidationError('Password and Confirm password does not match')
        return attrs
    
    def create(self, validate_data):
        return MyUser.objects.create_user(**validate_data)
    
    
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = MyUser
        fields =['email','password']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['id','email','name']

class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255,style = {'input_type':'password'},write_only=True)
    password2 = serializers.CharField(max_length=255,style = {'input_type':'password'},write_only=True)
    class Meta:
        fields = ['password','password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError('Password and Confirm password does not match')
        user.set_password(password)
        user.save()
        return attrs