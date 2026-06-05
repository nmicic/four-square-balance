# Visualization

`index.html` is a single-page 3D view of the canonical four-square decomposition
and the gap-record rays.

For every n, the canonical representation

    n = x^2 + y^2 + z^2 + w^2,   x >= y >= z >= w >= 0

is a lattice point on the sphere of radius sqrt(n) in R^4. The diagonal
(1,1,1,1) is split off and the imbalance is projected into 3D with the Helmert
orthonormal basis:

    s1 = (x - y)/sqrt(2)
    s2 = (x + y - 2z)/sqrt(6)
    s3 = (x + y + z - 3w)/sqrt(12)

## Running

When GitHub Pages is enabled, open:

    https://nmicic.github.io/four-square-balance/viz/index.html

Open `index.html` in a browser. It loads three.js from a CDN, so it needs internet
access for the library.

The viewer shows a precomputed shape-space sample with three modes: Shell cloud,
Cone, and Multishell. It colors points by the balance gap and can overlay the
observed gap-record rays.

When opened through `file://`, the page uses the smaller embedded fallback sample
from `fsq4d_fallback.js`. For the full precomputed sample, serve the folder so the
page can fetch the binary:

    cd viz
    python3 -m http.server
    # open http://localhost:8000/

If `fsq4d_data.bin` is reachable, the page uses the full sample automatically.
Otherwise it uses the embedded fallback sample.

## Files

- `index.html` — the viewer.
- `fsq4d_data.bin` — precomputed visualization sample, interleaved `float32 x 5`
  per point: `s1, s2, s3, val, flag`, with `flag = mode*2`.
- `fsq4d_fallback.js` — smaller stratified sample used when the page is opened from
  `file://` and the binary cannot be fetched.
- `fsq4d_meta.json` — point count, source, scan bound, and mode map.
- `gen_data.py` — regenerates `fsq4d_data.bin` and `fsq4d_meta.json` from a
  packed canonical-decomposition table if such a table is available locally.

The visualization is supporting material for the gap-record-location sequence; it
is not a separate sequence submission.
