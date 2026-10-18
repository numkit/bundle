# graphics.export — deferred surface of saveas / exportgraphics / print

- **Status:** ✅ FIXED (`63b5fa4`)
- **Severity:** P3 (each item is a documented reference behaviour nk
  refuses with a clear error or renders in simplified form)
- **Kind:** stub
- **Found:** 2026-09-11, portion 32 close-out.

## What shipped (portion 32)

Engine-side renderer (`include/numkit/core/figure_render.hpp`
— display list + SVG, PDF, EPS, and RGB-raster backends, 5×7 bitmap font) behind
saveas / exportgraphics / print with the common argument forms (handle or
figure-number target, format flag `-dpng` / `-dpdf` / `-depsc`, `-r###` resolution, Name-Value
accept-and-ignore) writing `.svg`, `.pdf`, `.eps`, plus every image-toolbox raster format.

## Fixed

1. **Vector formats**: `.pdf` (`renderFigurePdf`) and `.eps` (`renderFigureEps`) implemented on top of `DisplayList`, including inline image rendering (`Cmd::IMAGE`).
2. **Rendered chart types**: `quiver` (auto-scaled arrows + arrowheads), `polarplot` / `polarscatter` / `polarhistogram` / `compass` (polar concentric circles, radial spokes, degree labels), and `yyaxis right` (secondary Y-axis range, right-side ticks/labels, and rotated secondary ylabel, plus side-scoped `prepareForPlot` preservation).

## Repro (self-contained)

```matlab
clear;
surf(peaks);
saveas(gcf, 's.pdf');
```

## References

- **Guard:** `DisplayTest.FigureExportGaps` (`modules/numkit/tests/gtest/builtins_test.cpp`)
