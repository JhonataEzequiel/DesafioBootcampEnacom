from science_optimization.builder import (
    BuilderOptimizationProblem,
    Variable,
    Constraint,
    Objective,
    OptimizationProblem
)
from science_optimization.function import (
    FunctionsComposite,
    LinearFunction,
    PolynomialFunction
)
from science_optimization.solvers import Optimizer
from science_optimization.algorithms.linear_programming import Glop
import numpy as np
from typing import List
import pandas as pd


class Investiments:

    def __init__(self, name, cost, ret):

        self.name = name
        self.cost = cost
        self.ret = ret

    def value_density(self):
        return self.ret/(self.cost + 1e-9)

    def __str__(self):
        return f'Name: {self.name}, Cost: {self.cost}, Ret: {self.ret}'


class Inv(BuilderOptimizationProblem):
    def __init__(self, limit, invests: List[Investiments]):
        self.__limit = limit
        self.__invests = invests

    @property
    def __num_vars(self):
        return len(self.__invests)

    @property
    def __cost(self):
        return np.array([invest.cost for invest in self.__invests]).reshape(-1, 1)

    @property
    def __ret(self):
        return np.array([invest.ret for invest in self.__invests]).reshape(-1, 1)

    def build_variables(self):
        x_min = np.zeros((self.__num_vars, 1))
        x_max = np.ones((self.__num_vars, 1))
        x_type = ['d']*self.__num_vars
        variables = Variable(x_min, x_max, x_type)

        return variables

    def build_constraints(self):
        constraint = LinearFunction(c=self.__cost, d=-self.__limit)

        ineq_cons = FunctionsComposite()
        ineq_cons.add(constraint)

        aux = [1, 0, 0, 0, 1, 0, 0, 0]
        aux = np.array(aux).reshape(-1, 1)
        constraint2 = LinearFunction(c=aux, d=-1)
        ineq_cons.add(constraint2)

        aux2 = [0, 1, 0, -1, 0, 0, 0, 0]
        aux2 = np.array(aux2).reshape(-1, 1)
        constraint3 = LinearFunction(c=aux2, d=0)
        ineq_cons.add(constraint3)

        constraints = Constraint(ineq_cons=ineq_cons)

        return constraints

    def build_objectives(self):
        obj_fun = LinearFunction(c=-self.__ret)

        obj_funs = FunctionsComposite()
        obj_funs.add(obj_fun)
        objective = Objective(objective=obj_funs)

        return objective


def optimization_problem(limit: float, available_inv: List[Investiments], verbose: bool = False):
    inv = Inv(limit, available_inv)
    problem = OptimizationProblem(builder=inv)
    if verbose:
        print(problem.info())
    return problem


def run_optimization(problem: OptimizationProblem, verbose: bool = False):
    optimizer = Optimizer(opt_problem=problem, algorithm=Glop())
    results = optimizer.optimize()
    decision_variables = results.x.ravel()
    if verbose:
        print(f"Decision variable: \n {decision_variables}")
    return decision_variables


def inv_milp(limit: float, invests: List[Investiments], verbose: bool = False):
    problem = optimization_problem(limit, invests, verbose)
    decision_variables = run_optimization(problem, verbose)

    chosen_inv = list()
    for inv, inv_was_chosen in zip(invests, decision_variables):
        if inv_was_chosen:
            chosen_inv.append(inv)
    return chosen_inv


def to_table(items: List[Investiments]):
    records = [{
        'Item': i.name,
        'Return': i.ret,
        'Cost': i.cost
        } for i in items]
    records.append({'Item': 'Total', 'Return': sum(i.ret for i in items), 'Cost': sum(i.cost for i in items)})
    return pd.DataFrame.from_records(records)