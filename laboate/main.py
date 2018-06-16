from machine import I2C
from machine import Pin

import config
from ssd1306 import SSD1306_I2C


# Setup screen
screen_config = config['ssd1306']
i2c = I2C(scl=Pin(screen_config['scl']),
          sda=Pin(screen_config['sda']))
screen = SSD1306_I2C(screen_config['width'],
                     screen_config['height'],
                     i2c,
                     addr=screen_config['address'])

# Test display
screen.fill(0)
screen.text('hello world', 0, 0)
screen.show()

print('Done')
