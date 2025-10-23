# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

from os import getenv
from adafruit_bitmap_font import bitmap_font
from adafruit_esp32spi import adafruit_esp32spi
from digitalio import DigitalInOut
from time import sleep
import adafruit_display_text.label
import board
import busio
import displayio
import framebufferio
import rgbmatrix
import adafruit_imageload
import adafruit_connection_manager
import adafruit_minimqtt.adafruit_minimqtt as MQTT




# CONSTANTS
SMALL_FONT = bitmap_font.load_font("fonts/5x7.bdf")
#MEDIUM_FONT = bitmap_font.load_font("fonts/6x9.bdf")
#BIG_FONT = bitmap_font.load_font("fonts/7x13.bdf")
BLACK_COLOR = 0x000000
WHITE_COLOR = 0x555555
RED_COLOR = 0x550000
BLUE_COLOR = 0x000055
GREEN_COLOR = 0x005500
ORANGE_COLOR = 0xFF9900
YELLOW_COLOR = 0xFFFF00
PURPLE_COLOR = 0xFF1493
PURPLE_COLOR = 0xFF1493





# DISPLAY INIT
LabelsList = {}
LabelsValues = {}
ScreenEnabled = True

bit_depth = 6
base_width = 64
base_height = 32
chain_across = 1
tile_down = 2
serpentine = True

width = base_width * chain_across
height = base_height * tile_down

addr_pins = [board.MTX_ADDRA, board.MTX_ADDRB, board.MTX_ADDRC, board.MTX_ADDRD]
rgb_pins = [
    board.MTX_R1,
    board.MTX_G1,
    board.MTX_B1,
    board.MTX_R2,
    board.MTX_G2,
    board.MTX_B2,
]
clock_pin = board.MTX_CLK
latch_pin = board.MTX_LAT
oe_pin = board.MTX_OE

displayio.release_displays()
matrix = rgbmatrix.RGBMatrix(
                width=width,
                height=height,
                bit_depth=bit_depth,
                rgb_pins=rgb_pins,
                addr_pins=addr_pins,
                clock_pin=clock_pin,
                latch_pin=latch_pin,
                output_enable_pin=oe_pin,
                tile=tile_down, serpentine=serpentine,
            )
display = framebufferio.FramebufferDisplay(matrix)
main_group = displayio.Group()
display.root_group = main_group





# Get WiFi details and Adafruit IO keys, ensure these are setup in settings.toml
ssid = getenv("MYWIFI_SSID")
password = getenv("MYWIFI_PASSWORD")
mqtt_username = getenv("JEEDOM_MQTT_USER")
mqtt_pwd = getenv("JEEDOM_MQTT_PASSWORD")
mqtt_broker = getenv("JEEDOM_IP")
mqtt_object_name = getenv("JEEDOM_OBJECT_NAME_MQTT")

# If you are using a board with pre-defined ESP32 Pins:
esp32_cs = DigitalInOut(board.ESP_CS)
esp32_ready = DigitalInOut(board.ESP_BUSY)
esp32_reset = DigitalInOut(board.ESP_RESET)

spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)




# Bitmap images for status
sprite_sheet_12, palette_12 = adafruit_imageload.load("/sprite_sheets/SpriteSheet_12.png",
                                                bitmap=displayio.Bitmap,
                                                palette=displayio.Palette)
sprite_sheet_24, palette_24 = adafruit_imageload.load("/sprite_sheets/SpriteSheet_24.png",
                                                bitmap=displayio.Bitmap,
                                                palette=displayio.Palette)
#for value in palette_12:
#    print(value)
#for value in palette_24:
#    print(value)
#print(dir(palette_12))
#print(dir(palette_24))
sprite_Modes = displayio.TileGrid(sprite_sheet_12, pixel_shader=palette_12,
                            width = 1,
                            height = 1,
                            tile_width = 12,
                            tile_height = 12,
                            x=0,
                            y=24)
main_group.append(sprite_Modes)
sprite_Alarms = displayio.TileGrid(sprite_sheet_12, pixel_shader=palette_12,
                            width = 1,
                            height = 1,
                            tile_width = 12,
                            tile_height = 12,
                            x=13,
                            y=24)
