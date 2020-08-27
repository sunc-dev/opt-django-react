# zurich/apps/optimizer/serializers.py
''' app serializers to convert requests to send information to the rest
framework and pack/unpack database objects'''

from rest_framework import serializers
from .models import Endpoints
from .models import Algorithms
from .models import AlgorithmStatus
from .models import Requests
from .models import ModelConstraints


class EndpointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endpoints
        read_only_fields = ('id', 'name', 'owner', 'created_at')
        fields = read_only_fields


class AlgorithmSerializer(serializers.ModelSerializer):

    current_status = serializers.SerializerMethodField(read_only=True)

    def get_current_status(self, algorithm):
        return AlgorithmStatus.objects.filter(
            parent_algorithm=algorithm).latest('created_at').status

    class Meta:
        model = Algorithms
        read_only_fields = ("id", "algorithm_name", "description", "version",
                            "owner", "created_at", "parent_endpoint",
                            "current_status")
        fields = read_only_fields


class AlgorithmStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlgorithmStatus
        read_only_fields = ("id", "active")
        fields = ("id", "active", "status", "created_by", "created_at",
                  "parent_algorithm")


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requests
        read_only_fields = ("id", "data", "full_response", "response",
                            "created_at", "parent_algorithm")
        fields = ("id", "data", "full_response", "response", "inputs",
                  "created_at", "parent_algorithm")


class ModelConstraintsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelConstraints
        read_only_fields = ("id", "created_at")
        fields = ('__all__')
