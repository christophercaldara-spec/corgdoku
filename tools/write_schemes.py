"""Rewrites the SCHEMES block in index.html from tools/_generated.json.

Keeps every existing scheme's non-region colours exactly as they are and swaps
only the `regions` array, then appends the new schemes defined below.
"""
import json
import os
import re

HERE = os.path.dirname(__file__)
HTML = os.path.join(HERE, "..", "index.html")
GEN = json.load(open(os.path.join(HERE, "_generated.json")))

# Four additions: three dark schemes (the set was 6 light to 2 dark) and one
# built for colour blindness rather than for looks.
NEW = {
    "midnight": dict(label="Midnight Meadow", dark=True,
        bgTop="#121D2B", bgBottom="#0A1320", surface="#1A2637", surfaceBorder="#2E3D52",
        ink="#E6ECF5", inkMuted="#98A6BC", accent="#6FB1FF", accentHover="#8CC2FF",
        accentInk="#06192E", frame="#070C15", badge="rgba(11,18,32,.84)",
        pawInk="#E6ECF5", ripple="rgba(255,255,255,.16)"),
    "ember": dict(label="Campfire Ember", dark=True,
        bgTop="#1E1613", bgBottom="#130D0A", surface="#281E19", surfaceBorder="#423128",
        ink="#F4E8DE", inkMuted="#B49C8A", accent="#FF8A4C", accentHover="#FFA269",
        accentInk="#2B1206", frame="#0D0806", badge="rgba(20,13,10,.84)",
        pawInk="#F4E8DE", ripple="rgba(255,255,255,.15)"),
    "harbor": dict(label="Harbor Lights", dark=True,
        bgTop="#15252A", bgBottom="#0D1A1E", surface="#1E2F35", surfaceBorder="#344952",
        ink="#E5EFF2", inkMuted="#9AAFB7", accent="#4FC3E8", accentHover="#70D2F0",
        accentInk="#04242F", frame="#081012", badge="rgba(12,22,24,.84)",
        pawInk="#E5EFF2", ripple="rgba(255,255,255,.16)"),
    "clear": dict(label="Color-Safe", dark=False,
        bgTop="#F7FAFC", bgBottom="#E8EEF3", surface="#FFFFFF", surfaceBorder="#D3DDE5",
        ink="#10202B", inkMuted="#55697A", accent="#0B6FD1", accentHover="#0959AA",
        accentInk="#FFFFFF", frame="#1B2A33", badge="rgba(255,255,255,.94)",
        pawInk="#10202B", ripple="rgba(255,255,255,.5)"),
}

NEW_NOTE = {
    "clear": ("Built for deuteranopia rather than for looks: the themed palettes "
              "above are tuned purely for normal vision, which buys them a much "
              "wider perceptual spread but leaves some pairs near-identical to a "
              "colour-blind player. This one trades some of that spread to keep "
              "every pair separable both ways."),
}

src = open(HTML, encoding="utf-8").read()

def regions_body(key):
    return "      regions:[" + ",".join('"%s"' % c for c in GEN[key]) + "]"

def regions_line(key):
    return regions_body(key) + " }"

# Swap regions on the existing schemes.
for key in GEN:
    if key in NEW:
        continue
    pat = re.compile(r'(\b' + key + r':\s*\{\s*label:"[^"]+",\s*dark:(?:true|false).*?)regions:\[.*?\]\s*\}',
                     re.S)
    if not pat.search(src):
        raise SystemExit("could not find scheme " + key)
    src = pat.sub(lambda m: m.group(1) + regions_line(key).strip(), src, count=1)

# Append the new ones just before the closing brace of SCHEMES.
block = ""
for key, s in NEW.items():
    note = NEW_NOTE.get(key)
    if note:
        words, line, lines = note.split(), "", []
        for w in words:
            if len(line) + len(w) > 68:
                lines.append(line); line = w
            else:
                line = (line + " " + w).strip()
        lines.append(line)
        block += "".join("    // %s\n" % l for l in lines)
    block += (
        '    %s: { label:"%s", dark:%s,\n'
        '      bgTop:"%s", bgBottom:"%s", surface:"%s", surfaceBorder:"%s",\n'
        '      ink:"%s", inkMuted:"%s", accent:"%s", accentHover:"%s", accentInk:"%s",\n'
        '      frame:"%s", badge:"%s", pawInk:"%s", ripple:"%s",\n'
        '%s },\n'
    ) % (key, s["label"], "true" if s["dark"] else "false",
         s["bgTop"], s["bgBottom"], s["surface"], s["surfaceBorder"],
         s["ink"], s["inkMuted"], s["accent"], s["accentHover"], s["accentInk"],
         s["frame"], s["badge"], s["pawInk"], s["ripple"],
         regions_body(key))

marker = re.search(r'(slate:\s*\{.*?regions:\[.*?\]\s*\}\n)(\s*\};)', src, re.S)
if not marker:
    raise SystemExit("could not find end of SCHEMES")
src = src[:marker.end(1)] + block.rstrip(",\n") + "\n" + src[marker.start(2):]
# the slate entry needs a trailing comma now that entries follow it
src = src.replace(marker.group(1), marker.group(1).rstrip() + ",\n", 1)

# Keep the :root fallbacks in step with the default scheme.
root_new = "\n".join("    --pack-%d:%s;" % (i, c) for i, c in enumerate(GEN["mint"]))
src = re.sub(r"(    --pack-0:.*?--pack-\d+:#[0-9A-Fa-f]{6};)", root_new, src, count=1, flags=re.S)

open(HTML, "w", encoding="utf-8", newline="").write(src)
print("rewrote SCHEMES: %d existing updated, %d added" % (len(GEN) - len(NEW), len(NEW)))
