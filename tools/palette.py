"""Region-palette generator and audit for Corgdoku's colour schemes.

The region colours are what tell one yard from another, so two that read alike
are a gameplay bug, not a taste problem. The original palettes stepped hue
evenly around the wheel at a fixed saturation, which looks principled and
isn't: even hue steps are not even *perceptual* steps, so they bunched up
badly in the green-yellow band and again in blue-purple.

This picks colours by the measure that actually matters - maximising the
smallest CIEDE2000 distance between any two of them - inside per-scheme
bounds that keep each scheme's mood. Deuteranopia (the common form of
colour blindness, and the one that flattens exactly the green-yellow band
these palettes leaned on) is scored alongside normal vision.

    python tools/palette.py audit      # check what's in index.html now
    python tools/palette.py generate   # propose replacements
"""

import math
import random
import re
import sys
import os

# --- colour space ---------------------------------------------------------

def _inv_gamma(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def _gamma(c):
    c = 12.92 * c if c <= 0.0031308 else 1.055 * (c ** (1 / 2.4)) - 0.055
    return c

def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

def rgb2hex(rgb):
    return "#" + "".join("%02X" % max(0, min(255, int(round(v)))) for v in rgb)

def rgb2lab(rgb):
    r, g, b = [_inv_gamma(v) for v in rgb]
    x = r * 0.4124564 + g * 0.3575761 + b * 0.1804375
    y = r * 0.2126729 + g * 0.7151522 + b * 0.0721750
    z = r * 0.0193339 + g * 0.1191920 + b * 0.9503041
    xn, yn, zn = 0.95047, 1.0, 1.08883
    def f(t):
        return t ** (1 / 3) if t > 0.008856 else (7.787 * t) + 16 / 116
    fx, fy, fz = f(x / xn), f(y / yn), f(z / zn)
    return (116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz))

def lab2rgb(lab):
    L, a, b = lab
    fy = (L + 16) / 116
    fx = fy + a / 500
    fz = fy - b / 200
    def finv(t):
        return t ** 3 if t ** 3 > 0.008856 else (t - 16 / 116) / 7.787
    x, y, z = finv(fx) * 0.95047, finv(fy) * 1.0, finv(fz) * 1.08883
    r = x * 3.2404542 + y * -1.5371385 + z * -0.4985314
    g = x * -0.9692660 + y * 1.8760108 + z * 0.0415560
    bb = x * 0.0556434 + y * -0.2040259 + z * 1.0572252
    return tuple(_gamma(max(0.0, min(1.0, v))) * 255 for v in (r, g, bb))

def in_gamut(lab, tol=0.6):
    """lab2rgb clamps, so a colour is only real if the round trip survives."""
    rgb = lab2rgb(lab)
    if any(v < -tol or v > 255 + tol for v in rgb):
        return False
    back = rgb2lab(tuple(max(0, min(255, v)) for v in rgb))
    return all(abs(back[i] - lab[i]) < 1.2 for i in range(3))

def ciede2000(lab1, lab2):
    L1, a1, b1 = lab1
    L2, a2, b2 = lab2
    avg_L = (L1 + L2) / 2
    C1, C2 = math.hypot(a1, b1), math.hypot(a2, b2)
    avg_C = (C1 + C2) / 2
    G = 0.5 * (1 - math.sqrt(avg_C ** 7 / (avg_C ** 7 + 25 ** 7))) if avg_C > 0 else 0
    a1p, a2p = (1 + G) * a1, (1 + G) * a2
    C1p, C2p = math.hypot(a1p, b1), math.hypot(a2p, b2)
    avg_Cp = (C1p + C2p) / 2
    h1p = math.degrees(math.atan2(b1, a1p)) % 360
    h2p = math.degrees(math.atan2(b2, a2p)) % 360
    dLp, dCp = L2 - L1, C2p - C1p
    if C1p * C2p == 0:
        dhp = 0
    elif abs(h2p - h1p) <= 180:
        dhp = h2p - h1p
    elif h2p - h1p > 180:
        dhp = h2p - h1p - 360
    else:
        dhp = h2p - h1p + 360
    dHp = 2 * math.sqrt(C1p * C2p) * math.sin(math.radians(dhp) / 2)
    if C1p * C2p == 0:
        avg_hp = h1p + h2p
    elif abs(h1p - h2p) <= 180:
        avg_hp = (h1p + h2p) / 2
    elif h1p + h2p < 360:
        avg_hp = (h1p + h2p + 360) / 2
    else:
        avg_hp = (h1p + h2p - 360) / 2
    T = (1 - 0.17 * math.cos(math.radians(avg_hp - 30))
         + 0.24 * math.cos(math.radians(2 * avg_hp))
         + 0.32 * math.cos(math.radians(3 * avg_hp + 6))
         - 0.20 * math.cos(math.radians(4 * avg_hp - 63)))
    d_ro = 30 * math.exp(-(((avg_hp - 275) / 25) ** 2))
    Rc = 2 * math.sqrt(avg_Cp ** 7 / (avg_Cp ** 7 + 25 ** 7)) if avg_Cp > 0 else 0
    Sl = 1 + (0.015 * (avg_L - 50) ** 2) / math.sqrt(20 + (avg_L - 50) ** 2)
    Sc = 1 + 0.045 * avg_Cp
    Sh = 1 + 0.015 * avg_Cp * T
    Rt = -math.sin(math.radians(2 * d_ro)) * Rc
    return math.sqrt((dLp / Sl) ** 2 + (dCp / Sc) ** 2 + (dHp / Sh) ** 2
                     + Rt * (dCp / Sc) * (dHp / Sh))

