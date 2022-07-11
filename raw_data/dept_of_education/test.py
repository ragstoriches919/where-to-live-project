import cfg
import pandas as pd
import requests

API_KEY_DEPT_OF_EDUCATION = cfg.API_KEY_DEPT_OF_EDUCATION


def get_df_college_score_card(parameters, fields, year):

    parameters_str = "" if parameters == [] else ",".join(parameters)
    fields_str = "" if fields == [] else "_fields=" + "".join(fields)
    url_header = r"https://api.data.gov/ed/collegescorecard/v1/schools?"
    # url = f"{url_header}&{parameters_str}&per_page=100&page=0&{fields_str},{year}.student.size&api_key={cfg.API_KEY_DEPT_OF_EDUCATION}"
    url = f"{url_header}&{parameters_str}&per_page=1&page=0&{fields_str}&api_key={cfg.API_KEY_DEPT_OF_EDUCATION}"

    print(url)
    response = requests.get(url).json()
    print(response)
    data = response["results"]
    df = pd.json_normalize(data)
    df.to_csv('test.csv')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


if __name__ == "__main__":

    parameters = ["school.name=New%20York"]

    fields = ["school.name", "id", "school.type", "school.zip", "school.city", "state", "tuition_revenue_per_fte",
              "student.demographics.unemployment", "student.demographics.median_hh_income", "students.demographics.avg_family_income"]
    
    get_df_college_score_card(parameters, fields, 2020)