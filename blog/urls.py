from rest_framework.routers import DefaultRouter 
from django.urls import path,include
from . import views

router=DefaultRouter()

router.register('list',views.BlogViewSet)
router.register('latest',views.LatestBlogs,basename='latest')

urlpatterns = [ 
    path('',include(router.urls)),
    path('list/<int:blogId>/comments',views.get_comments,name="get_comments"),
    
]
