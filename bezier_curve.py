import pygame

# colors
WHITE = (255, 255, 255)
LIGHT_GRAY = (230, 230, 230)
BLACK = (0, 0, 0)
YELLOW = (255, 205, 0)
BLUE = (60, 21, 184)
RED = (251, 0, 13)

# initial configuration for different number of points
set_of_initial_points = [
    [[200, 400], [600, 400]],
    [[200, 400], [400, 100], [600, 400]],
    [[200, 400], [200, 100], [600, 100], [600, 400]],
    [[200, 400], [200, 250], [400, 100], [600, 250], [600, 400]],
    [[200, 400], [200, 250], [300, 100], [500, 100], [600, 250], [600, 400]]
]


buttons = {
    'pause_button': {'clickable': pygame.Rect(50, 25, 50, 50), 'drawable': [[50, 25, 20, 50], [80, 25, 20, 50]]},
    'play_button': {'clickable': pygame.Rect(125, 25, 50, 50), 'drawable': [(125, 25), (150, 50), (125, 75)]},
    'point_increase_button': {'clickable': pygame.Rect(450, 30, 25, 40), 'drawable': [(450, 30), (475, 50), (450, 70)]},
    'point_decrease_button': {'clickable': pygame.Rect(325, 30, 25, 40), 'drawable': [(350, 30), (325, 50), (350, 70)]},
    'speed_up_button': {'clickable': pygame.Rect(750, 30, 25, 40), 'drawable': [(750, 30), (775, 50), (750, 70)]},
    'speed_down_button': {'clickable': pygame.Rect(625, 30, 25, 40), 'drawable': [(650, 30), (625, 50), (650, 70)]}
}


