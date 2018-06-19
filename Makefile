# help: MICROPYTHON_VERSION		Micropython version
MICROPYTHON_VERSION ?= "v1.9.4"
# help: TARGET					Target system (esp8266 or esp32)
TARGET ?= esp8266
# help: PORT					Port to which the microcontroller is connected
PORT ?= /dev/ttyUSB0
# help: BAUDRATE				Connection baudrate (default: 115200)
BAUDRATE ?= 115200


flash:
	curl "http://micropython.org/resources/firmware/${TARGET}-20180511-${MICROPYTHON_VERSION}.bin" > /tmp/micropython.bin;
	esptool.py --port ${PORT} erase_flash
	esptool.py --chip ${TARGET} --port ${PORT} --baud ${BAUDRATE} write_flash --flash_size=detect -fm dio 0 /tmp/micropython.bin


upload:
	mkdir -p vendors
	curl https://raw.githubusercontent.com/micropython/micropython/master/drivers/display/ssd1306.py > vendors/ssd1306.py
	curl https://raw.githubusercontent.com/micropython/micropython-lib/master/urequests/urequests.py > vendors/urequests.py
	ampy -p ${PORT} -b ${BAUDRATE} put vendors/ssd1306.py
	ampy -p ${PORT} -b ${BAUDRATE} put vendors/urequests.py
	ampy -p ${PORT} -b ${BAUDRATE} put laboate/config.py
	ampy -p ${PORT} -b ${BAUDRATE} put laboate/font.py
	ampy -p ${PORT} -b ${BAUDRATE} put laboate/gfx.py
	ampy -p ${PORT} -b ${BAUDRATE} put laboate/lenuage.py
	ampy -p ${PORT} -b ${BAUDRATE} put laboate/main.py


shell:
	picocom ${PORT} -b ${BAUDRATE}
