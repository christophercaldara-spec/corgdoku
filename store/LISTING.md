# Corgdoku — Play Store listing

Everything here is a draft you can paste into the Play Console. Edit freely —
you know how you'd describe it better than I do.

---

## App name (max 30 chars)

```
Corgdoku
```

## Short description (max 80 chars)

```
A corgi-flavored logic puzzle. One good boy per yard, no guessing required.
```
*(74 characters)*

## Full description (max 4000 chars)

```
Corgdoku is a cosy logic puzzle about putting one corgi in every yard.

Every board is a grid split into colored pastures. Place exactly one corgi in
each pasture, with no two sharing a row or a column, and never letting two
stand nose-to-nose diagonally. That's the whole rule set — the depth comes
from working out where they have to go.

NEVER A GUESS
Every puzzle is checked before you see it: a solver that only uses moves a
person could actually reason through has to be able to finish the whole board.
If it can't, the board is rebuilt. So if you're stuck, there is always a next
step to find — you're never being asked to flip a coin.

GETS HARDER THE RIGHT WAY
Levels run from 1 upward, and bigger boards demand sharper reasoning rather
than just more squares. Early levels only ask you to spot a pasture with one
square left. Later ones need you to see that two pastures between them own two
rows, so everything else in those rows is out. Every tenth level is a 12x12
boss board.

A DAILY PUZZLE YOU CAN SHARE
Everyone gets the same daily board, generated from the date itself. Compare
times with whoever else is playing.

STUCK? ASK THE PACK
The hint button points at a square you can work out right now and tells you
which rule forces it — so it teaches the technique instead of just handing over
the answer.

ALSO IN THE BOX
• A dozen corgis and ten paw prints to unlock as you climb, and mix as you like
• Paw-print notes for marking squares you've ruled out
• Combo bonuses for finding corgis in quick succession
• Lifetime stats: win streak, fastest win, corgis found, flawless wins
• Eight colour themes, each checked so every pasture is easy to tell apart
• Plays completely offline
• Back up your progress and carry it to a new phone

NO NONSENSE
No ads. No accounts. No sign-up. No tracking or analytics of any kind. Nothing
you do leaves your phone. It's a puzzle game, and that's all it is.
```

---

## Screenshots

Play needs at least 2 phone screenshots (min 320px on the short side, max
3840px, aspect ratio between 16:9 and 9:16).

**Take these on your actual Pixel** rather than using anything generated here —
real device captures are higher resolution and will look noticeably sharper in
the listing. Good ones to grab:

1. **The home screen**, with a level number and some stats filled in.
2. **A board mid-solve**, showing corgis placed, a few paw-print notes, and the
   paws tracker — ideally with one of the single-square pastures visible.
3. *(optional)* **The win screen** with the hopping corgis.
4. *(optional)* **The settings sheet** showing the colour themes.

Power + Volume Down takes a screenshot on a Pixel; they land in Photos.

## Feature graphic

`feature-graphic-1024x500.png` in this folder — 1024x500, exactly what Play
asks for.

## App icon

Play wants a 512x512 PNG: use `icon-512.png` from the project root.

---

## Content rating questionnaire

It's a puzzle game with no violence, no in-app purchases, no ads, no user
content and no data collection, so this should come out as suitable for
everyone. Answer honestly and it'll sort itself out.

## Data safety form

- Does your app collect or share any of the required user data types? **No.**
- Is all user data encrypted in transit? Not applicable — no data is transmitted.
- Do you provide a way for users to request deletion? Not applicable — data
  never leaves the device, and uninstalling removes it.

This is accurate as of the self-hosting change: the app makes no third-party
requests at all. Fonts and the confetti animation are served from the app's own
files, so nothing about the player reaches anyone.

## Privacy policy URL

```
https://christophercaldara-spec.github.io/corgdoku/privacy.html
```

**Before submitting:** open `privacy.html` and replace the
`[add your contact email here]` placeholder with a real address. Play requires
a reachable contact.

## App category

Games → Puzzle

---

## Before you upload

- The signed bundle is at `android-build/Corgdoku.aab`.
- Keep `android-build/signing.keystore` and `signing-key-info.txt` safe — Play
  ties all future updates to that key.
- The app is a Trusted Web Activity pointing at the live site, so content
  updates ship by pushing to the repo. You only need a new bundle if something
  about the native wrapper changes (icon, package name, permissions).
- Worth re-generating the bundle at PWABuilder shortly before submitting so it
  targets whatever API level Play currently requires.
