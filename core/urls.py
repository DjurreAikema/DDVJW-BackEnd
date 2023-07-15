from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core.views import LoginAPIView, RefreshAPIView, LogoutAPIView, ForgotAPIView, ResetAPIView, UserAPIView
from core.viewsuser import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    # Auth
    # path('register', RegisterAPIView.as_view()),
    path('login', LoginAPIView.as_view()),
    path('refresh', RefreshAPIView.as_view()),
    path('logout', LogoutAPIView.as_view()),
    path('forgot', ForgotAPIView.as_view()),
    path('reset', ResetAPIView.as_view()),

    # User
    path('user', UserAPIView.as_view()),
    path('', include(router.urls))
]
