from hitman.hitman import HC, HitmanReferee, complete_map_example
from pprint import pprint


def phase1_run(hr):
    f = open("sat.cnf", "a")

    status = hr.turn_clockwise()
    print("\n=========== Status turn 1 ===========\n ")
    pprint(status)
    init_sat(status, f)
    status = hr.turn_clockwise()
    print("\n=========== Status turn 2 ===========\n ")
    pprint(status)
    init_sat(status, f)
    status = hr.turn_clockwise()
    print("\n=========== Status turn 3 ===========\n ")
    pprint(status)    
    init_sat(status, f)
    status = hr.turn_clockwise()
    print("\n=========== Status turn 4 ===========\n ")
    pprint(status)
    init_sat(status, f)
    status = hr.move()
    pprint(status)
    init_sat(status, f)
    status = hr.move()
    pprint(status)
    init_sat(status, f)
    status = hr.turn_clockwise()
    pprint(status)
    init_sat(status, f)
    status = hr.move()
    pprint(status)
    init_sat(status, f)
    status = hr.move()
    pprint(status)
    init_sat(status, f)
    status = hr.move()
    pprint(status)
    init_sat(status, f)
    status = hr.move()
    pprint(status)
    init_sat(status, f)
    status = hr.turn_anti_clockwise()
    pprint(status)
    init_sat(status, f)
    status = hr.move()
    pprint(status)
    init_sat(status, f)
    status = hr.move()
    pprint(status)
    init_sat(status, f)
    status = hr.turn_clockwise()
    pprint(status)
    init_sat(status, f)
    status = hr.move()
    pprint(status)
    init_sat(status, f)
    status = hr.turn_clockwise()
    pprint(status)
    init_sat(status, f)
    status = hr.move()
    pprint(status)
    init_sat(status, f)
    print("\n=========== Send content not complete map ===========\n ")
    # pprint(hr.send_content({(0, 0): HC.EMPTY}))
    print("\n=========== Send content true map ===========\n ")
    pprint(hr.send_content(complete_map_example))
    # complete_map_example[(7, 0)] = HC.EMPTY
    print("\n=========== Send content false map ===========\n ")
    # pprint(hr.send_content(complete_map_example))
    f.close()


def coord_to_index(x,y) :
    index = x + y
    return index

def index_to_coord(index) :
    x = index
    y = index
    return (x,y)

def init_sat(status, file) :
    for case in status.vision :
        index = case[0]
    file.write("0 0 0 \n")
    return


def main():
    hr = HitmanReferee()

    status = hr.start_phase1()
    print("\n=========== Status 1 ===========\n ")
    pprint(status)
    phase1_run(hr)
    _, score, history, true_map = hr.end_phase1()

    print("\n=========== Score ===========\n ")
    pprint(score)
    print("\n=========== True Map ===========\n ")
    pprint(true_map)
    print("\n=========== History ===========\n ")
    pprint(history)


if __name__ == "__main__":
    main()
