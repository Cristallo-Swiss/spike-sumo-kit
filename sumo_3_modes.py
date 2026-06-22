# ============================================================
#  SUMO BOT - SURVIVOR / BULLDOZER / JUDOKA / METAMORPHE (+ original)
#  LEGO SPIKE Prime (Python dans l'app SPIKE 3)
#
#  Robot de l'eleve :
#    - moteurs de deplacement : A + E
#    - capteurs couleur F + D : detecteurs de BORD (ligne blanche)
#    - capteur distance B      : detecteur d'ADVERSAIRE
#    - capteur force  C        : pare-chocs (sait quand il pousse)
#
#  >>> CECI EST LE FICHIER DE SECOURS (dernier recours). <<<
#  L'ideal : l'eleve construit ces modes EN BLOCS lui-meme.
#  Il apprend en reglant les chiffres.
# ============================================================

from hub import port, button, light_matrix
import runloop
import motor_pair
import color_sensor
import distance_sensor
import force_sensor
import color

# ---- PORTS (verifier que ca correspond au vrai robot) ----
PAIR        = motor_pair.PAIR_1
LEFT_MOTOR  = port.A
RIGHT_MOTOR = port.E
EDGE_L      = port.F   # capteur couleur gauche  -> bord
EDGE_R      = port.D   # capteur couleur droite  -> bord
EYE         = port.B   # capteur distance        -> adversaire
BUMPER      = port.C   # capteur force           -> contact

# ============================================================
#  >>> LES CHIFFRES QUE L'ELEVE REGLE EN TESTANT <<<
#  Regle UN seul a la fois, lance un match, observe, ajuste.
# ============================================================
EDGE_LIGHT     = 50    # bord = reflexion AU-DESSUS de ce seuil (0-100, blanc = haut)
SEE_OPP_MM     = 360   # voit l'adversaire si plus proche que ca (mm)  (36 cm)
SEARCH_SPEED   = 400   # vitesse de recherche      (deg/s)
CRUISE_SPEED   = 650   # vitesse "sure" / controlee (deg/s)
ATTACK_SPEED   = 1000  # vitesse plein gaz          (deg/s)
PIVOT_MS       = 250   # duree du pivot du Judoka (= angle d'attaque)
PUSH_STALEMATE_MS = 700  # contact prolonge sans progres -> le Metamorphe contourne
# ============================================================

#  MODE : change juste ce mot pour tester un autre style
#  ->  "survivor" | "bulldozer" | "judoka" | "metamorphe" | "original"
MODE = "survivor"


# ---------- CAPTEURS (les "sens" du robot) ----------
def on_edge():
    # bord blanc vu par UN des deux capteurs ? -> danger de tomber
    return (color_sensor.reflection(EDGE_L) > EDGE_LIGHT or
            color_sensor.reflection(EDGE_R) > EDGE_LIGHT)

def opponent_mm():
    d = distance_sensor.distance(EYE)
    return 9999 if d < 0 else d          # -1 = rien vu -> tres loin

def sees_opponent():
    return opponent_mm() < SEE_OPP_MM


# ---------- REFLEXE COMMUN : ne pas tomber ----------
async def back_off():
    motor_pair.move(PAIR, 0, velocity=-ATTACK_SPEED)   # recule vite
    await runloop.sleep_ms(300)
    motor_pair.move(PAIR, 100, velocity=SEARCH_SPEED)  # tourne vers l'interieur
    await runloop.sleep_ms(350)


# ============================================================
#  MODE 0 : ORIGINAL - le RETOUR (~ reproduit le programme gagnant)
# ============================================================
async def original():
    motor_pair.move(PAIR, 0, velocity=600)
    while True:
        cF = color_sensor.color(EDGE_L)
        cD = color_sensor.color(EDGE_R)
        if cF in (color.WHITE, color.RED, color.BLUE) or cF is None:
            await motor_pair.move_for_degrees(PAIR, 360, 0, velocity=-800)
            await motor_pair.move_for_time(PAIR, 430, 100, velocity=800)
        elif cD in (color.WHITE, color.RED, color.BLUE) or cD is None:
            await motor_pair.move_for_time(PAIR, 400, -100, velocity=800)
        elif sees_opponent():
            motor_pair.move(PAIR, 0, velocity=1000)
        elif force_sensor.pressed(BUMPER):
            await motor_pair.move_for_degrees(PAIR, 720, 100, velocity=1000)
        else:
            motor_pair.move(PAIR, 0, velocity=750)
        await runloop.sleep_ms(1)


