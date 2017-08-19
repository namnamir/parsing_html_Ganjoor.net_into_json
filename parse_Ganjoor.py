#!/usr/bin/env python
# -*- coding: utf-8 -*-

#for opening links
import urllib2
#for json files
import simplejson

try:
	from bs4 import BeautifulSoup
except ImportError:
	from BeautifulSoup import BeautifulSoup

#for parsing CDATA
import re
#handeling UTF8 for json files | read more: http://code.opoki.com/loading-utf-8-json-file-in-python/
import codecs

# intitiating the link-style of the pages as well as giving the list of poems
style = ['ganjoor.net/hafez/ghazal/sh',
		 'https://ganjoor.net/moulavi/shams/ghazalsh/sh',
		 'https://ganjoor.net/moulavi/shams/ghazalsh/sh',
		 'https://ganjoor.net/moulavi/shams/ghazalsh/sh',
		 'https://ganjoor.net/moulavi/shams/ghazalsh/sh',
		 'https://ganjoor.net/moulavi/shams/ghazalsh/sh',
		 'https://ganjoor.net/moulavi/shams/ghazalsh/sh',
		 'https://ganjoor.net/saadi/divan/ghazals/sh',
		 'https://ganjoor.net/khayyam/robaee/sh']

poets = ['https://ganjoor.net/hafez/ghazal/', 
		 'https://ganjoor.net/moulavi/shams/a-kh/', 
		 'https://ganjoor.net/moulavi/shams/d/', 
		 'https://ganjoor.net/moulavi/shams/r-l/',
		 'https://ganjoor.net/moulavi/shams/m/',
		 'https://ganjoor.net/moulavi/shams/n-h/',
		 'https://ganjoor.net/moulavi/shams/y/',
		 'https://ganjoor.net/saadi/divan/ghazals/',
		 'https://ganjoor.net/khayyam/robaee/']

file      = 'poem.json'
directory = '/home/'

# opening the json file
def open_file(file):
	with open(file, 'rb') as json_file:
		return(simplejson.load(json_file))

# writing into the json file and close it
def close_file(file, poems):
	# using codecs helps to fix the problem of unicode. It write as UTF8 into the json file instead of writing as unicode or unicode-escape
	# read more: http://code.opoki.com/loading-utf-8-json-file-in-python/
	with codecs.open(file, 'w', encoding="utf-8") as json_outfile:  
		simplejson.dump(poems, json_outfile, sort_keys=True, indent=4, ensure_ascii=False)
	json_outfile.close()

# opening the link of each poem on Ganjoor and create the json after parsing poems by calling get_poem() function
def parse_links(file_name, link, link_style, poet, book):
	j = 0
	# opening the json file into a list
	poem_list = open_file(file_name)
	# parsing the page of poems to find the link of each poem
	page = BeautifulSoup(urllib2.urlopen(link).read(), 'html.parser')
	for anchor in page.findAll('a', href=True):
		# checking if the found like is exacly what it should be, based on the defined style
		if link_style in anchor['href']:
			print "{}\t == Parsing  ==> {}".format(j,anchor['href'])
			# converting each poem into json by calling get_poem() function which parse the HTML page of each poem
			poem = {get_poem(anchor['href'])[0]:{"Title":get_poem(anchor['href'])[1],
												 "Author":poet,"Book":book, 
												 "Poem":get_poem(anchor['href'])[2], 
												 "Audio":get_poem(anchor['href'])[3], 
												 "Source":anchor['href']}}
			# appending each json item into a global list
			poem_list[0].update(poem)
			j += 1
	print "{} poems are loaded into json".format(j)
	close_file(file_name, poem_list)

# prasing the poem page and get the necessary items
def get_poem(link):
	page = urllib2.urlopen(link).read()
	soup = BeautifulSoup(page, 'html.parser')
	# finding the ID of post
	poem_id = soup.find('div', class_="poem", id=True)['id'][5:]
	verses_box = soup.find("article")
	# finding the title of the poem
	title = verses_box.find('a', rel=True).contents[0]
	# finding all verses
	verses = verses_box.findAll('p',string=True)
	poem = ''
	# binding verses into one
	for i in range(0, len(verses)):
		poem += verses[i].contents[0]
		if (i % 2 == 0):
			poem += '\n'
		else:	
			poem += '\n\n'
	# check if the page contains audi file
	cdata = soup.find(text=re.compile("CDATA"))
	audio = 'https://i.ganjoor.net/a/'+poem_id+'.ogg'
	if (cdata == None) or (audio not in cdata):
		audio = None
	# retuned the parsed items
	return poem_id, title, poem, audio


# starting the script and defining the name of the poet as well as the book's names
# if the variable "file_name" is the globla "file" (it is commented now) then all poems will save in a file otherwise will create a file for each poet.
for i in range(0, len(poets)):
	if i == 0:
		poet = 'حافظ'
		book = 'غزلیات حافظ'
		file_name = 'Hafez.json'
	elif i >= 1 and i <= 6:
		poet = 'مولانا'
		book = 'دیوان شمس'
		file_name = 'Molana.json'
	elif i == 7:
		poet = 'سعدی'
		book = 'غزلیات سعدی'
		file_name = 'Saadi.json'
	elif i == 8:
		poet = 'خیام'
		book = 'رباعیات خیام'
		file_name = 'Khayam.json'
	#file_name = file
	parse_links(directory+file_name, poets[i], style[i], poet, book)
