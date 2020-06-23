from map_helpers import load_map

from route_finder import RoutePlanner

MAP_40_TEST_CASES = [
    (5, 34, [5, 16, 37, 12, 34]),
    (5, 5,  [5]),
    (8, 24, [8, 14, 16, 37, 12, 17, 10, 24])
]

def test(route_planner, test_cases):
    correct = 0
    for start, goal, answer_path in test_cases:
        path = route_planner.compute_shortest_path(start, goal)
        if path == answer_path:
            print("\nShortest path from {} to {} is:\n{}".format(start, goal, path))
            correct += 1
        else:
            print("For start:", start, 
                  "Goal:     ", goal,
                  "Your path:", path,
                  "Correct:  ", answer_path)
    if correct == len(test_cases):
        print("\nAll tests pass!")
    else:
        print("\nYou passed", correct, "/", len(test_cases), "test cases")


if __name__ == "__main__":
    map_40 = load_map('map-40.pickle')
    route_planner = RoutePlanner()
    route_planner.import_map(map_40)
    test(route_planner, MAP_40_TEST_CASES)
    