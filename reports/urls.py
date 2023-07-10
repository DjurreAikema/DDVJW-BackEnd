from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import ReportViewSet, api_root

router = DefaultRouter()
router.register(r'reports', ReportViewSet, basename='report')

urlpatterns = [
    path('', api_root),
    path('', include(router.urls)),
]
