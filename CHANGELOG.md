# Changelog

All notable changes to this project are documented in this file. The format is
based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this
project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-09-25

### Added

- `journal` argument on `use_paper_format`, `paper_format`, and
  `compute_figsize_cm`, selecting a publication template that sets fonts, font
  sizes, and default paper size and margins. First template: **SBFin**
  (Sociedade Brasileira de Finanças) — A5, 2 cm margins, Nimbus Roman / Times
  fonts, STIX math, sizes 9/8/7/7/7.
- `lines_linewidth` and `axes_linewidth` arguments on `use_paper_format` and
  `paper_format` to override the data and axes line widths (defaults 0.9 / 0.7).
- Exported `AVAILABLE_JOURNALS` and `JOURNALS`.
- `tight_view` argument on `use_paper_format` and `paper_format`: sets
  `axes.xmargin = 0` so the axes box hugs the data range and plotted lines start
  exactly where the box opens, removing the default 5% x-padding.

### Changed

- `vertical_margin_cm` and `horizontal_margin_cm` are now optional when a
  `journal` supplies them; explicit values still override the journal defaults.
- Text font is now Computer Modern (`cmr10`) by default, matching a standard
  LaTeX document even when `usetex=False`. Added `axes.unicode_minus = False`
  and `axes.formatter.use_mathtext = True`, which `cmr10` requires.
- License changed from MIT to PolyForm Noncommercial License 1.0.0
  (Copyright Klaus Colletti Oehling).

## [0.1.0] - 2026-06-14

### Added

- `use_paper_format` to apply standardized academic matplotlib styling with a
  figure size derived from paper margins, height fraction, and width split.
- `paper_format` context manager equivalent that restores previous rcParams.
- `compute_figsize_cm` for computing figure dimensions without side effects.
- `savefig` helper supporting SVG and PNG output at 300 dpi.
- Exported style constants (`AXES_LINEWIDTH`, `LINE_LINEWIDTH`, `CM_PER_INCH`,
  `PAPER_SIZES_CM`).
