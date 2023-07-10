from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .viewsauth import UserAuthViewSet

router = DefaultRouter()
router.register('user-auth', UserAuthViewSet, basename='user-auth')

urlpatterns = [
    # JWT Tokens
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('', include(router.urls)),
    path('reset/<str:token>/', UserAuthViewSet.as_view(), name='password_reset'),
]
