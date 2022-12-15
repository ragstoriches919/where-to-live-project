import raw_data.census.census_data as census
import geographic_data.build_geo as geo
import raw_data.census.helpers_census as helpers_census
import pandas as pd
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

    return df_educ



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Work Functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def get_df_education_level(year, state_abbrev, zcta=None):

    """
    Gets data by educational attainment, e.g. high school, undergrad, grad, etc.
    :param year: integer Ex.) 2019
    :param state_abbrev: String Ex.) "CT"
    :param zcta: String Ex.) "06074"
    :return: DataFrame
    """

    census_codes_educ = ['B06009_001E', 'B06009_002E', 'B06009_003E', 'B06009_004E', 'B06009_005E', 'B06009_006E']
    df_educ = census.get_df_census_data(census_codes_educ, year, state_abbrev, zcta=zcta)

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
    df_educ["%_college_or_higher"] = df_educ["%_education_bachelors_degree"] + df_educ["%_education_graduate_or_professional_degree"]

    return df_educ

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Percentiles
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def get_df_educ_percentile_zip(year, zip):
    """
    Get income percentile by zip
    :param year: (int) Ex.) 2020
    :param zip: (str) Ex.) "06074"
    :return: DataFrame
    """

    df_all_zips = geo.get_df_zip_code_complete(use_csv=True)
    df_zip = df_all_zips.loc[df_all_zips["zip"] == zip]

    # Get income percentiles relative to towns in the same state
    state = df_zip["state"].iloc[0]
    df_income_state = get_df_income_percentile_state(year, state)
    state_cols = helpers_census.list_diff(df_income_state.columns, df_zip.columns) + ["zip"]
    df_zip = pd.merge(df_zip, df_income_state[state_cols], on="zip")

    # Get income percentiles relative to towns in the same CBSA
    cbsa_name = df_zip["cbsa_name"].iloc[0]
    df_income_cbsa = get_df_income_percentile_cbsa(year, cbsa_name)
    cbsa_cols = helpers_census.list_diff(df_income_cbsa.columns, df_zip.columns) + ["zip"]
    df_zip = pd.merge(df_income_cbsa[cbsa_cols], df_income_state, on="zip", how="outer")

    return df_zip


def get_df_educ_percentile_state(year, state):
    """
    Returns income percentile by state
    :param year: (int) Ex.) 2020
    :param state: (str) Ex.) "CT"
    :return: DataFrame
    """

    df_educ = helpers_census.helper_get_df_state_percentile(year, state, get_df_education_level, "%_college_or_higher")
    df_zip = geo.get_df_zip_code_complete(use_csv=True)

    columns_order = ["percentile_state_%_college_or_higher", "%_college_or_higher"] + list(set(df_zip.columns)) #+ list(df_zip.columns)

    df_educ = df_educ[columns_order]
    df_educ = df_educ.sort_values(by=["percentile_state_%_college_or_higher"])

    return df_educ


def get_df_income_percentile_cbsa(year, cbsa_name):
    """
    Returns the income percentile of all towns in the given CBSA
    :param year: (int) Ex.) 2020
    :param cbsa_name: (str) Ex.) "Dallas-Fort Worth-Arlington, TX"
    :return:
    """

    col_name = "median_household_income_2019_dollars"
    df_income_percentile_cbsa = helpers_census.helper_get_df_cbsa_percentile(year, cbsa_name, get_df_median_income,
                                                                             col_name)

    return df_income_percentile_cbsa


def get_df_education_level_percentiles():
    pass

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Education Summary
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def get_df_zip_education_summary(year, zip):

    df_zip_educ = get_df_education_level(year, zip)

    df_zip_educ = df_zip_educ.loc[df_zip_educ["zip"] == zip]

    return df_zip_educ

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == "__main__":

    # df = get_df_education_level(2020, "CT", "06074")
    # print(df)

    df = get_df_educ_percentile_state(2020, "FL")
    print(df)