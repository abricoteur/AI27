from hitman.hitman import HC, HitmanReferee, complete_map_example
from pprint import pprint
import heapq

class Map :
    def __init__(self, m, n, hr) :
        self.directions = {(0, 1) : HC.N,  (1, 0): HC.E, (0, -1): HC.S , (-1, 0):HC.W}
        self.hr = hr
        self.lignes = m
        self.colonnes = n
        self.total_case = m*n
        self.known_case = 0
        self.status = hr.turn_clockwise()
        self.map = {}
        self.heuristic_map = {}
        self.civils_coord = []
        self.weapon = None
        self.target = None
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
    
    def look_around(self) :
        for _ in range(4) :
            self.status = self.hr.turn_clockwise()
            for value in self.status["vision"]:
                coord,element = value
                
                if self.map[coord] == None :
                    self.known_case += 1
                self.map[coord] = element
                if element == HC.PIANO_WIRE :
                    self.weapon = coord
                if element == HC.TARGET :
                    self.target = coord
                if element == HC.CIVIL_E or element == HC.CIVIL_N or element == HC.CIVIL_S or element == HC.CIVIL_W :
                    self.feed_heuristic_map(coord, "CIVIL")
                if element == HC.GUARD_E or element == HC.GUARD_N or element == HC.GUARD_S or element == HC.GUARD_W :
                    self.feed_heuristic_map(coord, "GUARD")
                
                
    def is_fully_explored(self) :
        pprint("Cases connues : " + str(self.known_case) + " / " + str(self.total_case))
        return self.known_case == self.total_case
    
    def get_neighbors(self, position):
        (x, y) =  position
        voisins = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
        
        if self.status["position"] == (x, y):
            print("Looking around...")
            self.look_around()
        
        voisins_valide = []
        for (nx, ny) in voisins:
            
            if 0 <= nx < self.colonnes and 0 <= ny < self.lignes and not (self.map[(nx,ny)] in [HC.WALL,HC.GUARD_E,HC.GUARD_N,HC.GUARD_S,HC.GUARD_W]):  # Vérifie à l'intérieur du monde et pas un obstacle
                voisins_valide.append((nx, ny))
        return voisins_valide
    
    def a_star(self, goal):
        
        start = self.status["position"]
        queue = []
        heapq.heappush(queue, (0, start))
        cases_parcourues = {start: None}
        cout_cumule = {start: 0}
        
        while queue:
            (priority, current) = heapq.heappop(queue)

            if current == goal or self.map[goal] in [2,3,4,5,6]:
                break
            
            for voisin in self.get_neighbors(current):
                nouveau_cout = cout_cumule[current] + self.heuristic_map[voisin]
                if voisin not in cout_cumule or nouveau_cout < cout_cumule[voisin]:
                    cout_cumule[voisin] = nouveau_cout
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

        return chemin_optimal
        
    
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
                chemin_optimal = self.a_star(objectif)
                initial_position = self.status["position"]
                print(chemin_optimal)
                for i in chemin_optimal:
                    if i == initial_position:
                        continue
                    
                    print("Actual Position : " + str(self.status["position"]))
                    print("Next Position : " + str(i))
                    while self.status["orientation"] != (self.directions[i[0]-self.status["position"][0],i[1]-self.status["position"][1]]):
                        self.status = self.hr.turn_clockwise()
                    
                    print(self.map[i])
                    if self.map[i] in [HC.WALL,HC.GUARD_E,HC.GUARD_N,HC.GUARD_S,HC.GUARD_W]:
                        break
                    self.status = self.hr.move()
                    self.look_around()
                    print("Moved to :"+ str(self.status["position"]))
        
    def go_to(self, objectif ) :
        
        chemin_optimal = self.a_star(objectif)
        print(chemin_optimal)
        
        initial_position = self.status["position"]
        for i in chemin_optimal:
            if i == initial_position:
                continue
            
            print("Actual Position : " + str(self.status["position"]))
            print("Next Position : " + str(i))
            while self.status["orientation"] != (self.directions[i[0]-self.status["position"][0],i[1]-self.status["position"][1]]):
                self.status = self.hr.turn_clockwise()
            
            if self.map[i] in [HC.WALL,HC.GUARD_E,HC.GUARD_N,HC.GUARD_S,HC.GUARD_W]:
                break
            self.status = self.hr.move()
            self.look_around()
            print("Moved to :"+ str(self.status["position"]))
            
    def heuristic(self, a, b):
        (x1, y1) = a
        (x2, y2) = b
        return abs(x1 - x2) + abs(y1 - y2)
    
    def feed_heuristic_map(self, position, element) :
        if element == "CIVIL" :
            self.civils_coord.append(position)
            return
        (x,y) = position
        vision_field = [(x-1, y),(x-2, y), (x+1, y),(x+2, y), (x, y-1),(x, y-2), (x, y+1),(x, y+2)]
        for i in vision_field :
            if i not in self.civils_coord :
                self.heuristic_map[i] = 6






    
    
    #f = open("sat.cnf", "a")
    
    #print("\n=========== Status turn 1 ===========\n ")
    # init_sat(status, f)
    
    
    # print("\n=========== Send content not complete map ===========\n ")
    # pprint(hr.send_content({(0, 0): HC.EMPTY}))
    # print("\n=========== Send content true map ===========\n ")
    # pprint(hr.send_content(complete_map_example))
    # complete_map_example[(7, 0)] = HC.EMPTY
    #print("\n=========== Send content false map ===========\n ")
    #pprint(hr.send_content(complete_map_example))
    #f.close()