main_group.append(sprite_Alarms)
sprite_Heaters = displayio.TileGrid(sprite_sheet_12, pixel_shader=palette_12,
                            width = 1,
                            height = 1,
                            tile_width = 12,
                            tile_height = 12,
                            x=26,
                            y=24)
main_group.append(sprite_Heaters)
sprite_Bins = displayio.TileGrid(sprite_sheet_12, pixel_shader=palette_12,
                            width = 1,
                            height = 1,
                            tile_width = 12,
                            tile_height = 12,
                            x=39,
                            y=24)
main_group.append(sprite_Bins)
sprite_Weathers = displayio.TileGrid(sprite_sheet_24, pixel_shader=palette_24,
                            width = 1,
                            height = 1,
                            tile_width = 24,
                            tile_height = 24,
                            x=64,
                            y=37)
main_group.append(sprite_Weathers)
sprite_Weathers_NextHour = displayio.TileGrid(sprite_sheet_24, pixel_shader=palette_24,
                            width = 1,
                            height = 1,
                            tile_width = 24,
                            tile_height = 24,
                            x=64,
                            y=37)
main_group.append(sprite_Weathers_NextHour)





### Feeds MQTT & Labels placement###
LabelsList[f"{mqtt_object_name}/time/hour"] = adafruit_display_text.label.Label(
    font=SMALL_FONT, text="", scale=1, x=42, y=14, base_alignment=True)
hour_dots = adafruit_display_text.label.Label(
    font=SMALL_FONT, text="", scale=1, x=51, y=14, base_alignment=True)
main_group.append(hour_dots)
arrow_weather = adafruit_display_text.label.Label(
    font=SMALL_FONT, text="", scale=1, x=30, y=52, base_alignment=True)
main_group.append(arrow_weather)
LabelsList[f"{mqtt_object_name}/time/minute"] = adafruit_display_text.label.Label(
    font=SMALL_FONT, text="", scale=1, x=55, y=14, base_alignment=True)

LabelsList[f"{mqtt_object_name}/temperature/int/etage"] = adafruit_display_text.label.Label(
    font=SMALL_FONT, text="", scale=1, x=0, y=6, base_alignment=True)
LabelsList[f"{mqtt_object_name}/temperature/int/rdc"] = adafruit_display_text.label.Label(
    font=SMALL_FONT, text="", scale=1, x=0, y=14, base_alignment=True)
LabelsList[f"{mqtt_object_name}/temperature/ext"] = adafruit_display_text.label.Label(
    font=SMALL_FONT, text="", scale=1, x=0, y=22, base_alignment=True)

LabelsList[f"{mqtt_object_name}/temperature/tend/int/etage"] = adafruit_display_text.label.Label(
    font=SMALL_FONT, text="", scale=1, x=30, y=6, base_alignment=True)
LabelsList[f"{mqtt_object_name}/temperature/tend/int/rdc"] = adafruit_display_text.label.Label(
    font=SMALL_FONT, text="", scale=1, x=30, y=14, base_alignment=True)
LabelsList[f"{mqtt_object_name}/temperature/tend/ext"] = adafruit_display_text.label.Label(
    font=SMALL_FONT, text="", scale=1, x=30, y=22, base_alignment=True)

LabelsList[f"{mqtt_object_name}/energy/elec/papp"] = adafruit_display_text.label.Label(
    font=SMALL_FONT, text="", scale=1, x=40, y=6, base_alignment=True)

counters_days = adafruit_display_text.label.Label(
    font=SMALL_FONT, text="", scale=1, x=40, y=22, base_alignment=True)
main_group.append(counters_days)

for mqtt_object, label in LabelsList.items():
    main_group.append(label)
    LabelsValues[mqtt_object] = 0





