import pandas as pd
import cfg
from fredapi import Fred

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Helper Functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def helper_get_fred_series_data(fred_id, start_date=None, end_date=None):

    """
    Returns a pandas series containing data for given FRED id
    :param fred_id: String Ex.) "SFXRSA"
    :param start_date: String Ex.) "2020-01-01"
    :param end_date: String Ex.) "2020-12-31"
    :return: Pandas Series
    """

    fred = Fred(api_key=cfg.API_KEY_FRED)
    series_data = fred.get_series(fred_id, observation_start=start_date, observation_end=end_date)

    return series_data


def helper_get_fred_series_info(fred_id):

    """
    Returns a pandas series containing info about the given FRED id
    :param fred_id: String Ex.) "SFXRSA"
    :return: Pandas Series
    """

    fred = Fred(api_key=cfg.API_KEY_FRED)
    series_info = fred.get_series_info(fred_id)

    return series_info


def get_df_series_data(fred_ids, start_date=None, end_date=None):

    """
    Returns df of data for given FRED ids
    :param fred_ids: List of strings Ex.) ['SFXRSA', 'LXXRSA', 'SDXRSA']
    :return: DataFrame
    """

    df_series = pd.DataFrame()

    # Get data for each id from fredapi
    for id in fred_ids:
        df_info = helper_get_fred_series_info(id)
        title = df_info["title"]
        print(f"Getting data for {title}.  id={id}")

        df_data = helper_get_fred_series_data(id, start_date=start_date, end_date=end_date).to_frame()
        df_data.columns = [title]

        if df_series.empty:
            df_series = df_data
        else:
            # df_series = pd.concat([df_series, df_data])
            df_series = pd.merge(df_series, df_data, left_index=True, right_index=True, how="outer")

    return df_series


def get_df_series_info(fred_ids):

    """
    Returns df of info for given FRED ids
    :param fred_ids: List of strings Ex.) ['SFXRSA', 'LXXRSA', 'SDXRSA']
    :return: DataFrame
    """

    data = []

    # Get info for each id from fredapi
    for id in fred_ids:
        df_temp = helper_get_fred_series_info(id)
        data.append([df_temp["id"], df_temp["title"]])

    df_series_info = pd.DataFrame(data, columns = ["id", "title"])

    return df_series_info


def search_for_ids_by_keyword(search_term):

    """
    This doesn't work all that well.  Usually returns a timeout exception.
    :param search_term: String Ex.) "Potential GDP"
    :return: DataFrame
    """

    fred = Fred(api_key=cfg.API_KEY_FRED)
    search_results = fred.search(search_term).T
    print(search_results)
    fred_ids = search_results.columns
    df_search_info = get_df_series_info(fred_ids)

    return df_search_info


def search_for_ids_by_category(category_id):

    """
    Returns data given a FRED category id
    FRED API has category ids for specific datasets, like 32455 for inflation expectations
    :param category_id: int Ex.) 32455
    :return: DataFrame
    """

    fred = Fred(api_key=cfg.API_KEY_FRED)
    search_results = fred.search_by_category(category_id).T

    data = []
    for col in search_results:

        id = search_results[col]["id"]
        title = search_results[col]["title"]

        data.append([id, title])

    df_search = pd.DataFrame(data, columns=["id", "title"])

    return df_search


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == "__main__":

    search = search_for_ids_by_category(32217)
    print(search)
