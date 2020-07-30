from .views import *
from rest_framework.routers import DefaultRouter
from django.urls import include, path


# declare View Sets for User models
router = DefaultRouter()
router.register(r'account', AccountViewset, basename='account')
router.register(r'customer_profile', CustomerProfileViewset, basename='customer_profile')
router.register(r'profile', UserViewset, basename='user_profile')

urlpatterns = [
    path('', include(router.urls)),
    # auth from rest_auth framework
    path('auth/', include('rest_auth.urls')),
    path('auth/registration/', include('rest_auth.registration.urls')),
    path('test_profile/', get_user_profile)
]
