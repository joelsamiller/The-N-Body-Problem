import argparse
import os
from runpy import run_path
from time import perf_counter

import matplotlib.pyplot as plt
import numpy as np

from the_n_body_problem.objects import Body, System

TIME_TO_SECONDS = {
    "s": 1,
    "h": 3600,
    "d": 3600 * 24,
    "y": 3600 * 24 * 365.25,
}


def plot_results(system: System):
    paths = np.array([list(zip(*b.path)) for b in system.bodies])
    colours = [b.colour for b in system.bodies]

    for b in range(len(system.bodies)):
        plt.plot(paths[b, 0, :], paths[b, 1, :], c=colours[b])
    plt.scatter(paths[:, 0, -1], paths[:, 1, -1], c=colours)
    plt.axis("equal")
    plt.show()


def save_results(system: System, filename: str) -> None:
    np.save(filename, system.bodies)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="The N Body Problem: System Solver",
        description="Solve ODEs for a system of bodies interacting under gravity",
    )
    parser.add_argument("system_path")
    parser.add_argument("-m", "--method", default="leapfrog")
    parser.add_argument("-t", "--time")
    parser.add_argument("-dt", "--time_step")

    args = parser.parse_args()
    initial_conditions = run_path(os.path.join(args.system_path, "initial_conditions.py"))
    
    time_unit = args.time[-1] if args.time[-1].isalpha() else "s"
    time_step_unit = args.time_step[-1] if args.time[-1].isalpha() else "s"
    
    if time_unit not in TIME_TO_SECONDS:
        raise Exception(f"Invalid time unit {time_unit}")
    if time_step_unit not in TIME_TO_SECONDS:
        raise Exception(f"Invalid time unit {time_step_unit}")
    
    total_time = np.round(int(args.time[0:-1]) * TIME_TO_SECONDS[time_unit])
    time_step = np.round(int(args.time_step[0:-1]) * TIME_TO_SECONDS[time_step_unit])
    time_array = np.linspace(0, total_time, int(np.round(total_time / time_step)))

    system = System(
        [b for b in initial_conditions.values() if isinstance(b, Body)]
    )
    print("*" * 64)
    print("The N Body Problem".center(64))
    print("*" * 64)
    print("System Info:")
    print(f"    N = {len(system.bodies)}")
    print(f"    T = {args.time}")
    print(f"    dt = {args.time_step}")
    print(f"    Number of time steps = {int(np.round(total_time / time_step))}")
    print("*" * 64)
    t0 = perf_counter()
    system.solve(time_array, method=args.method)
    t1 = perf_counter()
    print(f"System solved in {t1 - t0:.1f} seconds usign the {args.method.replace("_", " ")} method")
    save_results(
        system,
        filename=os.path.join(
            args.system_path,
            "outputs",
            f"T{args.time}_dt{args.time_step}.npy",
        ),
    )
    plot_results(system)


if __name__ == "__main__":
    main()
