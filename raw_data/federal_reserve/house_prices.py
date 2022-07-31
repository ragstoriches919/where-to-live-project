import fred_data

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Helper Functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def get_df_case_shiller_home_prices(start_date=None, end_date=None):

    """
    Gets Case-Shiller home price indices
    :return: DataFrame
    """

    fred_case_shiller_ids = ['SFXRSA', 'LXXRSA', 'SDXRSA', 'SEXRSA', 'NYXRSA', 'CHXRSA', 'PHXRSA', 'DNXRSA', 'DAXRSA',
                               'MIXRSA', 'BOXRSA', 'ATXRSA', 'WDXRSA', 'TPXRSA', 'LVXRSA', 'MNXRSA', 'POXRSA', 'CRXRSA',
                               'DEXRSA', 'CEXRSA']

    df_case_shiller_info = fred_data.get_df_series_data(fred_case_shiller_ids, start_date=start_date, end_date=end_date)
    df_case_shiller_info.to_csv('test.csv')

    return df_case_shiller_info


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == "__main__":

    get_df_case_shiller_home_prices(start_date= "2018-01-01", end_date="2022-12-31")