### Functions ###
# Define callback methods which are called when events occur
def connected(client, userdata, flags, rc):
    global LabelsList
    for mqtt_object, label in LabelsList.items():
        client.subscribe(f"{mqtt_object}")
    client.subscribe(f"{mqtt_object_name}/screen/disable")
    client.subscribe(f"{mqtt_object_name}/screen/luminosity")
    client.subscribe(f"{mqtt_object_name}/status/mode")
    client.subscribe(f"{mqtt_object_name}/status/alarm")
    client.subscribe(f"{mqtt_object_name}/status/heater")
    client.subscribe(f"{mqtt_object_name}/status/bins")
    client.subscribe(f"{mqtt_object_name}/status/weather")
    client.subscribe(f"{mqtt_object_name}/status/weather_nexthour")
    client.subscribe(f"{mqtt_object_name}/screen/reboot")
    client.subscribe(f"{mqtt_object_name}/counters/days/value")
    #client.subscribe(f"{mqtt_object_name}/counters/days/color")


def disconnected(client, userdata, rc):
    # This method is called when the client is disconnected
    print("MQTT Disconnected")


def message(client, topic, message):
    global LabelsList, LabelsValues, hour_dots, rgbmatrix, ScreenEnabled
    # This method is called when a topic the client is subscribed to
    # has a new message.
    print(f"New message on topic {topic}: {message}")
    if("/counters/days/color" not in topic):
        LabelsValues[f"{topic}"] = float(f"{message}")
    if "screen" in topic:
        if "disable" in topic:
            if int(message) == 0:
                ScreenEnabled = True
            else:
                ScreenEnabled = False
        elif "luminosity" in topic:
            print(f"Luminosity: {message}")
            #rgbmatrix.brightness = float(message)
        elif "reboot" in topic:
            if int(message) == 1:
                print(f"Restart")
                #adafruit_esp32spi.ESP_SPIcontrol.reset()
    if ScreenEnabled == True:
        if "time/minute" in topic:
            hour_dots.text = ":"
            if LabelsValues[f"{mqtt_object_name}/time/hour"] == LabelsValues[f"{mqtt_object_name}/time/minute"]:
                LabelsList[f"{mqtt_object_name}/time/hour"].color = PURPLE_COLOR
                hour_dots.color = PURPLE_COLOR
                LabelsList[f"{mqtt_object_name}/time/minute"].color = PURPLE_COLOR
            else:
                LabelsList[f"{mqtt_object_name}/time/hour"].color = ORANGE_COLOR
                hour_dots.color = ORANGE_COLOR
                LabelsList[f"{mqtt_object_name}/time/minute"].color = ORANGE_COLOR
            LabelsList[f"{topic}"].text = f"{message:0>2}"
        elif "/time/hour" in topic:
            LabelsList[f"{topic}"].text = f"{message:0>2}"
        elif "/counters" in topic:
            if "/counters/days/value" in topic:
                ValueInt = int(f"{message}")
                if(ValueInt > 0) :
                    counters_days.text = f"J-{ValueInt}"
                else:
                    counters_days.text = ""
                if(ValueInt > 100) :
                    counters_days.x = 40
                elif(ValueInt > 10) :
                    counters_days.x = 45
                else:
                    counters_days.x = 50
            #elif "/counters/days/color" in topic:
            #    counters_days.color = message
        elif "temperature" in topic and not "tend" in topic:
            if LabelsValues[f"{topic}"] < 10 and LabelsValues[f"{topic}"] >= 0:
                LabelsList[f"{topic}"].x = 5
            else:
                LabelsList[f"{topic}"].x = 0
            LabelsList[f"{topic}"].text = f"{float(message):.1f}°C"
            LabelsList[f"{topic}"].color = WHITE_COLOR
        elif "temperature" in topic and "tend" in topic:
            if LabelsValues[f"{topic}"] == 1:
                LabelsList[f"{topic}"].text = f"▲"
                LabelsList[f"{topic}"].color = GREEN_COLOR
            elif LabelsValues[f"{topic}"] == -1:
                LabelsList[f"{topic}"].text = f"▼"
                LabelsList[f"{topic}"].color = RED_COLOR
            else:
                LabelsList[f"{topic}"].text = f"-"
                LabelsList[f"{topic}"].color = BLUE_COLOR
        elif "energy/elec" in topic:
            if LabelsValues[f"{topic}"] < 1000:
                LabelsList[f"{topic}"].x = 45
            else:
                LabelsList[f"{topic}"].x = 40
            LabelsList[f"{topic}"].text = f"{message}W"
            if LabelsValues[f"{topic}"] <= 550:
                LabelsList[f"{topic}"].color = GREEN_COLOR
            elif LabelsValues[f"{topic}"] <= 800:
                LabelsList[f"{topic}"].color = WHITE_COLOR
            elif LabelsValues[f"{topic}"] <= 1500:
                LabelsList[f"{topic}"].color = YELLOW_COLOR
            elif LabelsValues[f"{topic}"] <= 2500:
                LabelsList[f"{topic}"].color = ORANGE_COLOR
            else:
                LabelsList[f"{topic}"].color = RED_COLOR
        elif "status/" in topic:
            if "mode" in topic:
                sprite_Modes[0] = int(message)
            elif "alarm" in topic:
                sprite_Alarms[0] = int(message)
            elif "bins" in topic:
                sprite_Bins[0] = int(message)
            elif "heater" in topic:
                sprite_Heaters[0] = int(message)
            elif "weather" in topic and not "nexthour" in topic:
                sprite_Weathers[0] = int(message)
                sprite_Weathers.x = 0
            elif "weather_nexthour" in topic:
                sprite_Weathers_NextHour[0] = int(message)
            if "weather" in topic and f"{mqtt_object_name}/status/weather" in LabelsValues and f"{mqtt_object_name}/status/weather_nexthour" in LabelsValues:
                if LabelsValues[f"{mqtt_object_name}/status/weather"] == LabelsValues[f"{mqtt_object_name}/status/weather_nexthour"]:
                    arrow_weather.text = ""
                    sprite_Weathers_NextHour.x = 64
                else:
                    arrow_weather.text = "▶"
                    sprite_Weathers_NextHour.x = 40
                arrow_weather.color = ORANGE_COLOR
        else:
            if f"{topic}" in LabelsList:
                LabelsList[f"{topic}"].text = f"{message}"
    else:
        hour_dots.text = ""
        arrow_weather.text = ""
        if f"{topic}" in LabelsList:
            LabelsList[f"{topic}"].text = ""
        sprite_Modes[0] = 0
        sprite_Alarms[0] = 0
        sprite_Bins[0] = 0
        sprite_Heaters[0] = 0
        sprite_Weathers.x = 64
        sprite_Weathers_NextHour.x = 64
        counters_days.text = ""





