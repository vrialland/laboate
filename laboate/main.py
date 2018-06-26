from machine import idle, I2C, Pin
import network
import time

from gfx import render_tile_item
from lenuage import LeNuage
from ssd1306 import SSD1306_I2C
import config
import uasyncio as asyncio


# Setup screen
i2c = I2C(scl=Pin(config.SSD1306_SCL), sda=Pin(config.SSD1306_SDA))
screen = SSD1306_I2C(config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT, i2c,
                     addr=config.SSD1306_ADDRESS)

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

    while True:
        print('Fetching tiles informations')
        tiles_data = await nuage.get_tiles()
        for tile in tiles_data['tiles']:
            print('Fetching tile data')
            tile_data = await nuage.get_tile(tile['id'])
            # Clear screens
            screen.fill(0)
            # Render tiles
            for item in tile_data[b'items']:
                render_tile_item(screen, item, config.DISPLAY_SCALE)
            # Update display
            screen.show()
            # Wait
            time.sleep_ms(tile_data[b'duration'])
    print('Done')

# Setup asyncio
loop = asyncio.get_event_loop()
loop.run_until_complete(main_loop())
loop.close()
