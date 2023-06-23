from hitman.hitman import HC, HitmanReferee, complete_map_example
from pprint import pprint


def phase1_run(hr):
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
    # pprint(hr.send_content({(0, 0): HC.EMPTY}))
    pprint(hr.send_content(complete_map_example))
    # complete_map_example[(7, 0)] = HC.EMPTY
    # pprint(hr.send_content(complete_map_example))


def phase2_run(hr):
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
    status = hr.neutralize_guard()
    pprint(status)
    status = hr.turn_anti_clockwise()
    pprint(status)
    status = hr.neutralize_guard()
    pprint(status)
    status = hr.turn_clockwise()
    pprint(status)
    status = hr.turn_clockwise()
    pprint(status)
    status = hr.neutralize_civil()
    pprint(status)
    status = hr.turn_clockwise()
    pprint(status)
    status = hr.move()
    pprint(status)
    status = hr.move()
    pprint(status)
    status = hr.turn_anti_clockwise()
    pprint(status)
    status = hr.take_weapon()
    pprint(status)
    status = hr.move()
    pprint(status)
    status = hr.take_weapon()
    pprint(status)
    status = hr.turn_clockwise()
    pprint(status)
    status = hr.turn_clockwise()
    pprint(status)
    status = hr.move()
    pprint(status)
    status = hr.turn_clockwise()
    pprint(status)
    status = hr.move()
    pprint(status)
    status = hr.turn_anti_clockwise()
    pprint(status)
    status = hr.move()
    pprint(status)
    status = hr.turn_clockwise()
    pprint(status)
    status = hr.neutralize_guard()
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
    status = hr.move()
    pprint(status)
    status = hr.turn_anti_clockwise()
    pprint(status)
    status = hr.move()
    pprint(status)
    status = hr.move()
    pprint(status)
    status = hr.kill_target()
    pprint(status)
    status = hr.turn_anti_clockwise()
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
    status = hr.move()
    pprint(status)
    status = hr.turn_clockwise()
    pprint(status)
    pprint(hr.end_phase2())
    status = hr.move()
    pprint(status)
    status = hr.move()
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
    status = hr.turn_anti_clockwise()
    pprint(status)
    status = hr.move()
    pprint(status)


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

    # status = hr.start_phase2()
    # print("\n=========== Status 2 ===========\n ")
    # pprint(status)
    # phase2_run(hr)
    # _, score, history = hr.end_phase2()
    # print("\n=========== Score 2 ===========\n ")
    # pprint(score)
    # print("\n=========== History 2 ===========\n ")
    # pprint(history)


if __name__ == "__main__":
    main()