# Machado et al. (2009), severity 1.0, applied in linear RGB.
_DEUT = ((0.367322, 0.860646, -0.227968),
         (0.280085, 0.672501, 0.047413),
         (-0.011820, 0.042940, 0.968881))

def simulate_deut(rgb):
    lin = [_inv_gamma(v) for v in rgb]
    out = []
    for row in _DEUT:
        v = sum(row[i] * lin[i] for i in range(3))
        out.append(_gamma(max(0.0, min(1.0, v))) * 255)
    return tuple(out)

def pair_scores(labs, rgbs):
    """Smallest normal-vision and deuteranopic distance across all pairs."""
    deut_labs = [rgb2lab(simulate_deut(c)) for c in rgbs]
    worst_n = worst_d = 1e9
    worst_pair = None
    for i in range(len(labs)):
        for j in range(i + 1, len(labs)):
            dn = ciede2000(labs[i], labs[j])
            dd = ciede2000(deut_labs[i], deut_labs[j])
            if dn < worst_n:
                worst_n, worst_pair = dn, (i, j)
            worst_d = min(worst_d, dd)
    return worst_n, worst_d, worst_pair

# --- scheme bounds --------------------------------------------------------
# L/C windows chosen to keep each scheme recognisably itself. `guard` colours
# are things the regions sit against - the piece badge (which would vanish on
# a region too close to it) and the board frame (which draws the region
# borders, so a region that matches it loses its outline).

SCHEME_BOUNDS = {
    "cozy":     dict(L=(58, 84), C=(24, 62), guard=["#FFFBF5", "#2F4A3C"]),
    "material": dict(L=(54, 82), C=(32, 78), guard=["#FFFFFF", "#16202A"]),
    "evening":  dict(L=(40, 64), C=(18, 48), guard=["#0A0A0A", "#05080A"]),
    # Pastel's original window (L 70-87, C 12-40) is simply too small a volume
    # to fit ten separable colours in - even optimally packed it only reached
    # dE 11. The room is bought from lightness rather than chroma: letting the
    # chroma ceiling up instead just produced vivid cyans that stop reading as
    # pastel at all.
    "pastel":   dict(L=(58, 90), C=(14, 42), guard=["#FFFFFF", "#8FBFA3"]),
    "autumn":   dict(L=(36, 64), C=(30, 70), guard=["#FFF8ED", "#5C3A21"]),
    "mint":     dict(L=(60, 85), C=(24, 62), guard=["#FFFFFF", "#12332C"]),
    "retro":    dict(L=(54, 82), C=(42, 88), guard=["#FFFFFF", "#1A1A1A"]),
    "slate":    dict(L=(42, 66), C=(16, 46), guard=["#121717", "#12171B"]),
    "midnight": dict(L=(42, 66), C=(20, 50), guard=["#0B1220", "#070C15"]),
    "ember":    dict(L=(40, 64), C=(24, 54), guard=["#140D0A", "#0D0806"]),
    "harbor":   dict(L=(44, 68), C=(18, 46), guard=["#0C1618", "#081012"]),
    # The colour-blind-safe scheme leans on the one axis deuteranopia leaves
    # intact, so it gets a much wider lightness range to work with.
    "clear":    dict(L=(46, 86), C=(16, 62), guard=["#FFFFFF", "#1B2A33"]),
}

