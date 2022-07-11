import cfg
import pandas as pd
import requests
import os


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Global variables
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

API_KEY_DEPT_OF_EDUCATION = cfg.API_KEY_DEPT_OF_EDUCATION
PICKLE_COLLEGE_SCORE_CARD = os.path.join(cfg.ROOT_DIR, "raw_data/dept_of_education/pickled_files/college_score_card.pkl")


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Work Functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_df_college_score_card(parameters, fields, year):

    """
    Returns relevant information from the DOE college score card API
    To read documentation:  https://collegescorecard.ed.gov/data/documentation/
    :param parameters: List of Strings Ex.) ["school.name=New%20York"]
    :param fields: List of Strings Ex.) ["school.name", "id", "school.zip", "location.lat", "location.lon", "school.city", "school.state"]
    :param year: Integer -- I don't call this anywhere in the function yet.
    :return: DataFrame
    """

    parameters_str = "" if parameters == [] else ",".join(parameters)
    fields_str = "" if fields == [] else "_fields=" + ",".join(fields)
    url_header = r"https://api.data.gov/ed/collegescorecard/v1/schools?"
    per_page = str(100)
    url = f"{url_header}&{parameters_str}&per_page={per_page}&page=0&{fields_str}&api_key={cfg.API_KEY_DEPT_OF_EDUCATION}"
    response = requests.get(url).json()
    print(response)
    total_results = response["metadata"]["total"]

    for i in range(total_results//int(per_page) + 1):
        if i == 0:
            print("page " + str(i))
            print(url)
            data = response["results"]
            df_colleges = pd.json_normalize(data)
            df_colleges = df_colleges[fields]
        else:
            print("page " + str(i))
            url = url.replace("page=" + str(i-1), "page=" + str(i))
            print(url)
            response = requests.get(url).json()
            data = response["results"]
            df_colleges_temp = pd.json_normalize(data)
            df_colleges_temp = df_colleges_temp[fields]
            df_colleges = pd.concat([df_colleges, df_colleges_temp])

    df_colleges = df_colleges.sort_values(by=[df_colleges.columns[0]])
    df_colleges.to_pickle(PICKLE_COLLEGE_SCORE_CARD)
    return df_colleges

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


if __name__ == "__main__":

    # parameters = ["school.name=New%20York"]
    parameters = ["school.state=CT"]

    fields = ["school.name", "id", "school.zip", "location.lat", "location.lon", "school.city", "school.state",
              "school.tuition_revenue_per_fte", "latest.student.demographics.unemployment",
              "latest.student.demographics.median_hh_income", "latest.student.demographics.avg_family_income",
              "latest.cost.tuition.in_state",
              "latest.cost.tuition.out_of_state", "latest.cost.tuition.program_year",
              "latest.cost.avg_net_price.overall", "latest.student.size", "latest.admissions.admission_rate.overall",
              "latest.admissions.sat_scores.midpoint.math", "latest.admissions.sat_scores.midpoint.writing",
              "latest.admissions.sat_scores.midpoint.critical_reading", "latest.admissions.sat_scores.average.overall"]
    #
    get_df_college_score_card(parameters, fields, 2020)

    df = pd.read_pickle(PICKLE_COLLEGE_SCORE_CARD)
    print(df)