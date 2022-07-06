import os

API_KEY_CENSUS = r"4715d5f869c5ebbad9f7a58d3fd8deb1ff0401a8"
API_KEY_OPENSTATES = r"ed531324-579a-4ef6-ad87-4cee13663e25"
NOAA_TOKEN = r"kOKWxjRWxlMRqNUUwihFmRXklcbIDqeZ"


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_CENSUS_CODES = os.path.join(ROOT_DIR, "helper_data", "census_codes.csv")
CSV_STATE_CODES = os.path.join(ROOT_DIR, "helper_data", "state_codes.csv")
CSV_ZTCA_TO_MSA = os.path.join(ROOT_DIR, "helper_data", "ztca_to_msa.csv")
CSV_ZIP_CODE_TO_COORDS = os.path.join(ROOT_DIR, "helper_data", "zip_code_to_coordinates.csv")
# EXCEL_ZIPCODE_TO_ZCTA = os.path.join(ROOT_DIR, "helper_data", "ZiptoZcta_Crosswalk_2021.xlsx")
CSV_ZIPCODE_TO_ZCTA = os.path.join(ROOT_DIR, "helper_data", "zip_code_to_zcta_2021.csv")

