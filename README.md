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
    - [SKlearn on RPi](https://scikit-learn.org/stable/install.html)
        - `>> pip3 install -U scikit-learn`
        - `>> pip3 install numpy`
        - `>> sudo apt-get install python-dev libatlas-base-dev`
    - [Adafruit_Python_DHT](https://github.com/adafruit/Adafruit_Python_DHT)
        - `>> sudo apt-get update`
        - `>> sudo apt-get install python3-pip`
        - `>> sudo python3 -m pip install --upgrade pip setuptools wheel`
        - `>> cd libs/Adafruit_Python_DHT `
        - `>> sudo python3 setup.py install`
        - Read comments to understand Google Sheets Oauth2: `libs\Adafruit_Python_DHT\examples\google_spreadsheet.py`
            - Add google-auth.json to `src/`
            - Create Google Service Account
            - Specify Google Sheet to log data to `src/settings.py`
    - [Gspread](https://pypi.org/project/gspread/)
        - `>> sudo pip3 install gspread oauth2client`
        - `>> sudo apt-get update`
        - `>> sudo apt-get install python-openssl`
- Change settings regarding your needs under `src/settings.py`
# How to Train
- Run: `src/main_randomSettings.py`

    - This will collect Data about the system and save it to a  google spreadsheet specified in `src/settings.py`

    - This process can take a while depending on how many datapoints you want to create (10 min for one row of data)

- Export the data from google spreadsheet (as CSV) and save it in the project folder

    - Specify `TRAINING_DATA_PATH` in `src/settings.py` according to your previous choosen save location

- Run `src/linear_regression.ipynb`. This will create a .pkl file that contains your trained model (Path is specified in `src/settings.py`)

# How to Run
( Make sure you followed all previous instructions, otherwise this will fail )
- Run: `src/main_hillClimb.py`

    - This will control the climate system based on your trained model

    - You can change the `TARGET_TEMPERATURE` and `TARGET_HUMIDITY` in `src/settings.py`

# Disclaimer

- The System is just as good as the data that went into the model. If you used to few Datapoints or placed your System somewhere different than where you trained the model, results may not be as expected

- If you scale this project up/down you probably need different Hardware components

- There is no active cooling / humidifying / dehumidifying

    - That means that the system has limited capabilities when influencing the climate