def getSoilData(root):

	soilData = []
	for child in root:
		subData ={}
		newRoot = child.iter('*')
		for child in newRoot:
			if('/mapserver' in child.tag):
				#add to subData dictionary
				newTag = child.tag.replace('{http://mapserver.gis.umn.edu/mapserver}', '')
				subData[newTag] = child.text
		#add subData to soilData
		soilData.append(subData)

	return soilData

#{http://www.opengis.net/gml}

