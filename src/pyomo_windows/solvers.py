from pathlib import Path
from subprocess import STDOUT, check_output, TimeoutExpired

import pyomo.environ as pyo
from pyomo.contrib.appsi.solvers import Highs

from pyomo_windows import solver_executables, get_target_folder
from pyomo_windows.download_solver import DownloadSolvers


class SolverManager:

    def __init__(self, target: str | Path = None):
        self.target = get_target_folder(target)

    def get_solver_executable(self, solver_name: str) -> Path:
        """Returns full path of the executable of a given solver"""
        solver_name = solver_name.lower()
        if solver_name not in solver_executables:
            raise ValueError(f"Solver '{solver_name}' not know. Valid ones are {', '.join(solver_executables.keys())}")
        return self.target / solver_name / solver_executables.get(solver_name)

    def check_solver(self, solver_name: str) -> str | None:
        executable = self.get_solver_executable(solver_name)
        if not executable.exists():
            downloader = DownloadSolvers(self.target)
            getattr(downloader, f"download_{solver_name}")()
            if not executable.exists():
                raise FileNotFoundError(f"Executable not found for solver '{solver_name}'")
        try:
            result = check_output(f"{executable} --version", stderr=STDOUT, timeout=1)
        except TimeoutExpired as toe:
            result = toe.output
        assert result != b""
        first_line = result.splitlines()[0]
        print(first_line)
        return first_line.decode()

    def get_solver(self, solver_name: str) -> pyo.SolverFactory:
        solver_name = solver_name.lower()
        if solver_name == "highs":
            return Highs()
        executable = self.get_solver_executable(solver_name)
        return pyo.SolverFactory(solver_name, executable=executable)


if __name__ == '__main__':
    solver_manager = SolverManager()
    for executable in solver_executables.keys():
        print(solver_manager.check_solver(executable))
