# paperplot

Standardized, paper-ready [matplotlib](https://matplotlib.org/) formatting. Call
one function before you plot and every figure adopts a consistent academic style
(Computer Modern serif font, 300 dpi, thin axes) **and** a size derived from the
printable area of your page — so figures drop into a LaTeX or Word document at
exactly the intended physical size, with no rescaling.

## Installation

Install directly from GitHub:

```bash
pip install git+https://github.com/klaus-oehling/Paperplot.git
```

Then import it as `paperplot`:

```python
import paperplot as pp
```

Requires Python 3.9+ and matplotlib 3.5+ (installed automatically). LaTeX
rendering (`usetex=True`) is optional and needs a system LaTeX installation
(e.g. TeX Live or MiKTeX).

## Quick start

```python
import matplotlib.pyplot as plt
import paperplot as pp

# A4, 2.5 cm margins all around (summed: 5 cm vertical, 5 cm horizontal),
# figure = 40% of the printable height, full printable width.
pp.use_paper_format(vertical_margin_cm=5, horizontal_margin_cm=5, height=0.4)

fig, ax = plt.subplots()
ax.plot([0, 1, 2], [0, 1, 4])
ax.set_ylabel(r"$f(x)$")

pp.savefig("demo", directory="figures", fmt="png")
```

## How sizing works

The figure is sized from the **printable area** = paper size − margins.

For A4 (21 × 29.7 cm) with 2.5 cm on each side:

- Printable width = 21 − 5 = **16 cm**
- Printable height = 29.7 − 5 = **24.7 cm**

From there, `height` scales the height and `width_split` divides the width.
Margins are passed as **summed** values (top + bottom, and left + right), so
2.5 cm on all four sides means `vertical_margin_cm=5` and
`horizontal_margin_cm=5`. Asymmetric margins work too — just pass the sums.

## Functions

### `use_paper_format(...)`

Activates the formatting on matplotlib's **global** settings. Call it once
before creating figures; every figure made afterwards uses the style until the
settings are changed again. Returns the applied figure size `(width_cm, height_cm)`.

| Argument | Type / allowed values | Default | What it does |
| --- | --- | --- | --- |
| `vertical_margin_cm` | `float` ≥ 0, `< page height` | *required*¹ | Sum of top + bottom margins, in cm. 2.5 cm each → `5`. |
| `horizontal_margin_cm` | `float` ≥ 0, `< page width` | *required*¹ | Sum of left + right margins, in cm. 2.5 cm each → `5`. |
| `height` | `float` in `(0, 1]` | `1.0` | Figure height as a fraction of the printable height. `1.0` = full height, `0.5` = half. |
| `width_split` | `1`, `2`, `3`, or `4` | `1` | Splits the printable width into equal columns. `1` = full width, `2` = half (two side by side), etc. |
| `journal` | `"SBFin"` or `None` | `None` | Applies a publication template — fonts, sizes, and default paper/margins (see [Journal templates](#journal-templates)). `None` = the Computer Modern style. |
| `paper_size` | `"A4"`, `"A5"`, `"A3"`, `"LETTER"`, or `None` | `None` | The sheet the printable area is computed from. `None` uses the journal's paper size, else `A4`. |
| `usetex` | `bool` | `False` | `True` renders all text through a real LaTeX install (exact LaTeX output). `False` uses matplotlib fonts, no LaTeX needed. |
| `tight_view` | `bool` | `False` | `True` sets `axes.xmargin = 0` so the box hugs the data and a line starts at the box edge. `False` leaves the x-margin untouched. |
| `lines_linewidth` | `float` or `None` | `None` → `0.9` | Data line width (`lines.linewidth`), in points. |
| `axes_linewidth` | `float` or `None` | `None` → `0.7` | Axes / spine line width (`axes.linewidth`), in points. |

¹ The two margins are required **unless** a `journal` that fixes them is given.
When both a journal and explicit margins are supplied, the explicit values win.

```python
# Full page height, full width, A4 (defaults)
pp.use_paper_format(5, 5)

# Two half-width figures, 30% height, tight x-axis
pp.use_paper_format(5, 5, height=0.3, width_split=2, tight_view=True)

# Thicker data and axes lines
pp.use_paper_format(5, 5, lines_linewidth=1.2, axes_linewidth=1.0)

# Journal template — A5, 2 cm margins and fonts come from the template
pp.use_paper_format(journal="SBFin", height=0.5)

# Exact LaTeX rendering on Letter paper
pp.use_paper_format(5, 5, height=0.5, usetex=True, paper_size="LETTER")
```

### `paper_format(...)` — context manager

Same arguments and behaviour as `use_paper_format` (including `journal`,
`lines_linewidth`, and `axes_linewidth`), but the previous matplotlib settings
are **restored on exit**. Use it when only some figures in a script should be
styled. Yields the figure size `(width_cm, height_cm)`.

```python
with pp.paper_format(journal="SBFin", height=0.3, width_split=2, tight_view=True):
    fig, ax = plt.subplots()
    ax.plot([0, 1, 2], [0, 1, 4])
    pp.savefig("inside", directory="figures")
# matplotlib settings are back to normal here
```

### `compute_figsize_cm(...)`

Returns the `(width_cm, height_cm)` that would be applied, **without** touching
matplotlib. Useful for checking or reporting sizes.

| Argument | Type / allowed values | Default | What it does |
| --- | --- | --- | --- |
| `vertical_margin_cm` | `float` ≥ 0, `< page height` | *required*¹ | Sum of top + bottom margins, in cm. |
| `horizontal_margin_cm` | `float` ≥ 0, `< page width` | *required*¹ | Sum of left + right margins, in cm. |
| `height` | `float` in `(0, 1]` | `1.0` | Height as a fraction of the printable height. |
| `width_split` | `1`, `2`, `3`, or `4` | `1` | Number of equal columns the printable width is split into. |
| `paper_size` | `"A4"`, `"A5"`, `"A3"`, `"LETTER"`, or `None` | `None` | Sheet used for the calculation. `None` uses the journal's, else `A4`. |
| `journal` | `"SBFin"` or `None` | `None` | Uses the journal's paper size and margins as defaults. |

¹ Required unless a `journal` that fixes them is given.

```python
pp.compute_figsize_cm(5, 5, height=0.4, width_split=2)  # -> (8.0, 9.88)
pp.compute_figsize_cm(journal="SBFin")                  # -> (10.8, 17.0)
```

### `savefig(...)`

Saves a figure with paper-ready defaults (tight layout, tight bounding box,
300 dpi). Creates the directory if needed and returns the written file path.

| Argument | Type / allowed values | Default | What it does |
| --- | --- | --- | --- |
| `name` | `str` | *required* | File name **without** extension. |
| `directory` | `str` | `"."` | Output directory; created if missing. |
| `fmt` | `"svg"` or `"png"` | `"svg"` | Output format and file extension. |
| `fig` | `Figure` or `None` | `None` | Figure to save; `None` uses the current figure (`plt.gcf()`). |
| `dpi` | `int` | `300` | Resolution for raster output (PNG). |
| `tight_layout` | `bool` | `True` | Call `fig.tight_layout()` before saving. |
| `bbox_inches` | `str` or `None` | `"tight"` | `"tight"` trims surrounding whitespace. |
| `transparent` | `bool` | `False` | Transparent background. |
| `close` | `bool` | `True` | Close the figure after saving (frees memory). |

```python
pp.savefig("plot")                                  # ./plot.svg
pp.savefig("plot", directory="figures", fmt="png")  # figures/plot.png
pp.savefig("plot", fmt="png", transparent=True, close=False)
```

### Constants

Importable from the top level (`pp.AXES_LINEWIDTH`, etc.):

| Constant | Value | Use |
| --- | --- | --- |
| `AXES_LINEWIDTH` | `0.7` | Default axes line width; reuse for manual elements (`axhline`, `grid`) so they match. |
| `LINE_LINEWIDTH` | `0.9` | Default data line width. |
| `CM_PER_INCH` | `2.54` | The cm→inch conversion used internally. |
| `PAPER_SIZES_CM` | `dict` | Supported sheets and their `(width, height)` in cm: `A4`, `A5`, `A3`, `LETTER`. |
| `AVAILABLE_JOURNALS` | `tuple` | Names of the available journal templates, e.g. `("SBFin",)`. |
| `JOURNALS` | `dict` | The full journal template definitions (fonts, sizes, paper, margins). |

```python
ax.axhline(0, color="black", linestyle="--", linewidth=pp.AXES_LINEWIDTH)
```

## Journal templates

Pass `journal="..."` to switch the whole style to a publication template. The
template sets the fonts and font sizes, and supplies a default paper size and
margins (which you can still override with explicit arguments). `height`,
`width_split`, `tight_view`, and the line widths work exactly as usual.

```python
pp.use_paper_format(journal="SBFin", height=0.5)   # A5, 2 cm margins, Times-like fonts
```

Available templates (`pp.AVAILABLE_JOURNALS`):

**SBFin** — Sociedade Brasileira de Finanças.

| Setting | Value |
| --- | --- |
| Paper size | `A5` |
| Margins | 2 cm all sides (summed: 4 cm vertical, 4 cm horizontal) |
| `font.serif` | `Nimbus Roman No9 L`, then `Times New Roman`, `Times`, `Liberation Serif` |
| `mathtext.fontset` | `stix` |
| `axes.titlesize` | 9 |
| `axes.labelsize` | 8 |
| `xtick.labelsize` / `ytick.labelsize` | 7 / 7 |
| `legend.fontsize` | 7 |

The body font is Nimbus Roman No9 L — URW's free, metric-compatible clone of
Times / Times New Roman (TeX distributions can't ship the actual Microsoft
font). The fallback list lets matplotlib pick whichever Times-like face is
installed on your system. Math uses the STIX fontset, a Times-metric-compatible
math font with full symbol coverage — the closest built-in match to the
template's `mathptmx` math, and coherent with the Times-like body text.

## Fonts and LaTeX

The text font is **Computer Modern** (matplotlib's bundled `cmr10`), so figures
match the body font of a standard LaTeX document out of the box — no LaTeX
installation required. (`axes.unicode_minus` and `axes.formatter.use_mathtext`
are set as `cmr10` requires.)

Pass `usetex=True` for exact LaTeX typesetting (full LaTeX math, identical
kerning, the `amsfonts`/`amssymb` preamble). This requires a working LaTeX
installation. It is **off by default**. Note that with `usetex=True`, LaTeX
chooses the fonts, so a journal's `font.serif` / `mathtext.fontset` settings do
not take effect on that path.

Selecting a `journal` replaces the fonts and sizes with that template's — see
[Journal templates](#journal-templates).

## Style applied (default profile)

These are the values for the default (Computer Modern) profile; a `journal`
overrides the font and size rows.

| rcParam | Value |
| --- | --- |
| `font.family` / `font.serif` | `serif` / `cmr10` (Computer Modern) |
| `mathtext.fontset` | `cm` (Computer Modern) |
| `axes.unicode_minus` | `False` |
| `axes.formatter.use_mathtext` | `True` |
| `axes.titlesize` / `axes.labelsize` | 12 / 11 |
| `xtick.labelsize` / `ytick.labelsize` | 10 / 10 |
| `legend.fontsize` | 10 |
| `figure.dpi` / `savefig.dpi` | 300 / 300 |
| `lines.linewidth` | 0.9 (override with `lines_linewidth`) |
| `axes.linewidth` | 0.7 (override with `axes_linewidth`) |
| `axes.xmargin` | 0 only when `tight_view=True` |
| `text.usetex` | `False` (opt-in via `usetex=True`) |

## License

PolyForm Noncommercial License 1.0.0 — free for noncommercial use. See
[LICENSE](LICENSE).

Required Notice: Copyright Klaus Colletti Oehling
