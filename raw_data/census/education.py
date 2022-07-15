import raw_data.census.census_data as census
import pandas as pd
import cfg

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Helper Functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def get_df_education_level_percentages(df_educ):

    """
    Return a df containing percentage of population by educational attainment
    :param df_educ: DataFrame (get_df_education_level())
    :return: DataFrame
    """

    educ_columns = [col for col in df_educ.columns if "education" in col]
    for col in educ_columns:
        if col != "education_total_population_>25":
            df_educ["%_" + col] = df_educ[col] / df_educ["education_total_population_>25"] * 100

    df_educ["%_bachelors_and_higher"] = df_educ["%_education_bachelors_degree"] + df_educ["%_education_graduate_or_professional_degree"]

    return df_educ


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Work Functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def get_df_education_level(year, state_abbrev, zcta=None):

    """
    Get stats related to education levels
    :param year: Integer
    :param state_abbrev: String
    :param zcta: String Ex.) "06074"
    :return: DataFrame
    """

    census_codes_educ = ['B06009_001E', 'B06009_002E', 'B06009_003E', 'B06009_004E', 'B06009_005E', 'B06009_006E']
    df_educ = census.get_df_census_data(census_codes_educ, year, state_abbrev, zcta=None)

    # Rename columns
    df_educ = df_educ.rename(columns = {"Total: Place Of Birth By Educational Attainment In The United States": "education_total_population_>25"})
    for col in df_educ.columns[:len(census_codes_educ)]:
        new_col_name = col.strip()
        new_col_name = new_col_name.replace("Total:!!", "education_")
        new_col_name = new_col_name.replace(" Place Of Birth By Educational Attainment In The United States", "")
        new_col_name = new_col_name.replace("'", "")
        new_col_name = new_col_name.replace(" ", "_")
        new_col_name = new_col_name.lower()

        df_educ = df_educ.rename(columns = {col: new_col_name})

    df_educ = get_df_education_level_percentages(df_educ)

    # Generate percentile of educated people relative to rest of the state
    df_educ["%_highly_educated_percentile_state"] = df_educ["%_bachelors_and_higher"].rank(pct=True)

    if zcta:
        df_educ = df_educ.loc[df_educ["zcta"] == zcta]

    return df_educ


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == "__main__":

    get_df_education_level(2019, "CT", zcta=None)
