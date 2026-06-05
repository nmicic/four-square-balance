#!/usr/bin/env python3
"""Generate viz data from a local packed canonical-decomposition binary.
Writes a compact interleaved Float32 file the viewer fetches:
  per point: s1, s2, s3, val, flag   (5 x float32 = 20 bytes)
    flag = mode*2   (mode 0=shell, 1=cone, 2=multishell)
Also writes a small JS fallback (embedded sample) so the HTML works via file://.

Usage: python3 viz/gen_data.py [PACKED_XYZW.bin] [SHELL_N] [SHELL_M]
"""
import sys, json, numpy as np

SRC   = sys.argv[1] if len(sys.argv) > 1 else "local/xyzw.bin"
SHN   = int(sys.argv[2]) if len(sys.argv) > 2 else 300_000_000
SHM   = int(sys.argv[3]) if len(sys.argv) > 3 else 60_000      # shell size (dense cloud)

a = np.memmap(SRC, dtype=np.uint32, mode="r"); NMAX = len(a) // 4
e1 = np.array([1,-1,0,0])/np.sqrt(2); e2 = np.array([1,1,-2,0])/np.sqrt(6); e3 = np.array([1,1,1,-3])/np.sqrt(12)
Bm = np.stack([e1,e2,e3])

def shape(W):
    Wf = W.astype(np.float64); D = Wf - Wf.mean(1, keepdims=True); return D @ Bm.T

rows = []  # (s1,s2,s3,val,flag)

# --- mode 0: dense shell cloud, colored by balance gap in the viewer ---
W = np.array(a[SHN*4:(SHN+SHM)*4], dtype=np.int64).reshape(-1,4); n = np.arange(SHN+1, SHN+SHM+1)
S = shape(W); xm = np.ceil(np.sqrt(n/4)).astype(np.int64); gap = W[:,0]-xm
for i in range(len(W)):
    rows.append((S[i,0], S[i,1], S[i,2], float(gap[i]), 0*2))

# --- mode 1: cone (normalized shape directions across octaves) ---
for k in range(20, 31):
    lo = 1 << k
    if lo >= NMAX: break
    step = max(1, (1 << (k-3)) // 1500)
    idx = np.arange(lo, min(lo + (1 << (k-3)), NMAX-1), step)
    W = np.array(a.reshape(-1,4)[idx], dtype=np.int64); S = shape(W)
    U = S/(np.linalg.norm(S,axis=1,keepdims=True)+1e-9)*30
    for i in range(len(idx)):
        rows.append((U[i,0], U[i,1], U[i,2], float(k+1), 1*2 + 0))

# --- mode 2: multishell (cloud at several n, colored by log n; scaled to compare) ---
for j,Ns in enumerate([5_000_000, 30_000_000, 100_000_000, 300_000_000, 600_000_000]):
    if Ns+4000 >= NMAX: break
    W = np.array(a[Ns*4:(Ns+4000)*4], dtype=np.int64).reshape(-1,4); S = shape(W)
    S = S/np.sqrt(Ns)*1e4    # normalize by sqrt(n) so shells are comparable
    for i in range(len(W)):
        rows.append((S[i,0], S[i,1], S[i,2], float(j), 2*2 + 0))

arr = np.array(rows, dtype=np.float32)
arr.tofile("viz/fsq4d_data.bin")
meta = {"n_points": len(arr), "shell_N": SHN, "shell_M": SHM, "src": SRC,
        "src_NMAX": int(NMAX), "stride_bytes": 20,
        "modes": {"0":"shell cloud","1":"cone vs n","2":"multishell (normalized)"}}
with open("viz/fsq4d_meta.json","w") as _f: json.dump(meta,_f,indent=1)
# embedded fallback for file:// (no server): STRATIFIED across all modes so every
# button works on double-click. ~5k shell + 4k cone + 3k multishell.
modecol = arr[:,4].astype(int) // 2
fb = []
for m, k in [(0, 5000), (1, 4000), (2, 3000)]:
    idx = np.where(modecol == m)[0]
    if len(idx) > k: idx = idx[np.linspace(0, len(idx)-1, k).astype(int)]
    fb += arr[idx].tolist()
open("viz/fsq4d_fallback.js","w").close()
with open("viz/fsq4d_fallback.js","w") as _ff: _ff.write(
    "window.FSQ4D_FALLBACK="+json.dumps([[round(v,3) for v in r] for r in fb])+";")
print(f"wrote viz/fsq4d_data.bin ({len(arr)} pts, {arr.nbytes//1024} KB), meta, "
      f"fallback ({len(fb)} stratified pts)")
