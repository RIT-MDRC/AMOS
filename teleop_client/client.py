import pygame
import socket

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
HOST = '127.0.0.1'

_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
_server.connect((HOST, 5362))


def send_to_server(left, right):
    binary = bytearray()
    binary.append(int((left * 127) + 127))
    binary.append(int((right * 127) + 127))
    _server.sendall(binary)


pygame.init()
clock = pygame.time.Clock()

joystick = pygame.joystick.Joystick(0)
joystick.init()
done = False

pygame.display.set_caption('WiFi Drive Visualizer')
screen = pygame.display.set_mode([250, 900])

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    left = -joystick.get_axis(1)
    right = -joystick.get_axis(3)
    full = joystick.get_button(1)

    if not full:
        left /= 2
        right /= 2

    screen.fill(WHITE)
    pygame.draw.rect(screen, BLACK, [50, (900 / 2) - 25, 50, 400 * -left])
    pygame.draw.rect(screen, BLACK, [150, (900 / 2) - 25, 50, 400 * -right])
    pygame.draw.rect(screen, GREEN if not full else BLUE, [0, 900 - 50, 250, 50])
    pygame.display.flip()

    send_to_server(left, right)
    clock.tick(50)

# HAT:
#  (x, y), behaves as expected
#
# BUTTONS:
#  00 = square
#  01 = x
#  02 = circle
#  03 = triangle
#  04 = left bumper
#  05 = right bumper
#  06 = left trigger (non-zero)
#  07 = right trigger (non-zero)
#  08 = share
#  09 = options
#  10 = press on left joystick
#  11 = press on right joystick
#  12 = playstation button
#  13 = press on touchscreen
#
# AXES:
#  0 = x component of left joystick
#  1 = y component of left joystick (inverted)
#  2 = x component of right joystick
#  3 = y component of right joystick (inverted)
#  4 = left trigger (-1 to 1)
#  5 = right trigger (-1 to 1)
