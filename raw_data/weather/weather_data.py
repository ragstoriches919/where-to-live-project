from datetime import datetime
import matplotlib.pyplot as plt
from meteostat import Stations, Daily, units, Monthly, Hourly, Point
import pandas as pd
import numpy as np
import os
import cfg
import raw_data.census.census_data as census

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Global variables
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

NOAA_TOKEN = cfg.NOAA_TOKEN
CSV_ZIP_CODE_TO_COORDS = cfg.CSV_ZIP_CODE_TO_COORDS

PICKLE_WEATHER_TOP_METROS = os.path.join(cfg.ROOT_DIR, "raw_data/weather/pickled_files/weather_top_metros.pkl")

# PICKLE_TEMPERATURE_HISTORICAL_USING_POINT_DATA = r"pickled_files/temperature_historical_using_points.pkl"

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
            df_temperature = get_df_daily_weather_by_coord_point(row["latitude"], row["longitude"], start_datetime, end_datetime)
        except:
            print("failed to get point data, trying to get station data now...")
            try:
                df_temperature = get_df_daily_weather_by_station(row["latitude"], row["longitude"], start_datetime, end_datetime)
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

    # if b_point_data:
    #     df_all_temperatures.to_pickle(PICKLE_TEMPERATURE_HISTORICAL_USING_POINT_DATA)
    # else:
    #     df_all_temperatures.to_pickle(PICKLE_TEMPERATURE_HISTORICAL)

    return df_coords


def get_df_daily_weather_by_station(latitude, longitude, start_datetime, end_datetime):

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

    # Get daily data
    df_weather = Hourly(station, start_datetime, end_datetime)
    df_weather = df_weather.convert(units.imperial)
    df_weather = df_weather.fetch()
    df_weather = df_weather.reset_index()

    return df_weather


def get_df_monthly_weather_by_station(df_weather):

    # Add tavg, tmax, tmin
    df_weather["date"] = pd.to_datetime(df_weather["time"].astype(str).str[:10])
    df_weather = df_weather.groupby(["date"])["temp"].agg({'mean', 'min', 'max'}).reset_index()
    df_weather["month"] = df_weather["date"].dt.month

    df_weather_grouped = df_weather.groupby(["month"])['mean', 'min', 'max'].mean().reset_index()
    df_weather_grouped.columns = ["month", "tavg", "tmin", "tmax"]

    return df_weather_grouped


def get_df_daily_weather_by_coord_point(latitude, longitude, start_datetime, end_datetime):

    """
    # More trustworthy way of getting data I think...
    :param latitude: Float Ex.) 42.7654
    :param longitude: Float Ex.) -71.4676
    :param start_datetime: datetime(2020, 1, 1)
    :param end_datetime: datetime(2020, 1, 5)
    :return:
    """

    # Create Point for given latitude/longitude
    my_location = Point(latitude, longitude, 70)

    # Get daily data for location
    df_weather = Daily(my_location, start_datetime, end_datetime)
    df_weather = df_weather.convert(units.imperial)
    df_weather = df_weather.fetch()
    df_weather = df_weather.reset_index()

    return df_weather


def get_df_monthly_weather_by_coord_point(df_weather):

    """
    Aggregates daily weather into monthly
    :param df_weather: DataFrame.  Can use either get_df_weather_by_coord_point() or get_df_weather_by_station().
    :return: DataFrame
    """

    df_weather["time"] = pd.to_datetime(df_weather["time"])
    df_weather["month"] = pd.DatetimeIndex(df_weather['time']).month
    df_avg_temp_by_month = df_weather.groupby(df_weather['month'])['tavg', 'tmax', 'tmin'].mean().reset_index()

    return df_avg_temp_by_month


