import pygame
import math
import dataclasses
import time
import numpy as np
import pyastar
pygame.init()

BLACK = (0, 0, 0)
CREAM = (240, 255, 240)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (211, 211, 211)
LIGHT_GRAY = (225, 225, 225)
ARIAL = pygame.font.SysFont("arial", 20)


@dataclasses.dataclass
class Obstacle:
    x: int
    y: int
    radius: int


DIMENSION_IN = 650
ROBOT_LENGTH_IN = 36
ROBOT_HEIGHT_IN = 24
OBSTACLE_BUFFER_IN = 24
OBSTACLES = [
    Obstacle(x=int((DIMENSION_IN // 2) + 100), y=int(DIMENSION_IN // 2), radius=30),
    Obstacle(x=int((DIMENSION_IN // 2) - 50), y=int(DIMENSION_IN // 2), radius=20)
]


def main():
    # joystick = pygame.joystick.Joystick(0)
    # joystick.init()
    clock = pygame.time.Clock()
    pygame.display.set_caption('World Visualizer')
    screen = pygame.display.set_mode([DIMENSION_IN, DIMENSION_IN])
    done = False

    rtenable = False
    selected = OBSTACLES[0] if OBSTACLES else None

    while not done:
        print('Start frame', time.time())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            selected.y -= 4
        if keys[pygame.K_a]:
            selected.x -= 4
        if keys[pygame.K_s]:
            selected.y += 4
        if keys[pygame.K_d]:
            selected.x += 4

        if keys[pygame.K_f]:
            for obstacle in OBSTACLES:
                if obstacle != selected:
                    selected = obstacle
                    break

        if keys[pygame.K_e]:
            rtenable = False
        elif keys[pygame.K_r]:
            rtenable = True

        matrix = np.full(fill_value=1, shape=(DIMENSION_IN, DIMENSION_IN), dtype=np.float32)

        screen.fill(WHITE)

        draw_frame(screen, matrix, selected)

        if rtenable:
            path = pyastar.astar_path(matrix, (DIMENSION_IN // 2, DIMENSION_IN // 2), (DIMENSION_IN - 1, DIMENSION_IN // 2))

            for x, y in path:
                pygame.draw.circle(screen, RED, [int(x), int(y)], int(2), 0)

        pygame.display.flip()
        print('End frame', time.time())
        clock.tick(60)


def draw_robot(screen):
    pygame.draw.rect(screen, BLACK, [
        (DIMENSION_IN / 2) - (ROBOT_LENGTH_IN / 2),
        (DIMENSION_IN / 2) - (ROBOT_HEIGHT_IN / 2),
        ROBOT_LENGTH_IN,
        ROBOT_HEIGHT_IN
    ])


def draw_fov(screen, fov, radius, color):
    fov_radians = math.radians(fov) / 2

    pygame.draw.arc(screen, color, [
        (DIMENSION_IN // 2) - radius,
        (DIMENSION_IN // 2) - radius,
        radius * 2,
        radius * 2
    ], -fov_radians, fov_radians, 1)


def draw_distance_ref(screen, feet):
    text = ARIAL.render(f'{feet}ft', True, LIGHT_GRAY)

    pygame.draw.circle(screen, LIGHT_GRAY, [DIMENSION_IN // 2, DIMENSION_IN // 2], feet * 12, 1)
    screen.blit(text, (
        (DIMENSION_IN // 2) - (text.get_width() / 2),
        (DIMENSION_IN // 2) - (feet * 12) - 14)
    )


def draw_obstacle(screen, matrix, obstacle, is_selected):
    x = obstacle.x
    y = obstacle.y
    r = obstacle.radius
    buffer_r = obstacle.radius + OBSTACLE_BUFFER_IN

    for x1 in range(x - r - OBSTACLE_BUFFER_IN, x + r + OBSTACLE_BUFFER_IN):
        for y1 in range(y - r - OBSTACLE_BUFFER_IN, y + r + OBSTACLE_BUFFER_IN):
            if (x1 - x) ** 2 + (y1 - y) ** 2 < buffer_r ** 2:
                matrix[x1][y1] = np.inf

    pygame.draw.circle(screen, GREEN if is_selected else RED, [x, y], r, 0)
    pygame.draw.circle(screen, GRAY, [x, y], r + OBSTACLE_BUFFER_IN, 1)


def draw_overlay(screen):
    overlay_pos = [10, 10, 10 + 110, 10 + 150]
    pygame.draw.rect(screen, CREAM, overlay_pos)
    pygame.draw.rect(screen, GRAY, overlay_pos, 2)


def draw_lanes(screen, matrix):
    l1_pos = [0, (DIMENSION_IN // 2) - 80, DIMENSION_IN, 6]
    l2_pos = [0, (DIMENSION_IN // 2) + 80, DIMENSION_IN, 6]

    pygame.draw.rect(screen, WHITE, l1_pos)
    pygame.draw.rect(screen, BLACK, l1_pos, 1)
    pygame.draw.rect(screen, WHITE, l2_pos)
    pygame.draw.rect(screen, BLACK, l2_pos, 1)


def draw_frame(screen, matrix, selected):
    for marker in [5, 10, 15, 20, 25, 30, 35, 40, 45]:
        draw_distance_ref(screen, marker)

    draw_fov(screen, 82.5, 393, BLACK)  # depth camera
    draw_fov(screen, 69.5, 383, BLUE)  # rgb camera

    draw_lanes(screen, matrix)

    for obstacle in OBSTACLES:
        draw_obstacle(screen, matrix, obstacle, selected == obstacle)

    draw_robot(screen)
    draw_overlay(screen)


if __name__ == '__main__':
    main()
