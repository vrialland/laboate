# LaBoate

> Micropython version of LaBoite (https://github.com/redgick/Redgick_Laboite)

[![Build Status](https://travis-ci.org/vrialland/laboate.svg?branch=master)](https://travis-ci.org/vrialland/laboate)

## Required hardware

- An ESP8266 or ESP32 board
- An SSD1306 OLED screen


## Setup

- Clone the repository
- Depending on your board `export TARGET=esp8266` or `export TARGET=esp32`
- Run `make flash` to download the appropriate Micropython firmware and flash your board with it
- Create `laboate/config.py` file based on `laboate/config.py.sample`
- Run `make upload` to upload the required files to the board
- Reset the board
- Profit!


## Makefile variables

Depending on your setup, you can override these environment variables:
- `MICROPYTHON_VERSION`: version of Micropython you want to use, default is 1.9.4
- `TARGET`: type of your board, can be `esp8266` or `esp32` (case sensitive!)
- `PORT`: port on which your board is connected to your computer, default is `/dev/ttyUSB0`
- `BAUDRATE`: baud rate used to communicate with your board, default is `115200`


## Configuration file

You will find a ready to use config file in `laboate` folder named `config.py.sample`.
As storing the configuration consumes RAM, and in order to keep it as low as possible,
please use `const` for integer values and prefer `bytes` over `str` for textual values.
Here are the available options:

### Display

Configuration related to the display used (SSD1306 only at the moment)

- `DISPLAY_WIDTH`: width (in pixels) of the screen
- `DISPLAY_HEIGHT`: height (in pixels) of the screen
- `DISPLAY_SCALE`: : as LeNuage (http://github.com/laboiteproject/lenuage/) is made for smaller screens, upscale the rendering with this factor (int)

### SSD1306

Configuration related to the SSD1306 screen:

- `SSD1306_ADDRESS`: address used to communicate with the screen, can be `0x3c` or `0x3d` (this should be written on the screen)
- `SSD1306_SDA`: GPIO pin (number required, not `D1` for example) connected to the SDA pin on the screen
- `SSD1306_SCL`: GPIO pin (number required, not `D2` for example) connected to the SCL pin on the screen

### WIFI

Configuration about your Wifi network

- `WIFI_SSID`: name of the SSID of the network
- `WIFI_PASSWORD`: password used to connect to the network

### LeNuage

Configuration about LeNuage

- `LENUAGE_BASE_URL`: URL of LeNuage instance
- `LENUAGE_API_KEY`: API key of your Boite object
