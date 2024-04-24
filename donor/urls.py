from rest_framework.routers import DefaultRouter
from django.urls import path,include
from .views import UserRegistration,activate,DivisionView,DivisionsView,DistrictsView,DistrictView
from . import views


router=DefaultRouter()
router.register('list',UserRegistration)
router.register('district',DistrictsView)

urlpatterns = [
    path('',include(router.urls)),
    path('active/<uid64>/<token>/', activate, name = 'activate'),
    path('divisions/',DivisionsView.as_view(), name = 'divisions'),
    path('divisions/<int:pk>',DivisionView, name = 'division'),
    # path('district/',DistrictsView.as_view(), name = 'districts'),
    path('district/<int:pk>',DistrictView, name = 'district'),
    path('login/',views.UserLoginView.as_view(), name = 'login'),
    path('logout/',views.UserLogout.as_view(), name = 'logout'),
    path('logouta/',views.UserLogoutView.as_view(), name = 'logouta'),
    path('logoutt/',views.logOutView, name = 'logoutt'),
    path('donation-request/',views.DonationRequestViewSet.as_view(), name='donation-request'),
]
