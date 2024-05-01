import argparse
import os

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="The N Body Problem: Render Animation",
        description="Render the output of a solved system to a animation",
    )
    parser.add_argument("system_output_path")
    parser.add_argument("-f", "--fps", default=48)
    parser.add_argument("-d", "--dpi", default=300)

    args = parser.parse_args()
    outputs_directory = os.path.split(args.system_output_path)[0]
    filename = os.path.split(args.system_output_path)[-1].split(".")[0]
    system_name = os.path.split(os.path.split(outputs_directory)[0])[-1]

    bodies = np.load(args.system_output_path, allow_pickle=True)

    paths = np.array([list(zip(*b.path)) for b in bodies])
    colours = [b.colour for b in bodies]
    m = np.array([b.mass for b in bodies])[:, None, None]
    system_CoM = np.sum(m * paths, axis=0) / np.sum(m)
    paths = paths - system_CoM[None, :]  # Recenter coordinates
    max_distance = np.max(paths)

    def update(i):
        ax.clear()
        ax.set(xlim=[-max_distance, max_distance], ylim=[-max_distance, max_distance])
        ax.axis('equal')
        trail_start = max(0, i-1000)
        for b in range(len(bodies)):
            plt.plot(paths[b, 0, trail_start:i],
                        paths[b, 1, trail_start:i], c=colours[b])
        plt.scatter(paths[:, 0, i], paths[:, 1, i], c=colours)

    fig = plt.figure()
    ax = fig.gca()
    ax.axis('equal')
    ax.set(xlim=[-max_distance, max_distance], ylim=[-max_distance, max_distance])

    frames = np.arange(len(bodies[0].path))
    ani = animation.FuncAnimation(fig, update, frames=frames[::60])
    ani.save(os.path.join(outputs_directory, f"{filename}.mp4"), fps=args.fps, dpi=args.dpi, writer="ffmpeg")

if __name__ == "__main__":
    main()