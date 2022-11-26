import random


class Ant:
    def __init__(self, number_of_nodes):
        self.visited_nodes = [random.randint(0, number_of_nodes - 1)]

    def visit_node(self, nodes, pheromones, random_movement_chance, alpha, beta):
        if random_movement_chance >= random.random():
            self._visit_random_node(len(nodes))
        else:
            self._visit_probabilistically_node(nodes, pheromones, alpha, beta)

    def _visit_random_node(self, number_of_nodes):
        all_nodes = list(range(number_of_nodes))
        available_nodes = [x for x in all_nodes if x not in self.visited_nodes]
        self.visited_nodes.append(random.choice(available_nodes))

    def _visit_probabilistically_node(self, nodes, pheromones, alfa, beta):
        active_node = self.visited_nodes[-1]
        all_nodes = list(range(len(nodes)))
        available_nodes = [x for x in all_nodes if x not in self.visited_nodes]

        index_list = []
        probability_list = []

        for node in available_nodes:
            index_list.append(node)
            pheromone = pow(pheromones[active_node][node], alfa)
            heuristics = pow(1 / nodes[active_node][node], beta)
            probability = pheromone * heuristics
            probability_list.append(probability)

        probability_sum = sum(probability_list)

        probability_list = [x / probability_sum for x in probability_list]
        selection = self._roulette_selection(index_list, probability_list, len(available_nodes))
        self.visited_nodes.append(selection[0])

    @staticmethod
    def _roulette_selection(index_list, probability_list, number_of_available_nodes):
        sections = []
        probability_sum = 0
        for i in range(number_of_available_nodes):
            sections.append([index_list[i], probability_sum, probability_sum + probability_list[i]])
            probability_sum += probability_list[i]

        random_number = random.random()
        for section in sections:
            if section[1] < random_number <= section[2]:
                return section

    def get_distance_traveled(self, nodes):
        distance_traveled = 0
        for i in range(1, len(self.visited_nodes)):
            distance_traveled += nodes[self.visited_nodes[i - 1]][self.visited_nodes[i]]

        return distance_traveled


class AntColony:
    def __init__(self, number_of_nodes, ants_multiplayer, evaporation_rate, random_movement_chance, alpha, beta):
        self.ants_multiplayer = ants_multiplayer
        self.evaporation_rate = evaporation_rate
        self.random_movement_chance = random_movement_chance
        self.alpha = alpha
        self.beta = beta
        self.ants = []
        self.best_ant = None
        self.pheromones = [[1 for _ in range(number_of_nodes)] for _ in range(number_of_nodes)]

    def create_ants(self, number_of_nodes):
        number_of_ants = int(number_of_nodes * self.ants_multiplayer)
        ants = []
        for i in range(number_of_ants):
            ants.append(Ant(number_of_nodes))

        self.ants = ants

    def move_ants(self, nodes):
        for ant in self.ants:
            ant.visit_node(nodes, self.pheromones, self.random_movement_chance, self.alpha, self.beta)

    def update_pheromones(self, nodes):
        number_of_nodes = len(nodes)
        for x in range(number_of_nodes):
            for y in range(number_of_nodes):
                self.pheromones[x][y] = self.pheromones[x][y] * self.evaporation_rate
        for ant in self.ants:
            add_pheromone = 1 / ant.get_distance_traveled(nodes)
            for i in range(1, len(ant.visited_nodes)):
                from_node = ant.visited_nodes[i - 1]
                to_node = ant.visited_nodes[i]

                self.pheromones[from_node][to_node] = add_pheromone + self.pheromones[from_node][to_node]

    def get_best_route(self, nodes):
        for ant in self.ants:
            if self.best_ant is None:
                self.best_ant = ant
            else:
                distance_traveled = ant.get_distance_traveled(nodes)
                if distance_traveled < self.best_ant.get_distance_traveled(nodes):
                    self.best_ant = ant

        return [self.best_ant.visited_nodes, self.best_ant.get_distance_traveled(nodes)]


def start(ant_colony, nodes, number_of_iterations=100):
    node_len = len(nodes)
    best_route = None
    for i in range(number_of_iterations):
        try:
            ant_colony.create_ants(node_len)
            for j in range(node_len - 1):
                ant_colony.move_ants(nodes)
            ant_colony.update_pheromones(nodes)
            best_route = ant_colony.get_best_route(nodes)
        except ZeroDivisionError:
            # print(i)
            ant_colony.pheromones = [[1 for _ in range(len(nodes))] for _ in range(len(nodes))]

    # for row in ant_colony.pheromones:
    #     print(row)

    return best_route


if __name__ == '__main__':
    my_nodes = [[0, 8, 7, 4, 6, 4],
                [8, 0, 5, 7, 11, 5],
                [7, 5, 0, 9, 6, 7],
                [4, 7, 9, 0, 5, 6],
                [6, 11, 6, 5, 0, 3],
                [4, 5, 6, 6, 3, 0]]

    my_ant_colony = AntColony(len(my_nodes), 0.5, 0.4, 0.3, 2, 3)
    print(start(my_ant_colony, my_nodes, 1000))
