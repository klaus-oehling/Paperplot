"""Tests for paperplot sizing and rcParams configuration."""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")  # headless backend for tests

import matplotlib.pyplot as plt
import pytest

import paperplot as pp
from paperplot import config
from paperplot.formatting import compute_figsize_cm


# --- sizing math -----------------------------------------------------------


def test_full_area_a4_default_margins():
    width_cm, height_cm = compute_figsize_cm(
        vertical_margin_cm=5, horizontal_margin_cm=5, height=1.0, width_split=1
    )
    assert width_cm == pytest.approx(16.0)  # 21 - 5
    assert height_cm == pytest.approx(24.7)  # 29.7 - 5


def test_height_fraction_scales_height_only():
    width_cm, height_cm = compute_figsize_cm(5, 5, height=0.5, width_split=1)
    assert width_cm == pytest.approx(16.0)
    assert height_cm == pytest.approx(12.35)  # 24.7 * 0.5


@pytest.mark.parametrize(
    "split, expected_width",
    [(1, 16.0), (2, 8.0), (3, 16.0 / 3.0), (4, 4.0)],
)
def test_width_split_divides_printable_width(split, expected_width):
    width_cm, _ = compute_figsize_cm(5, 5, height=1.0, width_split=split)
    assert width_cm == pytest.approx(expected_width)


def test_asymmetric_margins():
    width_cm, height_cm = compute_figsize_cm(
        vertical_margin_cm=4, horizontal_margin_cm=6, height=1.0
    )
    assert width_cm == pytest.approx(15.0)  # 21 - 6
    assert height_cm == pytest.approx(25.7)  # 29.7 - 4


# --- validation ------------------------------------------------------------


@pytest.mark.parametrize("height", [0.0, -0.1, 1.01, 2.0])
def test_invalid_height_raises(height):
    with pytest.raises(ValueError):
        compute_figsize_cm(5, 5, height=height)


@pytest.mark.parametrize("split", [0, 5, -1, 1.5])
def test_invalid_width_split_raises(split):
    with pytest.raises(ValueError):
        compute_figsize_cm(5, 5, width_split=split)


def test_margin_exceeding_page_raises():
    with pytest.raises(ValueError):
        compute_figsize_cm(vertical_margin_cm=30, horizontal_margin_cm=5)
    with pytest.raises(ValueError):
        compute_figsize_cm(vertical_margin_cm=5, horizontal_margin_cm=25)


def test_unknown_paper_size_raises():
    with pytest.raises(ValueError):
        compute_figsize_cm(5, 5, paper_size="B7")


# --- rcParams application --------------------------------------------------


def test_use_paper_format_sets_figsize_in_inches():
    returned = pp.use_paper_format(5, 5, height=1.0)
    width_in, height_in = plt.rcParams["figure.figsize"]
    assert width_in == pytest.approx(16.0 / config.CM_PER_INCH)
    assert height_in == pytest.approx(24.7 / config.CM_PER_INCH)
    assert returned == pytest.approx((16.0, 24.7))


def test_use_paper_format_sets_style_keys():
    pp.use_paper_format(5, 5)
    assert plt.rcParams["font.family"] == ["serif"]
    assert plt.rcParams["font.serif"][0] == "cmr10"
    assert plt.rcParams["mathtext.fontset"] == "cm"
    assert plt.rcParams["axes.linewidth"] == pytest.approx(config.AXES_LINEWIDTH)
    assert plt.rcParams["lines.linewidth"] == pytest.approx(config.LINE_LINEWIDTH)
    assert plt.rcParams["figure.dpi"] == 600


# --- linewidth overrides ---------------------------------------------------


def test_linewidth_defaults():
    pp.use_paper_format(5, 5)
    assert plt.rcParams["lines.linewidth"] == pytest.approx(0.9)
    assert plt.rcParams["axes.linewidth"] == pytest.approx(0.7)


def test_linewidth_overrides():
    pp.use_paper_format(5, 5, lines_linewidth=1.5, axes_linewidth=1.1)
    assert plt.rcParams["lines.linewidth"] == pytest.approx(1.5)
    assert plt.rcParams["axes.linewidth"] == pytest.approx(1.1)


