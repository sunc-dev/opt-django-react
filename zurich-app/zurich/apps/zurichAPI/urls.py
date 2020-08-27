# zurich-api/zurich/apps/optimizers/urls.py
''' define url endpoints for our api '''

# from django.contrib import admin
# from django.urls import path
from django.conf.urls import url, include

from rest_framework import routers

# import views
from apps.zurichAPI.views import EndpointsViewSet
from apps.zurichAPI.views import AlgorithmsViewSet
from apps.zurichAPI.views import AlgorithmStatusViewSet
from apps.zurichAPI.views import RequestsViewSet
from apps.zurichAPI.views import ModelView
from apps.zurichAPI.views import ILPOptimizeView
from apps.zurichAPI.views import ConstraintsViewSet

router = routers.DefaultRouter()
router.register(r"endpoints", EndpointsViewSet, basename='endpoint')
router.register(r"algorithms", AlgorithmsViewSet, basename='algorithms')
router.register(r"status", AlgorithmStatusViewSet, basename='status')
router.register(r"requests", RequestsViewSet, basename='requests')
router.register(r"constraints", ConstraintsViewSet, basename='constraints')

urlpatterns = [
    url(r"^api/", include(router.urls)),
    url(r"^api/(?P<endpoint_name>.+)/optimize$",
        ILPOptimizeView.as_view(),
        name="optimize"),
    url(r"^api/v1/model", ModelView.as_view(), name='model')
]
