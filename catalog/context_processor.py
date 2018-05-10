from django.core.urlresolvers import reverse

def menu(request):
	menu = {'menu1':[
		{'name': 'Home', 'url': reverse('index')},
		{'name': 'All books', 'url': reverse('books')},
		{'name': 'All authors', 'url': reverse('authors')},
	],
	'menu2':[
		{'name': 'My Borrowed', 'url': reverse('my-borrowed')},
	],
	'menu3':[
		{'name': 'All Borrowed', 'url': reverse('all-borrowed')},
	]}
	
	for item in menu['menu1']:
		if request.path == item['url']:
			item['active'] = True
	
	for item in menu['menu2']:
		if request.path == item['url']:
			item['active'] = True

	for item in menu['menu3']:
		if request.path == item['url']:
			item['active'] = True
			
	return menu