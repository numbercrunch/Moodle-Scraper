import os
import re

SETTINGS = open('SETTINGS').read().splitlines()
SEMESTER = SETTINGS[2]
COURSELIST = [x.strip() for x in SETTINGS[6:]] 

#Checks if the needed folder-structure is ready, otherwise it creates it
def check_dir_structure():
	# print('Start of check_dir_structure')
	print(COURSELIST)
	check_semester_dir()
	check_courses_dir()
	# print('End of check_dir_structure')

#Checks if their is a directory for the semester, if not creates one
def check_semester_dir():
	# print('Start of check_semester_dir')
	# print("checking directory for "+SEMESTER)
	if not os.path.exists(SEMESTER):
		print('Creating directory for' + SEMESTER)
		os.makedirs(SEMESTER)
	# print('End of check_semester_dir')

#Checks if their are all the course-folders, if not creates one for each course
def check_courses_dir():
	# print('Start of check_semester_dir')
	semester_path=""+SEMESTER+"/"
	for course in COURSELIST:
		# print("checking directory for "+course)
		if not os.path.exists(SEMESTER+'/'+course):
			print("Creating directory for "+ course + " in semester "+ SEMESTER)
			os.makedirs(SEMESTER+'/'+course)
	# print('End of check_semester_dir')

def check_course_subdir(course,dir_name):
	if not os.path.exists(SEMESTER+'/'+course+'/'+dir_name):
		print("Creating directory for "+course+"/"+dir_name )
		os.makedirs(SEMESTER+'/'+course+'/'+dir_name)

