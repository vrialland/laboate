from machine import idle, I2C, Pin
import network
import time

from config import CONFIG
from gfx import render_tile_item
from lenuage import LeNuage
from ssd1306 import SSD1306_I2C


# Setup screen
screen_config = CONFIG['ssd1306']
i2c = I2C(scl=Pin(screen_config['scl']),
          sda=Pin(screen_config['sda']))
screen = SSD1306_I2C(screen_config['width'],
                     screen_config['height'],
                     i2c,
                     addr=screen_config['address'])

# Setup Wifi connection
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
print('Connecting to Wifi network "{}"'.format(CONFIG['wifi']['ssid']))
sta_if.connect(CONFIG['wifi']['ssid'], CONFIG['wifi']['password'])
while not sta_if.isconnected():
    idle()
    print('.', end='')
print()

# Setup lenuage
nuage = LeNuage(CONFIG['lenuage']['base_url'],
                CONFIG['lenuage']['api_key'])

while True:
    print('Fetching tiles informations')
    tiles_data = nuage.get_tiles()
    for tile in tiles_data['tiles']:
        print('Fetching tile data')
        tile_data = nuage.get_tile(tile['id'])
        # Clear screens
        screen.fill(0)
        # Render tiles
        for item in tile_data['items']:
            render_tile_item(screen, item, CONFIG['ssd1306']['scale'])
        # Update display
        screen.show()
        # Wait
        time.sleep_ms(tile_data['duration'])

print('Done')
