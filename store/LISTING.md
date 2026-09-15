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
Levels run from 1 upward in blocks of ten, and every block is a mix: a couple
of quick ones, a couple that make you work, a breather, then a 10x10 boss.
Climbing doesn't turn every board into a grind — it raises what the hard ones
ask of you while leaving the gentle ones gentle, so there's always somewhere
to catch your breath.

Early on, a board might only ask you to spot a pasture with one square left.
Further up, the tough ones need you to see that two pastures between them own
two rows, so everything else in those rows is ruled out. Each board is built
to need that reasoning — not merely to allow it.

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
• Optional sign-in that backs up your progress as you play, and brings it all
  back on a new phone

PLAY WITH YOUR PACK
Sign in with Google and your progress backs itself up, so a new phone picks up
exactly where the old one left off. Make a pack, share the code, and see how
everyone's climb is going.

NO NONSENSE
No ads. No tracking or analytics of any kind. Signing in is entirely optional
and the whole game works without it — signed out, nothing you do leaves your
phone. It's a puzzle game, and that's all it is.
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

A puzzle game with no violence, no in-app purchases and no ads, so it should
come out suitable for everyone.

**Two answers changed when accounts landed** — answer these honestly:
- Does the app let users interact or share content? **Yes** — pack members see
  each other's display name, level and stats.
- Is there user-generated content? **Effectively yes** — the display name comes
  from the user's Google account and is visible to their pack.

## Data safety form

Accurate as of the accounts release. Sign-in is optional, but Play asks what
the app *can* collect, not what it always collects.

- Does your app collect or share any of the required user data types? **Yes.**
- What's collected, only when the user signs in:
  - **Personal info → Name** (the Google account display name)
  - **Personal info → User IDs** (the Firebase account identifier)
  - **App activity → In-app actions** (level reached, stats, chosen corgi/paw)
- Is any of it shared with third parties? **No** — it's stored in the
  developer's own Firebase project, not sold or handed on. Pack members seeing
  each other is in-app visibility, not sharing.
- Is collection optional? **Yes** — the game is fully playable signed out, and
  signed out it transmits nothing.
- Is all user data encrypted in transit? **Yes** — Firebase is HTTPS only.
- Do you provide a way for users to request deletion? **Yes** — in-app, at
  Settings → Account → Delete my data, which erases the stored progress, removes
  them from any pack and closes the account. Email deletion is offered as a
  fallback in the privacy policy.

## Privacy policy URL

```
https://christophercaldara-spec.github.io/corgdoku/privacy.html
```

The contact address on it is christophercaldara@gmail.com.

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
