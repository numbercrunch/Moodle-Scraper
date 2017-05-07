# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup
import requests
import os
import dir_structure as ds
from clint.textui import progress

SETTINGS = open('SETTINGS').read().splitlines()
SEMESTER = SETTINGS[2]
COURSELIST = [x.strip() for x in SETTINGS[6:]] 

def find_course_links(sauce):
	'''Finds links to this semesters courses on moodle startpage given through sauce'''
	course_links=[]
	soup=BeautifulSoup(sauce,"html.parser")
	for div in soup.findAll('div', class_=re.compile('termdiv coc-term-'+SEMESTER)):
		a = div.div.h3.a
		for course in COURSELIST:
			if course in a.get('title'):
				course_links.append([course, a.get('href')])
				print(a.get('title')+' --- found ✅')
				COURSELIST.remove(course)
				break
	for course in COURSELIST:
		print("Couldn't find "+course+" - check your SETTINGS?")
	return course_links


def find_resource_links(sauce):
    '''Finds relevent resource links to views for resources on 
	given moodle course source code coming in through sauce.'''
    soup=BeautifulSoup(sauce, "html.parser")
    resource_links=[]
    for li in soup.findAll('li', class_=re.compile('activity resource modtype_resource ')):
        for a in li.findAll('a'):
            resource_links.append(a.get('href'))
    return resource_links

def scrape_IN0010():
	ds.check_course_subdir('IN0010','altklausuren')
	ds.check_course_subdir('IN0010','assignments')
	ds.check_course_subdir('IN0010','lecture_slides')
	ds.check_course_subdir('IN0010','tutorials')
	ds.check_course_subdir('IN0010','altklausuren/midterm')
	ds.check_course_subdir('IN0010','altklausuren/endterm')
	ds.check_course_subdir('IN0010','altklausuren/retake')
	ds.check_course_subdir('IN0010','altklausuren/cheatsheet')

	base= 'http://grnvs.net.in.tum.de'


	print("Start scrapin page for GRNVS (IN0010)")

	connection = requests.Session()
	
	base_sauce = connection.get(base).content
	base_soup = BeautifulSoup(base_sauce, "html.parser")

	altklausuren_sauce = connection.get(base+'/altklausuren').content
	altklausuren_soup = BeautifulSoup(altklausuren_sauce, "html.parser")

	for link in altklausuren_soup.findAll('a'):
		link_href = link.get('href')
		#filename= link_href.split('/')[-1]#[:-4]

		if '../' in link_href:
			continue
		if 'midterm' in link_href:
			download_pdf(connection,'2017-1/IN0010/altklausuren/midterm/'+link_href,base+'/altklausuren/'+link_href)
		if 'endterm' in link_href:
			download_pdf(connection,'2017-1/IN0010/altklausuren/endterm/'+link_href,base+'/altklausuren/'+link_href)
		if 'retake' in link_href:
			download_pdf(connection,'2017-1/IN0010/altklausuren/retake/'+link_href,base+'/altklausuren/'+link_href)
		if 'cheatsheet' in link_href:
			download_pdf(connection,'2017-1/IN0010/altklausuren/cheatsheet/'+link_href,base+'/altklausuren/'+link_href)


	for link in base_soup.findAll('a'):
		link_href= link.get('href')
		print(link_href)
		if '../' or 'assignments/' in link_href:
			continue
		if 'assignment' in link_href:
			download_pdf(connection,'2017-1/IN0010/assignments/'+link_href, base+'/'+link_href)
		if 'slides_chap' in link_href:
			download_pdf(connection,'2017-1/IN0010/lecture_slides/'+link_href, base+'/'+link_href)
		if 'tutorial' in link_href:
			download_pdf(connection,'2017-1/IN0010/tutorials/'+link_href, base+'/'+link_href)

	print('All files from GRNVS downloaded 🍺')

def download_pdf(session, path, pdf_url):

	
	pdf_page = session.get(pdf_url, stream=True)
	filename= path.split('/')[-1]
	print(pdf_url+'  -----  '+filename+' 📩')

	if os.path.exists(path):
		print('~~~~~~~~  already exists, continue with next file ~~~~~~~~')
		return

	with open(path, 'wb') as f:
		total_length = int(pdf_page.headers.get('content-length'))
		for chunk in progress.bar(pdf_page.iter_content(chunk_size=1024), expected_size=(total_length/1024)+1):
			if chunk:
				f.write(chunk)
				f.flush()
		print('                                                             ✅')


	