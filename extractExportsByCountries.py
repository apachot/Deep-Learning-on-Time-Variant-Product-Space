import pandas as pd
import os
import math
from sklearn import preprocessing
dta_file = 'input/country_hsproduct6digit_year.dta'
print("Loading", dta_file,"...")

data = pd.io.stata.read_stata(dta_file)
print("Normalization...")

data['export_value'] = [0 if math.isnan(x) else x for x in data['export_value']]
data['import_value'] = [0 if math.isnan(x) else x for x in data['import_value']]

frames = pd.DataFrame(data['export_value'])
frames['import_value'] = data['import_value']

print(frames.head())
data_normalized = preprocessing.normalize(frames, axis=1)
print(data_normalized)
data['export_value'] = data_normalized[:,0]
data['import_value'] = data_normalized[:,1]
print("data['export_value']", data['export_value'])
print("data['import_value']", data['import_value'])

location_id = pd.unique(data['location_id'])
location_code = pd.unique(data['location_code'])
years = pd.unique(data['year'])
for location in location_code:
	location_folder = "./input/exports/"+str(location)
	if not os.path.exists(location_folder):
		os.makedirs(location_folder)
	for year in years:
		print("Processing year", year, "location", location)
		data_temp = data[data['year']==int(year)]
		data_temp = data_temp[data['location_code']==str(location)]
		file_path = location_folder+'/exports_'+str(location)+'_'+str(year)+'.csv'
		print("writing", file_path)
		data_temp.to_csv(file_path)	