column = None
line = None

def coord_to_index(x,y) :
    return (column * (y+1)) - (column - (x+1)) 

def index_to_coord(index) :
    y = (index-1) /column
    x = (index-1) //column
    return (x, y)

def init_sat(case, file) :
    index = coord_to_index(case[0][0], case[0][1])
    content = case[1]
    file.write("\n{} 0".format(((index-1) * 13) + content))
    return

def main():
    hr = HitmanReferee()

    
    print("\n=========== Phase 1 : Status Initial ===========\n ")
    status = hr.start_phase1()
    pprint(status)
    print("\n=========== Phase 1 : Status Initialize Map ===========\n ")
    game = Map(status['m'],status['n'],hr)
    game.explore()

    print("\n=========== Score ===========\n ")
    if(hr.send_content(game.map)) :
        print("Map is correct")
    _, score, history, true_map = hr.end_phase1()
    pprint(score)
    
    
    print("\n=========== Phase 2 : Status Initial ===========\n ")
    game.status = hr.start_phase2()
    pprint(game.status)
    print("\n=========== Phase 2 : Status Playing ===========\n ")
    print(game.weapon)
    game.go_to(game.weapon)
    hr.take_weapon()
    game.go_to(game.target)
    hr.kill_target()
    game.go_to((0,0))

    print("\n=========== Score 2 ===========\n ")
    result, score, history = hr.end_phase2()
    if result :
        print("Target killed, going back home !")
    pprint(score)
    
    
    

    
    
    # _, score, history, true_map = hr.end_phase1()

    # print("\n=========== Score ===========\n ")
    # pprint(score)
    # print("\n=========== True Map ===========\n ")
    # pprint(true_map)
    # print("\n=========== History ===========\n ")
    # pprint(history)

    result = subprocess.run(["gophersat", "-verbose", "test.cnf"])

    # phase1_run(hr)
    #_, score, history, true_map = hr.end_phase1()

    #print("\n=========== Score ===========\n ")
    #pprint(score)
    #print("\n=========== True Map ===========\n ")
    #pprint(true_map)
    #print("\n=========== History ===========\n ")
    #pprint(history)"""

if __name__ == "__main__":
    main()
