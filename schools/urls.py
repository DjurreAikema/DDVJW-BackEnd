from django.urls import path

from schools import views

urlpatterns = [
    path('', views.SchoolList.as_view()),
    path('/<int:pk>', views.SchoolDetail.as_view()),
]
