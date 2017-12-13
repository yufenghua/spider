def cleanElement(elist):
	if elist is None:
		return None
	resultList=[]
	for item in elist:
		if item is None or item.string='' or item.string='\n':
			continue
		resultList.add(item)
