import unittest
from time import time

import pyomo.environ as pyo

from pyomo_windows.simple_model import create_model2


class TestSolvers(unittest.TestCase):
    solvers = [
        "ipopt",
        "glpk",
        # "highs",
        "cbc"
    ]

    def test_solver_installation(self):
        """Tests that solvers are properly installed"""
        for solver in self.solvers:
            with self.subTest(solver=solver):
                self.assertTrue(pyo.SolverFactory(solver).available(),
                                f"solver {solver} not properly installed")

    def test_solver_works(self):
        for solver in self.solvers:
            with self.subTest(solver=solver):
                tic = time()
                model = create_model2()
                # model = create_model1()
                opt = pyo.SolverFactory(solver)
                res = opt.solve(model)
                print(f"Solved {solver} in {time() - tic:.5f} seconds")
                print(res)
                # print_results(model)


if __name__ == '__main__':
    unittest.main()
