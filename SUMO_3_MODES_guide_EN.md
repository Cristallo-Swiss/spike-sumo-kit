# SUMO BOT — 4 Modes 🤖
### LEGO SPIKE Prime — BUILD with blocks (don't just copy)

**Goal:** push the opponent out of the ring WITHOUT falling out yourself.  
**Key rule:** the robot must wait **5 seconds** after start before moving.

The robot already has everything:
| Part | Role |
|---|---|
| Motors **A + E** | movement |
| Color sensors **F + D** | **EDGE** detectors (see the white line) |
| Distance sensor **B** | **OPPONENT** detector |
| Force sensor **C** | **BUMPER** (knows when it pushes) |

---

## 🧱 THE SKELETON (shared by all modes)

> The student builds this ONCE, then only changes the "brain" (the `forever` loop).

```
when [right] button pressed
  set movement motors to  A+E
  set movement acceleration to  fast
  wait 5 seconds              <-- sumo rule (mandatory!)
  forever
      ┌── THE BRAIN (changes per mode, see below)
      └──
```

**Golden rule for ALL modes:** the **first** `if` inside `forever` checks the  
**EDGE** (sensors F or D see white) → back up + turn.
> 👉 Hint for the student: *"Why must the edge be checked FIRST and not last?"*  
> (answer to discover: if you attack first, you fall before checking the floor.)

The anti-fall reflex (the "back off"), to put in every mode:
```
move  ↓ (back)  fast , for a short time
then turn  (right)  for a short time   <-- return toward center
```

---

## 🛡️ MODE 1 — SURVIVOR (safe)
*"I win because I NEVER fall."* — beats aggressive robots that self-destruct.

```
forever
  if  < F or D see WHITE (edge) >  then
      back off + turn            # absolute priority
  else if  < B closer than 36 cm >  then
      start moving up  at  CRUISE speed (~65%)   # push, but controlled
  else
      start moving  turning slowly               # search for opponent
```

---

## ⚡ MODE 2 — BULLDOZER (aggressive)
*"Max speed, slip under, push before they react."* — beats heavy/slow robots.

```
when started (after 5 s) :
  move straight at FULL speed for 0.5 s     # opening LUNGE: first 0.5 s decide

forever
  if  < F or D see WHITE (edge) >  then
      back off + turn            # safety net, ULTRA fast reaction
  else if  < B closer than 36 cm >  OR  < C is pressed >  then
      start moving up at FULL speed          # FULL GAS while touching
  else
      start moving  turning fast             # search fast
```
> ⚠️ Hint: *"The Bulldozer can fall out on its own if it misses. How do you set  
> the edge threshold so it brakes in time WITHOUT braking too early?"*

---

## 🥋 MODE 3 — JUDOKA (creative)
*"Never face-on. Dodge and hit the SIDE."* — beats stronger robots by positioning.

```
forever
  if  < F or D see WHITE (edge) >  then
      back off + turn
  else if  < B closer than 36 cm >  then
      turn  (right)  for a SHORT time        # 1) take an angle (dodge)
      then move straight at FULL speed for 0.4 s   # 2) charge the flank
  else
      start moving  turning slowly           # search
```
> Why it works: a robot pushed **sideways** has zero traction to resist.  
> 👉 Hint: *"The pivot angle is the whole secret. Too small = you push face-on  
> (you lose). Too big = you miss. Find it by testing."*

---

## 🦎 MODE 4 — METAMORPH (adaptive)
*"I don't guess the opponent. I react to what I feel right now."*

**Honest framing:** with only a distance sensor + a bumper, the robot cannot  
"recognize the type of opponent in front of it." But it can **sense what is happening**:
- touching and pushing forward? → Bulldozer mode
- touching and stuck for a while? → Judoka mode (break off + flank)
- at the edge? → Survivor mode (absolute priority)
- sees the target? → charge
- sees nothing? → search

```
forever
  if  < F or D see WHITE (edge) >  then
      back off + turn                        # SURVIVOR: don't fall
  else if  < C is pressed >  then
      if  < contact has lasted a long time >  then
          turn away + pivot + charge side    # JUDOKA: go around
      else
          move straight at FULL speed        # BULLDOZER: push hard
  else if  < B closer than 36 cm >  then
      start moving up at FULL speed          # target seen -> charge
  else
      start moving turning slowly            # search
```

> ⚠️ Hint: *"The Survivor/Bulldozer/Judoka triangle (rock-paper-scissors) is a nice
> teaching story, NOT a physical law. The Metamorph does not promise to win: it just tries
> not to stay stuck in a tactic that is currently failing."*

---

## 🎛️ THE NUMBERS THE STUDENT MUST FIND HIMSELF
*(THIS is learning — we give the structure, he finds the numbers)*

| Setting | Effect | Method |
|---|---|---|
| **Distance threshold B** (e.g. 36 cm) | too far → charges at nothing ; too short → reacts too late | test against a still robot |
| **Speed** (%) | push ↔ control tradeoff | increase until it slips, then drop one notch |
| **Back-off time** | too short → falls again ; too long → wastes time | watch on the ring |
| **Pivot angle** (Judoka) | miss vs face-on hit | the finest tuning |
| **Stalemate time** (Metamorph) | too short → panics ; too long → stays stuck | when the push is blocked |

**Learning rule:** change ONLY ONE number at a time, run a match, observe.  
Otherwise you understand nothing.

---

## 🧪 HOW TO TEST (internal tournament)
1. Build **Survivor** first (the foundation: anti-fall).
2. Copy it 2× → make **Bulldozer** and **Judoka**.
3. Make them fight **each other** → the student sees for real which style wins and why.
4. Once the three work, try the **Metamorph** — but sell the truth: it reacts, it does not guess.
5. Keep the winner for the tournament, and be able to **explain it to the judge**.

---

## 🆘 Last Resort
If he really gets stuck: the file **`sumo_3_modes.py`** (same folder) has all 4 modes  
ready to run in **Python inside the SPIKE app**. Change the word `MODE = "survivor"`  
at the top to test another style (`survivor`, `bulldozer`, `judoka`, `metamorph`).  
*(But the goal remains: he builds it himself.)*

---
*Prepared by équipe Cristallo — 22 June 2026*
