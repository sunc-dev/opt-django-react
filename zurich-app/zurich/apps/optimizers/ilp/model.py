# -*- coding: utf-8 -*-
"""
Created on Tue Aug 18 07:59:21 2020

@author: csunj
"""

try:
    import pulp as pl
    import pandas as pd

    from .preprocessing import Processor

except (RuntimeError, Exception) as err_msg:
    print("Some Modules are Missing {}".format(err_msg))


class Model(object):
    def __init__(self, constraints=None):

        self.modelName = 'porfolio-opt'
        self.constraints = constraints

    def checkDict(self):
        # method to
        keys = [
            'budget', 'proximity', 'endangerment', 'trees', 'water', 'area'
        ]

        if (self.constraints is None) or (not self.constraints):
            self.constraints = {key: 0 for key in keys}
        else:
            constraints = {}
            for item, value in self.constraints.items():
                for key in keys:
                    if item == key:
                        value = float(value)
                        constraints[item] = value
            self.constraints = constraints
            # self.constraint = self.constraints

        return self.constraints

    def load(self):
        '''function to transform data'''

        trf = Processor()
        data = trf.get_data('input.csv')
        inputs = trf.normalize_data(data)
        return inputs

    def init_model(self, inputs):
        '''function to ILP initalize model'''

        decisions = []
        objective = []
        equation = []

        try:
            model = pl.LpProblem(self.modelName, pl.LpMaximize)
            decisions = [
                pl.LpVariable(str('x' + str(index)),
                              lowBound=0,
                              upBound=1,
                              cat='Binary') for index in inputs.index
            ]
            # for decision in decisions:
            #    print(decision)

            equation = pl.lpSum([
                (inputs.Area[i] + inputs.Trees[i] + inputs.Water[i] +
                 inputs.Endangered[i] + inputs.NaturalReserve[i]) *
                decisions[j] for i in inputs.index
                for j, decision in enumerate(decisions) if i == j
            ])

            objective += equation
            model += objective
            # print("Objective Function: " + str(objective))

        except Exception as err_msg:
            print("Model initialization failure, {}".format(err_msg))
        return model, decisions

    def add_constraints(self, model, inputs, decisions):
        '''method to setup ILP constraints'''
        constraints = Model.checkDict(self)
        budget = ''
        proximity = ''
        endangerment = ''
        trees = ''
        water = ''
        area = ''

        try:
            for index, row in inputs.iterrows():
                for i, decision in enumerate(decisions):
                    if index == i:

                        budget += row.Price * decision
                        proximity += row.NaturalReserve * decision
                        endangerment += row.Endangered * decision
                        trees += row.Trees * decision
                        water += row.Water * decision
                        area += row.Area * decision

            # Constraint inequalities
            model += (budget <= constraints['budget'], 'budget_constraint')
            model += (proximity <= constraints['proximity'],
                      'proximity_constraint')
            model += (endangerment >= constraints['endangerment'],
                      'endangered_constraint')
            model += (trees >= constraints['trees'], 'trees_constraint')
            model += (water >= constraints['water'], 'water_constraint')
            model += (area >= constraints['area'], 'area_constraint')

        except Exception as err_msg:
            print("Constraint initialization failure, {}".format(err_msg))

        # print("Optimization function: " + str(model))
        return model

    def solve(self, model, inputs):
        '''function to run ILP solver'''
        solver = pl.PULP_CBC_CMD(msg=True, warmStart=True)
        result = model.solve(solver)

        print("Model status: " + pl.constants.LpStatus[result])
        print("Optimal solution output: ", pl.value(model.objective))
        # for variable in model.variables():
        #    print('Decision: ' + variable.name, "=", variable.varValue)

        decisions = [(int(i.name.strip('x')), i.varValue)
                     for i in model.variables()]
        decisions = pd.DataFrame(list(decisions), columns=['id', 'isSelected'])

        result = inputs.merge(decisions[['id', 'isSelected']],
                              how='left',
                              left_on=inputs.index,
                              right_on=['id'])

        return result, decisions

    def postprocessing(self, result, decisions):
        '''method to run post processing on result, dictionary conversion'''
        result = result.drop(['id'], axis=1)
        result = result.to_dict('index')
        decisions = decisions.to_dict('index')
        return result, decisions

        return result
