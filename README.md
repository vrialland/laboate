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
Here are the available options and sections

### SSD1306

Configuration related to the SSD1306 screen:

- `address`: address used to communicate with the screen, can be `0x3c` or `0x3d` (this should be written on the screen)
- `sda`: GPIO pin (number required, not `D1` for example) connected to the SDA pin on the screen
- `scl`: GPIO pin (number required, not `D2` for example) connected to the SCL pin on the screen
- `width`: width (in pixels) of the screen
- `height`: height (in pixels) of the screen
- `scale`: as LeNuage (http://github.com/laboiteproject/lenuage/) is made for smaller screens, upscale the rendering with this factor (int)

### WIFI

Configuration about your Wifi network

- `ssid`: name of the SSID of the network
- `password`: password used to connect to the network

### LeNuage

Configuration about LeNuage

- `base_url`: URL of LeNuage instance
- `api_key`: API key of your Boite object
