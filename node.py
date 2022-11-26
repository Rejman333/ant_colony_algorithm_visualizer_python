from pygame import draw
import random


class Node:
    def __init__(self, node_id, x, y, radius, node_color, font, font_color):
        self.id = node_id
        self.position = self.x, self.y = x, y
        self.radius = radius
        self.color = node_color

        self.font = font
        self.font_color = font_color

    def change_location(self, new_location):
        self.position = self.x, self.y = new_location

    def draw(self, surface):
        draw.circle(surface, self.color, self.position, self.radius)
        node_text = self.font.render(f"{self.id}", False, self.font_color)
        surface.blit(node_text, node_text.get_rect(center=self.position))

    def draw_line(self, surface, node, node_distances, line_color, line_thickness, line_font, line_font_color):
        distance = node_distances[self.id][node.id]
        draw.line(surface, line_color, self.position, node.position, line_thickness)

        line_text = line_font.render(f"{distance:.2f}", False, line_font_color)
        center = line_text.get_rect(center=self.calculate_midpoint_for_point(node.position))
        surface.blit(line_text, center)

    def calculate_distance_for_point(self, point):
        point_x, point_y = point

        return pow(pow(point_x - self.x, 2) + pow(point_y - self.y, 2), 1 / 2)

    def calculate_midpoint_for_point(self, point):
        point_x, point_y = point

        return (self.x + point_x) / 2, (self.y + point_y) / 2

    def recalculate_distance(self, node_list, nodes_distances):
        for node in node_list:
            nodes_distances[node.id][self.id] = self.calculate_distance_for_point(node.position)
            nodes_distances[self.id][node.id] = nodes_distances[node.id][self.id]

        return nodes_distances


def create_random_nodes(padding, node_radius, node_color, font, font_color, number_of_nodes):
    grid_sample = [(i, j) for j in range(8) for i in range(8)]
    sample = random.sample(grid_sample, number_of_nodes)
    sample = [
        (padding + node_radius + (padding + node_radius * 2) * s[0],
         padding + node_radius + (padding + node_radius * 2) * s[1])
        for s in sample]

    nodes = [Node(i, s[0], s[1], node_radius, node_color, font, font_color) for i, s in enumerate(sample)]
    nodes_distances = []

    for node in nodes:
        row = []
        for different_node in nodes:
            row.append(node.calculate_distance_for_point(different_node.position))
        nodes_distances.append(row)

    return nodes, nodes_distances
