# zurich/apps/optimizers/views.py
# from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import views, status
from rest_framework.response import Response
from rest_framework import exceptions
from django.db import transaction

from zurich.wsgi import registry

# from apps.optimizers.registry import OptimizeRegistry

import json

from apps.zurichAPI.models import Endpoints
from apps.zurichAPI.serializers import EndpointSerializer

from apps.zurichAPI.models import Algorithms
from apps.zurichAPI.serializers import AlgorithmSerializer

from apps.zurichAPI.models import AlgorithmStatus
from apps.zurichAPI.serializers import AlgorithmStatusSerializer

from apps.zurichAPI.models import Requests
from apps.zurichAPI.serializers import RequestSerializer

from apps.zurichAPI.models import ModelConstraints
from apps.zurichAPI.serializers import ModelConstraintsSerializer


class EndpointsViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin,
                       mixins.ListModelMixin):
    serializer_class = EndpointSerializer
    queryset = Endpoints.objects.all()


class AlgorithmsViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin,
                        mixins.ListModelMixin):
    serializer_class = AlgorithmSerializer
    queryset = Algorithms.objects.all()


def deactivate_status(instance):
    prev_status = AlgorithmStatus.objects.filter(
        parent_algorithm=instance.parent_algorithm,
        created_at__lt=instance.created_at,
        active=True)

    for i in range(len(prev_status)):
        prev_status[i].active = False
    AlgorithmStatus.objects.bulk_update(prev_status, ["active"])


class AlgorithmStatusViewSet(viewsets.GenericViewSet,
                             mixins.RetrieveModelMixin, mixins.ListModelMixin,
                             mixins.CreateModelMixin):
    serializer_class = AlgorithmStatusSerializer
    queryset = AlgorithmStatus.objects.all()

    def perform_create(self, serializer):
        try:
            with transaction.atomic():
                instance = serializer.save(active=True)
                deactivate_status(instance)

        except Exception as e:
            raise exceptions.APIException(str(e))


class RequestsViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin,
                      mixins.ListModelMixin, mixins.UpdateModelMixin):
    serializer_class = RequestSerializer
    queryset = Requests.objects.all()


class ModelConstraintsModelViewSet(viewsets.ModelViewSet):
    serializer_class = ModelConstraintsSerializer
    queryset = ModelConstraints.objects.all()


''' endpoint for our optimization view '''


class ILPOptimizeView(views.APIView):
    def post(self, request, endpoint_name, format=None):

        # algorithm_id = self.request.query_params.get("id")
        algorithm_status = self.request.query_params.get(
            "status", "production")

        version = self.request.query_params.get("version")

        algs = Algorithms.objects.filter(parent_endpoint__name=endpoint_name,
                                         status__status=algorithm_status,
                                         status__active=True)

        if version is not None:
            algs = algs.filter(version=version)

        if len(algs) == 0:
            return Response(
                {
                    "status": "Error",
                    "message": "ML algorithm is not available"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        alg_index = 0
        algorithm_object = registry.endpoints[algs[alg_index].id]
        full_response, response = algorithm_object.optimize(request.data)

        model_request = Requests(
            data=json.dumps(request.data),
            full_response=full_response,
            response=response,
            feedback="",
            parent_ilpalgorithm=algs[alg_index],
        )

        model_request.save()

        full_response["request_id"] = model_request.id

        return Response(full_response)
