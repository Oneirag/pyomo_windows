import unittest
from time import time
from pyomo_windows.simple_model import create_model2
from pyomo_windows.solvers import SolverManager
from pyomo_windows import solver_executables


class TestSolvers(unittest.TestCase):

    solvers = [
        "ipopt",
        "glpk",
        # "highs",
        "cbc"
    ]

    def setUp(self) -> None:
        self.solvers = SolverManager()

    def test_solver_installation(self):
        """Tests that solvers are properly installed"""
        for solver in solver_executables:
            with self.subTest(solver=solver):
                self.solvers.check_solver(solver)

        # Checks that a non-existing solver raises error
        with self.assertRaises(ValueError):
            self.solvers.check_solver("bla bla")


    def test_solver_works(self):
        for solver in solver_executables:
            with self.subTest(solver=solver):
                tic = time()
                model = create_model2()
                # model = create_model1()
                opt = self.solvers.get_solver(solver)
                res = opt.solve(model)
                print(f"Solved {solver} in {time()-tic:.5f} seconds")
                print(res)
                # print_results(model)
        # Checks that a non-existing solver raises error
        with self.assertRaises(ValueError):
            self.solvers.get_solver("bla bla")


if __name__ == '__main__':
    unittest.main()
