import json
import sys
import time
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import settings

class Log:
    def __init__(self, spreadsheet_name=settings.GDOCS_SPREADSHEET_NAME):
        self.worksheet = self.login_open_sheet(settings.GDOCS_OAUTH_JSON, spreadsheet_name)
        self.spreadsheet_name = spreadsheet_name
        print('Logging sensor measurements to {0} every {1} seconds.'.format(spreadsheet_name, settings.FREQUENCY_SECONDS))

    def log(self, temperature_inside, humidity_inside, temperature_outside, humidity_outside, fan_speed=0, is_heating=False, score=""):
        if self.worksheet is None:
            self.worksheet = self.login_open_sheet(settings.GDOCS_OAUTH_JSON, self.spreadsheet_name)

        print('Temperature inside: {0:0.1f} C'.format(temperature_inside))
        print('Humidity inside:    {0:0.1f} %'.format(humidity_inside))

        print('Temperature outside: {0:0.1f} C'.format(temperature_outside))
        print('Humidity outside:    {0:0.1f} %'.format(humidity_outside))

        print('Fan Speed: {0}'.format(fan_speed))
        print('Is heating: {0}'.format(is_heating))



        try:
            self.worksheet.append_row((datetime.datetime.now().isoformat(), temperature_inside, humidity_inside, temperature_outside, humidity_outside, fan_speed, is_heating, score))
        except:
            print('Append error, logging in again')
            self.worksheet = None

        print('Wrote a row to {0}'.format(self.spreadsheet_name))

    def log2(self, temperature_inside, humidity_inside, temperature_outside, humidity_outside, previous_temperature_inside, previous_humidity_inside, previous_temperature_outside, previous_humidity_outside, fan_speed=0, is_heating=False):
        if self.worksheet is None:
            self.worksheet = self.login_open_sheet(settings.GDOCS_OAUTH_JSON, self.spreadsheet_name)

        print('Previous Temperature inside: {0:0.1f} C'.format(previous_temperature_inside))
        print('Previous Humidity inside:    {0:0.1f} %'.format(previous_humidity_inside))

        print('Previous Temperature outside: {0:0.1f} C'.format(previous_temperature_outside))
        print('Previous Humidity outside:    {0:0.1f} %'.format(previous_humidity_outside))

        print('Temperature inside: {0:0.1f} C'.format(temperature_inside))
        print('Humidity inside:    {0:0.1f} %'.format(humidity_inside))

        print('Temperature outside: {0:0.1f} C'.format(temperature_outside))
        print('Humidity outside:    {0:0.1f} %'.format(humidity_outside))

        print('Fan Speed: {0}'.format(fan_speed))
        print('Is heating: {0}'.format(is_heating))

        try:
            self.worksheet.append_row((datetime.datetime.now().isoformat(), temperature_inside, humidity_inside, temperature_outside, humidity_outside, previous_temperature_inside, previous_humidity_inside, previous_temperature_outside, previous_humidity_outside, fan_speed, is_heating))
        except:
            print('Append error, logging in again')
            self.worksheet = None

        print('Wrote a row to {0}'.format(self.spreadsheet_name))

    def log3(self, temperature_inside, humidity_inside, temperature_outside, humidity_outside, previous_temperature_inside, previous_humidity_inside, previous_temperature_outside, previous_humidity_outside, fan_speed=0, is_heating=False, score=0, real_score=0, predicted_humidity="", predicted_temperature=""):
        if self.worksheet is None:
            self.worksheet = self.login_open_sheet(settings.GDOCS_OAUTH_JSON, self.spreadsheet_name)

        print('Previous Temperature inside: {0:0.1f} C'.format(previous_temperature_inside))
        print('Previous Humidity inside:    {0:0.1f} %'.format(previous_humidity_inside))

        print('Previous Temperature outside: {0:0.1f} C'.format(previous_temperature_outside))
        print('Previous Humidity outside:    {0:0.1f} %'.format(previous_humidity_outside))

        print('Temperature inside: {0:0.1f} C'.format(temperature_inside))
        print('Humidity inside:    {0:0.1f} %'.format(humidity_inside))

        print('Temperature outside: {0:0.1f} C'.format(temperature_outside))
        print('Humidity outside:    {0:0.1f} %'.format(humidity_outside))

        print('Score estimated: {0}'.format(score))
        print('Temperature estimated: {0}'.format(predicted_temperature))
        print('Humidity estimated: {0}'.format(predicted_humidity))
        print('Fan Speed: {0}'.format(fan_speed))
        print('Is heating: {0}'.format(is_heating))

        try:
            self.worksheet.append_row((datetime.datetime.now().isoformat(), temperature_inside, humidity_inside, temperature_outside, humidity_outside, previous_temperature_inside, previous_humidity_inside, previous_temperature_outside, previous_humidity_outside, fan_speed, is_heating, score, real_score))
        except:
            print('Append error, logging in again')
            self.worksheet = None

        print('Wrote a row to {0}'.format(self.spreadsheet_name))

    def login_open_sheet(self, oauth_key_file, spreadsheet):
        """Connect to Google Docs spreadsheet and return the first worksheet."""
        try:
            scope =  ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
            credentials = ServiceAccountCredentials.from_json_keyfile_name(oauth_key_file, scope)
            gc = gspread.authorize(credentials)
            worksheet = gc.open(spreadsheet).sheet1
            return worksheet
        except Exception as ex:
            print('Unable to login and get spreadsheet.  Check OAuth credentials, spreadsheet name, and make sure spreadsheet is shared to the client_email address in the OAuth .json file!')
            print('Google sheet login failed with error:', ex)
            sys.exit(1)