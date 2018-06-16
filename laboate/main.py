from machine import idle, I2C, Pin
import network

from config import CONFIG
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

# Test display
screen.fill(0)
screen.text('hello world', 0, 0)
screen.show()

print('Done')
