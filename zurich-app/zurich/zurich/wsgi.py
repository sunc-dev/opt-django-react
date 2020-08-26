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
    registry.add_algorithm(
        endpoint_name='ilp',
        algorithm_object=model,
        algorithm_name='integer programming',
        algorithm_status='production',
        algorithm_version='0.0.1',
        owner='Chris Sun',
        algorithm_description='integer programming with processing')
except Exception as err_msg:
    print('Error while loading algorithm to registry,', str(err_msg))
