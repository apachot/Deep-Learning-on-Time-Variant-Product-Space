import pandas as pd
import os
data = pd.io.stata.read_stata('input/country_hsproduct6digit_year.dta')
location_id = pd.unique(data['location_id'])
location_code = pd.unique(data['location_code'])
years = pd.unique(data['year'])
for location in location_code:
	location_folder = "./input/"+str(location)
	if not os.path.exists(location_folder):
		os.makedirs(location_folder)
	for year in years:
		print("Processing year", year, "location", location)
		data_temp = data[data['year']==int(year)]
		data_temp = data_temp[data['location_code']==str(location)]
		file_path = location_folder+'/exports_'+str(location)+'_'+str(year)+'.csv'
		print("writing", file_path)
		data_temp.to_csv(file_path)	