from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import ContactSerializer
from rest_framework.response import Response

# Create your views here.
class ContactViewSet(APIView):
    serializer_class=ContactSerializer
    def post(self,request):
        serializer=self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("success")
        return Response(serializer.errors)