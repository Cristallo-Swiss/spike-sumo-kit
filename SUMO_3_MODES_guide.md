# SUMO BOT — 4 modes 🤖
### LEGO SPIKE Prime — à CONSTRUIRE en blocs (pas à copier bêtement)

**But du jeu :** pousser l'adversaire hors du cercle SANS tomber soi-même.
**Règle clé :** le robot doit attendre **5 secondes** après le départ avant de bouger.

Le robot a déjà tout :
| Pièce | Rôle |
|---|---|
| Moteurs **A + E** | déplacement |
| Capteurs couleur **F + D** | **détecteurs de BORD** (voient la ligne blanche) |
| Capteur distance **B** | **détecteur d'ADVERSAIRE** |
| Capteur force **C** | **pare-chocs** (sait quand il pousse) |

---

## 🧱 LE SQUELETTE (commun aux modes)

> L'élève construit ça UNE fois, puis il change juste le "cerveau" (le `forever`).

```
when [right] button pressed
  set movement motors to  A+E
  set movement acceleration to  fast
  wait 5 seconds              <-- règle sumo (obligatoire !)
  forever
      ┌── LE CERVEAU (change selon le mode, voir plus bas)
      └──
```

**La règle d'or, dans TOUS les modes :** le tout **premier** `if` du `forever` teste
le **BORD** (capteurs F ou D voient le blanc) → recule + tourne.
> 👉 Indice à l'élève : *« Pourquoi le bord doit-il être vérifié en PREMIER et pas en dernier ? »*
> (réponse à trouver : si tu attaques d'abord, tu tombes avant d'avoir vérifié le sol.)

Le réflexe anti-chute (le « back off »), à mettre dans chaque mode :
```
move  ↓ (back)  fast , for a short time
then turn  (right)  for a short time   <-- revient vers le centre
```

---

## 🛡️ MODE 1 — SURVIVOR (le sûr)
*« Je gagne parce que je ne tombe JAMAIS. »* — bat les fonceurs qui se suicident.

```
forever
  if  < F or D see WHITE (edge) >  then
      back off + turn            # priorité absolue
  else if  < B closer than 36 cm >  then
      start moving up  at  CRUISE speed (~65%)   # pousse, mais contrôlé
  else
      start moving  turning slowly               # cherche l'adversaire
```

---

## ⚡ MODE 2 — BULLDOZER (l'agressif)
*« Vitesse max, je passe dessous, je pousse avant qu'il réagisse. »* — bat les lourds/lents.

```
when started (après les 5 s) :
  move straight at FULL speed for 0.5 s     # le LUNGE de départ : les 0.5 s décident

forever
  if  < F or D see WHITE (edge) >  then
      back off + turn            # filet de sécurité, réaction ULTRA rapide
  else if  < B closer than 36 cm >  OR  < C is pressed >  then
      start moving up at FULL speed          # PLEIN GAZ tant qu'il touche
  else
      start moving  turning fast             # cherche vite
```
> ⚠️ Indice : *« Le Bulldozer peut sortir tout seul s'il rate. Comment règle-t-on
> le seuil du bord pour qu'il freine à temps SANS freiner trop tôt ? »*

---

## 🥋 MODE 3 — JUDOKA (le créatif)
*« Jamais de face. J'esquive et je frappe le CÔTÉ. »* — bat les plus FORTS par le placement.

```
forever
  if  < F or D see WHITE (edge) >  then
      back off + turn
  else if  < B closer than 36 cm >  then
      turn  (right)  for a SHORT time        # 1) prend un angle (esquive)
      then move straight at FULL speed for 0.4 s   # 2) charge le flanc
  else
      start moving  turning slowly           # cherche
```
> Pourquoi ça marche : un robot poussé **de côté** n'a aucune traction pour résister.
> 👉 Indice : *« L'angle du pivot, c'est tout le secret. Trop petit = tu le pousses
> de face (tu perds). Trop grand = tu le rates. Trouve-le en testant. »*

---

## 🦎 MODE 4 — MÉTAMORPHE (l'adaptatif)
*« Je ne devine pas qui est l'adversaire. Je réagis aux signaux du moment. »*

**Honnêteté pédago :** avec juste un capteur distance + un pare-chocs, le robot ne peut pas
« reconnaître le type de robot en face ». Par contre il peut **sentir ce qui se passe** :
- il touche et ça avance ? → il pousse comme un Bulldozer
- il touche et ça bloque depuis longtemps ? → il décroche et contourne comme un Judoka
- il est au bord ? → il devient Survivant (priorité absolue)
- il voit la cible ? → il fonce
- il ne voit rien ? → il cherche

```
forever
  if  < F or D see WHITE (edge) >  then
      back off + turn                        # SURVIVANT : ne tombe pas
  else if  < C is pressed >  then
      if  < contact dure depuis longtemps >  then
          turn away + pivot + charge side    # JUDOKA : contourne
      else
          move straight at FULL speed        # BULLDOZER : pousse fort
  else if  < B closer than 36 cm >  then
      start moving up at FULL speed          # cible vue -> fonce
  else
      start moving turning slowly            # cherche
```

> ⚠️ Indice : *« Le triangle Survivant/Bulldozer/Judoka (pierre-feuille-ciseaux) c'est une
> belle histoire pour apprendre, PAS une loi physique. Le Métamorphe ne promet pas de gagner :
> il essaie juste de ne pas rester coincé dans une tactique qui marche mal. »*

---

## 🎛️ LES CHIFFRES QUE L'ÉLÈVE DOIT TROUVER LUI-MÊME
*(c'est ÇA, apprendre — on donne la structure, il trouve les nombres)*

| Réglage | Effet | Méthode |
|---|---|---|
| **Seuil de distance B** (ex. 36 cm) | trop grand → fonce sur du vide ; trop petit → réagit trop tard | teste contre un robot immobile |
| **Vitesse** (%) | poussée ↔ contrôle | monte jusqu'à ce qu'il dérape, puis redescends un cran |
| **Temps de "back off"** | trop court → re-tombe ; trop long → perd du temps | observe sur le ring |
| **Angle du pivot** (Judoka) | rate vs frappe de face | le réglage le plus fin |
| **Temps de stalemate** (Métamorphe) | trop court → panique ; trop long → reste coincé | quand la poussée bloque |

**Règle d'apprentissage :** on change **UN seul** chiffre à la fois, on lance un match, on observe. Sinon on comprend rien.

---

## 🧪 COMMENT TESTER (tournoi interne)
1. Construire le **Survivor** d'abord (c'est la fondation : l'anti-chute).
2. Le copier 2× → en faire un **Bulldozer** et un **Judoka**.
3. Les faire combattre **l'un contre l'autre** → l'élève voit en vrai quel style gagne et pourquoi.
4. Quand les 3 marchent, essayer le **Métamorphe** — mais en vendant la vérité : il réagit, il ne devine pas.
5. Garder celui qui gagne pour le tournoi, et savoir **l'expliquer au juge**.

---

## 🆘 Dernier recours
Si vraiment il bloque : le fichier **`sumo_3_modes.py`** (même dossier) contient les 4 modes
prêts à tourner en **Python dans l'app SPIKE**. On change le mot `MODE = "survivor"` en haut
pour tester un autre style (`survivor`, `bulldozer`, `judoka`, `metamorphe`). *(Mais l'objectif reste : il le construit lui-même.)*

---
*Préparé par équipe Cristallo — 22 juin 2026*
