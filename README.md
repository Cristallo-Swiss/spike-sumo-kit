# SPIKE Prime Sumo Bot — 4 Modes Pack

A pédago-first kit for a LEGO SPIKE Prime sumo-robot student.
Build in blocks first; use the Python file only as a last-resort fallback.

## Files

| File | What |
|---|---|
| `SUMO_3_MODES_guide.md` | 🇫🇷 French guide — main teaching material |
| `SUMO_3_MODES_guide_EN.md` | 🇬🇧 English version |
| `SUMO_3_MODES_guide_TH.md` | 🇹🇭 Thai version |
| `sumo_3_modes.py` | Python fallback for the SPIKE 3 app |

## Robot mapping

- Motors **A + E** → movement
- Color sensors **F + D** → edge (white line)
- Distance sensor **B** → opponent
- Force sensor **C** → bumper/contact

## The modes

1. **Survivor** — never fall first. Foundation of all the others.
2. **Bulldozer** — max speed, opening lunge, full-gas while touching.
3. **Judoka** — angle in, hit the flank, avoid face-to-face pushing.
4. **Metamorph** — adaptive mode. Reacts to live signals: edge → survive, short contact → push, stuck contact → flank, target seen → charge, nothing → search. It reacts, it does not "read" the opponent type.
5. **Original** — Python approximation of the student's existing block program (fallback only).

## Teaching flow

1. Build **Survivor** in blocks first.
2. Fork it into **Bulldozer** and **Judoka**.
3. Run an internal tournament between the three.
4. Try the **Metamorph** once the base modes work — keep the honest framing: it reacts, it doesn't guess.
5. Pick the winner for the real tournament, and make sure the student can explain it to the judge.
6. Use `sumo_3_modes.py` only if the student gets completely stuck.

## Honest tuning notes

- Verify real port letters on the student's actual robot.
- Edge threshold, distance threshold, speeds and pivot time must be tuned on the real ring.
- That tuning phase is exactly where the learning happens.

---
*Prepared by équipe Cristallo — 22 June 2026*
