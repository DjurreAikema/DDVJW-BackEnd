from django.urls import path

from core.views import RegisterAPIView, LoginAPIView, UserAPIView, RefreshAPIView, LogoutAPIView, ForgotAPIView, ResetAPIView, \
    UserUpdateView

urlpatterns = [
    # Auth
    path('register', RegisterAPIView.as_view()),
    path('login', LoginAPIView.as_view()),
    path('refresh', RefreshAPIView.as_view()),
    path('logout', LogoutAPIView.as_view()),
    path('forgot', ForgotAPIView.as_view()),
    path('reset', ResetAPIView.as_view()),

    # User
    path('user', UserAPIView.as_view()),
    path('users/<int:pk>/', UserUpdateView.as_view(), name='user-update'),
]
