#!python3

from selenium import webdriver
import random
import time
import sys
import platform
import os

def login_to_portal(browser, reg_num, unn_hostel_portal):
	browser.get(unn_hostel_portal)

	time.sleep(5) # Let the user actually see something

	# fill reg num and submit
	regNum_field = browser.find_element_by_id('ContentPlaceHolder1_txtRegNo')
	regNum_field.send_keys(reg_num)

	time.sleep(5) # Let the user see something

	# click to submit
	browser.find_element_by_id('ContentPlaceHolder1_btnSubmit').click()

	time.sleep(10) # Let the user see something

	# click on continue to proceed
	browser.find_element_by_id('ContentPlaceHolder1_btnContinue').click()

	print("you are now fully logged In..")
	return 


def get_num_of_hostel_available(browser):

	print('getting number of available hostels...')

	hostel_list_btns = browser.find_element_by_id('ContentPlaceHolder1_DataList1')
	hostel_list = hostel_list_btns.find_elements_by_tag_name('span')

	print("done.")
	return len(hostel_list)


def start_hostel_application(browser, num_of_hostel):

	tries = 10 #1000

	seconds = 10
	max_num = num_of_hostel - 1

	count = 1

	# Getting the current page url
	current_page = browser.current_url
	while True:
		if count > tries:
			print('maximum tries reached..')
			print("To continue trying press '[Y]' or any other key to quit")
			reply = input().lower()
			if reply == 'y':
				count = 1
				continue
			else:
				break

	

		# # refresh page at every 10 counts before continuing
		# if count in count_refresh:
		# 	browser.refresh()
	
		# Get any of the random hostel buttons
		num = 0
		num += random.randint(0,max_num)

		hostel_btn = 'ContentPlaceHolder1_DataList1_btnOption_'+str(num)
		hostel = browser.find_element_by_id(hostel_btn)
		print(f"\n Trying {hostel.get_attribute('value')} ... ")
		time.sleep(3.5)
		hostel.click() # click button
		

		try:
			
			# check if there is an alert of no hostel available
			time.sleep(8)
			if browser.switch_to.alert:
				Alert = browser.switch_to.alert
				print(Alert.text)
				time.sleep(2)
				Alert.accept()
			else:
				if current_page != browser.current_url:
					print('The current Page needs your attention.. \n go checkout it out')
					break
			

			print(f"done...")

			# if current_page != browser.current_url:
			# 	print('The current Page needs your attention.. \n go checkout it out')
			# 	break

					
			
			count += 1
			# put in waiting time here
			print(f"\nwaiting for {seconds} seconds before retrying another hostel...")
			time.sleep(seconds)
			print(f'ready...\ndoing trial: {count}/{tries}')
			
			
			# # try again on another hostel after waiting
			# return start_hostel_application(browser, num_of_hostel, count_refresh)

		except:
			print('Error:', sys.exc_info()[1])
			print("I'm Confused: This current page is strange and I need your attention..")
			print("It's either there is an error from server or this is a new page I don't recognise..\n")		
			# There should be a form of notification to get attention here
			time.sleep(5) # Let the user see something
			raise
			break

def terminate_program(browser):
	if browser:
		browser.quit()
	print('Goodbye...')
	sys.exit()

# This will get the current OS
def get_platform():
	return platform.system()


# Main Program Commands

os_platform = get_platform()

unn_portal_link = 'http://unnportal.unn.edu.ng/modules/hostelmanager/ApplyForHostel.aspx' 
# reg_number = '2015/197595'
reg_number = sys.argv[2]

#browser_choice = 'firefox'
browser_choice = sys.argv[1]

#passwd = ''
browser_driver = ''
browser_path = ''



count = 1

print(f'Hi Welcome, I am gabriel\n your Hostel Angel [*.*] ;) :)\n Loading up {browser_choice} browser now.\nPlease wait...')
try:
	# start browser engine 
	if browser_choice == 'firefox':
		browser_driver = webdriver.Firefox()
	elif browser_choice == 'chrome':
		browser_path = ''
		root = 'drivers'
		if os_platform.lower() == "windows":
			browser_path = os.path.join(root,"chromedriverwindows.exe" ) 
		elif os_platform.lower() == "linux":
			browser_path = os.path.join(root, "chromedriverlinux")
		elif os_platform.lower() == "darwin":
			browser_path = os.path.join(root, "chromedrivermac")
		else:
			print("The availbale driver is not compatible wiith your browser\nupdate your chrome browser \
			and try again..")
			terminate_program(0)

		# print("Available driiver is not compatible with your system/browser")
		# sys.exit()
		
		browser_driver = webdriver.Chrome(browser_path)
	else:
		print("I can't help you now...\n To Continue, you need to have either 'Firefox' or 'Chrome' installed")
		terminate_program(browser_driver)

	login_to_portal(browser_driver, reg_number, unn_portal_link)
	print('Logged in successfully...')

	print("\nTime to start applying for hostel...\n")

except:
	print('Error in connection and could not login')
	print(sys.exc_info())
	terminate_program(browser_driver)


# get max number of buttons
time.sleep(2) # Let the user see something
max_hostel_available = get_num_of_hostel_available(browser_driver)
print(f"There are only {max_hostel_available} hostels available.")


# # first get multiples of 5 for purpose of refreshing
# mult_of_five = [x*5 for x in range(1,201)] 

print()
print('='*5, '-| Starting hostel Application Process now |-', '='*5)
# start applying for any random hostel
start_hostel_application(browser_driver, max_hostel_available)

# print('When you are done and you are yet to get hostel click on Get hostel to continue the hostel application...')

# print('Make sure your details and other options are set correctly before clicking.')

print('The program has stopped temporarily..')
print("To continue trying press '[Y]' or any other key to quit")
try:
	reply = input().lower()
	if reply == 'y':
		start_hostel_application(browser_driver, max_hostel_available)
except:
	print('error', sys.exc_info()[0])
finally:
	terminate_program(browser_driver)
	raise

