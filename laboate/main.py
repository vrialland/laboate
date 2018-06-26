from machine import idle, I2C, Pin
import network
import time

from config import CONFIG
from gfx import render_tile_item
from lenuage import LeNuage
from ssd1306 import SSD1306_I2C
import uasyncio as asyncio


async def main_loop():
    # Setup Wifi connection
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    print(b'Connecting to Wifi network "%s"' % (
        CONFIG['wifi']['ssid'].encode('utf-8')))
    sta_if.connect(CONFIG['wifi']['ssid'], CONFIG['wifi']['password'])
    while not sta_if.isconnected():
        idle()
        print(b'.', end='')
    print()

    # Setup screen
    screen_config = CONFIG[b'ssd1306']
    i2c = I2C(scl=Pin(screen_config[b'scl']),
              sda=Pin(screen_config[b'sda']))
    screen = SSD1306_I2C(screen_config[b'width'],
                         screen_config[b'height'],
                         i2c,
                         addr=screen_config[b'address'])

    # Setup lenuage
    nuage = LeNuage(CONFIG[b'lenuage'][b'base_url'],
                    CONFIG[b'lenuage'][b'api_key'])

    while True:
        print(b'Fetching tiles informations')
        tiles_data = await nuage.get_tiles()
        for tile in tiles_data['tiles']:
            print(b'Fetching tile data')
            tile_data = await nuage.get_tile(tile['id'])
            # Clear screens
            screen.fill(0)
            # Render tiles
            for item in tile_data[b'items']:
                render_tile_item(screen, item, CONFIG[b'ssd1306'][b'scale'])
            # Update display
            screen.show()
            # Wait
            time.sleep_ms(tile_data[b'duration'])
    print(b'Done')

# Setup asyncio
loop = asyncio.get_event_loop()
loop.run_until_complete(main_loop())
loop.close()
