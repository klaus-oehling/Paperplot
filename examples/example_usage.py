"""Minimal example reproducing the paperplot workflow.

Run with::

    python examples/example_usage.py

Figures are written to ``examples/figures/``.
"""

from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt

import paperplot as pp

OUTPUT_DIR = "examples/figures"


def main() -> None:
    # Full-width figure at 40% of the printable height (A4, 2.5 cm margins).
    pp.use_paper_format(
        vertical_margin_cm=5,
        horizontal_margin_cm=5,
        height=0.4,
        width_split=1,
        tight_view=True,  # box hugs the data; the line starts at the box edge
    )

    x = np.linspace(0, 10, 200)
    fig, ax = plt.subplots()
    ax.plot(x, np.sin(x), label=r"$\sin(x)$")
    ax.axhline(0, color="black", linestyle="--", linewidth=pp.AXES_LINEWIDTH)
    ax.grid(True, linestyle="--", alpha=0.6, linewidth=pp.AXES_LINEWIDTH)
    ax.set_xlabel(r"$x$")
    ax.set_ylabel(r"$f(x)$")
    ax.legend(loc="upper right")
    pp.savefig("sine_full_width", directory=OUTPUT_DIR, fmt="png")

    # Half-width figure (two side by side) using the context manager.
    with pp.paper_format(5, 5, height=0.3, width_split=2):
        fig, ax = plt.subplots()
        ax.hist(np.random.default_rng(0).normal(size=500), bins=20)
        ax.set_xlabel(r"$z$")
        ax.set_ylabel("Count")
        pp.savefig("hist_half_width", directory=OUTPUT_DIR, fmt="svg")

    print(f"Figures written to {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