# Connect to WiFi
print("Wait Wifi")
while not esp.is_connected:
    try:
        esp.connect_AP(ssid, password)
    except RuntimeError as e:
        print("Error Wifi")
        continue
    except ConnectionError as e:
        print("Error Wifi")
        continue

pool = adafruit_connection_manager.get_radio_socketpool(esp)
ssl_context = adafruit_connection_manager.get_radio_ssl_context(esp)





# Set up a MiniMQTT Client
mqtt_client = MQTT.MQTT(
    broker=mqtt_broker,
    username=mqtt_username,
    password=mqtt_pwd,
    socket_pool=pool,
    ssl_context=ssl_context,
)

# Setup the callback methods above
mqtt_client.on_connect = connected
mqtt_client.on_disconnect = disconnected
mqtt_client.on_message = message






# Connect the client to the MQTT broker.
print("Wait MQTT")
mqtt_client.will_set(f"{mqtt_object_name}/screen/is_alive","LAST_WILL_ACTIVE")
mqtt_client.connect()

# LOOP
print("Start Loop")
while True:
    try:
        mqtt_client.loop()
    except (ValueError, RuntimeError) as e:
        print("Timeout, reconnecting\n", e)
        esp.reset()
        sleep(1)
        while not esp.is_connected:
            try:
                esp.connect_AP(ssid, password)
            except RuntimeError as e:
                print("Error Wifi")
                continue
            except ConnectionError as e:
                print("Error Wifi")
                continue
        mqtt_client.reconnect()
        continue
    except Exception as e:
        print(f"General Error : {e}")
        esp.reset()
        sleep(1)
        while not esp.is_connected:
            try:
                esp.connect_AP(ssid, password)
            except RuntimeError as e:
                print("Error Wifi")
                continue
            except ConnectionError as e:
                print("Error Wifi")
                continue
        mqtt_client.reconnect()
        continue
    #sleep(1)
