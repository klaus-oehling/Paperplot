# paperplot

Standardized, paper-ready [matplotlib](https://matplotlib.org/) formatting. Call
one function before you plot and every figure adopts a consistent academic style
(Computer Modern serif font, 600 dpi, thin axes) **and** a size derived from the
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
| `vertical_margin_cm` | `float` ≥ 0, `< page height` | *required* | Sum of top + bottom margins, in cm. 2.5 cm each → `5`. |
| `horizontal_margin_cm` | `float` ≥ 0, `< page width` | *required* | Sum of left + right margins, in cm. 2.5 cm each → `5`. |
| `height` | `float` in `(0, 1]` | `1.0` | Figure height as a fraction of the printable height. `1.0` = full height, `0.5` = half. |
| `width_split` | `1`, `2`, `3`, or `4` | `1` | Splits the printable width into equal columns. `1` = full width, `2` = half (two side by side), etc. |
| `usetex` | `bool` | `False` | `True` renders all text through a real LaTeX install (exact LaTeX output). `False` uses Computer Modern via matplotlib, no LaTeX needed. |
| `tight_view` | `bool` | `False` | `True` sets `axes.xmargin = 0` so the box hugs the data and a line starts at the box edge. `False` leaves the x-margin untouched. |
| `paper_size` | `"A4"`, `"A5"`, `"A3"`, `"LETTER"` | `"A4"` | The sheet the printable area is computed from. |

```python
# Full page height, full width, A4 (defaults)
pp.use_paper_format(5, 5)

# Two half-width figures, 30% height, tight x-axis
pp.use_paper_format(5, 5, height=0.3, width_split=2, tight_view=True)

# Exact LaTeX rendering on Letter paper
pp.use_paper_format(5, 5, height=0.5, usetex=True, paper_size="LETTER")
```

### `paper_format(...)` — context manager

Same arguments and behaviour as `use_paper_format`, but the previous matplotlib
settings are **restored on exit**. Use it when only some figures in a script
should be styled. Yields the figure size `(width_cm, height_cm)`.

```python
with pp.paper_format(5, 5, height=0.3, width_split=2, tight_view=True):
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
| `vertical_margin_cm` | `float` ≥ 0, `< page height` | *required* | Sum of top + bottom margins, in cm. |
| `horizontal_margin_cm` | `float` ≥ 0, `< page width` | *required* | Sum of left + right margins, in cm. |
| `height` | `float` in `(0, 1]` | `1.0` | Height as a fraction of the printable height. |
| `width_split` | `1`, `2`, `3`, or `4` | `1` | Number of equal columns the printable width is split into. |
| `paper_size` | `"A4"`, `"A5"`, `"A3"`, `"LETTER"` | `"A4"` | Sheet used for the calculation. |

```python
pp.compute_figsize_cm(5, 5, height=0.4, width_split=2)  # -> (8.0, 9.88)
```

### `savefig(...)`

Saves a figure with paper-ready defaults (tight layout, tight bounding box,
600 dpi). Creates the directory if needed and returns the written file path.

| Argument | Type / allowed values | Default | What it does |
| --- | --- | --- | --- |
| `name` | `str` | *required* | File name **without** extension. |
| `directory` | `str` | `"."` | Output directory; created if missing. |
| `fmt` | `"svg"` or `"png"` | `"svg"` | Output format and file extension. |
| `fig` | `Figure` or `None` | `None` | Figure to save; `None` uses the current figure (`plt.gcf()`). |
| `dpi` | `int` | `600` | Resolution for raster output (PNG). |
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
| `AXES_LINEWIDTH` | `0.7` | Reuse for manual elements (`axhline`, `grid`) so they match the styled axes. |
| `LINE_LINEWIDTH` | `0.9` | The data line width applied by the style. |
| `CM_PER_INCH` | `2.54` | The cm→inch conversion used internally. |
| `PAPER_SIZES_CM` | `dict` | Supported sheets and their `(width, height)` in cm: `A4`, `A5`, `A3`, `LETTER`. |

```python
ax.axhline(0, color="black", linestyle="--", linewidth=pp.AXES_LINEWIDTH)
```

## Fonts and LaTeX

The text font is **Computer Modern** (matplotlib's bundled `cmr10`), so figures
match the body font of a standard LaTeX document out of the box — no LaTeX
installation required. (`axes.unicode_minus` and `axes.formatter.use_mathtext`
are set as `cmr10` requires.)

Pass `usetex=True` for exact LaTeX typesetting (full LaTeX math, identical
kerning, the `amsfonts`/`amssymb` preamble). This requires a working LaTeX
installation. It is **off by default**.

## Style applied

| rcParam | Value |
| --- | --- |
| `font.family` / `font.serif` | `serif` / `cmr10` (Computer Modern) |
| `mathtext.fontset` | `cm` (Computer Modern) |
| `axes.unicode_minus` | `False` |
| `axes.formatter.use_mathtext` | `True` |
| `axes.titlesize` / `axes.labelsize` | 12 / 11 |
| `xtick.labelsize` / `ytick.labelsize` | 10 / 10 |
| `legend.fontsize` | 10 |
| `figure.dpi` / `savefig.dpi` | 600 / 600 |
| `lines.linewidth` | 0.9 |
| `axes.linewidth` | 0.7 |
| `axes.xmargin` | 0 only when `tight_view=True` |
| `text.usetex` | `False` (opt-in via `usetex=True`) |

## License

PolyForm Noncommercial License 1.0.0 — free for noncommercial use. See
[LICENSE](LICENSE).

Required Notice: Copyright Klaus Colletti Oehling
