# Content images

Every content image a page shows is served as AVIF with a WebP fallback, in the responsive sizes `scripts/image-variants.py` generates. The original PNG/JPG/WebP stays in the repo as the source and is not referenced by the page. An image added in its original format reaches visitors at full weight: the 2026-10-24 conversion cut the case pages from 4.5 MB to 0.8 MB of images.

## Steps

1. Run `python scripts/image-variants.py <image>`. It writes the variants next to the source and prints the `srcset` values.
2. Write the markup using the patterns below. Keep the `<img>`'s `width`/`height` as the original's dimensions, plus its `alt`, `class`, `loading="lazy"` (anything below the fold) and `decoding="async"`.
3. Check layout: the image renders at the same position and size as with the original, at desktop (1440), tablet (1024) and mobile (412, 320). In the browser, `currentSrc` should end in `.avif`.

Done when every `<img>` and `<source>` on the page points at generated variants and the layout check passes at all four widths.

## Markup

Standalone image (two sizes). `sizes` is the width the image actually renders at: measure it.

```html
<picture class="img-sources">
  <source type="image/avif" srcset="x-800.avif 800w, x-1600.avif 1600w" sizes="(max-width: 768px) 88vw, 563px" />
  <img src="x-800.webp" srcset="x-800.webp 800w, x-1600.webp 1600w" sizes="(max-width: 768px) 88vw, 563px" width="1920" height="1200" loading="lazy" decoding="async" alt="…" />
</picture>
```

- `.img-sources` (in `global.css`) is `display: contents`, so the `<img>` stays the layout child of its grid or flex parent. A selector like `.parent > img` needs a twin, `.parent > .img-sources > img`, because selectors still see the `<picture>`.
- Single size (source ≤ 800 px): `<source type="image/avif" srcset="x-430.avif" />` and a plain `<img src="x-430.webp">`, with no `w` descriptors and no `sizes`.
- With `w` descriptors, the image's intrinsic width becomes the `sizes` value. Images styled with `width: auto` (Harmony evidence) then render at that width instead of their real one. For those, set `sizes` to the original's natural width in px, so `max-width: 100%` caps it as before.
- Art direction (an existing `<picture>` with `<source media=…>`) gets one AVIF and one WebP `<source>` per media query.

Out of scope: the About photo (`index.html`, already AVIF/WebP) and video posters (`poster` takes a single URL; keep it WebP).
