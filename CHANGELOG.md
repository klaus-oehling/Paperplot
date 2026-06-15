# Changelog

All notable changes to this project are documented in this file. The format is
based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this
project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `tight_view` argument on `use_paper_format` and `paper_format`: sets
  `axes.xmargin = 0` so the axes box hugs the data range and plotted lines start
  exactly where the box opens, removing the default 5% x-padding.

### Changed

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
