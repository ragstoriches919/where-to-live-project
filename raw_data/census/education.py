import raw_data.census.census_data as census
import pandas as pd
import cfg


def get_df_education_level(year, state_abbrev, zcta=None):

    census_codes_educ = ['B06009_002E', 'B06009_003E', 'B06009_004E', 'B06009_005E', 'B06009_006E']
    df_educ = census.get_df_census_data(census_codes_educ, year, state_abbrev, zcta=zcta)

    print(df_educ)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == "__main__":

    df = get_df_education_level(2020, "CT", zcta="06074")
    print(df)