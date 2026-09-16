# Corgdoku — art brief #2: win dance + lab splash

Two new assets this round. Unlike the first brief, this one is specs, not
ready-to-paste prompts — you're writing the descriptions yourself. This is
what each image needs to satisfy technically so it drops in cleanly.

---

## 1. Win-screen dance — a sequence of frames, not one image

Right now the win screen bounces three small corgi *faces* (the same head
icons used everywhere else). The goal is a genuine full-body corgi doing a
little dance, cycled through as a flipbook.

### One character, not sixty-two

This plays on every win regardless of which of the 62 corgis you have
equipped — the same way the win sound and confetti are already universal.
Animating even 6 frames across all 62 skins would be 372 images, which isn't
worth it for a screen nobody stares at for long. So: design **one** corgi for
this — doesn't need to match an existing skin, though it can if you want
(Party Pup already has a hat that'd suit a celebration).

### Frame count

**6 frames** is the sweet spot — enough to read as motion, few enough that
drift between generations stays manageable (see below). If it's coming out
great, more is fine; if consistency is fighting you, 4 still works.

### The one thing that will make or break this

AI image generation is good at "draw me a dancing corgi" and bad at "draw me
*the same* corgi in a *slightly different pose*, at *exactly the same size
and position*." If the character drifts in scale or shifts around the frame
between images, cycling through them looks like jittering, not dancing.

The fix is the same trick that worked for the corgi/paw sets, just stricter:

1. Generate **one base frame** first — a neutral standing pose. Get the
   character design locked (colors, costume, proportions) before anything
   else.
2. For every other frame, **attach that base image** and explicitly say the
   character, size, and position in frame must stay identical — only the
   pose changes. Something like: *"Same corgi, same size, same position in
   the frame, same camera distance — change only the pose to: [describe]."*
3. If a generation comes back bigger, smaller, or shifted compared to the
   base — even if the pose itself looks great — regenerate it. A perfect
   pose at the wrong scale will visibly jump when it cycles in.

### Pose ideas (pick your favorites, mix freely)

Paws up in the air · a little hop with ears flopping · a hip-wiggle /
side-lean · spinning with one paw out · a proud chest-out pose · tongue out
mid-bounce. Whatever reads as "silly and pleased with itself."

**Bonus if you can manage it:** make the last frame flow back naturally into
the first one's pose, so the loop doesn't visibly jump when it repeats.

### Technical spec (same as everything else so far)

- Square canvas, generated at whatever size the tool defaults to (1024px is
  fine) — full body, centered, with real breathing room on all sides so nothing
  gets clipped mid-pose.
- Plain solid background (white is easiest) — don't worry about making it
  transparent yourself, I'll matte it the same way as the rest of the art.
- Flat vector / bold outline, roughly matching the existing house style, so
  it doesn't look like a different game's mascot wandered in. It doesn't need
  to match any single existing skin's colors.

---

## 2. Mad scientist corgi — the launch splash

The screen that shows "Gizmo's Laboratory" for about a second and a half on
launch currently has a hand-drawn flask icon, not a corgi at all. This
replaces that with something that actually plays into the theme.

### What it needs to survive

This is shown small (roughly 100–140px on a phone screen) for a very short
time — clarity at a glance matters more than detail. Same constraint as the
board-size icons: if it's fussy or fine-lined, it'll just read as a blob at
that size.

### Composition

Your call on bust/head-and-shoulders vs. something wider (e.g. peeking over
a bubbling beaker) — whichever reads clearest small. A single scientist-corgi
character: think lab coat, maybe safety goggles pushed up on the head, wild
"static-shock" ear/fur styling, a beaker or test tube as a prop if there's
room. Doesn't need to hold a specific pose — this is one static image, not a
sequence.

### Technical spec

- Square canvas, transparent background this time is a genuine plus (it'll
  sit directly on the splash screen's dark green), but a plain white
  background works too and I'll matte it either way.
- Same flat vector / bold outline house style as everything else.
- One image. No frame sequence needed here.

---

## Handoff

Name the files so I know what's what — something like `dance-1.png` through
`dance-6.png` for the sequence (in pose order), and `mad-scientist.png` for
the splash art. Send them together and tell me if you want the dance
character tied to a specific existing skin's look or left as its own thing.

I'll handle background cleanup, sizing, and wiring both into the game the
same way as the rest of the art — nothing else needed from you after the
files land.
