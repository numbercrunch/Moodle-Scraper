# -*- coding: utf-8 -*-
from selenium import webdriver
import scraper as s
import requests
import time as t
import os as os
from clint.textui import progress
import dir_structure as ds
import platform as p

SETTINGS = open('SETTINGS').read().splitlines()
USERNAME = SETTINGS[0]
PASSWORD = SETTINGS[1]
SEMESTER = SETTINGS[2]
COURSELIST = [x.strip() for x in SETTINGS[4:]]
PATH = 'bin/phantomjs'

print (os.curdir)

driver = webdriver.PhantomJS(PATH)
session = requests.Session()

# if 'x86' in p.machine():
#     PATH = PATH+'phantomjs'
# else:
#     PATH = PATH+'geckodriver'

# try:
#     driver = webdriver.PhantomJS(PATH)
#     session = requests.Session()
# except:
#     print('Error loading driver: correct driver present? Abort.')
#     quit()

SESS = ''


def login(USERNAME, PASSWORD):
    '''Login into moodle startpage'''
    print('Start logging into moodle 🔮')
    driver.get("https://www.moodle.tum.de/Shibboleth.sso/Login?providerId=https%3A%2F%2Ftumidp.lrz.de%2Fidp%2Fshibboleth&target=https%3A%2F%2Fwww.moodle.tum.de%2Fauth%2Fshibboleth%2Findex.php")
    
    try:
        driver.find_element_by_id('username').send_keys(USERNAME)
        driver.find_element_by_id('password').send_keys(PASSWORD)
        driver.find_element_by_name('_eventId_proceed').click()
        SESS = driver.find_element_by_name('sesskey').get_attribute('value')
        print('Login was successful ')
    except:
        print('Could not login - did you check your SETTINGS?')
        exit()
    
    cookies = driver.get_cookies()
    for cookie in cookies: 
        session.cookies.set(cookie['name'], cookie['value'])

    openCourses()

def openCourses():
    '''Open all courses as browsers'''
    # print('Start of open course')
    courses = s.find_course_links(driver.page_source)
    pages = []
    print (pages)
    for course, page in courses:
        pages.append([course, session.get(page)])
        # print(course+' ~~~~ ',page)
    ds.check_dir_structure()
    for course, page in pages:
        openResources(course,page)
    # print('End of open course')
    logout()

def openResources(course, page):
    '''Open the resources for each respective code:
        -arguments: list of courses 'courses'
        '''
    # print('Start opening resource links')
    resources = s.find_resource_links(page.content)
    for resource in resources:
        r = session.get(resource, stream=True)
        filename = r.url.split('/')[-1].split('.')[0]+'.'+r.url.split('.')[-1]
        filename = filename.replace("%20", " ")
        print(resource+'  -----  '+filename+' 📩')
        if os.path.exists(os.getcwd()+'/'+SEMESTER+'/'+course+'/'+filename):
            print('~~~~~~~~  already exists, continue with next file ~~~~~~~~')
            continue
        r = session.get(r.url, stream=True)
        with open(SEMESTER+'/'+course+'/'+filename, 'wb') as f:
            total_length = int(r.headers.get('content-length'))
            for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1): 
                if chunk:
                    f.write(chunk)
                    f.flush()
            print('                                                             ✅')
    print('All files for ' +course+ ' downloaded 🍺\n')

def logout():
    '''Logout from moodle main page and exit webbrowser'''
    print('Logging out')
    session.get("https://www.moodle.tum.de/login/logout.php?sesskey="+SESS)
    driver.quit()
    driver.stop_client()
    session.cookies.clear_session_cookies()
    session.close()
    print('End of logout ✅')


login(USERNAME, PASSWORD)