class BezierCurveApp:
    """Class BezierCurveApp

        Attributes
        ----------
        n : int
            initial number of control points
        screen : pygame.Screen
            screen for drawing

        fps: int
            frame per second for rendering
        """
    def __init__(self, n, screen, fps):
        assert 2 <= n <= len(set_of_initial_points) + 2
        self.n = n
        self.t = 0
        self.sign = 1
        self.fps = fps
        self.running = True
        self.bezier_running = True
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.points = set_of_initial_points[n - 2]
        self.dots = self.calculate_bezier_points()
        w, h = self.screen.get_size()
        self.menu_surface = pygame.Surface((w, 100))
        self.workspace = pygame.Surface((w, h - 100))

    def draw_bezier_construct(self):
        point_radius = 5
        cur_points = self.points
        while len(cur_points) != 1:
            new_points = []
            for i in range(len(cur_points) - 1):
                p1, p2 = cur_points[i], cur_points[i + 1]
                pygame.draw.line(self.workspace, BLACK, p1, p2, 1)
                # calculate new points
                p = (p1[0] + self.t * (p2[0] - p1[0]), p1[1] + self.t * (p2[1] - p1[1]))
                pygame.draw.circle(self.workspace, YELLOW, p1, point_radius)
                new_points.append(p)
            pygame.draw.circle(self.workspace, YELLOW, cur_points[-1], point_radius)
            cur_points = new_points
        pygame.draw.circle(self.workspace, BLUE, cur_points[-1], point_radius)
        for point in self.points:
            pygame.draw.circle(self.workspace, RED, point, point_radius)

    def draw_background(self):
        # draw grid
        w, h = self.workspace.get_size()
        self.workspace.fill(WHITE)
        step = 50
        for i in range(h // step):
            pygame.draw.line(self.workspace, LIGHT_GRAY, (0, i * step), (w, i * step))
        for i in range(w // step):
            pygame.draw.line(self.workspace, LIGHT_GRAY, (i * step, 0), (i * step, h))

    def calculate_bezier_points(self):
        dots = []
        t = 0
        while t < 1:
            cur_points = self.points
            while len(cur_points) != 1:
                new_points = []
                for i in range(len(cur_points) - 1):
                    p1, p2 = cur_points[i], cur_points[i + 1]
                    p = (p1[0] + t * (p2[0] - p1[0]), p1[1] + t * (p2[1] - p1[1]))
                    new_points.append(p)
                cur_points = new_points
            dots.append(cur_points[0])
            t += 0.005
        return dots

    def draw_bezier_curve(self):
        for i in range(len(self.dots) - 1):
            pygame.draw.line(self.workspace, BLACK, self.dots[i], self.dots[i + 1], 2)

    def draw_menu(self):
        self.menu_surface.fill(LIGHT_GRAY)
        for button_name in buttons:
            if button_name == 'pause_button':
                pygame.draw.rect(self.menu_surface, WHITE, buttons[button_name]['drawable'][0])
                pygame.draw.rect(self.menu_surface, WHITE, buttons[button_name]['drawable'][1])
                continue
            pygame.draw.polygon(self.menu_surface, WHITE, buttons[button_name]['drawable'])

        font1 = pygame.font.SysFont(None, 40)
        text1 = font1.render('point', True, WHITE)
        self.menu_surface.blit(text1, (365, 40))

        font2 = pygame.font.SysFont(None, 40)
        text2 = font2.render('speed', True, WHITE)
        self.menu_surface.blit(text2, (660, 40))

    @staticmethod
    def is_point_in_circle(point, center, radius):
        return (point[0] - center[0]) ** 2 + (point[1] - center[1]) ** 2 <= radius ** 2

    def on_point_pressed(self, mouse_pos):
        point_radius = 5
        for i in range(len(self.points)):
            if self.is_point_in_circle(mouse_pos, self.points[i], point_radius):
                return i
        return None

    def on_buttons_pressed(self, mouse_pos):
        for button_name in buttons:
            if buttons[button_name]['clickable'].collidepoint(mouse_pos):
                if button_name == 'pause_button':
                    self.bezier_running = False
                elif button_name == 'play_button':
                    self.bezier_running = True

                elif button_name == 'point_increase_button':
                    max_n = len(set_of_initial_points) + 1
                    self.n = max_n if self.n == max_n else self.n + 1
                    self.points = set_of_initial_points[self.n - 2]
                    self.dots = self.calculate_bezier_points()
                    if not self.bezier_running:
                        self.update()
                elif button_name == 'point_decrease_button':
                    self.n = 2 if self.n == 2 else self.n - 1
                    self.points = set_of_initial_points[self.n - 2]
                    self.dots = self.calculate_bezier_points()
                    if not self.bezier_running:
                        self.update()

                elif button_name == 'speed_up_button':
                    self.fps += 10
                elif button_name == 'speed_down_button':
                    self.fps = 10 if self.fps <= 10 else self.fps - 10

    def update(self):
        self.draw_background()
        self.draw_bezier_curve()
        self.draw_bezier_construct()
        self.screen.blit(self.workspace, (0, 100))
        pygame.display.flip()

    def update_t(self):
        self.t += 0.01 * self.sign
        if self.t >= 1:
            self.sign = -1
            self.t = 1
        if self.t <= 0:
            self.sign = 1
            self.t = 0

    def event_handler(self, event, press_point, offset_x, offset_y):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            press_point = self.on_point_pressed((event.pos[0], event.pos[1] - 100))
            if press_point is None:
                self.on_buttons_pressed(event.pos)
            else:
                offset_x = self.points[press_point][0] - event.pos[0]
                offset_y = self.points[press_point][1] - event.pos[1]
        elif event.type == pygame.MOUSEBUTTONUP:
            press_point = None
        elif event.type == pygame.MOUSEMOTION:
            if press_point is not None:
                self.points[press_point][0] = event.pos[0] + offset_x
                self.points[press_point][1] = event.pos[1] + offset_y
                if self.points[press_point][1] <= 0:
                    self.points[press_point][1] = 0
                self.dots = self.calculate_bezier_points()
                if not self.bezier_running:
                    self.update()
        return press_point, offset_x, offset_y

    def run(self):
        self.draw_menu()
        # throw menu surface on main screen
        self.screen.blit(self.menu_surface, (0, 0))
        press_point = None
        offset_x, offset_y = 0, 0
        while self.running:
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                press_point, offset_x, offset_y = self.event_handler(event, press_point, offset_x, offset_y)
            if self.bezier_running:
                self.update()
                self.update_t()

