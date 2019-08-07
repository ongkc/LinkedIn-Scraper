from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

from random import randint
import datetime
import os
import time
import csv
import logging
import pandas as pd
import tkinter as tk 

from tkinter.filedialog import askopenfilename

# file path where chrome driver is saved
chrome_path= r"C:/Users/ongkc/Desktop/chromedriver.exe"

# chrome driver setting
options = Options()
# hide browser when the script is running
options.add_argument('--headless')
options.add_argument('--disable-gpu')  
# run in incognito mode
options.add_argument('--incognito')

LARGE_FONT= ("Verdana", 12)
NORM_FONT= ("Verdana", 10)
SMALL_FONT= ("Verdana", 8)

# pop up message when the script ends
def popupmsg(message):

    popup = tk.Tk()
    popup.wm_title("!")
    label = tk.Label(popup, text=message, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = tk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()

    x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
    y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
    
    popup.geometry("+%d+%d" % (x, y))
    popup.call('wm', 'attributes', '.', '-topmost', '1')
    popup.mainloop()

#create a new csv file
def create_new_file(file_name):
    file_name = file_name + '.csv'
    with open(file_name, 'w', newline='', encoding="utf-8") as f:
        fieldnames = ['name', 'profile_url', 'description']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

# save to a csv file
def save_to_csv(file_name, role, driver):
    '''this function finds linkedin profile and saves to csv
    '''
    #open the csv to input the information
    f = open(file_name + ".csv", 'a', newline='', encoding="utf-8")
    fieldnames = ['name', 'profile_url', 'description']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    for _ in range(100):
        relevant_profiles = 9
        SCROLL_PAUSE_TIME = 1
        time.sleep(SCROLL_PAUSE_TIME)

        # #scroll the page to load all the profiles in the page
        # driver.execute_script("window.scrollTo(0, 540)")
        # time.sleep(2)

        driver.execute_script("window.scrollTo(0, 1080)")
        time.sleep(SCROLL_PAUSE_TIME)

        # driver.execute_script("window.scrollTo(0, 1620)")
        # time.sleep(2)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)

        #retrieve all the person profile information on each page
        profiles_section_check = driver.find_elements_by_xpath('//li[@class="search-result search-result__occluded-item ember-view"]')
        if(len(profiles_section_check) == 0):
            f.close() 
            break
        profiles_section = driver.find_elements_by_xpath('//li[@class="search-result search-result__occluded-item ember-view"]')
        # profiles = profiles_section.find_elements_by_css_selector('.search-result__info.pt3.pb4.ph0')
        for profile in profiles_section:                        
            name_tag = profile.find_elements_by_css_selector('.name.actor-name')
            if(len(name_tag) == 0):
                continue
            name = profile.find_element_by_css_selector('.name.actor-name').text
            description = profile.find_element_by_css_selector('.subline-level-1.t-14.t-black.t-normal.search-result__truncate').text
            profile_url = "="+"HYPERLINK" +"(" + '"' + profile.find_element_by_css_selector('.search-result__result-link.ember-view').get_attribute("href") +'"' + ")"
            # profile_url = profile.find_element_by_css_selector('.search-result__result-link.ember-view').get_attribute("href")

            companies = []
            companies.append(file_name.lower())
            position = []
            position.append(role.lower())
            #check and filter irrelevant profile found with the wrong company and position 
            try:
                if any(word in description.lower() for word in companies):
                    if any(word in description.lower() for word in position):

                        row = {
                            'name': name,
                            'profile_url': profile_url,
                            'description': description
                        }

                        writer.writerow(row)
                    else:
                        relevant_profiles -=1    
                else:
                    relevant_profiles -=1
            except:
                logger.exception('something went wrong')
        print(relevant_profiles)
        if(relevant_profiles <= 0) :
            break
        #Go to the next page
        next1 = driver.find_elements_by_css_selector('.artdeco-pagination__button.artdeco-pagination__button--next.artdeco-button.artdeco-button--muted.artdeco-button--icon-right.artdeco-button--1.artdeco-button--tertiary.ember-view')    
        if(len(next1) == 0):
            f.close()                
            break
        driver.find_element_by_css_selector('.artdeco-pagination__button.artdeco-pagination__button--next.artdeco-button.artdeco-button--muted.artdeco-button--icon-right.artdeco-button--1.artdeco-button--tertiary.ember-view').click()
    f.close()

#search based on keyword
def search(key_word,driver):
    search = driver.find_element_by_tag_name("input")
    search.clear()
    search.send_keys(key_word)
    search.send_keys(Keys.ENTER)
    time.sleep(2)

#filter profiles
def filter(location, company, driver):
    '''
    further filtering 
    '''
    time.sleep(1)
    filter_button_element_path = '//button[@class="search-filters-bar__all-filters flex-shrink-zero mr3 artdeco-button artdeco-button--muted artdeco-button--2 artdeco-button--tertiary ember-view"]'
    location_search_element_path = '//*[@class="search-s-facet__values search-s-facet__values--geoRegion"]'
    company_search_element_path = '//*[@class="search-s-facet search-s-facet--currentCompany inline-block ember-view"]'
    apply_button_element_path = '//button[@class="search-advanced-facets__button--apply ml4 mr2 artdeco-button artdeco-button--3 artdeco-button--primary ember-view"]'

    filter = driver.find_element_by_xpath(filter_button_element_path)
    filter.click()
    time.sleep(1)


    #filter by location
    location_search = driver.find_element_by_xpath(location_search_element_path)            
    location_search.find_element_by_tag_name("input").send_keys(location)
    time.sleep(2)
    location_search.find_element_by_tag_name("input").send_keys(Keys.DOWN)
    location_search.find_element_by_tag_name("input").send_keys(Keys.ENTER)
    time.sleep(1)    
    #filter by company
    company_search = driver.find_element_by_xpath(company_search_element_path)
    companyList = list(company)
    for letter in companyList:
        company_search.find_element_by_tag_name("input").send_keys(letter)
        company_search.find_element_by_tag_name("input").send_keys(Keys.DOWN)
        time.sleep(1)
    time.sleep(2)
    company_search.find_element_by_tag_name("input").send_keys(Keys.DOWN)
    company_search.find_element_by_tag_name("input").send_keys(Keys.ENTER)
    time.sleep(1) 

    driver.execute_script("window.scrollTo(0, 2140)")
    time.sleep(1)

    apply = driver.find_element_by_xpath(apply_button_element_path)
    apply.click()

def login(login_id, login_password, driver):
    '''login using credentials
    '''
    driver.get("https://www.linkedin.com/login?trk=guest_homepage-basic_nav-header-signin")
    driver.maximize_window()
    username = driver.find_element_by_id("username")
    password = driver.find_element_by_id("password")

    username.send_keys(login_id)
    password.send_keys(login_password)

    driver.find_element_by_xpath( '//button[@class="btn__primary--large from__button--floating"]').click()

def main(name, role, username, password):
    # driver = webdriver.Chrome(chrome_path, chrome_options=options)
    driver = webdriver.Chrome(executable_path=chrome_path)


    login_id = username
    login_password = password
    
    locations = "United States"
    companies = name.split(",")
    login(login_id, login_password, driver)
    roles = role.split(",")


    for company in companies:
        x = 0
        if(x != 0):
            check_clear =  driver.find_elements_by_css_selector('.search-filters-bar__selected-filter-count.mv0.ml1')
            if (len(check_clear) != 0):
                #clear the filtering
                driver.find_element_by_xpath( '//span[@class="search-filters-bar__selected-filter-count mv0 ml1"]').click()
            filter(locations, company.capitalize(), driver)
        
        create_new_file(company.capitalize())
        for role_ in roles:        
            key_word = company.capitalize() + " " + role_
            print(key_word)
            search(key_word, driver)
            if(x == 0):
                check_clear =  driver.find_elements_by_css_selector('.search-filters-bar__selected-filter-count.mv0.ml1')
                if (len(check_clear) != 0):
                    #clear the filtering
                    driver.find_element_by_xpath( '//span[@class="search-filters-bar__selected-filter-count mv0 ml1"]').click()
                filter(locations, company.capitalize(), driver)
                x += 1
            save_to_csv(company.capitalize(), role_, driver)
    message = "Completed!"
    popupmsg(message)
# check if all box filled
def show_entry_fields():
    if(e2.get() and e4.get() and e6.get() and e8.get()):
        main(e2.get(), e4.get(), e6.get(), e8.get())
    else:
        popupmsg("Please fill up all boxes!")

# application UI window
root = tk.Tk()
canvas1 = tk.Canvas(root, width = 300, height = 300) 
canvas1.pack()
e1 = tk.Label(root, 
         text="Company")
e2 = tk.Entry(root)

e3 = tk.Label(root, 
         text="Key Word")
e4 = tk.Entry(root)

e5 = tk.Label(root, 
         text="Username")
e6 = tk.Entry(root)

e7 = tk.Label(root, 
         text="Password")
e8 = tk.Entry(root)

# e1.grid(row=0, column=1)

button2 = tk.Button(root, 
          text='Quit', 
          command=root.quit)
button3 = tk.Button(root, 
          text='Start', command=show_entry_fields)

canvas1.create_window(100, 50, window=e1) 
canvas1.create_window(200, 50, window=e2) 
canvas1.create_window(100, 100, window=e3) 
canvas1.create_window(200, 100, window=e4) 
canvas1.create_window(100, 150, window=e5) 
canvas1.create_window(200, 150, window=e6) 
canvas1.create_window(100, 200, window=e7) 
canvas1.create_window(200, 200, window=e8)

canvas1.create_window(100, 250, window=button3) 
canvas1.create_window(200, 250, window=button2) 

x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2

root.geometry("+%d+%d" % (x, y))   
root.mainloop()
