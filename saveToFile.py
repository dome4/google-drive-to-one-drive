import os, io, json


def saveToFile(content, filename):

	"""
	save response in file
	"""
	filename = str(filename) + '.txt'
	
	"""
	remove file before setting new content
	"""
	try:
	    os.remove(filename)
	except OSError: 
	    print ('something went wrong')
	
	"""
	open stream to file
	"""
	file = io.open(filename, 'w', encoding='utf-8')
	
	
	"""
	write result in file
	"""   
	file.write(json.dumps(content, ensure_ascii=False))
	
	"""
	close file strem
	"""
	file.close()