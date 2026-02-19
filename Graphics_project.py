import pygame
import math

pygame.init()

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shadow Physics Playground")

clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
BLACK = (0, 0, 0)

# Scene Objects (rectangles)
objects = [
    pygame.Rect(200, 200, 100, 80),
    pygame.Rect(450, 150, 120, 100),
    pygame.Rect(600, 350, 150, 90),
]

def normalize(vx, vy):
    length = math.sqrt(vx * vx + vy * vy)
    if length == 0:
        return 0, 0
    return vx / length, vy / length


def draw_shadow(rect, light_pos):
    corners = [
        rect.topleft,
        rect.topright,
        rect.bottomright,
        rect.bottomleft
    ]

    shadow_points = []

    for corner in corners:
        dx = corner[0] - light_pos[0]
        dy = corner[1] - light_pos[1]

        nx, ny = normalize(dx, dy)

        # Extend shadow far away
        far_point = (
            corner[0] + nx * 2000,
            corner[1] + ny * 2000
        )

        shadow_points.append((corner, far_point))

    shadow_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    for i in range(len(shadow_points)):
        current = shadow_points[i]
        next_point = shadow_points[(i + 1) % len(shadow_points)]

        polygon = [
            current[0],
            next_point[0],
            next_point[1],
            current[1]
        ]

        pygame.draw.polygon(shadow_surface, (0, 0, 0, 120), polygon)

    screen.blit(shadow_surface, (0, 0))


running = True
while running:
    clock.tick(60)
    screen.fill(GRAY)

    light_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw Shadows
    for obj in objects:
        draw_shadow(obj, light_pos)

    # Draw Objects
    for obj in objects:
        pygame.draw.rect(screen, WHITE, obj)

    # Draw Light
    pygame.draw.circle(screen, (255, 255, 180), light_pos, 15)

    pygame.display.flip()

pygame.quit()
