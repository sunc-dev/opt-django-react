"""
WSGI config for zurich project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""
import os
from django.core.wsgi import get_wsgi_application
from apps.optimizers.registry import OptimizerRegistry
from apps.optimizers.ilp.optimize import ILPOptimizer
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zurich.settings')

application = get_wsgi_application()

# request to add ILP algorithmn

try:
    registry = OptimizerRegistry()
    model = ILPOptimizer()
    registry.add_algorithm(endpoint_name=model.endpoint_name,
                           algorithm_object=model,
                           algorithm_name=model.name,
                           algorithm_status=model.status,
                           algorithm_version=model.version,
                           owner=model.owner,
                           algorithm_description=model.description)
except Exception as err_msg:
    print('Error while loading algorithm to registry,', str(err_msg))
