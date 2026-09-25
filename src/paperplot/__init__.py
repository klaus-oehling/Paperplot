"""paperplot: standardized, paper-ready matplotlib formatting.

Configure matplotlib once so that every subsequent figure adopts a consistent
academic style and a size derived from the printable area of a sheet of paper.

Example
-------
>>> import matplotlib.pyplot as plt
>>> import paperplot as pp
>>> pp.use_paper_format(vertical_margin_cm=5, horizontal_margin_cm=5, height=0.4)
>>> fig, ax = plt.subplots()
>>> ax.plot([0, 1, 2], [0, 1, 4])
>>> pp.savefig("demo", directory="figures", fmt="png")
"""

from __future__ import annotations

from .config import (
    AVAILABLE_JOURNALS,
    AXES_LINEWIDTH,
    CM_PER_INCH,
    JOURNALS,
    LINE_LINEWIDTH,
    PAPER_SIZES_CM,
)
from .formatting import compute_figsize_cm, paper_format, use_paper_format
from .io import savefig

__all__ = [
    "use_paper_format",
    "paper_format",
    "compute_figsize_cm",
    "savefig",
    "AVAILABLE_JOURNALS",
    "JOURNALS",
    "AXES_LINEWIDTH",
    "LINE_LINEWIDTH",
    "CM_PER_INCH",
    "PAPER_SIZES_CM",
]

__version__ = "0.2.0"
