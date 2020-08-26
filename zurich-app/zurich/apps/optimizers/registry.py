# file backend/server/apps/optimizers/registry.py
from apps.zurichAPI.models import Endpoints
from apps.zurichAPI.models import Algorithms
from apps.zurichAPI.models import AlgorithmStatus


class OptimizerRegistry():
    '''Object represents our optimizer registry, methods to add algorithms'''
    def __init__(self):
        self.endpoints = {}

    def add_algorithm(self, endpoint_name, algorithm_object, algorithm_name,
                      algorithm_status, algorithm_version, owner,
                      algorithm_description):
        '''Method to add algorithm to registry'''
        endpoint, _ = Endpoints.objects.get_or_create(name=endpoint_name,
                                                      owner=owner)

        db_object, algorithm_created = Algorithms.objects.get_or_create(
            algorithm_name=algorithm_name,
            description=algorithm_description,
            version=algorithm_version,
            owner=owner,
            parent_endpoint=endpoint)

        if algorithm_created:
            status = AlgorithmStatus(status=algorithm_status,
                                     created_by=owner,
                                     parent_algorithm=db_object,
                                     active=True)
            status.save()

        self.endpoints[db_object.id] = algorithm_object
