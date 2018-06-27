from font import FONT_4x6, FONT_5x7, FONT_4x6_CHARS, FONT_5x7_CHARS
from utils import timeit
import time
from micropython import const


# Scroll directions
TRANSITION_NONE = const(0)
TRANSITION_FADE = const(1)
TRANSITION_LEFT = const(2)
TRANSITION_RIGHT = const(3)
TRANSITION_UP = const(4)
TRANSITION_DOWN = const(5)
_TRANSITION_STEPS = const(32)


def render_string(fb, string, font=FONT_5x7, x=0, y=0, scale=1):
    if font == FONT_4x6:
        char_width = 4
        char_height = 6
        font = FONT_4x6_CHARS
    else:
        char_width = 5
        char_height = 7
        font = FONT_5x7_CHARS
    for char in string:
        char = font.get(char, font['?'])
        render_bitmap(fb, char_width, char_height, char, x, y, False, scale)
        x += char_width


def render_bitmap(fb, width, height, content, x=0, y=0, decr_offset=False,
                  scale=1):
    # Read content bit by bit
    offset = width * height
    if decr_offset:
        offset -= 1
    for row in range(height):
        for col in range(width):
            # Use fill_rect instead of pixel to automatically upscale drawing
            # if needed
            fb.fill_rect((col + x) * scale, (row + y) * scale,
                         scale, scale, content >> offset & 1)
            offset -= 1


@timeit
def render_tile_item(fb, item, scale=1):
    print('Rendering tile item', item)
    if item['type'] == 'text':
        render_string(fb, item['content'], item['font'],
                      item['x'], item['y'], scale)
    elif item['type'] == 'bitmap':
        render_bitmap(fb, item['width'], item['height'], int(item['content']),
                      item['x'], item['y'], True, scale)
    return fb


def transition(screen, old_fb, new_fb, width, height, effect=TRANSITION_NONE,
               duration=500):
    screen.fill(0)

    # No transition exit ASAP
    if effect == TRANSITION_NONE:
        screen.blit(new_fb, 0, 0)
        screen.show()
        return

    # Show old framebuffer
    screen.blit(old_fb, 0, 0)
    screen.show()
    # Clear screen
    screen.fill(0)

    sleep = duration // _TRANSITION_STEPS

    if effect == TRANSITION_FADE:
        # TODO
        return transition(screen, old_fb, new_fb, width, height,
                          TRANSITION_NONE)
    elif effect == TRANSITION_LEFT:
        for x in range(0, width + 1, width // _TRANSITION_STEPS):
            screen.blit(old_fb, -x, 0)
            screen.blit(new_fb, width - x, 0)
            screen.show()
            time.sleep_ms(sleep)
    elif effect == TRANSITION_RIGHT:
        for x in range(0, width + 1, width // _TRANSITION_STEPS):
            screen.blit(old_fb, x, 0)
            screen.blit(new_fb, x - width, 0)
            screen.show()
            time.sleep_ms(sleep)
    elif effect == TRANSITION_UP:
        for y in range(0, height + 1, height // _TRANSITION_STEPS):
            screen.blit(old_fb, 0, -y)
            screen.blit(new_fb, 0, height - y)
            screen.show()
            time.sleep_ms(sleep)
    elif effect == TRANSITION_DOWN:
        for y in range(0, height + 1, height // _TRANSITION_STEPS):
            screen.blit(old_fb, 0, y)
            screen.blit(new_fb, 0, y - height)
            screen.show()
            time.sleep_ms(sleep)
