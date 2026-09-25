"""Constants and style profiles for :mod:`paperplot`.

All sizing is expressed in centimetres internally and converted to inches
(matplotlib's native unit for ``figure.figsize``) only when the rcParams are
applied.

A *style profile* bundles the font and font-size rcParams for a given look,
plus optional page geometry defaults (paper size and fixed margins). The
default profile reproduces a standard LaTeX / Computer Modern document. Named
*journal* profiles (see :data:`JOURNALS`) target a specific publication
template and may also fix the paper size and margins.
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

#: Default outline / axes line width (``axes.linewidth``), in points. Used when
#: the caller does not pass ``axes_linewidth``.
AXES_LINEWIDTH: float = 0.7

#: Default data line width (``lines.linewidth``), in points. Used when the
#: caller does not pass ``lines_linewidth``.
LINE_LINEWIDTH: float = 0.9

#: rcParams shared by every figure regardless of profile.
COMMON_RCPARAMS: dict[str, object] = {
    "figure.dpi": 300,
    "savefig.dpi": 300,
}

#: Font and font-size rcParams for the default (Computer Modern) look.
#:
#: The font is Computer Modern, matplotlib's bundled ``cmr10``, so that text
#: matches the body font of a standard LaTeX document even when ``usetex`` is
#: off. ``axes.unicode_minus`` is disabled and ``axes.formatter.use_mathtext``
#: enabled because ``cmr10`` renders its minus sign through mathtext.
DEFAULT_STYLE_RCPARAMS: dict[str, object] = {
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
}

#: Named journal profiles. Each maps to a dict with:
#:   ``rcparams``            - font and font-size rcParams for the template,
#:   ``paper_size``          - default paper size (may be overridden),
#:   ``vertical_margin_cm``  - default summed top+bottom margin,
#:   ``horizontal_margin_cm``- default summed left+right margin.
#:
#: SBFin (Sociedade Brasileira de Finanças): body text is Nimbus Roman No9 L
#: (URW's free, metric-compatible clone of Times / Times New Roman); the
#: fallback list lets matplotlib pick whichever Times-like face is installed.
#: Math uses the ``stix`` fontset, a Times-metric-compatible math font with
#: full symbol coverage — the closest match to the template's ``mathptmx``
#: math. The template is set on A5 with 2 cm margins on all four sides (summed
#: to 4 cm vertical and 4 cm horizontal).
JOURNALS: dict[str, dict[str, object]] = {
    "SBFin": {
        "rcparams": {
            "font.family": "serif",
            "font.serif": [
                "Nimbus Roman No9 L",
                "Times New Roman",
                "Times",
                "Liberation Serif",
            ],
            "mathtext.fontset": "stix",
            "axes.unicode_minus": False,
            "axes.formatter.use_mathtext": True,
            "axes.titlesize": 9,
            "axes.labelsize": 8,
            "xtick.labelsize": 7,
            "ytick.labelsize": 7,
            "legend.fontsize": 7,
        },
        "paper_size": "A5",
        "vertical_margin_cm": 4.0,
        "horizontal_margin_cm": 4.0,
    },
}

#: Names of the available journal profiles.
AVAILABLE_JOURNALS: tuple[str, ...] = tuple(JOURNALS)

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
