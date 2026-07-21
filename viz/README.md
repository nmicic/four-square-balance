# Visualization

Both pages show the same object — the canonical four-square decomposition and the
gap-record rays — in the **Helmert shape 3-space**. For every n, the most-balanced
representation

    n = x^2 + y^2 + z^2 + w^2,   x >= y >= z >= w >= 0

is a lattice point on the sphere of radius sqrt(n) in R^4. The equal-parts diagonal
`(1,1,1,1)` is split off and what remains is projected to 3D with the
orthonormal Helmert basis:

    s1 = (x - y)/sqrt(2)
    s2 = (x + y - 2z)/sqrt(6)
    s3 = (x + y + z - 3w)/sqrt(12)

The origin is the equal-parts point (`x=y=z=w`). The direction records the
imbalance shape, while the viewer uses a display-scaled radius so the rays remain
legible. The OEIS statistic is still the balance gap `x - ceil(sqrt(n/4))`; the
shape-space position is supporting geometry.

## Two viewers

There are two viewer pages — `index.html` and `fsq4d.html`. They render the *same*
shape space but differ in how they get their points and what they depend on.

### `index.html` — self-contained, live-compute (default)

- **Zero dependencies, no CDN, no data files.** A single HTML file with a
  hand-rolled 2D-canvas 3D projection. It works when opened directly from
  `file://` — no server, no internet.
- **Computes every point live in the browser.** It solves the most-balanced four
  squares for each n on the fly (an exact box-scan, `cmin4`), so the "all numbers"
  cloud is the real decomposition of every positive n up to the chosen bound
  (2k / 20k / 100k), colored by balance gap. Nothing is precomputed or sampled.
- Shows the gap-record **family rays** colored per ×4 chain, a draggable shape
  space, and a record number line.
- A console self-check recomputes all 37 record gaps and prints `PASS`.

### `fsq4d.html` — three.js + precomputed sample

- The original viewer (its `fsq4d*` support files share its name). Loads **three.js
  and OrbitControls from a CDN**, so it needs internet access for the library, and
  renders a **precomputed** sample (`fsq4d_data.bin`, interleaved `float32 x 5` per
  point: `s1, s2, s3, val, flag`).
- Offers three sampling modes — **Shell cloud**, **Cone (vs n)**, and
  **Multishell** — that are nice for showing how the same shape persists across
  scales (the cone narrowing with n toward `(m,m,m,m')`).
- When opened from `file://` it cannot fetch the binary and falls back to the
  smaller embedded sample in `fsq4d_fallback.js`. For the full sample, serve the
  folder:

      cd viz
      python3 -m http.server
      # open http://localhost:8000/

**Use `index.html` for an honest, dependency-free, exact view; use
`fsq4d.html` for the WebGL multi-mode sampled view.**

## The four-square doubling twist

The most balanced four squares do **not** scale cleanly under ×4 for most n: e.g.
`4 = 1^2+1^2+1^2+1^2` is more balanced than `(2,0,0,0)`. Clean doubling survives
only along the verified **record families** `96*4^m`, `224*4^m`, `2816*4^m`.
That is why the records form straight rays in shape space while the surrounding
cloud does not.

## Files

- `index.html` — self-contained live-compute viewer (default).
- `fsq4d.html` — three.js + precomputed-sample viewer (the original).

The `fsq4d*` files all support `fsq4d.html`:

- `fsq4d_data.bin` — precomputed sample for `fsq4d.html`; interleaved
  `float32 x 5` per point: `s1, s2, s3, val, flag` with `flag = mode*2`.
- `fsq4d_fallback.js` — smaller stratified sample used by `fsq4d.html` when
  opened from `file://` and the binary cannot be fetched.
- `fsq4d_meta.json` — point count, source, scan bound, and mode map.
- `gen_data.py` — regenerates `fsq4d_data.bin` and `fsq4d_meta.json` from a packed
  canonical-decomposition table, if one is available locally.

## Power-balance family (`power-balance/`)

`power-balance/` holds a second, exploratory pair of viewers that generalize the
balance-gap construction from squares to sums of four p-th powers, p = 2..7
(three.js from a CDN, so they need internet access). The p >= 3 record data is
archived in `../archive/exploratory-sequences/power-balance-p3/` …
`power-balance-p7/`; see `power-balance/README.md`.

The visualization is supporting material for the gap-record-location sequence; it
is not a separate sequence submission.