# --- journal profiles ------------------------------------------------------


def test_sbfin_geometry_from_journal():
    # A5 (14.8 x 21) minus 4 cm margins each way -> 10.8 wide x 17 tall.
    size = pp.use_paper_format(journal="SBFin")
    assert size == pytest.approx((10.8, 17.0))


def test_sbfin_sets_fonts_and_sizes():
    pp.use_paper_format(journal="SBFin")
    assert plt.rcParams["font.serif"][0] == "Nimbus Roman No9 L"
    assert plt.rcParams["mathtext.fontset"] == "stix"
    assert plt.rcParams["axes.titlesize"] == pytest.approx(9)
    assert plt.rcParams["axes.labelsize"] == pytest.approx(8)
    assert plt.rcParams["xtick.labelsize"] == pytest.approx(7)
    assert plt.rcParams["ytick.labelsize"] == pytest.approx(7)
    assert plt.rcParams["legend.fontsize"] == pytest.approx(7)


def test_journal_is_case_insensitive():
    assert pp.use_paper_format(journal="sbfin") == pytest.approx((10.8, 17.0))


def test_unknown_journal_raises():
    with pytest.raises(ValueError):
        pp.use_paper_format(journal="Nature")


def test_explicit_args_override_journal():
    # Override the journal's A5/4cm defaults with A4/5cm.
    size = pp.use_paper_format(
        vertical_margin_cm=5, horizontal_margin_cm=5,
        journal="SBFin", paper_size="A4",
    )
    assert size == pytest.approx((16.0, 24.7))
    # Fonts still come from the journal.
    assert plt.rcParams["mathtext.fontset"] == "stix"


def test_missing_margins_without_journal_raises():
    with pytest.raises(ValueError):
        pp.use_paper_format()  # no margins, no journal
    with pytest.raises(ValueError):
        compute_figsize_cm(vertical_margin_cm=5)  # only one margin


def test_usetex_default_off():
    pp.use_paper_format(5, 5)
    assert plt.rcParams["text.usetex"] is False


def test_tight_view_false_leaves_xmargin_untouched():
    # A custom x-margin set beforehand must survive when tight_view is False.
    plt.rcParams["axes.xmargin"] = 0.12
    pp.use_paper_format(5, 5, tight_view=False)
    assert plt.rcParams["axes.xmargin"] == pytest.approx(0.12)
    matplotlib.rcdefaults()


def test_tight_view_zeroes_xmargin():
    pp.use_paper_format(5, 5, tight_view=True)
    assert plt.rcParams["axes.xmargin"] == pytest.approx(config.TIGHT_AXIS_MARGIN)


def test_tight_view_in_context_manager():
    with pp.paper_format(5, 5, tight_view=True):
        assert plt.rcParams["axes.xmargin"] == pytest.approx(config.TIGHT_AXIS_MARGIN)


def test_context_manager_restores_state():
    matplotlib.rcdefaults()
    original = tuple(plt.rcParams["figure.figsize"])
    with pp.paper_format(5, 5, height=0.4) as size:
        assert size == pytest.approx((16.0, 24.7 * 0.4))
        assert plt.rcParams["font.family"] == ["serif"]
    assert tuple(plt.rcParams["figure.figsize"]) == original


# --- savefig ---------------------------------------------------------------


@pytest.mark.parametrize("fmt", ["svg", "png"])
def test_savefig_writes_file(tmp_path, fmt):
    pp.use_paper_format(5, 5, height=0.3)
    fig, ax = plt.subplots()
    ax.plot([0, 1, 2], [0, 1, 4])
    path = pp.savefig("demo", directory=str(tmp_path), fmt=fmt)
    assert path.endswith(f"demo.{fmt}")
    assert (tmp_path / f"demo.{fmt}").exists()


def test_savefig_rejects_bad_format(tmp_path):
    pp.use_paper_format(5, 5)
    fig, ax = plt.subplots()
    with pytest.raises(ValueError):
        pp.savefig("demo", directory=str(tmp_path), fmt="pdf")
    plt.close(fig)
