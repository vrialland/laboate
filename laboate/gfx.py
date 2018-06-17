import framebuf


def render_tile_item(item):
    print('Rendering tile item')
    buffer = bytearray(item['width'] * item['height'])
    fb = framebuf.FrameBuffer(buffer, item['width'],
                              item['height'], framebuf.MONO_HLSB)
    if item['type'] == 'text':
        fb.text(item['content'], item['x'], item['y'])
    elif item['type'] == 'bitmap':
        i = 0
        size = item['width'] * item['height']
        # Convert int to binary
        content = bin(int(item['content']))[2:]
        # Fill with leading zeros to match required length
        content = '0' * (size - len(content)) + content
        for row in range(item['height']):
            for col in range(item['width']):
                fb.pixel(col, row, int(content[i]))
                i += 1
    return fb
