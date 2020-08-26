from django.test import TestCase
from apps.optimizers.ilp.optimize import ILPOptimizer
from apps.optimizers.registry import OptimizerRegistry


# test algorithm class
class AlgTests(TestCase):
    '''ILP Test object to run test against our ILP algorithm'''
    def test_algorithm(self):
        '''method to run algorithm tests'''
        test_constraints = {
            "budget": 7500,
            "proximity": 20,
            "endangerment": 15,
            "trees": 10,
            "water": 22,
            "area": 15
        }
        test_alg = ILPOptimizer()
        response = test_alg.optimize(test_constraints)
        print(response)

    # tests for registry class
    def test_registry(self):
        '''Method to run test on the algorithm registry'''
        registry = OptimizerRegistry()
        self.assertEqual(len(registry.endpoints), 0)
        endpoint_name = "ilp optimizer"
        algorithm_object = ILPOptimizer().optimize()
        algorithm_name = "ilp optimizer"
        algorithm_status = "production"
        algorithm_version = "0.0.1"
        algorithm_owner = "Chris Sun"
        algorithm_description = "ILP optimization model with preprocesing"
        # add to registry
        registry.add_algorithm(
            endpoint_name,
            algorithm_object,
            algorithm_name,
            algorithm_status,
            algorithm_version,
            algorithm_owner,
            algorithm_description,
        )
        # there should be one endpoint available
        self.assertEqual(len(registry.endpoints), 1)
