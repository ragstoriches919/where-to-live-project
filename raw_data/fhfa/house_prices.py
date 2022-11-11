import pandas as pd
url_fhfa = r"https://www.fhfa.gov/DataTools/Downloads/Documents/HPI/HPI_PO_metro.xls"


def get_df_fhfa_data():

    df_fhfa = pd.read_excel(url_fhfa)
    df_fhfa["cbsa"] = df_fhfa["cbsa"].astype(str)
    df_fhfa["quarter_identifier"] = df_fhfa["yr"] * 4 + df_fhfa["qtr"]

    return df_fhfa


def get_df_fhfa_home_price_appreciation_estimate_by_cbsa(year):

    """
    Since census data is lagged by a couple years, we can add a column that shows the FHFA's home price appreciation values for the missing quarters.
    :param year: (int) Ex.) 2020
    :return: DataFrame
    """

    df_fhfa = get_df_fhfa_data()
    df_fhfa = df_fhfa.loc[df_fhfa["yr"]>year]

    min_quarter = df_fhfa["quarter_identifier"].min()
    max_quarter = df_fhfa["quarter_identifier"].max()

    df_min_qtr = df_fhfa.loc[df_fhfa["quarter_identifier"] == min_quarter][["cbsa", "metro_name", "index_nsa", "index_sa"]]
    df_max_qtr = df_fhfa.loc[df_fhfa["quarter_identifier"] == max_quarter][["cbsa", "metro_name", "index_nsa", "index_sa"]]
    df_hpa = pd.merge(df_min_qtr, df_max_qtr, on=["cbsa", "metro_name"], suffixes=("_min", "_max"))
    df_hpa["hpa_sa"] = (df_hpa["index_sa_max"] / df_hpa["index_sa_min"]) - 1
    df_hpa["hpa_nsa"] = (df_hpa["index_nsa_max"] / df_hpa["index_nsa_min"]) - 1

    # df_hpa.to_csv("test.csv")

    return df_hpa


df = get_df_fhfa_home_price_appreciation_estimate_by_cbsa(2020)