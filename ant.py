import random


class Ant:
    def __init__(self, number_of_nodes, node_list):
        random_node_id = random.randint(0, number_of_nodes - 1)
        self.visited_nodes = [random_node_id]
        self.position = self.x, self.y = node_list[random_node_id].position
        self.speed = 25.
        self.changed = False

    def change_location(self, new_location):
        self.position = self.x, self.y = new_location

    def _visit_random_node(self, number_of_nodes):
        all_nodes = list(range(number_of_nodes))
        available_nodes = [x for x in all_nodes if x not in self.visited_nodes]
        node_id = random.choice(available_nodes)
        self.visited_nodes.append(node_id)

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

    def visit_node(self, nodes, pheromones, random_movement_chance, alpha, beta):
        if random_movement_chance >= random.random():
            self._visit_random_node(len(nodes))
        else:
            self._visit_probabilistically_node(nodes, pheromones, alpha, beta)

    def get_distance_traveled(self, nodes):
        distance_traveled = 0
        for i in range(1, len(self.visited_nodes)):
            distance_traveled += nodes[self.visited_nodes[i - 1]][self.visited_nodes[i]]

        return distance_traveled

    def draw(self, surface, ant_img):
        rect = ant_img.get_rect()
        rect.center = self.position
        surface.blit(ant_img, rect)

    def move_to_node(self, node):
        dx, dy = (node.x - self.x, node.y - self.y)
        step_x, step_y = (dx / self.speed, dy / self.speed)
        self.change_location((self.x + step_x, self.y + step_y))

        if abs(self.x - node.x) < 1 and abs(self.y - node.y) < 1:
            self.change_location(node.position)
            return True

        return False


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
        self.stop_work = False
        self.ant_m = 1

    def create_ants(self, number_of_nodes, node_list):
        number_of_ants = int(number_of_nodes * self.ants_multiplayer)
        ants = []
        for i in range(number_of_ants):
            ants.append(Ant(number_of_nodes, node_list))

        self.ants = ants

    def move_ants(self, node_list):
        for ant in self.ants:
            ant.visit_node(node_list, self.pheromones, self.random_movement_chance, self.alpha, self.beta)

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

    def draw_ants(self, surface, ant_img):
        for ant in self.ants:
            ant.draw(surface, ant_img)

    def move_ants_on_screen(self, node_list):
        ants_not_moving = True
        for ant in self.ants:
            node_id = ant.visited_nodes[self.ant_m]
            node = node_list[node_id]
            stop_moving = ant.move_to_node(node)
            if stop_moving is False:
                ants_not_moving = False

        if ants_not_moving is True and self.ant_m < len(node_list) - 1:
            self.ant_m += 1
            return False
        return ants_not_moving

    def iterate(self, node_distances, node_list):
        self.ant_m = 1
        node_len = len(node_distances)
        if self.stop_work:
            return None
        self.create_ants(node_len, node_list)
        for j in range(node_len - 1):
            self.move_ants(node_distances)
        self.update_pheromones(node_distances)

        return self.pheromones


if __name__ == '__main__':
    pass
