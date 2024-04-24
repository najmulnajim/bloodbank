from rest_framework import serializers
from .models import UserModel,Division,District,DonationRequestModel
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import redirect

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model=District
        fields='__all__'
        
class DivisionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Division
        fields='__all__'
        

class UserSerializer(serializers.ModelSerializer):
    confirm_password=serializers.CharField(max_length=50,required=True,write_only=True)
    password=serializers.CharField(max_length=50,required=True,write_only=True)

    class Meta:
        model=UserModel
        fields='__all__'
        # fields=['first_name', 'last_name', 'gender', 'birth_date', 'email', 'password', 'confirm_password', 'phone','blood_group','division', 'District', 'last_donate']
        
  
    
    def save(self):
        email=self.validated_data['email']
        password=self.validated_data['password']
        confirm_password=self.validated_data['confirm_password']
        first_name=self.validated_data['first_name']
        last_name=self.validated_data['last_name']
        gender=self.validated_data['gender']
        phone=self.validated_data['phone']
        blood_group=self.validated_data['blood_group']
        division=self.validated_data['division']
        district=self.validated_data['District']
        last_donate=self.validated_data['last_donate']
        birth_date=self.validated_data['birth_date']
        image=self.validated_data['image']
        
        if User.objects.filter(username=email).exists():
            raise serializers.ValidationError({'error':'Email already exists!'})

        user=User.objects.create_user(username=email,email=email,first_name=first_name,last_name=last_name)
        user.set_password(password)
        user.is_active=False
        user.save()
        
        donor_email=email
        
        token=default_token_generator.make_token(user)
        uid=urlsafe_base64_encode(force_bytes(user.pk))
        confirm_link=f'http://127.0.0.1:8000/donor/active/{uid}/{token}'
        email_subject='Confirm your account.'
        body=render_to_string('confirmation.html',{'link':confirm_link})
        
        email = EmailMultiAlternatives(email_subject , '', to=[user.email])
        email.attach_alternative(body, "text/html")
        email.send()
        
        donor=UserModel.objects.create(email=donor_email,first_name=first_name,last_name=last_name,gender=gender,phone=phone,blood_group=blood_group,division=division,birth_date=birth_date,last_donate=last_donate,District=district,image=image)
        donor.save()
        return donor
    
class LoginSerializer(serializers.Serializer):
    email=serializers.CharField(required=True)
    password=serializers.CharField(required=True)
    
    
class DonationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model=DonationRequestModel
        fields='__all__'
        

        