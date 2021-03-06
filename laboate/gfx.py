from font import FONT_4x6, FONT_5x7, FONT_4x6_CHARS, FONT_5x7_CHARS
import framebuf


class ExtendedFrameBuffer(framebuf.FrameBuffer):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.buffer = bytearray(self.width * self.height // 8)
        super().__init__(self.buffer, self.width, self.height,
                         framebuf.MONO_VLSB)


def render_string(fb, string, font=FONT_5x7, x=0, y=0):
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
        render_bitmap(fb, char_width, char_height, char, x, y)
        x += char_width


def render_bitmap(fb, width, height, content, x=0, y=0, decr_offset=False):
    # Read content bit by bit
    offset = width * height
    if decr_offset:
        offset -= 1
    for row in range(height):
        for col in range(width):
            fb.pixel(col + x, row + y, content >> offset & 1)
            offset -= 1


def render_tile_item(fb, item):
    print('Rendering tile item', item)
    if item['type'] == 'text':
        render_string(fb, item['content'], item['font'], item['x'], item['y'])
    elif item['type'] == 'bitmap':
        render_bitmap(fb, item['width'], item['height'], int(item['content']),
                      item['x'], item['y'], True)
    return fb


def scale(src, dest, factor=1):
    for x in range(src.width):
        for y in range(src.height):
            value = src.pixel(x, y)
            for dx in range(factor):
                for dy in range(factor):
                    dest.pixel(x * factor + dx, y * factor + dy, value)
