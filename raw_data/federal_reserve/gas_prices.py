import fred_data

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Helper Functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def helper_find_gas_price_ids():

    s_header = r"Average Price: Gasoline, Unleaded Regular"
    s_cbsa = "(CBSA)"

    df_search = fred_data.search_for_ids_by_category(32217)
    df_search = df_search.loc[df_search["title"].str.contains(s_header)]
    df_search = df_search.loc[df_search["title"].str.contains(s_cbsa)]
    fred_ids = df_search["id"].unique()
    return fred_ids

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Work Functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def get_df_gas_prices(start_date=None, end_date=None):

    gas_price_ids = helper_find_gas_price_ids()

    df_gas_prices = fred_data.get_df_series_data(gas_price_ids, start_date=start_date, end_date=end_date)

    df_gas_prices.to_csv('test.csv')

    return df_gas_prices



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == "__main__":

    # df = fred_data.search_for_ids_by_category(32217)
    # df.to_csv('test.csv')

    print(get_df_gas_prices("2020-01-01", "2022-12-31"))

