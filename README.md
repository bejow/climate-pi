# climate-pi
An automated climate regulation system. The climate Pi uses sensor data in combination with a machine learning algorithm to obtain a specific climate situation (temperature and humidity) in small (< 2m³) enclosed spaces. The hardware parts (fan/heating mat) are interchangable and should orientate themselves on the Space that should be regulated (More Space --> Stronger Hardware).

# Requirements:

## Software
- Python 3.x
- Rasbian ^10.0.0 (now called Raspberry Pi OS)


## Hardware:
- [Raspberry Pi ^3.0.0](https://www.raspberrypi.com/)
- Enclosed Space < 2m³ (Chest, Wardrobe, Box)
- 2x [DHT 22 Temperature and Humdity Sensor](https://www.berrybase.de/sensoren-module/feuchtigkeit/dht22-digitaler-temperatur-und-luftfeuchtesensor)
- Heating Device (Heating Mat, Heating Cable, Heatfoil, ...)
- [Relay](https://www.berrybase.de/sensoren-module/relaiskarten/5v-2-kanal-relais-modul-mit-definierbarem-schaltsignal-40-high/low-41)
- [PC PWM Fan](https://www.bequiet.com/de/casefans/721)

# How to setup:
- [Create an SSH Key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent) and send it to me
- ```>> git clone git@github.com:bejow/climate-pi.git```
- ```>> cd climate_pi```
- Install Dependencies:
    - [Adafruit_Python_DHT](https://github.com/adafruit/Adafruit_Python_DHT)
        - `>> sudo apt-get update`
        - `>> sudo apt-get install python3-pip`
        - `>> sudo python3 -m pip install --upgrade pip setuptools wheel`
        - `>> cd libs/Adafruit_Python_DHT `
        - `>> sudo python3 setup.py install`
    
