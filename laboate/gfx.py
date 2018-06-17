import framebuf


def render_bitmap(fb, width, height, content):
    i = 0
    size = width * height
    # Convert int to binary
    content = bin(content)[2:]
    # Fill with leading zeros to match required length
    content = '0' * (size - len(content)) + content
    for row in range(height):
        for col in range(width):
            fb.pixel(col, row, int(content[i]))
            i += 1


def render_tile_item(item):
    print('Rendering tile item')
    buffer = bytearray(item['width'] * item['height'])
    fb = framebuf.FrameBuffer(buffer, item['width'],
                              item['height'], framebuf.MONO_HLSB)
    if item['type'] == 'text':
        fb.text(item['content'], item['x'], item['y'])
    elif item['type'] == 'bitmap':
        render_bitmap(fb, item['width'], item['height'], int(item['content']))
    return fb