GUARD_MIN = 26.0   # regions must stand clear of badge and frame by this much

# How hard to weigh deuteranopic separation against normal-vision separation.
# 0 ignores colour blindness entirely; ~1 treats the two as equally binding.
# Deuteranopia collapses the red-green axis, so insisting on both at once
# leaves only lightness and blue-yellow to separate ten colours in - which is
# why a nonzero value here costs real headroom on the normal-vision score.
CVD_WEIGHT = 1.15

def sample(bounds, rng):
    L = rng.uniform(*bounds["L"])
    C = rng.uniform(*bounds["C"])
    h = rng.uniform(0, 360)
    return (L, C * math.cos(math.radians(h)), C * math.sin(math.radians(h)))

def valid(lab, guards):
    if not in_gamut(lab):
        return False
    return all(ciede2000(lab, g) >= GUARD_MIN for g in guards)

def optimise(scheme, count=12, iters=9000, seed=7):
    """Hill-climb the palette, scoring the worse of normal and deuteranopic
    separation so a pair can't 'pass' by being distinct only to normal vision.

    Only one colour moves per step, so only that colour's row of the distance
    matrix is recomputed - 11 pair comparisons instead of 66.
    """
    rng = random.Random(seed)
    b = SCHEME_BOUNDS[scheme]
    guards = [rgb2lab(hex2rgb(g)) for g in b["guard"]]

    labs, dlabs = [], []
    while len(labs) < count:
        c = sample(b, rng)
        if valid(c, guards):
            labs.append(c)
            dlabs.append(rgb2lab(simulate_deut(lab2rgb(c))))

    def pair_cost(i, j, L, D):
        dn = ciede2000(L[i], L[j])
        if CVD_WEIGHT <= 0:
            return dn
        return min(dn, ciede2000(D[i], D[j]) * CVD_WEIGHT)

    # Maximising the single worst pair directly gives a near-flat objective -
    # almost every move leaves that one pair untouched, so a hill-climber
    # stalls at once. Treating the colours as mutually repelling particles
    # instead gives every move a gradient to follow, while the steep exponent
    # keeps the closest pair dominating the total. The reported figure is
    # still the true minimum distance.
    def energy_row(i, L, D):
        return sum((1.0 / max(pair_cost(i, j, L, D), 1e-6)) ** 6
                   for j in range(count) if j != i)

    def total_energy(L, D):
        return sum(energy_row(i, L, D) for i in range(count)) / 2

    E = total_energy(labs, dlabs)
    for step in range(iters):
        temp = 1.0 - step / iters
        i = rng.randrange(count)
        if rng.random() < 0.6:
            L, a, bb = labs[i]
            span = 1 + 16 * temp
            cand = (L + rng.gauss(0, span * 0.5),
                    a + rng.gauss(0, span),
                    bb + rng.gauss(0, span))
            C2 = math.hypot(cand[1], cand[2])
            if not (b["L"][0] <= cand[0] <= b["L"][1] and b["C"][0] <= C2 <= b["C"][1]):
                continue
        else:
            cand = sample(b, rng)
        if not valid(cand, guards):
            continue
        dcand = rgb2lab(simulate_deut(lab2rgb(cand)))
        trial_labs = labs[:i] + [cand] + labs[i + 1:]
        trial_dlabs = dlabs[:i] + [dcand] + dlabs[i + 1:]
        dE = energy_row(i, trial_labs, trial_dlabs) - energy_row(i, labs, dlabs)
        if dE < 0:
            labs, dlabs, E = trial_labs, trial_dlabs, E + dE
    worst = min(pair_cost(i, j, labs, dlabs)
                for i in range(count) for j in range(i + 1, count))
    return [rgb2hex(lab2rgb(l)) for l in labs], worst

