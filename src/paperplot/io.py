"""Saving helpers for paper-ready figures."""

from __future__ import annotations

import os
from typing import Optional

import matplotlib.pyplot as plt
from matplotlib.figure import Figure

#: File formats supported by :func:`savefig`.
SUPPORTED_FORMATS: tuple[str, ...] = ("svg", "png")


def savefig(
    name: str,
    directory: str = ".",
    fmt: str = "svg",
    *,
    fig: Optional[Figure] = None,
    dpi: int = 600,
    tight_layout: bool = True,
    bbox_inches: Optional[str] = "tight",
    transparent: bool = False,
    close: bool = True,
) -> str:
    """Save a figure to disk with paper-ready defaults.

    Parameters
    ----------
    name:
        File name without extension. The extension is derived from ``fmt``.
    directory:
        Target directory. Created if it does not exist.
    fmt:
        Output format, either ``"svg"`` or ``"png"``.
    fig:
        Figure to save. Defaults to the current figure (``plt.gcf()``).
    dpi:
        Resolution used for raster formats such as PNG.
    tight_layout:
        Whether to call ``Figure.tight_layout`` before saving.
    bbox_inches:
        Passed to ``Figure.savefig``; ``"tight"`` trims surrounding whitespace.
    transparent:
        Whether to use a transparent background.
    close:
        Whether to close the figure after saving to free memory.

    Returns
    -------
    str
        The full path of the written file.

    Raises
    ------
    ValueError
        If ``fmt`` is not a supported format.
    """
    fmt = fmt.lower()
    if fmt not in SUPPORTED_FORMATS:
        valid = ", ".join(SUPPORTED_FORMATS)
        raise ValueError(f"fmt must be one of: {valid}; got {fmt!r}.")

    figure = fig if fig is not None else plt.gcf()

    if tight_layout:
        figure.tight_layout()

    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, f"{name}.{fmt}")
    figure.savefig(
        path,
        format=fmt,
        dpi=dpi,
        bbox_inches=bbox_inches,
        transparent=transparent,
    )

    if close:
        plt.close(figure)

    return path