# ============================================================
#  MODE 1 : SURVIVOR (sur) - gagne en ne tombant JAMAIS
# ============================================================
async def survivor():
    while True:
        if on_edge():
            await back_off()
        elif sees_opponent():
            motor_pair.move(PAIR, 0, velocity=CRUISE_SPEED)
        else:
            motor_pair.move(PAIR, 30, velocity=SEARCH_SPEED)
        await runloop.sleep_ms(1)


# ============================================================
#  MODE 2 : BULLDOZER (agressif) - vitesse max, passe dessous
# ============================================================
async def bulldozer():
    motor_pair.move(PAIR, 0, velocity=ATTACK_SPEED)
    await runloop.sleep_ms(500)
    while True:
        if on_edge():
            await back_off()
        elif sees_opponent() or force_sensor.pressed(BUMPER):
            motor_pair.move(PAIR, 0, velocity=ATTACK_SPEED)
        else:
            motor_pair.move(PAIR, 20, velocity=ATTACK_SPEED)
        await runloop.sleep_ms(1)


# ============================================================
#  MODE 3 : JUDOKA (creatif) - esquive, attaque le FLANC
# ============================================================
async def judoka():
    while True:
        if on_edge():
            await back_off()
        elif sees_opponent():
            motor_pair.move(PAIR, 100, velocity=SEARCH_SPEED)
            await runloop.sleep_ms(PIVOT_MS)
            motor_pair.move(PAIR, 0, velocity=ATTACK_SPEED)
            await runloop.sleep_ms(400)
        else:
            motor_pair.move(PAIR, 30, velocity=SEARCH_SPEED)
        await runloop.sleep_ms(1)


# ============================================================
#  MODE 4 : METAMORPHE - s'ADAPTE en live
#  Honnete : il ne "devine" pas le type d'adversaire. Il REAGIT
#  aux signaux du moment et change de tactique. Defaut prudent.
# ============================================================
async def metamorphe():
    push_ms = 0
    while True:
        if on_edge():
            await back_off()
            push_ms = 0
        elif force_sensor.pressed(BUMPER):
            push_ms += 1
            if push_ms > PUSH_STALEMATE_MS:
                motor_pair.move(PAIR, -100, velocity=SEARCH_SPEED)
                await runloop.sleep_ms(180)
                motor_pair.move(PAIR, 100, velocity=ATTACK_SPEED)
                await runloop.sleep_ms(PIVOT_MS)
                motor_pair.move(PAIR, 0, velocity=ATTACK_SPEED)
                await runloop.sleep_ms(300)
                push_ms = 0
            else:
                motor_pair.move(PAIR, 0, velocity=ATTACK_SPEED)
        elif sees_opponent():
            push_ms = 0
            motor_pair.move(PAIR, 0, velocity=ATTACK_SPEED)
        else:
            push_ms = 0
            motor_pair.move(PAIR, 30, velocity=SEARCH_SPEED)
        await runloop.sleep_ms(1)


# ---------- DEMARRAGE ----------
async def main():
    motor_pair.pair(PAIR, LEFT_MOTOR, RIGHT_MOTOR)
    light_matrix.write(MODE[0].upper())
    await runloop.until(lambda: button.pressed(button.RIGHT) > 0)
    await runloop.sleep_ms(5000)
    if MODE == "original":
        await original()
    elif MODE == "bulldozer":
        await bulldozer()
    elif MODE == "judoka":
        await judoka()
    elif MODE == "metamorphe":
        await metamorphe()
    else:
        await survivor()

runloop.run(main())
