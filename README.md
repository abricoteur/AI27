# RAPPORT PROJET AI27
##### Mennessier Lucas - Li Alix
***
### Modélisation STRIPS


##### Fluents
***

    On(a, X), Empty(x), Item(a, Hitman)

##### Etat initial
***

    Init(Case((0,0)) ∧ Case(0,1) ∧ ... Case(0,5) ∧ 
     Case(1,0) ∧ Case(1,1) ∧ ... ∧ Case(1,5) ∧
     Case(2,0) ∧ Case(2,1) ∧ ... ∧ Case(2,5) ∧
     Case(3,0) ∧ Case(3,1) ∧ ... ∧ Case(3,5) ∧
     Case(4,0) ∧ Case(4,1) ∧ ... ∧ Case(4,5) ∧
     Case(5,0) ∧ Case(5,1) ∧ ... ∧ Case(5,5) ∧
     Case(6,0) ∧ Case(6,1) ∧ ... ∧ Case(6,5) ∧

     Adjacent(Case1,case2) pour tout Case1(x1,y1), Case2(x2,y2) où |x1-x2| = 1 ou |y1-y2| = 1 
     
     On(Hitman_N,(1,0)) ∧ On(Suit,(3,5)) ∧ On(Guard_S,(4,5)) ∧ On(Guard_E,(3,2)) ∧ On(Civil_N,(5,2)) ∧ On(Civil_E,(5,3)) ∧ On(Civil_O,(6,2)) ∧ On(Piano,(5,0)) ∧ On(Target,(0,3))

     On(Wall,(0,2)) ∧ On(Wall,(1,2)) ∧ On(Wall,(1,3)) ∧ On(Wall,(1,4)) ∧ On(Wall,(2,0)) ∧
     On(Wall,(3,0)) ∧ On(Wall,(5,5)) ∧ On(Wall,(6,5))

     Empty(0,0) ∧ Empty(0,1) ∧ Empty(0,4) ∧ Empty(0,5) ∧ Empty(1,5) ∧ Empty(1,1) ∧ Empty(2,1) ∧ Empty(2,2) ∧ Empty(2,2) ∧ Empty(2,3) ∧ Empty(2,4) ∧ Empty(2,5) ∧ 
     Empty(3,1) ∧ Empty(3,3) ∧ Empty(3,4) ∧ Empty(4,0) ∧ Empty(4,1) ∧ Empty(4,2) ∧ Empty(4,3) ∧ Empty(4,4) ∧ Empty(5,1) ∧ Empty(5,4) ∧ Empty(6,0) ∧ Empty(6,1) ∧
     Empty(6,3) ∧ Empty(6,4) ∧ 
     )

##### But
***

    ¬On(Target, (x, y))

