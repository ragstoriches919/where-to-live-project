from datetime import datetime
import matplotlib.pyplot as plt
from meteostat import Stations, Daily, units, Monthly, Hourly, Point
import pandas as pd
import numpy as np

import cfg
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Global variables
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

NOAA_TOKEN = cfg.NOAA_TOKEN
CSV_ZIP_CODE_TO_COORDS = cfg.CSV_ZIP_CODE_TO_COORDS
PICKLE_TEMPERATURE_HISTORICAL = r"pickled_files/temperature_historical.pkl"
PICKLE_TEMPERATURE_HISTORICAL_USING_POINT_DATA = r"pickled_files/temperature_historical_using_points.pkl"

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Helper Functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Work functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_df_weather_for_all_zip_codes(b_point_data=True):
    df_coords = pd.read_csv(CSV_ZIP_CODE_TO_COORDS).head()
    df_coords["zip_code"] = df_coords['zip_code'].astype(str).str.zfill(5)
    start_datetime = datetime(2010, 1, 1)
    end_datetime = datetime(2020, 12, 31)

    df_all_temperatures = None

    for index, row in df_coords.iterrows():
        print("working on {}, latitude={}, longitude={}".format(row["zip_code"], row["latitude"], row["longitude"]))

        try:
            df_temperature = get_df_weather_by_coord_point(row["latitude"], row["longitude"], start_datetime, end_datetime)
        except:
            print("failed to get point data, trying to get station data now...")
            try:
                df_temperature = get_df_weather_by_station(row["latitude"], row["longitude"], start_datetime, end_datetime)
            except:
                df_temperature = pd.DataFrame()
                df_temperature['tavg'] = np.nan
                df_temperature['tmax'] = np.nan
                df_temperature['tmin'] = np.nan

        df_temperature["latitude"] = row["latitude"]
        df_temperature["longitude"] = row["longitude"]
        df_temperature["zip_code"] = row["zip_code"]

        if df_all_temperatures is None:
            df_all_temperatures = df_temperature
        else:
            df_all_temperatures = pd.concat([df_all_temperatures, df_temperature])

    if b_point_data:
        df_all_temperatures.to_pickle(PICKLE_TEMPERATURE_HISTORICAL_USING_POINT_DATA)
    else:
        df_all_temperatures.to_pickle(PICKLE_TEMPERATURE_HISTORICAL)

    return df_coords


def get_df_weather_by_station(latitude, longitude, start_datetime, end_datetime):

    """
    # Not as trustworthy as getting data by coord point I think...
    :param latitude: Float Ex.) 42.7654
    :param longitude: Float Ex.) -71.4676
    :param start_datetime: datetime(2020, 1, 1)
    :param end_datetime: datetime(2020, 1, 5)
    :return:
    """

    # Get closest weather station
    stations = Stations()
    stations = stations.nearby(latitude, longitude)
    stations = stations.inventory('daily', (start_datetime, end_datetime))
    station = stations.fetch(1)
    print(station)

    # Get daily data
    df_temps = Hourly(station, start_datetime, end_datetime)
    df_temps = df_temps.convert(units.imperial)
    df_temps = df_temps.fetch()
    df_temps = df_temps.reset_index()
    df_temps["time"] = pd.to_datetime(df_temps["time"])
    df_temps["month"] = pd.DatetimeIndex(df_temps['time']).month

    df_avg_temp_by_month = df_temps.groupby(df_temps['month'])['tavg', 'tmax', 'tmin'].mean()

    return df_avg_temp_by_month


def get_df_weather_by_coord_point(latitude, longitude, start_datetime, end_datetime):

    """
    # More trustworthy way of getting data I think...
    :param latitude: Float Ex.) 42.7654
    :param longitude: Float Ex.) -71.4676
    :param start_datetime: datetime(2020, 1, 1)
    :param end_datetime: datetime(2020, 1, 5)
    :return:
    """

    # Create Point for Vancouver, BC
    my_location = Point(latitude, longitude, 70)

    # Get daily data for location
    df_temps = Daily(my_location, start_datetime, end_datetime)
    df_temps = df_temps.convert(units.imperial)
    df_temps = df_temps.fetch()
    df_temps = df_temps.reset_index()

    df_temps["time"] = pd.to_datetime(df_temps["time"])
    df_temps["month"] = pd.DatetimeIndex(df_temps['time']).month

    df_avg_temp_by_month = df_temps.groupby(df_temps['month'])['tavg', 'tmax', 'tmin'].mean().reset_index()

    return df_avg_temp_by_month


if __name__ == "__main__":

    lat = 41.8237
    long = -72.6212
    start = datetime(2015, 1, 1)
    end = datetime(2020, 12, 31)

    df = get_df_weather_by_coord_point(lat, long, start, end)



