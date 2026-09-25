"""Apply standardized, paper-ready matplotlib formatting.

The public entry point is :func:`use_paper_format`, which configures
matplotlib's global ``rcParams`` so that any figure created afterwards adopts
a consistent academic style and a size derived from the printable area of a
sheet of paper.

A :func:`paper_format` context manager is also provided for callers who prefer
to scope the styling to a ``with`` block instead of mutating the global state.

Pass ``journal`` to switch the whole style to a publication template (see
:data:`paperplot.config.JOURNALS`); a journal may also supply the paper size
and margins, which the caller can still override explicitly.
"""

from __future__ import annotations

import contextlib
from typing import Iterator, Optional

import matplotlib as mpl
import matplotlib.pyplot as plt

from . import config


def _resolve_profile(journal: Optional[str]) -> dict[str, object]:
    """Return the style profile for ``journal`` (or the default profile).

    The returned dict has the keys ``rcparams``, ``paper_size``,
    ``vertical_margin_cm`` and ``horizontal_margin_cm``. For the default
    profile the three geometry values are ``None`` (no fixed page geometry).

    Raises
    ------
    ValueError
        If ``journal`` is not a known profile name.
    """
    if journal is None:
        return {
            "rcparams": config.DEFAULT_STYLE_RCPARAMS,
            "paper_size": None,
            "vertical_margin_cm": None,
            "horizontal_margin_cm": None,
        }

    match = {name.lower(): name for name in config.JOURNALS}.get(journal.lower())
    if match is None:
        valid = ", ".join(config.AVAILABLE_JOURNALS) or "(none)"
        raise ValueError(
            f"Unknown journal {journal!r}; available journals: {valid}."
        )
    return config.JOURNALS[match]


def _resolve_geometry(
    journal: Optional[str],
    vertical_margin_cm: Optional[float],
    horizontal_margin_cm: Optional[float],
    paper_size: Optional[str],
) -> tuple[dict[str, object], str, float, float]:
    """Resolve the profile and the effective paper size and margins.

    Explicit arguments take precedence over the journal's defaults, which in
    turn take precedence over the library default (A4, no fixed margins).
    """
    profile = _resolve_profile(journal)

    resolved_paper = (
        paper_size
        if paper_size is not None
        else profile["paper_size"] or "A4"
    )

    resolved_vertical = (
        vertical_margin_cm
        if vertical_margin_cm is not None
        else profile["vertical_margin_cm"]
    )
    resolved_horizontal = (
        horizontal_margin_cm
        if horizontal_margin_cm is not None
        else profile["horizontal_margin_cm"]
    )

    if resolved_vertical is None or resolved_horizontal is None:
        raise ValueError(
            "vertical_margin_cm and horizontal_margin_cm are required unless a "
            "journal that fixes them is given."
        )

    return profile, resolved_paper, resolved_vertical, resolved_horizontal


def _figsize_from_geometry(
    vertical_margin_cm: float,
    horizontal_margin_cm: float,
    height: float,
    width_split: int,
    paper_size: str,
) -> tuple[float, float]:
    """Validate the geometry and return the figure size in centimetres."""
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


