import raw_data.census.census_data as census
import pandas as pd
import cfg


def get_df_education_level(year, state_abbrev, zcta=None):

    census_codes_educ = ['B06009_001E', 'B06009_002E', 'B06009_003E', 'B06009_004E', 'B06009_005E', 'B06009_006E']
    df_educ = census.get_df_census_data(census_codes_educ, year, state_abbrev, zcta=zcta)

    # Rename columns
    df_educ = df_educ.rename(columns = {"Total: Place Of Birth By Educational Attainment In The United States": "education_total_population_>25"})
    for col in df_educ.columns[:len(census_codes_educ)]:
        print(col[-1])
        new_col_name = col.strip()
        new_col_name = new_col_name.replace("Total:!!", "education_")
        new_col_name = new_col_name.replace(" Place Of Birth By Educational Attainment In The United States", "")
        new_col_name = new_col_name.replace("'", "")
        new_col_name = new_col_name.replace(" ", "_")
        new_col_name = new_col_name.lower()

        df_educ = df_educ.rename(columns = {col: new_col_name})

    return df_educ


def get_df_education_level_percentages(df_educ):

    educ_columns = len([col for col in df_educ.columns])






# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == "__main__":

    df = get_df_education_level(2020, "MI", zcta="48130")
    print(df)