def get_df_daily_weather_by_zip_code(zip_code, start_datetime, end_datetime):

    """
    Gets daily values by zip code
    :param zip_code: String
    :param start_datetime: datetime(2020, 1, 1)
    :param end_datetime: datetime(2022, 12, 31)
    :return: DataFrame
    """

    df_coords = pd.read_csv(CSV_ZIP_CODE_TO_COORDS)
    df_coords["zip_code"] = df_coords['zip_code'].astype(str).str.zfill(5)
    latitude = df_coords.loc[df_coords["zip_code"] == zip_code]["latitude"].iloc[0]
    longitude = df_coords.loc[df_coords["zip_code"] == zip_code]["longitude"].iloc[0]

    print("working on {}, latitude={}, longitude={}".format(zip_code, latitude, longitude))
    df_weather = get_df_daily_weather_by_coord_point(latitude, longitude, start_datetime, end_datetime)

    df_weather["latitude"] = latitude
    df_weather["longitude"] = longitude
    df_weather["zip_code"] = zip_code

    return df_weather


def get_df_monthly_weather_by_zip_code(df_weather):

    """
    Gets monthly data by zip code
    :param df_weather: DataFrame (from get_df_daily_weather_by_zip_code())
    :return: DataFrame
    """

    df_weather["time"] = pd.to_datetime(df_weather["time"])
    df_weather["month"] = pd.DatetimeIndex(df_weather['time']).month
    df_avg_temp_by_month = df_weather.groupby(['month', 'latitude', 'longitude', 'zip_code'])['tavg', 'tmax', 'tmin'].mean().reset_index()

    return df_avg_temp_by_month


def get_df_weather_data_for_top_metro_areas():

    num_metro_areas = 25
    df_all_zips = census.get_df_zips_to_use_for_weather_analysis()
    df_top_metros = df_all_zips.head(num_metro_areas)

    start_datetime = datetime(2015, 1, 1)
    end_datetime = datetime(2020, 12, 31)

    df_all_weather = None
    for index, row in df_top_metros.iterrows():
        zip_code = str(row["zip_code"])
        city = str(row["po_name"])
        state = str(row["state"])


        try:
            df_daily = get_df_daily_weather_by_zip_code(zip_code, start_datetime, end_datetime)
            df_weather = get_df_monthly_weather_by_zip_code(df_daily)
            df_weather["latitude"] = df_weather["latitude"].iloc[0]
            df_weather["longitude"] = df_weather["longitude"].iloc[0]
            df_weather["zip_code"] = zip_code
            df_weather["city"] = city
            df_weather["state"] = state
            df_weather["data_type"] = "coordinate_point"

        except:
            try:
                print("Weather by coordinate point didn't work for {}.  Trying to fetch weather by station...".format(zip_code))
                df_coords = pd.read_csv(CSV_ZIP_CODE_TO_COORDS)
                df_coords["zip_code"] = df_coords['zip_code'].astype(str).str.zfill(5)
                latitude = df_coords.loc[df_coords["zip_code"] == zip_code]["latitude"].iloc[0]
                longitude = df_coords.loc[df_coords["zip_code"] == zip_code]["longitude"].iloc[0]

                df_weather = get_df_daily_weather_by_station(latitude, longitude, start_datetime, end_datetime)
                df_weather = get_df_monthly_weather_by_station(df_weather)
                df_weather["latitude"] = latitude
                df_weather["longitude"] = longitude
                df_weather["zip_code"] = zip_code
                df_weather["city"] = city
                df_weather["state"] = state
                df_weather["data_type"] = "station"


            except:
                print("Weather by station didn't work either for {}.  Skipping this zip code...".format(zip_code))

        if df_all_weather is None:
            df_all_weather = df_weather
        else:
            df_all_weather = pd.concat([df_all_weather, df_weather])
        df_all_weather.to_pickle(PICKLE_WEATHER_TOP_METROS)

    return df_all_weather


if __name__ == "__main__":

    lat = 29.827485999999997
    long = -95.65992
    start = datetime(2015, 1, 1)
    end = datetime(2020, 12, 31)

    # df = get_df_weather_data_for_top_metro_areas()
    # print(df)
    #
    df = pd.read_pickle(PICKLE_WEATHER_TOP_METROS)
    print(df)