def compute_figsize_cm(
    vertical_margin_cm: Optional[float] = None,
    horizontal_margin_cm: Optional[float] = None,
    height: float = 1.0,
    width_split: int = 1,
    paper_size: Optional[str] = None,
    journal: Optional[str] = None,
) -> tuple[float, float]:
    """Compute the figure size, in centimetres, for the given layout.

    The printable area of the sheet is the paper dimension minus the summed
    margins. The returned width fills the printable width (optionally divided
    into ``width_split`` equal columns) and the returned height is a fraction
    ``height`` of the printable height. This function only computes a size; it
    does not touch matplotlib.

    Parameters
    ----------
    vertical_margin_cm:
        Sum of the top and bottom margins, in centimetres. For 2.5 cm on each
        side, pass ``5``. May be omitted when ``journal`` fixes the margins.
    horizontal_margin_cm:
        Sum of the left and right margins, in centimetres. May be omitted when
        ``journal`` fixes the margins.
    height:
        Figure height as a fraction of the printable height, in the range
        ``(0, 1]``. With A4 and 5 cm of vertical margin, ``1.0`` maps to the
        full ``29.7 - 5 = 24.7`` cm and ``0.5`` to ``12.35`` cm.
    width_split:
        Number of equal columns the printable width is divided into. Must be
        one of ``1, 2, 3, 4``. ``1`` uses the full printable width.
    paper_size:
        One of :data:`paperplot.config.PAPER_SIZES_CM` (e.g. ``"A4"``). When
        ``None``, the journal's paper size is used, else ``"A4"``.
    journal:
        Name of a journal profile (see :data:`paperplot.config.JOURNALS`) whose
        paper size and margins are used as defaults.

    Returns
    -------
    tuple[float, float]
        ``(width_cm, height_cm)`` of the figure.

    Raises
    ------
    ValueError
        If any argument is outside its valid range, or the margins are missing
        and no journal supplies them.
    """
    _, paper, vertical, horizontal = _resolve_geometry(
        journal, vertical_margin_cm, horizontal_margin_cm, paper_size
    )
    return _figsize_from_geometry(vertical, horizontal, height, width_split, paper)


def _build_rcparams(
    profile: dict[str, object],
    figsize_cm: tuple[float, float],
    usetex: bool,
    tight_view: bool,
    lines_linewidth: float,
    axes_linewidth: float,
) -> dict[str, object]:
    """Assemble the rcParams dictionary for the requested configuration."""
    width_cm, height_cm = figsize_cm
    rcparams: dict[str, object] = dict(config.COMMON_RCPARAMS)
    rcparams.update(profile["rcparams"])
    rcparams["figure.figsize"] = (
        width_cm / config.CM_PER_INCH,
        height_cm / config.CM_PER_INCH,
    )
    rcparams["lines.linewidth"] = lines_linewidth
    rcparams["axes.linewidth"] = axes_linewidth
    # Keep the major tick marks the same weight as the axes spines.
    rcparams["xtick.major.width"] = axes_linewidth
    rcparams["ytick.major.width"] = axes_linewidth
    # Tie patch edges to the same weight. matplotlib has no legend-specific
    # line-width rcParam; the legend frame reads its border width from
    # ``patch.linewidth``, so setting it makes the legend box (and other patch
    # edges) match the spines and ticks.
    rcparams["patch.linewidth"] = axes_linewidth
    if tight_view:
        # Only touch the x-margin when tightening; otherwise leave whatever the
        # caller (or matplotlib's default) already has in place.
        rcparams["axes.xmargin"] = config.TIGHT_AXIS_MARGIN
    rcparams["text.usetex"] = usetex
    if usetex:
        rcparams["text.latex.preamble"] = config.LATEX_PREAMBLE
    return rcparams


