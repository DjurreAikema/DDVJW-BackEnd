from django.urls import path, include

from core.views import RegisterAPIView

urlpatterns = [
    path('register', RegisterAPIView.as_view()),
]