from machine import idle, I2C, Pin
import framebuf
import network
import time

from gfx import render_tile_item, scroll
from lenuage import LeNuage
from ssd1306 import SSD1306_I2C
import config
import uasyncio as asyncio


# Setup screen
i2c = I2C(scl=Pin(config.SSD1306_SCL), sda=Pin(config.SSD1306_SDA))
screen = SSD1306_I2C(config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT, i2c,
                     addr=config.SSD1306_ADDRESS)
# TODO Choose right color format
buffer_a = framebuf.FrameBuffer(
    bytearray(config.DISPLAY_WIDTH * config.DISPLAY_HEIGHT // 8),
    config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT, framebuf.MONO_VLSB)
buffer_b = framebuf.FrameBuffer(
    bytearray(config.DISPLAY_WIDTH * config.DISPLAY_HEIGHT // 8),
    config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT, framebuf.MONO_VLSB)

# Setup Wifi connection
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
print('Connecting to wifi network')
sta_if.connect(config.WIFI_SSID, config.WIFI_PASSWORD)
while not sta_if.isconnected():
    idle()
    print('.', end='')
print()


async def main_loop():
    # Setup lenuage
    nuage = LeNuage(config.LENUAGE_BASE_URL, config.LENUAGE_API_KEY)

    # Display buffer a
    screen.blit(buffer_a, 0, 0)
    screen.show()

    while True:
        print('Fetching tiles informations')
        tiles_data = await nuage.get_tiles()
        for tile in tiles_data['tiles']:
            print('Fetching tile data')
            tile_data = await nuage.get_tile(tile['id'])
            # Clear screen and buffer b
            screen.fill(0)
            buffer_b.fill(0)
            # Render tiles on buffer b
            for item in tile_data['items']:
                render_tile_item(buffer_b, item, config.DISPLAY_SCALE)
            # Animate
            scroll(screen, buffer_a, buffer_b,
                   config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT)
            # Wait
            time.sleep_ms(tile_data['duration'])

            # Copy buffer b on a
            buffer_a.fill(0)
            buffer_a.blit(buffer_b, 0, 0)
    print('Done')

# Setup asyncio
loop = asyncio.get_event_loop()
loop.run_until_complete(main_loop())
loop.close()
