import json

def createExampleDoc(document,question):
	output = []
	createExampleDocWorker(document, [], output,question)
	dd = reduce(merge, output)
	return json.dumps(dd, sort_keys=True, indent=2, separators=(',', ':')).replace('\\"', '"')

#json_data=open('document.json').read()

#data = json.loads(json_data)

#results= anonymizeFacebookStatuses(data)


def createExampleDocWorker(document, keys, output,question):
	if type(document) == type([]):
		for jj, item in enumerate(document):
			createExampleDocWorker(item, keys, output,question)			
			#t_keys = list(keys)
			#t_keys.append(str(jj))
			#try:
			#	t_keys = list(keys)
			#	t_keys.append(item.keys())			
			#	createExampleDocWorker(item, t_keys, output)
			#except Exception: pass
	elif type(document) == type({}):
		for key, value in document.items():
			t_keys = list(keys)
			t_keys.append(key)
			createExampleDocWorker(value, t_keys, output,question)
	else:
		keys = processKeys(keys,question)
		d = {}
		add_keys(d, keys, document)
		output.append(d)

def processKeys(keys,question=True):
		new_keys = []
		ignored_keys = ['0', '1']
		for jj,key in enumerate(keys):
			if not key in ignored_keys:
				if question:
					new_keys.append("<a href='#' onclick=\"$('#questions')[0].value += '"+ ".".join(keys[:jj]+[key])+",'\">"+str(key)+"</a>")
				else:
					new_keys.append("<a href='#' onclick=\"$('#fields')[0].value += '"+ ".".join(keys[:jj]+[key])+",'\">"+str(key)+"</a>")
			else: new_keys.append(key)
		return new_keys


def merge(a, b, path=None):
	    	if path is None: path = []
		for key in b:
			if key in a:
				if isinstance(a[key], dict) and isinstance(b[key], dict):
					merge(a[key], b[key], path + [str(key)])
			    	elif a[key] == b[key]:
					pass # same leaf value
			    	else:
					pass					
					#raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
			else:
			    	a[key] = b[key]

	    	return a


def add_keys(d, l, c=None):
		if len(l) > 1:
			d[l[0]] = _d = {}
		    	d[l[0]] = d.get(l[0], {})
		    	add_keys(d[l[0]], l[1:], c)
		else:
		    	d[l[0]] = c

