from heapq import heappop, heappush, heapify
from math import sqrt

class FrontierQueue():
    """docstring for Frontier"""
    def __init__(self):
        self.frontier = []
        self.cities = set()

    def __repr__(self):
        return str(self.frontier)

    def push(self, total_cost, path_cost, path):
        self.cities.add(path[-1])
        heappush(self.frontier, (total_cost, path_cost, path))

    def pop(self, index = None):
        if not index:
            total_cost, path_cost, path = heappop(self.frontier)
        else:
            total_cost, path_cost, path = self.frontier[index]
            self.frontier[index] = self.frontier[-1]
            self.frontier.pop()
            heapify(self.frontier)
        popped_city = path[-1]
        self.cities.remove(popped_city)
        return popped_city, total_cost, path_cost, path

    def lookup(self, city):
        index = 0
        for total_cost, path_cost, path in self.frontier:
            if path[-1] == city:
                return index, total_cost, path_cost, path
            index += 1
        return None, None, None

    def exists(self, city):
        if city in self.cities:
            return True
        return False

class RoutePlanner():
    """docstring for RoutePlanner"""
    def __init__(self):
        self.map = None
        self.cities = None
        self.neighbours = None
        self.frontier = None

    def import_map(self, M):
        self.map = M
        self.cities = M.intersections
        self.neighbours = M.roads

    def compute_distance(self, city_A, city_B):
        # Computes linear distance between 'city_A' and 'city_B'
        pos_A, pos_B = self.cities[city_A], self.cities[city_B]
        dist_x, dist_y = pos_A[0]-pos_B[0], pos_A[1]-pos_B[1]
        return sqrt(dist_x**2 + dist_y**2)

    def cost_function(self, prev_path_cost, cities):
        # Computes path costs and estimates residual cost for 'next_city'
        step_cost = self.compute_distance(cities[0], cities[1]) # (current_city, neighbour_city)
        path_cost = prev_path_cost + step_cost
        residual_cost = self.compute_distance(cities[1], cities[2]) # (neighbour_city, target_city)
        total_cost = path_cost + residual_cost # f = g + h
        return total_cost, path_cost

    def compute_shortest_path(self, start_city, target_city, map_plot):
        self.loop_count = 0
        # Initialize explore and frontier lists
        self.frontier = FrontierQueue()
        self.explored = [start_city]
        # Initialize loop variables
        current_city, current_path_cost, current_path = start_city, 0, [start_city]

        while current_city != target_city:
            #self.print_preliminary_results(current_city, current_path, current_path_cost)
            for neighbour_city in self.neighbours[current_city]:
                if neighbour_city not in self.explored:
                    # Estimate costs
                    cities = [current_city, neighbour_city, target_city]
                    total_cost, path_cost = self.cost_function(current_path_cost, cities)
                    neighbour_path = current_path + [neighbour_city]
                    # If neighbour already exists in frontier list, add new path only if cheaper
                    if self.frontier.exists(neighbour_city):
                        f_index, f_total_cost, f_path_cost, f_path = self.frontier.lookup(neighbour_city)
                        if (path_cost < f_path_cost):
                            self.frontier.pop(f_index)
                            self.frontier.push(total_cost, path_cost, neighbour_path)
                    else:
                        self.frontier.push(total_cost, path_cost, neighbour_path)

                # Visualization of search
                map_plot.highlight_nodes(start=start_city, goal=current_city, path=current_path)
            
            current_city, current_total_cost, current_path_cost, current_path = self.frontier.pop()
            self.explored.append(current_city)

        return current_path

    def print_preliminary_results(self, current_city, current_path, current_cost):
        print("\n########### Loop {} ########### ".format(self.loop_count))
        print("\nCurrent city: {}".format(current_city))
        print("\nCurrent path: {}, Current cost: {}".format(current_path, current_cost))
        print("\nExplored cities: {}".format(self.explored))
        print("\nFrontier cities: {}".format(self.frontier.cities))
        print("\nCurrent frontier: {}".format(self.frontier))
        self.loop_count += 1

