import pyomo.environ as pyo


def create_model1():
    model = pyo.ConcreteModel()

    model.x = pyo.Var([1, 2], domain=pyo.NonNegativeReals)

    @model.Objective(sense=pyo.maximize)
    def objective(model):
        return 2 * model.x[1] - 3 * model.x[2]

    @model.Constraint
    def constrain(model):
        return 3 * model.x[1] + 4 * model.x[2] <= 1

    return model


def create_model2():
    model = pyo.ConcreteModel()

    # declare decision variables
    model.x = pyo.Var(domain=pyo.NonNegativeReals)

    # declare objective
    model.profit = pyo.Objective(
        expr=40 * model.x,
        sense=pyo.maximize)

    # declare constraints
    model.demand = pyo.Constraint(expr=model.x <= 40)
    model.laborA = pyo.Constraint(expr=model.x <= 80)
    model.laborB = pyo.Constraint(expr=2 * model.x <= 100)

    return model


def print_results(model):
    print(f"Profit = {model.profit()} per week")
    print(f"X = {model.x()} units per week")


if __name__ == '__main__':
    for idx, model in enumerate([create_model1(), create_model2()]):
        print(f"Model {idx}")
        model.pprint()
