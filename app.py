import pygame
import threading
from colors import *
from node import create_random_nodes
from ant import AntColony, start


class App:
    def __init__(self, weight=840, height=640, starting_node_number=5):
        self._running = False
        self._display_surf = None
        self.clock = None
        self.size = self.weight, self.height = weight, height

        self.slider_font = None
        self.line_font = None
        self.node_font = None

        self.node_number = starting_node_number
        self.node_radius = 30
        self.node_padding = 15
        self.node_list = None
        self.node_distances = None

        self.line_thickness = 7

        self.moving_node = None
        self.offset_x = 0
        self.offset_y = 0

        self.iterations = 1000
        self.ants_multiplayer = 0.5
        self.evaporation_rate = 0.4
        self.random_movement_chance = 0.3
        self.alpha = 2
        self.beta = 3

        self.best_route = None
        self.best_route_length = None
        self.ant_colony = None

        self.ant_colony_thread = None

    def _pick_up_node(self, mouse_position):
        for node in self.node_list:
            if node.calculate_distance_for_point(mouse_position) <= node.radius:
                print(f"Start Moving Node: {node.id}")
                mouse_x, mouse_y = mouse_position
                self.moving_node = node
                self.offset_x = node.x - mouse_x
                self.offset_y = node.y - mouse_y

                self.best_route = None
                self.best_route_length = None
                break

    def _move_node(self, mouse_position):
        mouse_x, mouse_y = mouse_position
        self.moving_node.change_location((mouse_x + self.offset_x, mouse_y + self.offset_y))
        self.moving_node.recalculate_distance(self.node_list, self.node_distances)

    def _drop_node(self):
        print(f"Stopped Moving Node: {self.moving_node.id}")
        self.moving_node = None

    def _get_best_path(self):
        # or not self.ant_colony_thread.is_alive()
        if self.ant_colony_thread is None:
            print(f"Colony at work")
            self.ant_colony_thread = threading.Thread(target=start,
                                                      args=(self.ant_colony, self.node_distances,
                                                            self.iterations, self), daemon=True)
            self.ant_colony_thread.start()
        else:
            print("Kill")
            self.ant_colony.stop_work = True
            self.ant_colony_thread.join()
            self.ant_colony_thread = None
            self.ant_colony.stop_work = False



    def _draw_fps(self):
        text_surface = self.node_font.render("{:.2f}".format(self.clock.get_fps()), False, READ)
        self._display_surf.blit(text_surface, (0, 0))

    def _draw_nodes(self):
        for node in self.node_list:
            node.draw(self._display_surf)

    def _draw_best_rout(self):
        for i in range(len(self.best_route) - 1):
            start_node = self.node_list[self.best_route[i]]
            end_node = self.node_list[self.best_route[i + 1]]
            pygame.draw.line(self._display_surf, GOLDEN, start_node.position, end_node.position,
                             self.line_thickness)

    def _draw_nodes_connections(self):
        for start_node in self.node_list:
            for end_node in self.node_list:
                if start_node is end_node:
                    continue
                else:
                    start_node.draw_line(self._display_surf, end_node, self.node_distances, BLACK, self.line_thickness,
                                         self.line_font, READ)

    def on_init(self):
        pygame.init()

        self.node_font = pygame.font.SysFont('Comic Sans MS', 30)
        self.line_font = pygame.font.SysFont('Comic Sans MS', 18, bold=True)
        self.slider_font = pygame.font.SysFont('Comic Sans MS', 18, bold=True)

        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.clock = pygame.time.Clock()
        self._running = True

        self.node_list, self.node_distances = create_random_nodes(self.node_padding, self.node_radius, BLUE,
                                                                  self.node_font, BLACK,
                                                                  self.node_number)

        self.ant_colony = AntColony(self.node_number, self.ants_multiplayer, self.evaporation_rate,
                                    self.random_movement_chance, self.alpha, self.beta)

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self._pick_up_node(event.pos)

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.moving_node is not None:
                self._drop_node()

        if event.type == pygame.MOUSEMOTION:
            if self.moving_node is not None:
                self._move_node(event.pos)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self._get_best_path()
            if event.key == pygame.K_s:
                print(f"Sim")

    def on_loop(self):
        pass

    def on_render(self):
        print(threading.active_count())
        self._display_surf.fill(BACKGROUND_COLOR)
        self._draw_nodes_connections()
        if self.best_route is not None:
            self._draw_best_rout()
        self._draw_nodes()
        self._draw_fps()

        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        self.on_init()
        while self._running:
            self.clock.tick(60)
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
