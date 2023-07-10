from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .viewsauth import UserAuthViewSet

router = DefaultRouter()
router.register(r'api-auth', UserAuthViewSet, basename='api-auth')

urlpatterns = [
    # JWT Tokens
    path('api-auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api-auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('', include(router.urls))
]
