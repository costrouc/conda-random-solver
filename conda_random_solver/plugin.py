from conda import plugins

from conda_random_solver.solver import RandomSolver


@plugins.hookimpl
def conda_solvers():
    """
    The conda plugin hook implementation to load the solver into conda.
    """
    yield plugins.CondaSolver(
        name="random",
        backend=RandomSolver,
    )
