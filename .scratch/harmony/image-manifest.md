# Harmony foundation image manifest

Ticket [01](issues/01-fundamentos-compartilhados.md), 2026-10-24. Originals remain unchanged. [image-manifest.json](image-manifest.json) records every source identity/hash, original size, crop rectangle, destination coordinate, resulting size, format, and byte size. Reproduce from the repository root with `python .scratch/harmony/prepare-foundation-images.py` (existing Pillow installation).

Every original is 1920 × 1200. All derivatives are lossless optimized RGB PNG, with no resizing, sharpening, generated text, UI reconstruction, or edits to source values. The original captures already contain softened raster text. Lossless output avoids adding compression artifacts; total delivered derivatives are about 215 KB. The wide variables image uses the unchanged original.

| Source | Derivative in `assets/images/harmony/editorial/` | Output | Purpose and retained context |
| --- | --- | --- | --- |
| `color=primitives.png` | `primitive-primary-secondary-scales.png` | 1360 × 548 | Complete Primary and Secondary rows, their names, descriptions, ten values per row, and swatches. Removes broad empty margins, the unverified token-count heading, and the incomplete Tertiary row. Wide layout from 1025 px. |
| `color=primitives.png` | `primitive-selected-light-steps-mobile.png` | 296 × 480 | Two source selections with the Primary/Secondary names and their two lightest values, 50 and 100. The name fragments omit the longer use descriptions so no label is cut mid-word. This is explicitly a selection of steps, not a complete scale/palette. |
| `semantic-tokerns.png` | `semantic-surface-border-roles.png` | 1440 × 554 | Complete Surface and Border rows with nine named roles each. Removes count/alias assertions from the source heading and the incomplete Content row, whose AA wording is not evidence of compliance. |
| `semantic-tokerns.png` | `semantic-default-soft-roles-mobile.png` | 344 × 508 | Surface and Border labels with the complete Default and Soft swatches/labels from each. Retains naming by use; source use descriptions are deliberately omitted, not clipped. Does not imply an alias mapping to primitive values. |
| `variables.png` | `responsive-mode-selections-mobile.png` | 467 × 1520 | Three source panels in Desktop/Tablet/Mobile order, separated by dark gutters. Each pairs the same original Name column with one source mode column; retains ScreenSize 1440/768/390 and Gap Lighter/Soft/Default. The repeated Name column is a documented editorial juxtaposition, not the original application layout. Wider screens show the unchanged original, including the Gap/Padding/Radius/Icons group context. |

The mobile derivatives assemble source fragments into one image per evidence row. This is necessary to retain legible original labels at 320 px without a gallery, raw-image link, horizontal scrolling, or fabricated interface. Pixel values inside the crop fragments are copied unchanged. No source pixels are enlarged during preparation or presentation. Gutters separate excerpts, and the page captions explain the selections. These selections also serve tablets at their natural maximum widths; above 1024 px, fuller rows/table retain the relationships across scales and modes. At 768 px a full board reduced the source labels too far, so generous empty space around the focused selections is intentional.

For the exact rectangles of every fragment, use the adjacent JSON rather than inferring coordinates from a rendered screenshot. PNG was chosen for these small text-heavy excerpts after visual inspection; there is no lossy quality parameter. The mobile two-step color selection is intentionally limited to lighter steps; the wider source selection shows the full light-to-dark progression.

Other Harmony sources, including the old organization pair, stay in the repository. They are not rendered as foundation evidence. No additional assets for tickets 02–04 were prepared.

## Ticket 03 — template composition (2026-10-24)

This appended slice preserves the foundation record above. [template-image-manifest.json](template-image-manifest.json) owns the two template entries separately to avoid concurrent writes to the foundation JSON. It records full paths, source/derivative SHA-256 hashes, dimensions, byte sizes, crop rectangles, paste coordinates, background, format and retained context. Reproduce with `python .scratch/harmony/prepare-template-images.py`.

Original: `assets/images/harmony/templates.png`, 1920 × 1200. Inspected before cropping and preserved byte-for-byte. Both derivatives are optimized, lossless RGB PNG with unchanged source pixels: no resizing, sharpening, text replacement, generated interface, or recovery of absent detail.

| Derivative in `assets/images/harmony/editorial/` | Output | Crop and purpose |
| --- | --- | --- |
| `template-compositions-configuration-wide.png` | 1826 × 892 | Source rectangle `(80,108,1906,1000)`. Retains the form/list/loading compositions, selected success layout and adjacent Success configuration panel in their original spatial relationship. Removes only surrounding chrome/canvas. Preserves the profile switch, breadcrumb level, alert, row options and column/label settings. Used above 1024 px as a wide block. |
| `template-card-success-configuration-mobile.png` | 296 × 1012 | Three unchanged excerpts separated by dark gutters: List/CardView `(96,508,386,744)` at `(3,0)`; selected success layout including selection boundary `(812,540,1108,772)` at `(0,260)`; Success configuration through Row06 `(1634,108,1906,604)` at `(12,516)`. Keeps two different page compositions and the selected layout's configuration at useful source scale. Used through 1024 px, at no more than natural width. |

The narrow image is an editorial juxtaposition, explicitly described by its caption/alternative, rather than a claim that these excerpts were adjacent in Figma. The wider image retains the original composition and configuration relationship. The argument concerns layout structure and design configuration, not reading every tiny label in the page examples. PNG avoids additional lossy artifacts in text-heavy source selections. One `picture`/`img` renders one evidence; there are no raw-image links or controls. Exact hashes and byte sizes are in the slice JSON.
