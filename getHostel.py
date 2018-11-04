#!python3

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import random
import time
import sys
# import platform
# import os

def login_to_portal(browser, reg_num, unn_hostel_portal):
    browser.get(unn_hostel_portal)

    time.sleep(12) # Let the user actually see something



    # fill reg num and submit
    regNum_field = browser.find_element_by_id('ContentPlaceHolder1_txtRegNo')

    regNum_field.send_keys(reg_num)

    # click to submit
    browser.find_element_by_id('ContentPlaceHolder1_btnSubmit').click()

    time.sleep(10) # Let the user see something

    continue_page_elem = 'ContentPlaceHolder1_btnContinue'

   # select continue button
    continue_btn = browser.find_element_by_id(continue_page_elem)
    # click button
    continue_btn.click()

    # Note: I implement all this wait around because of slow browsing networks and response
    print("You are now fully logged in..")
    return


def get_num_of_hostel_available(browser):

    print('Getting the number of Hostels...')
    time.sleep(2)
    hostel_list_btns = browser.find_element_by_id('ContentPlaceHolder1_DataList1')
    hostel_list = hostel_list_btns.find_elements_by_tag_name('span')

    print("Done.")
    return len(hostel_list)


def start_hostel_application(browser, num_of_hostel):

    tries = 10 #1000

    seconds = 10
    max_num = num_of_hostel - 1

    count = 1

    # Getting the current page url
    application_page = browser.current_url

    print(f'ready...\ndone trial: {count}/{tries}')
    while True:
        if count >= tries:
            print('Maximum tries exceeded..')
            print("To Continue Trying Press '[Y]' or Any Other Key To Quit")
            reply = input().lower()
            if reply == 'y':
                count = 1
                continue
            else:
                terminate_program(browser)

        # # refresh page at every 10 counts before continuing
        # if count in count_refresh:
        # 	browser.refresh()

        # Get any of the random hostel buttons
        num = 0
        num += random.randint(0,max_num)

        hostel_btn = 'ContentPlaceHolder1_DataList1_btnOption_'+str(num)
        hostel = browser.find_element_by_id(hostel_btn)

        print(f"\n Trying {hostel.get_attribute('value')} ... ")
        time.sleep(2)
        hostel.click() # click button

        try:

            # check if there is an alert of no hostel available
            WebDriverWait(browser,15).until(EC.alert_is_present(), 'Timed out waiting for alerts to appear') #wait for alert
            alert = browser.switch_to.alert
            if alert.text:
                print(alert.text)
                time.sleep(5)
                alert.accept()
            else:
                print('No Response Alert message')


            print(f"done...")
            count += 1
            # put in waiting time here
            print(f"\nwaiting for {seconds} seconds before retrying another hostel...")
            time.sleep(seconds)
            print(f'ready...\ndone trial: {count}/{tries}')

        except: # This contains success of hostel application next page
            if application_page != browser.current_url:
                print('The current Page needs your attention.. \n go checkout it out')
                break

            else:
                print('There was a problem in connection...')
                print('warning:', sys.exc_info()[1])
                print('continuing with operation...')
                count += 1
                continue


def terminate_program(browser):
    if browser:
        browser.quit()
    print('Goodbye...')
    sys.exit()

# # This will get the current OS
# def get_platform():
# 	return platform.system()
#
#

#
# os_platform = get_platform()


# Main Program Commands
def main():
    unn_portal_link = 'https://unnportal.unn.edu.ng/modules/hostelmanager/ApplyForHostel.aspx'
    # reg_number = '2015/197595'
    reg_number = sys.argv[2]

    #browser_choice = 'firefox'
    browser_choice = sys.argv[1]

    #passwd = ''
    browser_driver = ''
    browser_path = ''



    count = 1

    print(f'Hi Welcome, I am gabriel\n your Hostel Angel 😇 ;) :)\n Loading up {browser_choice} browser now.\nPlease wait...')
    try:
        # start browser engine
        if browser_choice == 'firefox':
            browser_driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
        elif browser_choice == 'chrome':
            browser_driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
        else:
            print("I can't help you now...\n To Continue, you need to have either 'Firefox' or 'Chrome' installed")
            terminate_program(browser_driver)

        time.sleep(10)
        #browser_driver.implicitly_wait(8) # every action on browser give it this min time to execute
        print('Browser Loaded...')

        login_to_portal(browser_driver, reg_number, unn_portal_link)
        print('Logged in successfully...')

        print("\nTime to start applying for hostel...\n")
        time.sleep(5)
    except:
        print('Error in connection and could not login')
        print('Message:',sys.exc_info()[1])
        terminate_program(browser_driver)


    # get max number of hostels through button
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
    print("To Continue Trying Press '[Y]' or Any Other Key To Quit")
    try:
        reply = input().lower()
        if reply == 'y':
            start_hostel_application(browser_driver, max_hostel_available)
        else:
            terminate_program(browser_driver)
    except:
        print('error', sys.exc_info()[0])
        terminate_program(browser_driver)


if __name__ =='__main__':
    main()

