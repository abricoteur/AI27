from hitman.hitman import HC, HitmanReferee, complete_map_example
from pprint import pprint
import heapq
import sys
import subprocess

class Map :
    def __init__(self, m, n, hr) :
        self.directions = {(0, 1) : HC.N,  (1, 0): HC.E, (0, -1): HC.S , (-1, 0):HC.W}
        self.hr = hr
        self.lignes = m
        self.colonnes = n
        self.file = open("sat.cnf","w")
        self.file.write("p cnf 546 100\n")
        self.file = open("sat.cnf","a")
        self.total_case = m*n
        self.known_case = 0
        self.status = hr.turn_clockwise()
        self.map = {}
        self.heuristic_map = {}
        self.obstacles_coord = []
        self.weapon = None
        self.target = None
        self.suit = None
        self.heard_guard_map = {}
        self.last_position = None
        self.last_heard_guard_number = None
        for  i in range(self.colonnes) :
            for j in range(self.lignes) :
                self.map[(i,j)] = None
        for  i in range(self.colonnes) :
            for j in range(self.lignes) :
                self.heuristic_map[(i,j)] = 1
        self.look_around()
    
    def __getitem__(self, key):
        return self.map[key]
    
    def __setitem__(self, key, value):
        self.map[key] = value
    
    def __str__(self):
        return str(self.map)
    
    def __repr__(self):
        return str(self.map)
    
    def cost_to_turn(self,current, end_orientation):
        cardinal_order = [HC.N, HC.E, HC.S, HC.W, HC.N, HC.E, HC.S, HC.W]
        start_index = cardinal_order.index(current)
        end_index = cardinal_order.index(end_orientation, start_index)  # Start searching from start_index
        clockwise_turn = abs(end_index - start_index)
        counterclockwise_turn = 4 - clockwise_turn
        return min(clockwise_turn, counterclockwise_turn)

    
    def farthest_clockwise(self, direction):
        cardinal_order = [HC.N, HC.E, HC.S, HC.W, HC.N, HC.E, HC.S, HC.W]
        start_index = cardinal_order.index(direction)
        return cardinal_order[start_index + 3]
    
    
    def directions_to_turn(self) :  
        worth_turning = []
        x,y = self.status["position"]
        cardinal_order = [HC.N, HC.E, HC.S, HC.W, HC.N, HC.E, HC.S, HC.W]
        initial_orientation = self.status["orientation"]
        start_index = cardinal_order.index(initial_orientation)
        reference_order = cardinal_order[start_index + 1 : start_index + 4]
        
        expected_visions = {HC.E : [(x+1, y),(x+2, y),(x+3, y)], HC.N : [(x, y+1),(x, y+2),(x, y+3)], HC.W : [(x-1, y),(x-2, y),(x-3, y)], HC.S : [(x, y-1),(x, y-2),(x, y-3)]}
        for i in reference_order :
            compteur = 0
            for j in expected_visions[i] :
                nx, ny = j
                
                if not (0 <= nx < self.colonnes and 0 <= ny < self.lignes) or self.map[(nx,ny)] in [HC.WALL,HC.GUARD_E,HC.GUARD_N,HC.GUARD_S,HC.GUARD_W,HC.CIVIL_N,HC.CIVIL_E,HC.CIVIL_S,HC.CIVIL_W ,HC.TARGET,HC.SUIT,HC.PIANO_WIRE] :
                    break
                if self.map[(nx,ny)]==None :
                    compteur += 1
                if compteur >= 1 :
                    worth_turning.append(i)
                
        return worth_turning
                
                
    
    def look_around(self) :
             
        guard_in_front = None
        for value in self.status["vision"]:
            coord,element = value
            
            if self.map[coord] == None :
                self.init_sat(value)
                self.known_case += 1
            self.map[coord] = element
            if element == HC.PIANO_WIRE :
                self.weapon = coord
            if element == HC.TARGET :
                self.target = coord
            if element == HC.SUIT :
                self.suit = coord
            if element == HC.CIVIL_E or element == HC.CIVIL_N or element == HC.CIVIL_S or element == HC.CIVIL_W :
                self.feed_heuristic_map(coord, "OBSTACLE")
            if element == HC.GUARD_E or element == HC.GUARD_N or element == HC.GUARD_S or element == HC.GUARD_W :
                guard_in_front = element
                self.feed_heuristic_map(coord, element)
        
            

        if(self.status["is_in_guard_range"]):
            if guard_in_front is None:
                return
        
        directions_to_turn = self.directions_to_turn()
        farthest_clockwise = self.farthest_clockwise(self.status["orientation"])
        
        if(len(directions_to_turn)>0 and (directions_to_turn[0] and directions_to_turn[0] == farthest_clockwise) or (len(directions_to_turn)>1 and directions_to_turn[1] and directions_to_turn[1] == farthest_clockwise)) :
            for direction in directions_to_turn :
                while self.status["orientation"] != direction :
                    self.status = self.hr.turn_anti_clockwise()

                    for value in self.status["vision"]:
                        coord,element = value
                        if self.map[coord] == None :
                            self.init_sat(value)
                            self.known_case += 1
                        self.map[coord] = element
                        if element == HC.PIANO_WIRE :
                            self.weapon = coord
                        if element == HC.TARGET :
                            self.target = coord
                        if element == HC.SUIT :
                            self.suit = coord
                        if element == HC.CIVIL_E or element == HC.CIVIL_N or element == HC.CIVIL_S or element == HC.CIVIL_W or element == HC.SUIT or element == HC.PIANO_WIRE:
                            self.feed_heuristic_map(coord, "OBSTACLE")
                        if element == HC.GUARD_E or element == HC.GUARD_N or element == HC.GUARD_S or element == HC.GUARD_W :
                            self.feed_heuristic_map(coord, element)


        else : 
            for _ in  directions_to_turn :
                self.status = self.hr.turn_clockwise()
                   
                for value in self.status["vision"]:
                    coord,element = value
                    if self.map[coord] == None :
                        self.init_sat(value)
                        self.known_case += 1
                    self.map[coord] = element
                    if element == HC.PIANO_WIRE :
                        self.weapon = coord
                    if element == HC.TARGET :
                        self.target = coord
                    if element == HC.SUIT :
                        self.suit = coord
                    if element == HC.CIVIL_E or element == HC.CIVIL_N or element == HC.CIVIL_S or element == HC.CIVIL_W or element == HC.SUIT:
                        self.feed_heuristic_map(coord, "OBSTACLE")
                    if element == HC.GUARD_E or element == HC.GUARD_N or element == HC.GUARD_S or element == HC.GUARD_W :
                        self.feed_heuristic_map(coord, element)
                
                
    def is_fully_explored(self) :
        return self.known_case == self.total_case
    
    def get_valid_neighbors(self, position):
        (x, y) =  position
        voisins = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
        

        
        voisins_valide = []
        for (nx, ny) in voisins:
            
            if 0 <= nx < self.colonnes and 0 <= ny < self.lignes and not (self.map[(nx,ny)] in [HC.WALL,HC.GUARD_E,HC.GUARD_N,HC.GUARD_S,HC.GUARD_W]):  # Vérifie à l'intérieur du monde et pas un obstacle
                voisins_valide.append((nx, ny))
        return voisins_valide
    
    def a_star(self,start, goal):
        queue = []
        heapq.heappush(queue, (0, start))
        cases_parcourues = {start: None}
        cout_cumule = {start: 0}
        current_direction = self.status["orientation"]
        coord_to_direction = {
            (1, 0): HC.N,   # Moving up
            (-1, 0): HC.S,    # Moving down
            (0, -1): HC.W,   # Moving left
            (0, 1): HC.E     # Moving right
        }
        
        while queue:
            (priority, current) = heapq.heappop(queue)

            if current == goal or self.map[goal] in [2,3,4,5,6]:
                break
            
            for voisin in self.get_valid_neighbors(current):
                direction_change_cost = 0
                direction_change = current_direction
                if(current!= start):
                    direction_change = coord_to_direction[(voisin[0] - current[0], voisin[1] - current[1])]
                    direction_change_cost = self.cost_to_turn(current_direction, direction_change)
                if "is_suit_on" in self.status and self.status["is_suit_on"] == True:
                    nouveau_cout = cout_cumule[current] + 1 + direction_change_cost- 1
                else : nouveau_cout = cout_cumule[current] + self.heuristic_map[voisin] + direction_change_cost - 1
                if voisin not in cout_cumule or nouveau_cout < cout_cumule[voisin]:
                    cout_cumule[voisin] = nouveau_cout
                    current_direction = direction_change
                    priority = nouveau_cout + self.heuristic(goal, voisin)
                    heapq.heappush(queue, (priority, voisin))
                    cases_parcourues[voisin] = current

        # Reconstruction du chemin optimal
        chemin_optimal = []
        position = goal
        while position is not None:
            chemin_optimal.append(position)
            position = cases_parcourues[position]
        chemin_optimal.reverse()

        return chemin_optimal, cout_cumule[goal]
        
    
    def farthest_unknow_case(self):
        max_distance = -1
        farthest_unknow_case = None
        current_position = self.status["position"]
        for i in range(self.colonnes):
            for j in range(self.lignes):
                if self.map[(i, j)] is None:  # Si la case est non explorée
                    distance = abs(current_position[0] - i) + abs(current_position[1] - j)  # Distance de Manhattan
                    if distance > max_distance:
                        max_distance = distance
                        farthest_unknow_case = (i, j)
        return farthest_unknow_case
    
    def explore(self):
        
        while not self.is_fully_explored():
            objectif = self.farthest_unknow_case()
            while self.map[objectif] == None:
                chemin_optimal, cout_estime = self.a_star(self.status["position"], objectif )
                print("Chemin optimal : ",chemin_optimal)
                initial_position = self.status["position"]
                for i in chemin_optimal:
                    if i == initial_position:
                        continue
                    
                    direction_to_turn = self.directions[i[0]-self.status["position"][0],i[1]-self.status["position"][1]]
                    
                    while self.status["orientation"] != direction_to_turn:
                        if(self.farthest_clockwise(self.status["orientation"])==self.status["orientation"]):
                            self.status = self.hr.turn_anti_clockwise()
                        else : self.status = self.hr.turn_clockwise()
                    
                    if self.map[i] in [HC.WALL,HC.GUARD_E,HC.GUARD_N,HC.GUARD_S,HC.GUARD_W] :
                        break
                    self.status = self.hr.move()
                    self.look_around()
        self.file.write("\n")
        self.file.close()
        
    def go_to(self, objectif ) :
        
        chemin_optimal,_ = self.a_star(self.status["position"], objectif )
        
        initial_position = self.status["position"]
        print("Chemin optimal : ",chemin_optimal)
        for i in chemin_optimal:
            if i == initial_position:
                continue
            
            direction_to_turn = self.directions[i[0]-self.status["position"][0],i[1]-self.status["position"][1]]
            while self.status["orientation"] != direction_to_turn:
                        
                        if(self.farthest_clockwise(self.status["orientation"])==self.status["orientation"]):
                            self.status = self.hr.turn_anti_clockwise()
                        else : self.status = self.hr.turn_clockwise()
            
            if self.map[i] in [HC.WALL,HC.GUARD_E,HC.GUARD_N,HC.GUARD_S,HC.GUARD_W]:
                break
            self.status = self.hr.move()
            
    def heuristic(self, a, b):
        (x1, y1) = a
        (x2, y2) = b
        return abs(x1 - x2) + abs(y1 - y2)
    
    def feed_heuristic_map(self, position, element) :
        
        if element == "SAW" :
            self.heuristic_map[position] = 6
            return
        if element == "OBSTACLE" : 
            if position not in self.obstacles_coord :
                self.obstacles_coord.append(position)
            return
        
        (x,y) = position
        vision_field = {HC.GUARD_S : [(x-1, y),(x-2, y)],HC.GUARD_N : [(x+1, y),(x+2, y)],HC.GUARD_W : [(x, y-1),(x, y-2)], HC.GUARD_E : [(x, y+1),(x, y+2)]}
        for i in vision_field[element] :
            case = 0
            if i not in self.obstacles_coord or (case==0 and self.map[i] is not None and self.map[i]!=HC.WALL):
                self.heuristic_map[i] += 5
            else :
                print("Obstacle blocking vision field")
            case += 1

    def coord_to_index(self, x,y) :
        return (self.colonnes * (y+1)) - (self.colonnes - (x+1)) 

    def index_to_coord(self, index) :
        y = (index-1) /self.colonnes
        x = (index-1) //self.colonnes
        return (x, y)

    def init_sat(self, case) :
        index = self.coord_to_index(case[0][0], case[0][1])
        self.file.write("\n{} 0".format(((index-1) * 13) + case[1].value))
                

