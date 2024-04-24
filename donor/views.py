from .models import UserModel,Division,District
from .serializers import UserSerializer,DivisionSerializer,DistrictSerializer,LoginSerializer,DonationRequestSerializer
from . paginations import UserPagination

from django.shortcuts import render,redirect
from rest_framework import viewsets
from rest_framework.views import APIView
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate,login,logout
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
# for sending email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import redirect

from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.
class UserRegistration(viewsets.ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    pagination_class=UserPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['email', 'blood_group','division','District','first_name']
    
    def post(self,request):
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("success")
        return Response(serializer.errors)
    
def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except(User.DoesNotExist):
        user = None 
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('https://github.com/')
    else:
        return redirect('https://github.com/')
    
    
class DivisionsView(APIView):
    def get(self,request):
        queryset=Division.objects.all()
        serializer=DivisionSerializer(queryset,many=True)
        return Response(serializer.data)
    

@api_view(['GET'])
def DivisionView(request,pk):
    queryset=Division.objects.get(pk=pk)
    serializer=DivisionSerializer(queryset)
    return Response(serializer.data)

class DistrictsView(viewsets.ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['division']
    # def get(self,request):
    #     queryset=District.objects.all()
    #     serializer=DistrictSeralizer(queryset,many=True)
    #     return Response(serializer.data)
    

@api_view(['GET'])
def DistrictView(request,pk):
    queryset=District.objects.get(pk=pk)
    serializer=DistrictSerializer(queryset)
    return Response(serializer.data)

class UserLoginView(APIView):
    def post(self,request):
        serializer=LoginSerializer(data=self.request.data)
        if serializer.is_valid():
            username=serializer.validated_data["email"]
            password=serializer.validated_data["password"]
            user=authenticate(username=username,password=password)
            if user:
                try:
                    # Attempt to retrieve the user's ID
                    UID = UserModel.objects.get(email=username).id
                except UserModel.DoesNotExist:
                    UID = None
                print(UID)
                token,_=Token.objects.get_or_create(user=user)
                login(request,user)
                return Response({'token' : token.key, 'user_id' : UID})
            else:
                return Response({'error' : 'Invalid Credentials'},status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors)


class UserLogoutView(APIView):
    def get(self, request):
        # request.user.auth_token.delete()
        logout(request)
        return Response({'success' : "logout successful"})
    
@api_view(['POST',])
def logOutView(request):
    if request.method =='POST':
        request.user.auth_token.delete()
        logout(request)
        return Response({'success' : "logout successful"},status=status.HTTP_200_OK)
    return Response(status=status.HTTP_401_UNAUTHORIZED)
    

class UserLogout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Invalidate or delete the token associated with the user
        request.user.auth_token.delete()
        return Response({'success': 'Logged out successfully'}, status=status.HTTP_200_OK)
    
class DonationRequestViewSet(APIView):
    serializer_class=DonationRequestSerializer
    def post(self,request):
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid():
            patient=serializer.save()
            print(patient)
            print(patient.donor.email)
            email_subject = "new blood donate request"
            email_body = render_to_string('mail.html', {'data' :patient})
            
            email = EmailMultiAlternatives(email_subject , '', to=[patient.donor.email])
            email.attach_alternative(email_body, "text/html")
            email.send()
            return Response("success")
        return Response(serializer.errors)
    
