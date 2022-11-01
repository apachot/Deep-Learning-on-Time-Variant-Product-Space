import json
import numpy as np
import pandas as pd
import math
from sklearn import preprocessing

country_list = pd.read_csv('./input/country_list.csv', header=None, index_col=False).values
country_list = [i[0] for i in country_list]

for country in country_list:

	datatemp = pd.read_csv('./input/exports/FRA/exports_FRA_1995.csv')
	product_id = pd.unique(datatemp['product_id']).tolist()
	hs_product_code = pd.unique(datatemp['hs_product_code']).tolist()

	mynode_ids = pd.DataFrame(product_id, index=hs_product_code).to_dict()[0]
	#print(mynode_ids)


	data = pd.read_csv('./input/proximities/HS6_Proximities_0.55_2019.csv')
	del data['weight']
	myedges = data.values.tolist()
	for k in range(0, len(myedges)):
		i = myedges[k][0]
		j = myedges[k][1]
		
		if(i!='unspecified' and i!='travel' and i!='transport' and i!='financial' and i!='ict'):
			i = str(i).zfill(6)
		if(j!='unspecified' and j!='travel' and j!='transport' and j!='financial' and j!='ict'):
			j = str(j).zfill(6)
		#print("i",i,"j",j)

		index_i = hs_product_code.index(i)
		index_j = hs_product_code.index(j)
		code_i = product_id[index_i]-5000
		code_j = product_id[index_j]-5000
		if code_i >= 6000:
			code_i = code_i - 961
		if code_j >= 6000:
			code_j = code_j - 961
		

		myedges[k][0] = code_i
		myedges[k][1] = code_j
	
	# weights
	data = pd.read_csv('./input/proximities/HS6_Proximities_0.55_2019.csv')
	del data['target']
	del data['source']
	myweights = data.to_numpy().transpose()[0].tolist()

	print("country", country)
	myFX = []
	for year in range(1995, 2021):
		data = pd.read_csv('./input/exports/'+country+'/exports_'+country+'_'+str(year)+'.csv')
		myFXtmp = data['export_value'].values.tolist()
		myFXtmp = [0 if math.isnan(x) else x for x in myFXtmp]
		myFX.append(myFXtmp)

	print("myFX.len", len(myFX))
	print("myedges.len", len(myedges))
	print("myweights.len", len(myweights))

	dictionary = {
	    "edges": myedges,
	    "weights": myweights,
	    "X": myFX
	}
	json_name = "./dataset/productspace_"+country+".json"
	print("writing", json_name, "...")
	with open(json_name, "w") as outfile:
	    json.dump(dictionary, outfile)
