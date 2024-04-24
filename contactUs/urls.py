from django.urls import path,include
from .views import ContactViewSet

urlpatterns = [
    path('',ContactViewSet.as_view(),name='contact')
]

