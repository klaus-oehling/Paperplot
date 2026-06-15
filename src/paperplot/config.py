"""Constants and default style settings for :mod:`paperplot`.

All sizing is expressed in centimetres internally and converted to inches
(matplotlib's native unit for ``figure.figsize``) only when the rcParams are
applied.
"""

from __future__ import annotations

#: Centimetres per inch (matplotlib expresses figure sizes in inches).
CM_PER_INCH: float = 2.54

#: Physical dimensions of common paper sizes, ``(width_cm, height_cm)`` in
#: portrait orientation.
PAPER_SIZES_CM: dict[str, tuple[float, float]] = {
    "A4": (21.0, 29.7),
    "A5": (14.8, 21.0),
    "A3": (29.7, 42.0),
    "LETTER": (21.59, 27.94),
}

#: Default outline / axes line width (``axes.linewidth``), in points.
AXES_LINEWIDTH: float = 0.7

#: Default data line width (``lines.linewidth``), in points.
LINE_LINEWIDTH: float = 0.9

#: Base rcParams shared by every figure. Sizing keys (``figure.figsize``) and
#: LaTeX keys are added by :func:`paperplot.formatting.use_paper_format`.
#:
#: The font is Computer Modern, matplotlib's bundled ``cmr10``, so that text
#: matches the body font of a standard LaTeX document even when ``usetex`` is
#: off. ``axes.unicode_minus`` is disabled and ``axes.formatter.use_mathtext``
#: enabled because ``cmr10`` renders its minus sign through mathtext.
BASE_RCPARAMS: dict[str, object] = {
    "font.family": "serif",
    "font.serif": ["cmr10", "Computer Modern Roman", "DejaVu Serif"],
    "mathtext.fontset": "cm",
    "axes.unicode_minus": False,
    "axes.formatter.use_mathtext": True,
    "axes.titlesize": 12,
    "axes.labelsize": 11,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "lines.linewidth": LINE_LINEWIDTH,
    "axes.linewidth": AXES_LINEWIDTH,
}

#: x-axis margin applied when ``tight_view=True``: the box hugs the data range
#: exactly, so a plotted line starts where the axes box opens. When
#: ``tight_view`` is ``False`` the x-margin is left untouched (whatever the
#: caller or matplotlib's default ``0.05`` already provides).
TIGHT_AXIS_MARGIN: float = 0.0

#: LaTeX preamble injected when ``usetex=True``.
LATEX_PREAMBLE: str = r"""
\usepackage{amsfonts}
\usepackage{amssymb}
"""

#: Allowed values for the ``width_split`` argument.
ALLOWED_WIDTH_SPLITS: tuple[int, ...] = (1, 2, 3, 4)
