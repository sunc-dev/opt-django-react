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
                        if value:
                            value = float(value)
                            constraints[item] = value
                        else:
                            value = float(0)
                            constraints[item] = value
            self.constraints = constraints
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
        return model, constraints

    def solve(self, model, inputs):
        '''function to run ILP solver'''

        solver = pl.PULP_CBC_CMD(msg=True, warmStart=True)
        response = model.solve(solver)
        model_status = pl.constants.LpStatus[response]
        solution_value = pl.value(model.objective)

        response_decisions = [(int(i.name.strip('x')), i.varValue)
                              for i in model.variables()]
        response_decisions = pd.DataFrame(list(response_decisions),
                                          columns=['id', 'isSelected'])

        response = inputs.merge(response_decisions[['id', 'isSelected']],
                                how='left',
                                left_on=inputs.index,
                                right_on=['id'])

        response, response_descisions = Model.postprocessing(
            self, response, response_decisions)

        if model_status == 'Optimal' and solution_value != 0:
            status_description = 'Optimal solution found!'

        elif model_status == 'Optimal' and solution_value == 0:
            status_description = 'No constraints provided!'

        else:
            status_description = 'No optimal solutions was found!'
            print(response, response_decisions)
        return response, response_decisions, model_status, solution_value, status_description

    def postprocessing(self, response, response_decisions):
        '''method to run post processing on result, dictionary conversion'''

        response = response.drop(['id'], axis=1)
        response = response.to_dict('index')
        response_decisions = response_decisions.to_dict('index')
        return response, response_decisions
