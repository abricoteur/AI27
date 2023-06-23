from hitman.hitman import HC, HitmanReferee, complete_map_example
from pprint import pprint


def phase1_run(hr):
    f = open("sat.cnf", "a")

    status = hr.turn_clockwise()
    print("\n=========== Status turn 1 ===========\n ")
    pprint(status)
    status = hr.turn_clockwise()
    print("\n=========== Status turn 2 ===========\n ")
    pprint(status)
    status = hr.turn_clockwise()
    print("\n=========== Status turn 3 ===========\n ")
    pprint(status)    
    status = hr.turn_clockwise()
    print("\n=========== Status turn 4 ===========\n ")
    pprint(status)
    status = hr.move()
    pprint(status)
    status = hr.move()
    pprint(status)
    status = hr.turn_clockwise()
    pprint(status)
    status = hr.move()
    pprint(status)
    status = hr.move()
    pprint(status)
    status = hr.move()
    pprint(status)
    status = hr.move()
    pprint(status)
    status = hr.turn_anti_clockwise()
    pprint(status)
    status = hr.move()
    pprint(status)
    status = hr.move()
    pprint(status)
    status = hr.turn_clockwise()
    pprint(status)
    status = hr.move()
    pprint(status)
    status = hr.turn_clockwise()
    pprint(status)
    status = hr.move()
    pprint(status)
    print("\n=========== Send content not complete map ===========\n ")
    # pprint(hr.send_content({(0, 0): HC.EMPTY}))
    print("\n=========== Send content true map ===========\n ")
    pprint(hr.send_content(complete_map_example))
    # complete_map_example[(7, 0)] = HC.EMPTY
    print("\n=========== Send content false map ===========\n ")
    # pprint(hr.send_content(complete_map_example))
    f.close()

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
    print(index, content)
    file.write("\n{} 0".format(((index-1) * 13) + content))
    return

def main():
    hr = HitmanReferee()

    status = hr.start_phase1()
    print("\n=========== Status 1 ===========\n ")
    pprint(status)
    global line
    global column
    line = status["m"]
    column = status["n"]

    for i in range(7):
        for j in range(6):
            init_sat(((i,j),1), open("sat.cnf", "a"))
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
