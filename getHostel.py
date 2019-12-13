from __future__ import print_function
#!python3
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as chromeOptn
from selenium.webdriver.firefox.options import Options as firefoxOptn
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import argparse

import random
import time
import sys

# import platform
# import os


def print_student_details(browser):
    print() # print empty space at the top
    student_info = browser.find_elements_by_xpath("//table[@id='TABLE1']/tbody/tr") # returns 11 elements
    student_info = student_info[:9] # Only the first nine tr contains sutdent info
    print('+' * 10)
    for info in student_info:
        print(info.text) # prints out the text in the elements
    print('+' * 10)

    return


def login_to_portal(browser, reg_num, rrr_num, unn_hostel_portal):
    browser.get(unn_hostel_portal)

    # time.sleep(12) # Let the user actually see something # this is worst case scenario

    # this is average case scenario for wait
    WebDriverWait(browser, 12).until(EC.presence_of_element_located((By.ID, 'inputUsername')), 'Timed out waiting for Reg. Number to appear')  # wait for Login page

    # fill reg num, rrr number and submit
    regNum_field = browser.find_element_by_id('inputUsername')

    regNum_field.send_keys(reg_num)

    rrrNum_field = browser.find_element_by_id('txtRRR')

    rrrNum_field.send_keys(rrr_num)

    # click to submit
    browser.find_element_by_id('login').click()

    continue_page_elem = 'ContentPlaceHolder1_btnContinue'

    # time.sleep(10) # Let the user see something

#     WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, continue_page_elem)), 'Timed out waiting for Continue Page to Load')  # wait for continue page


#     # fetch and display Student details before clicking on continue button
  

#    # select continue button
#     continue_btn = browser.find_element_by_id(continue_page_elem)
#     # click button
#     continue_btn.click()

    print_student_details(browser)

    # Note: I implement all this wait around because of slow browsing networks and response
    print("\nYou are now fully logged in..")
    return


def get_num_of_hostel_available(browser):

    print('Getting the number of Hostels...')
    # time.sleep(2)
    
    WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.ID, 'DataList1')), 'Timed out waiting for Hostel buttons to Load')  # wait for Hostel buttons to load

    hostel_list_btns = browser.find_element_by_id('DataList1')
    hostel_list = hostel_list_btns.find_elements_by_tag_name('span')

    print("Done.")
    return len(hostel_list)


def start_hostel_application(browser, num_of_hostel, trials):

    tries = trials #1000

    seconds = 10
    max_num = num_of_hostel - 1

    count = 0
    # trying to make input function compatible
    # accross python 2 and python 3

    # Getting the current page url
    application_page = browser.current_url


    while True:

        if count >= tries:
            print('Specified Maximum tries reached..')
            continue_retry(browser, max_num, tries)

        # # refresh page at every 10 counts before continuing
        # if count in count_refresh:
        # 	browser.refresh()

        print('ready...\ndoing trial: {0}/{1}'.format(count+1, tries))
        # Get any of the random hostel buttons
        num = 0
        num += random.randint(0,max_num)

        try:
            hostel_btn = 'DataList1_btnOption_'+str(num)
            hostel = browser.find_element_by_id(hostel_btn)

            print("\n Trying {0} ... ".format(hostel.get_attribute('value')))
            time.sleep(2)
            hostel.click() # click button
        except:
            print('Warning: Error in connection..')
            print(sys.exc_info()[1])
            print('retrying...')
            count += 1
            continue

        try:

            # check if there is an alert of no hostel available
            WebDriverWait(browser,15).until(EC.alert_is_present(), 'Timed out waiting for alerts to appear') #wait for alert
            alert = browser.switch_to.alert
            if alert.text:
                print("| AlertBox Msg: " + alert.text + " |")
                print()
                time.sleep(3)
                alert.accept()
            else:
                print('No Response Alert message')


            print("done...")
            count += 1
            # put in waiting time here
            print("\nwaiting for {0} seconds before retrying another hostel...".format(seconds))
            time.sleep(seconds)

            #print('ready...\ndone trial: {0}/{1}'.format(count, tries))

        except: # This contains success of hostel application next page
            if application_page != browser.current_url:
                print('The current Page needs your attention.. \n go checkout it out')

                # screenshot and save unknown page for users before exitting (likely a success page)
                # screenshot image will be saved in d same directory as getHostel.py script
                browser.save_screenshot("Possbible_proof_of_success.png") 
                break

            else:
                print('Warning: There was a problem in connection...')
                print(sys.exc_info()[1])
                print('continuing with operation...')
                count += 1
                continue


def terminate_program(browser):
    if browser:
        browser.quit()
    print('Goodbye...')
    sys.exit()

