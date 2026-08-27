"""Apply standardized, paper-ready matplotlib formatting.

The public entry point is :func:`use_paper_format`, which configures
matplotlib's global ``rcParams`` so that any figure created afterwards adopts
a consistent academic style and a size derived from the printable area of a
sheet of paper.

A :func:`paper_format` context manager is also provided for callers who prefer
to scope the styling to a ``with`` block instead of mutating the global state.
"""

from __future__ import annotations

import contextlib
from typing import Iterator

import matplotlib as mpl
import matplotlib.pyplot as plt

from . import config


def compute_figsize_cm(
    vertical_margin_cm: float,
    horizontal_margin_cm: float,
    height: float = 1.0,
    width_split: int = 1,
    paper_size: str = "A4",
) -> tuple[float, float]:
    """Compute the figure size, in centimetres, for the given layout.

    The printable area of the sheet is the paper dimension minus the summed
    margins. The returned width fills the printable width (optionally divided
    into ``width_split`` equal columns) and the returned height is a fraction
    ``height`` of the printable height.

    Parameters
    ----------
    vertical_margin_cm:
        Sum of the top and bottom margins, in centimetres. For 2.5 cm on each
        side, pass ``5``.
    horizontal_margin_cm:
        Sum of the left and right margins, in centimetres. For 2.5 cm on each
        side, pass ``5``.
    height:
        Figure height as a fraction of the printable height, in the range
        ``(0, 1]``. With A4 and 5 cm of vertical margin, ``1.0`` maps to the
        full ``29.7 - 5 = 24.7`` cm and ``0.5`` to ``12.35`` cm.
    width_split:
        Number of equal columns the printable width is divided into. Must be
        one of ``1, 2, 3, 4``. ``1`` uses the full printable width.
    paper_size:
        Key into :data:`paperplot.config.PAPER_SIZES_CM` (e.g. ``"A4"``).

    Returns
    -------
    tuple[float, float]
        ``(width_cm, height_cm)`` of the figure.

    Raises
    ------
    ValueError
        If any argument is outside its valid range.
    """
    paper_key = paper_size.upper()
    if paper_key not in config.PAPER_SIZES_CM:
        valid = ", ".join(sorted(config.PAPER_SIZES_CM))
        raise ValueError(
            f"Unknown paper_size {paper_size!r}; expected one of: {valid}."
        )

    if not 0.0 < height <= 1.0:
        raise ValueError(
            f"height must be in the interval (0, 1]; got {height!r}."
        )

    if width_split not in config.ALLOWED_WIDTH_SPLITS:
        allowed = ", ".join(str(value) for value in config.ALLOWED_WIDTH_SPLITS)
        raise ValueError(
            f"width_split must be one of {allowed}; got {width_split!r}."
        )

    page_width_cm, page_height_cm = config.PAPER_SIZES_CM[paper_key]

    if not 0.0 <= horizontal_margin_cm < page_width_cm:
        raise ValueError(
            "horizontal_margin_cm must be in the interval "
            f"[0, {page_width_cm}); got {horizontal_margin_cm!r}."
        )
    if not 0.0 <= vertical_margin_cm < page_height_cm:
        raise ValueError(
            "vertical_margin_cm must be in the interval "
            f"[0, {page_height_cm}); got {vertical_margin_cm!r}."
        )

    printable_width_cm = page_width_cm - horizontal_margin_cm
    printable_height_cm = page_height_cm - vertical_margin_cm

    width_cm = printable_width_cm / width_split
    height_cm = printable_height_cm * height
    return width_cm, height_cm


def _build_rcparams(
    figsize_cm: tuple[float, float],
    usetex: bool,
    tight_view: bool,
) -> dict[str, object]:
    """Assemble the rcParams dictionary for the requested configuration."""
    width_cm, height_cm = figsize_cm
    rcparams: dict[str, object] = dict(config.BASE_RCPARAMS)
    rcparams["figure.figsize"] = (
        width_cm / config.CM_PER_INCH,
        height_cm / config.CM_PER_INCH,
    )
    if tight_view:
        # Only touch the x-margin when tightening; otherwise leave whatever the
        # caller (or matplotlib's default) already has in place.
        rcparams["axes.xmargin"] = config.TIGHT_AXIS_MARGIN
    rcparams["text.usetex"] = usetex
    if usetex:
        rcparams["text.latex.preamble"] = config.LATEX_PREAMBLE
    return rcparams


def use_paper_format(
    vertical_margin_cm: float,
    horizontal_margin_cm: float,
    height: float = 1.0,
    width_split: int = 1,
    *,
    usetex: bool = False,
    tight_view: bool = False,
    paper_size: str = "A4",
) -> tuple[float, float]:
    """Activate the standardized paper formatting on matplotlib's globals.

    Call this once before creating a figure. Every figure created afterwards
    inherits the academic style (serif fonts, Computer Modern mathtext,
    600 dpi, the configured line widths) and the size computed from the paper
    layout. The effect is global and persists until rcParams are changed again
    (e.g. via :func:`matplotlib.rcdefaults` or another call to this function).

    See :func:`compute_figsize_cm` for the meaning of the sizing arguments.

    Parameters
    ----------
    vertical_margin_cm, horizontal_margin_cm, height, width_split, paper_size:
        Forwarded to :func:`compute_figsize_cm`.
    usetex:
        When ``True``, render text with a system LaTeX installation and inject
        the ``amsfonts``/``amssymb`` preamble. Requires LaTeX to be installed.
        Defaults to ``False``; Computer Modern mathtext still renders ``$...$``
        math in a serif style without LaTeX.
    tight_view:
        When ``True``, set the x-axis margin to zero (``axes.xmargin = 0``) so
        the axes box hugs the data range exactly and a plotted line starts
        where the box opens, with no need to call ``xlim`` manually. When
        ``False`` (default), the x-margin is left untouched: any value already
        set by the caller is preserved, and otherwise matplotlib's usual 5%
        padding applies.

    Returns
    -------
    tuple[float, float]
        The applied figure size ``(width_cm, height_cm)`` in centimetres, for
        reference or logging.
    """
    figsize_cm = compute_figsize_cm(
        vertical_margin_cm=vertical_margin_cm,
        horizontal_margin_cm=horizontal_margin_cm,
        height=height,
        width_split=width_split,
        paper_size=paper_size,
    )
    plt.rcParams.update(_build_rcparams(figsize_cm, usetex, tight_view))
    return figsize_cm


@contextlib.contextmanager
def paper_format(
    vertical_margin_cm: float,
    horizontal_margin_cm: float,
    height: float = 1.0,
    width_split: int = 1,
    *,
    usetex: bool = False,
    tight_view: bool = False,
    paper_size: str = "A4",
) -> Iterator[tuple[float, float]]:
    """Scope the paper formatting to a ``with`` block.

    Identical configuration to :func:`use_paper_format` (including
    ``tight_view``), but the previous rcParams are restored on exit. Useful
    when only a subset of figures in a script should use the academic style.

    Yields
    ------
    tuple[float, float]
        The applied figure size ``(width_cm, height_cm)`` in centimetres.

    Examples
    --------
    >>> with paper_format(5, 5, height=0.4, tight_view=True):
    ...     fig, ax = plt.subplots()
    ...     ax.plot([0, 1], [0, 1])
    """
    figsize_cm = compute_figsize_cm(
        vertical_margin_cm=vertical_margin_cm,
        horizontal_margin_cm=horizontal_margin_cm,
        height=height,
        width_split=width_split,
        paper_size=paper_size,
    )
    with mpl.rc_context(_build_rcparams(figsize_cm, usetex, tight_view)):
        yield figsize_cm
