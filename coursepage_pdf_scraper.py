from BeautifulSoup import BeautifulSoup 
import requests
# Needed ? -- Difficult dependency management -- :: from urllib.requests import urlopen 

def get_resourcesLinkTag_list(html_string):
	print("Start of get_resourcesLinkTag_list")
	resources=[]
	soup = BeautifulSoup(html_string,"html.parser")
	for div in soup.findAll('div', {"class": "activityinstance"}):
		for link in div.findAll('a'):
			link_href= link.get('href')
			if '/resource/' in link_href:
				resources.append(link)
				print(link.span.text)
	
	print("End of get_resourcesLinkTag_list")
	return resources	