# Ten mutually-distinct colours need most of the hue circle, which costs a
# scheme like Autumn Harvest its identity - you cannot have ten separable
# colours that are all autumnal. But a board of size n only ever uses regions
# 0..n-1, and boards start at 5x5, so ordering the palette by how well each
# colour fits the scheme keeps the small boards firmly on-theme and defers the
# off-brand hues to the large boards that actually need them. Ordering does
# not move any colour, so the separation figures are untouched.
SIGNATURE = {
    "cozy":     dict(mode="hue", target=70),    # gold through leaf green
    "material": dict(mode="chroma", desc=True),
    "evening":  dict(mode="hue", target=60),
    "pastel":   dict(mode="chroma", desc=False),
    "autumn":   dict(mode="hue", target=45),    # rust, amber, gold
    "mint":     dict(mode="hue", target=165),
    "retro":    dict(mode="chroma", desc=True),
    "slate":    dict(mode="hue", target=85),
    "midnight": dict(mode="hue", target=240),
    "ember":    dict(mode="hue", target=45),
    "harbor":   dict(mode="hue", target=210),
    "clear":    dict(mode="chroma", desc=True),
}

def order_palette(scheme, cols):
    sig = SIGNATURE.get(scheme)
    if not sig:
        return cols
    def key(c):
        L, a, b = rgb2lab(hex2rgb(c))
        if sig["mode"] == "chroma":
            ch = math.hypot(a, b)
            return -ch if sig.get("desc") else ch
        h = math.degrees(math.atan2(b, a)) % 360
        d = abs(h - sig["target"]) % 360
        return min(d, 360 - d)
    return sorted(cols, key=key)

def best_palette(scheme, count=12, restarts=14, iters=9000):
    """Restart from fresh random seeds and keep the best - the energy surface
    has plenty of local minima and restarts cost almost nothing here."""
    best, best_score = None, -1
    for s in range(restarts):
        cols, sc = optimise(scheme, count=count, iters=iters, seed=101 + s * 17)
        if sc > best_score:
            best, best_score = cols, sc
    return best, best_score

# --- reading the current palettes -----------------------------------------

HTML = os.path.join(os.path.dirname(__file__), "..", "index.html")

def read_schemes():
    src = open(HTML, encoding="utf-8").read()
    found = re.findall(
        r'(\w+):\s*\{\s*label:"([^"]+)",\s*dark:(true|false)(.*?)regions:\[(.*?)\]',
        src, re.S)
    return [(k, lbl, dk == "true", re.findall(r'"(#[0-9A-Fa-f]{6})"', reg))
            for k, lbl, dk, _mid, reg in found]

USED = 10   # boards cap at 10x10, so only the first 10 ever appear at once

# The themed schemes are tuned for normal vision only - insisting on colour
# blindness too would cost them roughly a third of their separation, so that
# case is served by a dedicated scheme instead. Each is judged against the
# target it was actually built for.
NORMAL_FLOOR = 18.0
CVD_SAFE_SCHEMES = {"clear"}
CVD_FLOOR = 15.0

def audit():
    print(f"{'scheme':<12} {'dark':<6} {'min dE':<8} {'min dE (deut)':<14} verdict")
    print("-" * 64)
    worst_overall = 1e9
    failures = 0
    for key, label, dark, cols in read_schemes():
        cols = cols[:USED]
        labs = [rgb2lab(hex2rgb(c)) for c in cols]
        rgbs = [hex2rgb(c) for c in cols]
        wn, wd, pair = pair_scores(labs, rgbs)
        worst_overall = min(worst_overall, wn)
        ok = wn >= NORMAL_FLOOR
        if key in CVD_SAFE_SCHEMES:
            ok = ok and wd >= CVD_FLOOR
        verdict = "ok" if ok else "TOO CLOSE"
        if not ok:
            failures += 1
        print(f"{key:<12} {str(dark):<6} {wn:<8.1f} {wd:<14.1f} {verdict}"
              + ("" if ok else f"  <- {cols[pair[0]]}/{cols[pair[1]]}"))
    print(f"\nworst normal-vision separation across all schemes: dE {worst_overall:.1f}"
          f"  (floor {NORMAL_FLOOR:.0f})")
    if failures:
        print(f"{failures} scheme(s) below floor")
    return failures

def generate():
    for key, label, dark, _cols in read_schemes():
        if key not in SCHEME_BOUNDS:
            continue
        cols, sc = optimise(key)
        print(f'    // {label}: min dE {sc:.1f}')
        print(f'      regions:[{",".join(chr(34)+c+chr(34) for c in cols)}],')

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "audit"
    if cmd == "audit":
        audit()
    elif cmd == "generate":
        generate()
    else:
        print(__doc__)
