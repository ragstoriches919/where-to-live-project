import raw_data.census.census_data as census
import pandas as pd
import cfg


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Helper Functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# def get_df_marital_status_percentages(df_marital):
#
#     for col in df_marital.columns:
#         if "male"




# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Work Functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_df_marital_status(year, state_abbrev, zcta = None):

    """
    Returns marital status by gender
    :param year: Integer
    :param state_abbrev: String
    :param zcta: String Ex.) "06074"
    :return: DataFrame
    """
    
    census_codes_marital_status = ['B12001_002E', 'B12001_003E', 'B12001_004E', 'B12001_009E', 'B12001_010E',
                                   'B12001_011E', 'B12001_012E', 'B12001_013E', 'B12001_018E', 'B12001_019E']

    df_marital = census.get_df_census_data(census_codes_marital_status, year, state_abbrev, zcta=zcta)

    # Rename columns
    for col_name in df_marital.columns[0:len(census_codes_marital_status)]:

        new_col_name = col_name.replace('Total:!!', "")
        new_col_name = new_col_name.replace(' SEX BY MARITAL STATUS FOR THE POPULATION 15 YEARS AND OVER'.title(), "")
        new_col_name = new_col_name.replace(" ", "_")
        new_col_name = new_col_name.replace(",", "")
        new_col_name = new_col_name.replace(":!!", "_")
        new_col_name = new_col_name.replace(":", "")
        new_col_name = new_col_name.lower()

        df_marital = df_marital.rename(columns = {col_name : new_col_name})

    return df_marital

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == "__main__":

    get_df_marital_status(2020, "CT", "06074")