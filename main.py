import pygame
from bezier_curve import BezierCurveApp

WIDTH = 800
HEIGHT = 600
FPS = 30

if __name__ == "__main__":
    # init pygame
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Bezier curve visualization")
    # create and run app
    bezier_curve_drawable = BezierCurveApp(4, screen, FPS)
    bezier_curve_drawable.run()
    pygame.quit()