##### Actions
***

    Action(Turn_horaire_N(a))
    Precond:
        Hitman_N(a)
    Effect :
        Hitman_E(a) ∧ ¬Hitman_N(a)

    Action(Turn_horaire_E(a))
    Precond:
        Hitman_E(a)
    Effect :
        Hitman_S(a) ∧ ¬Hitman_E(a)

    Action(Turn_horaire_W(a))
    Precond:
        Hitman_W(a)
    Effect :
        Hitman_N(a) ∧ ¬Hitman_W(a)

        Action(Turn_horaire_S(a))
    Precond:
        Hitman_S(a)
    Effect :
        Hitman_W(a) ∧ ¬Hitman_S(a)

    Action(Turn_antihoraire_N(a))
    Precond:
        Hitman_N(a)
    Effect :
        Hitman_W(a) ∧ ¬Hitman_N(a)

    Action(Turn_antihoraire_W(a))
    Precond:
        Hitman_W(a)
    Effect :
        Hitman_S(a) ∧ ¬Hitman_W(a)

    Action(Turn_antihoraire_N(a))
    Precond:
        Hitman_S(a)
    Effect :
        Hitman_E(a) ∧ ¬Hitman_S(a)

    Action(Turn_antihoraire_E(a))
    Precond:
        Hitman_E(a)
    Effect :
        Hitman_N(a) ∧ ¬Hitman_E(a)

    Action(Move_N(a,x,y))
    Precond :
        North(y,x) ∧ Hitman_N(a) ∧ case(x) ∧ case(y) ∧ Adjacent(x,y) ∧ (Empty(y) v Civil_N(y) v Civil_S(y) v Civil_O(y) v Civi_E(y))
    Effect :
        On(Hitman_N, y) ∧ ¬Empty(y) ∧ Empty(x)

    Action(Move_W(a,x,y))
    Precond :
        West(y,x) ∧ Hitman_W(a) ∧ case(x) ∧ case(y) ∧ Adjacent(x,y) ∧ (Empty(y) v Civil_N(y) v Civil_S(y) v Civil_O(y) v Civi_E(y))
    Effect :
        On(Hitman_W, y) ∧ ¬Empty(y) ∧ Empty(x)

    Action(Move_E(a,x,y))
    Precond :
        East(y,x) ∧ Hitman-E(a) ∧ case(x) ∧ case(y) ∧ Adjacent(x,y) ∧ (Empty(y) v Civil_N(y) v Civil_S(y) v Civil_O(y) v Civi_E(y))
    Effect :
        On(Hitman_E, y) ∧ ¬Empty(y) ∧ Empty(x)

    Action(Move_S(a,x,y))
    Precond :
        South(y,x) ∧ Hitman_S(a) ∧ case(x) ∧ case(y) ∧ Adjacent(x,y) ∧ (Empty(y) v Civil_N(y) v Civil_S(y) v Civil_O(y) v Civi_E(y))
    Effect :
        On(Hitman_S, y) ∧ ¬Empty(y) ∧ Empty(x)

    Action(pick_up(item,x,y))
    Precond : 
        (On(Hitman_N,(x, y)) v On(Hitman_E,(x, y)) v On(Hitman_W,(x, y)) v On(Hitman_S,(x, y))) ∧ On(item, (x, y))
    Effect : 
        ¬On(item, (x,y)) ∧ Item(item, Hitman)

    Action(Kill_N(x,y)) :
    Precond : 
        (On(Hitman_N,(x, y-1)) v On(Hitman_E,(x-1, y)) v On(Hitman_W,(x+1, y))) ∧ (On(Civil_N,(x,y)) v On(Guard_N,(x,y)))
    Effect : 
        ¬On(Civil_N,(x, y)) ∧ ¬On(Guard_N,(x, y)) ∧ Empty(x,y)

    Action(Kill_S(x,y)) :
    Precond : 
        (On(Hitman_E,(x-1, y)) v On(Hitman_W,(x+1, y)) v On(Hitman_S,(x, y+1))) ∧ (On(Civil_S,(x,y)) v On(Guard_S,(x,y)))
    Effect : 
        ¬On(Civil_S,(x, y)) ∧ ¬On(Guard_S,(x, y)) ∧ Empty(x,y)

     Action(Kill_E(x,y)) :
    Precond : 
        (On(Hitman_N,(x, y-1)) v On(Hitman_E,(x-1, y)) v On(Hitman_S,(x, y+1))) ∧ (On(Civil_E,(x,y)) v On(Guard_E,(x,y)))
    Effect : 
        ¬On(Civil_E,(x, y)) ∧ ¬On(Guard_E,(x, y)) ∧ Empty(x,y)

    Action(Kill_W(x,y)) :
    Precond : 
        (On(Hitman_N,(x, y-1)) v On(Hitman_W,(x+1, y)) v On(Hitman_S,(x, y+1))) ∧ (On(Civil_W,(x,y)) v On(Guard_W,(x,y)))
    Effect : 
        ¬On(Civil_W,(x, y)) ∧ ¬On(Guard_W,(x, y)) ∧ Empty(x,y)

    Action(kill_target(a,x,y))
    Precond : 
        Hitman(a) ∧ (On(Hitman_N,(x, y)) v On(Hitman_E,(x, y)) v On(Hitman_W,(x, y)) v On(Hitman_S,(x, y))) ∧ On(Target,(x, y)) ∧ Item(item, Hitman)
    Effect : 
        ¬On(Target,(x,y))

***
### Fonctionnement du projet

Pour faire fonctionner notre projet, il suffira simplement d'exécuter le script main.py.
Celui-ci lancera les deux phases de jeu en affichant les principales informations liée à la partie en cours.
Il se chargera également de créer un fichier au format DIMACS (sat.cnf) dont les clauses correspondent aux informations recueuillies durant la partie.
Le fichier sat.cnf sera par la suite résolu par un solveur SAT (gophersat.exe).

***
### Forces de notre programme
***
### Faiblesses de notre programme