def use_paper_format(
    vertical_margin_cm: Optional[float] = None,
    horizontal_margin_cm: Optional[float] = None,
    height: float = 1.0,
    width_split: int = 1,
    *,
    journal: Optional[str] = None,
    paper_size: Optional[str] = None,
    usetex: bool = False,
    tight_view: bool = False,
    lines_linewidth: Optional[float] = None,
    axes_linewidth: Optional[float] = None,
) -> tuple[float, float]:
    """Activate the standardized paper formatting on matplotlib's globals.

    Call this once before creating a figure. Every figure created afterwards
    inherits the style (fonts, sizes, line widths) and the size computed from
    the paper layout. The effect is global and persists until rcParams are
    changed again (e.g. via :func:`matplotlib.rcdefaults` or another call).

    See :func:`compute_figsize_cm` for the meaning of the sizing arguments.

    Parameters
    ----------
    vertical_margin_cm, horizontal_margin_cm, height, width_split, paper_size:
        Forwarded to :func:`compute_figsize_cm`. The two margins may be omitted
        when ``journal`` fixes them.
    journal:
        Name of a journal profile (see :data:`paperplot.config.JOURNALS`, e.g.
        ``"SBFin"``). It switches the fonts and font sizes to that template and
        supplies default paper size and margins. Explicit ``paper_size`` /
        margin arguments still override the journal's defaults. When ``None``
        (default), the Computer Modern style is used.
    usetex:
        When ``True``, render text with a system LaTeX installation and inject
        the ``amsfonts``/``amssymb`` preamble. Requires LaTeX to be installed.
        Defaults to ``False``. Note that ``usetex=True`` lets LaTeX choose the
        fonts, so a journal's ``font.serif`` / ``mathtext.fontset`` settings do
        not apply on that path.
    tight_view:
        When ``True``, set the x-axis margin to zero (``axes.xmargin = 0``) so
        the axes box hugs the data range exactly and a plotted line starts
        where the box opens. When ``False`` (default), the x-margin is left
        untouched.
    lines_linewidth:
        Data line width (``lines.linewidth``), in points. Defaults to
        :data:`paperplot.config.LINE_LINEWIDTH` (``0.9``) when ``None``.
    axes_linewidth:
        Axes / spine line width (``axes.linewidth``), in points. Defaults to
        :data:`paperplot.config.AXES_LINEWIDTH` (``0.7``) when ``None``. The
        major tick marks (``xtick.major.width`` / ``ytick.major.width``) and the
        patch edge width (``patch.linewidth``, which governs the legend box
        border and other patch edges) are set to the same value so they all
        match the spines.

    Returns
    -------
    tuple[float, float]
        The applied figure size ``(width_cm, height_cm)`` in centimetres.
    """
    profile, paper, vertical, horizontal = _resolve_geometry(
        journal, vertical_margin_cm, horizontal_margin_cm, paper_size
    )
    figsize_cm = _figsize_from_geometry(
        vertical, horizontal, height, width_split, paper
    )
    lines_lw = config.LINE_LINEWIDTH if lines_linewidth is None else lines_linewidth
    axes_lw = config.AXES_LINEWIDTH if axes_linewidth is None else axes_linewidth
    plt.rcParams.update(
        _build_rcparams(
            profile, figsize_cm, usetex, tight_view, lines_lw, axes_lw
        )
    )
    return figsize_cm


@contextlib.contextmanager
def paper_format(
    vertical_margin_cm: Optional[float] = None,
    horizontal_margin_cm: Optional[float] = None,
    height: float = 1.0,
    width_split: int = 1,
    *,
    journal: Optional[str] = None,
    paper_size: Optional[str] = None,
    usetex: bool = False,
    tight_view: bool = False,
    lines_linewidth: Optional[float] = None,
    axes_linewidth: Optional[float] = None,
) -> Iterator[tuple[float, float]]:
    """Scope the paper formatting to a ``with`` block.

    Identical configuration to :func:`use_paper_format` (including ``journal``
    and the line-width arguments), but the previous rcParams are restored on
    exit. Useful when only a subset of figures in a script should use the
    style.

    Yields
    ------
    tuple[float, float]
        The applied figure size ``(width_cm, height_cm)`` in centimetres.

    Examples
    --------
    >>> with paper_format(journal="SBFin", height=0.5, tight_view=True):
    ...     fig, ax = plt.subplots()
    ...     ax.plot([0, 1], [0, 1])
    """
    profile, paper, vertical, horizontal = _resolve_geometry(
        journal, vertical_margin_cm, horizontal_margin_cm, paper_size
    )
    figsize_cm = _figsize_from_geometry(
        vertical, horizontal, height, width_split, paper
    )
    lines_lw = config.LINE_LINEWIDTH if lines_linewidth is None else lines_linewidth
    axes_lw = config.AXES_LINEWIDTH if axes_linewidth is None else axes_linewidth
    with mpl.rc_context(
        _build_rcparams(profile, figsize_cm, usetex, tight_view, lines_lw, axes_lw)
    ):
        yield figsize_cm
