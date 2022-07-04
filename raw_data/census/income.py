import raw_data.census.census_data as census
import pandas as pd
import cfg

def get_df_income(year, state_abbrev, zcta=None):

    group = "B19013"
    df_census_codes = pd.read_csv(cfg.CSV_CENSUS_CODES)
    census_codes_income = list(df_census_codes.loc[df_census_codes["group"] == group]["census_code"].unique())

    df_income = census.get_df_census_data(census_codes_income, year, state_abbrev, zcta=zcta)

    print(df_income)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == "__main__":

    df = get_df_income(2019, "CT", zcta="06074")