def main():
    hr = HitmanReferee()

    
    print("\n=========== Phase 1 : Status Initial ===========\n ")
    status = hr.start_phase1()
    pprint(status)
    print("\n=========== Phase 1 : Status Playing ===========\n ")
    game = Map(status['m'],status['n'],hr)
    game.explore()

    print("\n=========== Score ===========\n ")
    if(hr.send_content(game.map)) :
        print("Map is correct")
        print("Pénalités : ", str(game.status["penalties"]))
    _, score, history, true_map = hr.end_phase1()
    pprint(score)
    
    
    print("\n=========== Phase 2 : Status Initial ===========\n ")
    game.status = hr.start_phase2()
    print(game.status)
    
    print("\n=========== Phase 2 : Simulation Classique ===========\n ")
    
    cout_total_classique = 0
    _,cout = game.a_star(game.status["position"],game.weapon)
    cout_total_classique += cout
    print("Simulation Pénalité récupérer arme : " + str(cout_total_classique))
    _,cout = game.a_star(game.weapon, game.target)
    cout_total_classique += cout
    print("Simulation Pénalité tuer cible : " + str(cout_total_classique))
    _,cout = game.a_star(game.target, (0,0))
    cout_total_classique += cout
    print("Coût total classique : " + str(cout_total_classique))

    print("\n=========== Phase 2 : Status Playing ===========\n ")
    

    game.go_to(game.weapon)
    hr.take_weapon()
    print("Pénalité récupérer arme : " + str(game.status["penalties"]))
    game.go_to(game.target)
    hr.kill_target()
    print("Pénalité tuer cible : " + str(game.status["penalties"]))
    game.go_to((0,0))
    print("Pénalité fin de jeu : " + str(game.status["penalties"]))
        
    print("\n=========== Score 2 ===========\n ")
    result, score, history = hr.end_phase2()
    if result :
        print("Target killed, going back home !")
    pprint(score)
    
    print("\n=========== SAT ===========\n ")
    result = subprocess.run(["gophersat", "-verbose", "sat.cnf"])


if __name__ == "__main__":
    main()
