# Corgdoku — corgi & paw art generation brief

Use this with an AI image generator (ChatGPT/GPT image, Midjourney, Firefly,
etc.). It produces 12 corgi faces and 10 paw-print icons that drop straight
into the game's existing unlock system — no code changes needed beyond
swapping the art in.

**The one rule that matters most:** do this in a single conversation/session,
and after the first image generates, don't start fresh for the rest —
re-attach that first image each time and ask for a variant "in this exact
style." Text-only prompts drift in style from one generation to the next;
feeding the reference image back in is what keeps the set looking like one
family instead of twelve unrelated pieces.

---

## Part 1 — Corgis (12 poses)

### Step 1: generate the base image, alone

```
Generate a square (1:1) 2D flat vector icon of a corgi's face and ears only —
no body, no paws visible. Not a 3D render, not a photo, not a plush toy, not
clipart with gradients or drop shadows. Flat vector illustration style,
similar to a modern app icon or mascot logo.

The most important detail: the ears and the top of the head must form ONE
continuous, unbroken outline — like a single silhouette shape — not a
circular head with two separate triangle ears glued on top. Draw it the way
a hand-drawn corgi logo would unify the shape, angular and a little
asymmetric, not perfectly symmetric or geometric.

Bold, consistent outline stroke around the whole shape (same thickness
throughout). Simple dot-and-highlight eyes, small nose, minimal linework —
no fur texture, no whiskers, no fine detail, since this will be shown very
small. Centered in frame, filling about 80% of the canvas. Plain solid white
background, nothing else in the scene.

Coat: warm orange-tan with a cream muzzle/chest blaze. Expression: neutral,
friendly, mouth closed. This is the base/default version of a set of 12 — call
it "Classic."
```

Check the result before continuing: does the head+ears read as one unified
silhouette, not a circle with triangles stuck on? That's the detail every
earlier attempt at this tended to miss. If it's not there, regenerate step 1
before moving on — everything else builds off this one.

### Step 2: attach that image, then run these 11 deltas one at a time

```
Using the exact same art style, outline weight, and head/ear shape as the
attached image, generate a variant with the tongue out and mouth open in a
happy open smile. Same coat color. Call it "Happy."
```
```
Same style as attached. One eye winking closed, tongue out, happy expression.
Same coat color. Call it "Winker."
```
```
Same style as attached. Both eyes half-closed and droopy, calm sleepy
expression, mouth closed. Coat a slightly deeper honey-tan. Call it "Sleepy."
```
```
Same style as attached. Both eyes fully closed in a content/blissful
expression, tongue sticking out slightly ("blep"). Same coat color. Call it
"Blep."
```
```
Same style as attached, but the whole coat is a much lighter cream/blonde
color throughout, softer palette overall. Neutral expression. Call it
"Cream Puff."
```
```
Same style as attached, but the coat is a deeper, more saturated red-orange
(fox-red) rather than tan. Tongue out. Call it "Red Fox."
```
```
Same style as attached, but the coat is brown (not orange) with a cream
muzzle and chest, like a sable-coated corgi. Neutral expression. Call it
"Sable."
```
```
Same style as attached, but colored like a classic tri-color corgi: mostly
black coat, tan eyebrow-spot markings above the eyes, cream/white chest and
muzzle. Call it "Tri-Color."
```
```
Same style as attached, base coat light cream, with one larger irregular
rust-orange patch covering part of one side of the face. Call it "Patch."
```
```
Same style as attached, orange coat, wearing a pair of small dark sunglasses
over the eyes, tongue out, confident expression. Call it "Cool Shades."
```
```
Same style as attached, orange coat, wearing a small pointed birthday party
hat on top of the head between the ears, tongue out, festive expression.
Call it "Party Pup."
```

---

## Part 2 — Paw prints (10 shapes)

Different constraint here: these get tinted to different colors at runtime
(board-note ink, tracker accent, a red "last life" warning), so **they must
be a single flat silhouette in solid black — no shading, no gradient, no
color of their own** (except "Outline," which is deliberately hollow).

### Step 1: base shape, alone

```
Generate a square (1:1) icon: a single dog paw print silhouette, filled solid
black, no outline stroke, no shading or gradient, no texture — just one flat
shape. Round main pad at the bottom, four rounded toe shapes fanned out
above it. Centered, filling about 70% of the frame, plain white background.
Bold and slightly cartoonish/chunky rather than a realistic paw print. Call
it "Chunky."
```

### Step 2: attach that image, then run these 9 deltas

```
Same style as attached (solid black silhouette, no outline, no shading), but
a more traditional cartoon paw-print proportions: smaller rounder main pad,
four toe ovals rotated slightly outward like a fan. Call it "Classic."
```
```
Same style as attached. Make the whole shape wider and flatter/squatter —
wide main pad, short wide toes. Call it "Wide."
```
```
Same style as attached. Make it smaller and more delicate — thin elegant
toes, small dainty pad, petite proportions. Call it "Dainty."
```
```
Same style as attached, same shape as "Classic" but scaled down smaller
within the frame, more surrounding white space, like a small puppy's paw.
Call it "Puppy."
```
```
Same style as attached (classic paw shape), with a few small round mud-splat
droplets scattered around and below it. Call it "Muddy."
```
```
Same style as attached, but the main pad is heart-shaped instead of round,
with the four toes still fanned above it as usual. Call it "Heart."
```
```
Same solid-black-silhouette style, but instead of a paw: a dog bone shape —
two rounded knobs on each end connected by a bar. Call it "Bone."
```
```
Same solid-black-silhouette style, but instead of a paw: a circle with two
curved seam lines across it like a tennis ball. Call it "Tennis Ball."
```
```
Same paw shape as "Classic," but drawn as a hollow outline only — a bold
stroke tracing the paw shape with the inside left empty/transparent rather
than filled solid. Call it "Outline."
```

---

## Practical notes

- **Don't sweat exact hex colors.** Get the shapes and style right — colors
  get matched to the game's palette during integration.
- **Background:** most image tools are inconsistent about true transparency,
  so don't fight it — generate on the plain white background as prompted
  above and hand over the raw files as-is. Background removal can happen
  during integration; it doesn't need to be done up front.
- **Export at the largest size offered** (pick "high quality" if asked) —
  better to downscale a crisp large image than upscale a small one.
- **Naming:** when handing off the finished set, label each file with the
  name from its prompt ("Classic," "Happy," "Winker," …) so it's obvious
  which unlock slot each one fills.

## What happens after handoff

Send the full set of files (all 12 corgis + all 10 paws) together, labeled by
name. From there: sizing for the board/tracker/win-screen, color-matching to
the game's palette, and wiring each one into the existing unlock ladder —
none of which requires touching this brief again.