def continue_retry(browser_driver, max_hostel_available, tries):

    print('The program has stopped temporarily..')

    try:
        print("To Continue Trying Press and Enter '[Y]' or Any Other Key To Quit")
        input_func = input # trying for python3
        reply = str(input_func())
        if reply.lower() == 'y':
            while True:
                try:
                    tries = int(input("\nHow many times will you like me to retry: "))
                    break
                except:
                    print('Invalid reponse try again..')

            start_hostel_application(browser_driver, max_hostel_available, tries)
        else:
            terminate_program(browser_driver)
    except NameError:
        print("To Continue Trying Press '[Y]' or Any Other Key To Quit")
        input_func = raw_input
        reply = str(input_func())
        if reply.lower() == 'y':
            while True:
                try:
                    tries = int(input("\nHow many times will you like me to retry: "))
                    break
                except:
                    print('Invalid reponse try again..')

            start_hostel_application(browser_driver, max_hostel_available, tries)
        else:
            terminate_program(browser_driver)

    except:
        print(':', sys.exc_info()[1])
        terminate_program(browser_driver)


# # This will get the current OS
# def get_platform():
# 	return platform.system()
#
#

#
# os_platform = get_platform()


# Main Program Commands
def main():

    opt = argparse.ArgumentParser(description='A Script to Automate UNN Hostel Application process in your Browser')
    opt.add_argument('-b', '--browser', required=True,
                      help='Your preferred Browser to run automation in [firefox/chrome]')
    opt.add_argument('-r', '--regnumber', required=True,
                      help="A valid unn reg number of someone that has paid their school fee and is yet to get hostel")
    opt.add_argument('-n', '--rrrnumber', required=True,
                      help='A valid RRR number')
    opt.add_argument('-t', '--tries', required=False, help='Number of trials to attempt', default=0)
    opt.add_argument('-nb', '--headless', required=False, default=False, 
                      help='Set if script should run in headless mode or not (without browser)')

    args = vars(opt.parse_args())

    unn_portal_link = 'https://unnportal.unn.edu.ng/HostelLanding.aspx'


    #browser_choice = 'firefox'
    browser_choice = args['browser'].lower()
    
    # reg_number = '2015/197xxx'
    reg_number = args['regnumber']

    #browser_choice = 'firefox'
    browser_choice = args['browser'].lower()

    # Number of trials to attempt
    tries = int(args['tries']) # default is 0: num of tries not set
    
    # rrr_number ='63879xxx976xxx'
    rrr_num = args['rrrnumber']

    # set if script to run with or without browser [true/false]
    headless = bool(args['headless'])

    #passwd = ''
    chromeOpt = chromeOptn();
    firefoxOpt = firefoxOptn();

    if headless == True:
        chromeOpt.add_argument("--headless");
        firefoxOpt.add_argument("--headless");
    
    browser_driver = ''
    browser_path = ''

    print('Hi Welcome, I am gabriel\n your Hostel Angel \n Loading up {0} browser now.\nPlease wait...'.format(browser_choice))

    ## making number of tries a varying value
    if tries == 0: # if tries is not set
        while True:
            try:
                tries = int(input("\nHow many times will you like me to retry: "))
                break
            except:
                print('Invalid reponse try again..')

    try:
        # start browser engine
        if browser_choice == 'firefox':
            browser_driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), firefox_options=firefoxOpt)
        elif browser_choice == 'chrome':
            browser_driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), chrome_options=chromeOpt)
        else:
            print("I can't help you now...\n To Continue, you need to have either 'Firefox' or 'Chrome' installed")
            terminate_program(browser_driver)

        time.sleep(7)
        #browser_driver.implicitly_wait(8) # every action on browser give it this min time to execute
        print('Browser Loaded...')

        login_to_portal(browser_driver, reg_number, rrr_num, unn_portal_link)
        print('Logged in successfully...')

        print("\nTime to start applying for hostel...\n")
        time.sleep(5)

    except:
        print('Error in connection and could not login')
        print('Message:',sys.exc_info()[1])
        terminate_program(browser_driver)

    # get max number of hostels through button
    max_hostel_available = get_num_of_hostel_available(browser_driver)
    print("There are only {0} hostels available.".format(max_hostel_available))

    # # first get multiples of 5 for purpose of refreshing
    # mult_of_five = [x*5 for x in range(1,201)]

    print()
    print('='*5, '-| Starting hostel Application Process now |-', '='*5)
    # start applying for any random hostel
    start_hostel_application(browser_driver, max_hostel_available, tries)


if __name__ =='__main__':
    main()

