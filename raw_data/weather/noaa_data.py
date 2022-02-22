from datetime import datetime
import matplotlib.pyplot as plt
from meteostat import Stations, Daily, units
import pandas as pd

import cfg
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Global variables
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

NOAA_TOKEN = cfg.NOAA_TOKEN
CSV_ZIP_CODE_TO_COORDS = r"zip_code_to_coordinates.csv"
PICKLE_TEMPERATURE_HISTORICAL = r"temperature_historical.pkl"

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Helper Functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Work functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_df_weather_for_all_zip_codes():
    df_coords = pd.read_csv(CSV_ZIP_CODE_TO_COORDS)
    df_coords["zip_code"] = df_coords['zip_code'].astype(str).str.zfill(5)

    df_all_temperatures = None

    for index, row in df_coords.iterrows():
        print("working on {}, latitude={}, longitude={}".format(row["zip_code"], row["latitude"], row["longitude"]))
        df_temperature = get_df_weather_for_coords(row["latitude"], row["longitude"])
        df_temperature["latitude"] = row["latitude"]
        df_temperature["longitude"] = row["longitude"]
        df_temperature["zip_code"] = row["zip_code"]

        if df_all_temperatures is None:
            df_all_temperatures = df_temperature
        else:
            df_all_temperatures = pd.concat([df_all_temperatures, df_temperature])

    df_all_temperatures.to_pickle(PICKLE_TEMPERATURE_HISTORICAL)

    return df_coords


#todo: calc temperature stats by month.
def get_df_weather_for_coords(latitude, longitude):

    # Time period
    start = datetime(2010, 1, 1)
    end = datetime(2020, 12, 31)

    # Get closest weather station
    stations = Stations()
    stations = stations.nearby(latitude, longitude)
    stations = stations.inventory('daily', (start, end))
    station = stations.fetch(1)

    # Get daily data
    df_temps = Daily(station, start, end)
    df_temps = df_temps.convert(units.imperial)
    df_temps = df_temps.fetch()
    df_temps = df_temps.reset_index()
    df_temps["time"] = pd.to_datetime(df_temps["time"])
    df_temps["month"] = pd.DatetimeIndex(df_temps['time']).month

    df_avg_temp_by_month = df_temps.groupby(df_temps['month'])['tavg', 'tmax', 'tmin'].mean()

    return df_avg_temp_by_month


if __name__ == "__main__":

    df = get_df_weather_for_all_zip_codes()

    df = pd.read_pickle(PICKLE_TEMPERATURE_HISTORICAL)
    print(df)