# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 10:03:31 2020

@author: csunj
"""
'''ILP Optimization initializer v.001'''

try:
    from .model import Model
except (RuntimeError) as err_msg:
    print("Some Modules are Missing {}".format(err_msg))


class ILPOptimizer(object):
    '''object that represents the ILP optimization with an initalization method
    '''
    def __init__(self):
        self.name = 'ILP optimizer'
        self.version = '0.0.1'

    def optimize(self, constraints=None):
        '''function that execute model script'''
        keys = [
            'budget', 'proximity', 'endangerment', 'trees', 'water', 'area'
        ]

        if constraints is None:
            constraints = {key: 0 for key in keys}
        else:
            constraints = constraints
        try:
            modelize = Model(constraints)
            inputs = modelize.load()
            model, decisions = modelize.init_model(inputs)
            model = modelize.add_constraints(model, inputs, decisions)
            response, response_decisions = modelize.solve(model, inputs)
            response, response_decisions = modelize.postprocessing(
                response, response_decisions)

            # print('Model run successful')
            self.response = response
            self.response_decisions = response_decisions
            return self.response, self.response_decisions
        except Exception as err_msg:
            print("Model run failure, {}".format(err_msg))


if __name__ == '__main__':
    '''constraints = '{"budget": 7500,"proximity": 20,"endangerment": 15,
     "trees": 10,"water": 22,"area": 15}'
    x = ILPOptimizer()

    z, y = x.optimize(constraints)'''
