import pandas as pd
import os
data = pd.io.stata.read_stata('input/country_hsproduct6digit_year.dta')
location_code = pd.unique(data['location_code'])
print("location_code", location_code)
pd.DataFrame(location_code).to_csv('input/country_list.csv', header=False, index=False)
