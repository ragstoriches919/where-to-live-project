import os

API_KEY_CENSUS = r"4715d5f869c5ebbad9f7a58d3fd8deb1ff0401a8"
NOAA_TOKEN = r"kOKWxjRWxlMRqNUUwihFmRXklcbIDqeZ"


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_CENSUS_CODES = os.path.join(ROOT_DIR, "helper_data", "census_codes.csv")
CSV_STATE_CODES = os.path.join(ROOT_DIR, "helper_data", "state_codes.csv")
CSV_ZTCA_TO_MSA = os.path.join(ROOT_DIR, "helper_data", "ztca_to_msa.csv")
EXCEL_ZIPCODE_TO_ZCTA = os.path.join(ROOT_DIR, "helper_data", "ZiptoZcta_Crosswalk_2021.xlsx")

