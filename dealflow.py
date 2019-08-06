from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from random import randint
import datetime
import os
import time
import csv
import logging
import pandas as pd

import tkinter as tk 

from tkinter.filedialog import askopenfilename
#chrome driver setting
options = Options()
#hide browser
options.add_argument('--headless')
options.add_argument('--disable-gpu')
#Google chrome browser run in incognito mode  
options.add_argument('--incognito')
#file path where chrome driver is saved
chrome_path= r"C:/Users/ongkc/Desktop/chromedriver.exe"
#popup message font size 
LARGE_FONT= ("Verdana", 12)
NORM_FONT= ("Verdana", 10)
SMALL_FONT= ("Verdana", 8)

#pop up message when script ended
def popupmsg(msg):

    popup = tk.Tk()
    popup.wm_title("!")
    label = tk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = tk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()

    x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
    y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2

    popup.geometry("+%d+%d" % (x, y))
    popup.call('wm', 'attributes', '.', '-topmost', '1')

    popup.mainloop()

#Extract description from Traxcer
def description(fileName):
    driver = webdriver.Chrome(chrome_path, chrome_options=options)
    # driver = webdriver.Chrome(executable_path=chrome_path)
    df = pd.read_csv(fileName)
    #website to extract description 
    driver.get("https://tracxn.com/")

    driver.set_window_size(1024, 600)
    driver.maximize_window()
    time.sleep(2)
    driver.find_element_by_xpath("//a[@class='txn--cursor-pointer']").click()

    #login
    email = driver.find_element_by_xpath("//input[@placeholder='Enter email']")
    password = driver.find_element_by_xpath("//input[@placeholder='Password']")

    #input trxcer account password
    email.send_keys("")
    password.send_keys("")

    driver.find_element_by_xpath("//button[@id='loginButton']").click()
    time.sleep(5)

    x = 0
    for x in range(0, df.shape[0]):

        search = driver.find_element_by_xpath("//input[@placeholder='Search for Companies, Keywords, City, Founded year']").click()
        #clear the words entered
        driver.find_element_by_xpath("//input[@placeholder='Search for Companies, Keywords, City, Founded year']").send_keys(Keys.CONTROL + 'a')
        driver.find_element_by_xpath("//input[@placeholder='Search for Companies, Keywords, City, Founded year']").send_keys(Keys.DELETE)
        #enter the company name
        driver.find_element_by_xpath("//input[@placeholder='Search for Companies, Keywords, City, Founded year']").send_keys(df.ix[x, 'Company']) 
        time.sleep(3)

        not_found = driver.find_elements_by_css_selector('.txn--padding.text-muted.txn--padding-left-lg')
        if(len(not_found) > 0):
            if(driver.find_element_by_css_selector('.txn--padding.text-muted.txn--padding-left-lg').text == "No Results Found"):
                df.ix[x, 'Description'] = "not found"
                df.to_csv('C:/Users/ongkc/Desktop/company_description.csv', index = False)
                continue
        driver.find_element_by_css_selector('.global-search--suggestion ').click()
        time.sleep(3)
        #look up the description element
        description = driver.find_elements_by_css_selector('.LinesEllipsis')
        Company = []
        Company.append(df.ix[x, 'Company'].lower())
        #check if description element exists
        if(len(description) == 0):
            df.ix[x, 'Description'] = "not found"
            df.to_csv('C:/Users/ongkc/Desktop/company_description.csv', index = False)
            continue
        if any(word in description[0].text.lower() for word in Company):
            df.ix[x, 'Description'] = "not found"
            df.to_csv('C:/Users/ongkc/Desktop/company_description.csv', index = False)
            continue
        print(description[0].text)
        df.ix[x, 'Description'] = description[0].text
        time.sleep(1)
        x += 1
        #save to a csv file named Company_Description
        df.to_csv('C:/Users/ongkc/Desktop/company_description.csv', index = False)
    message = "Completed!"
    popupmsg(message)

#Extract company website from google
def linkedinWebsite(fileName):
    logger = logging.getLogger(__name__)
    driver = webdriver.Chrome(chrome_path, chrome_options=options)
    # driver = webdriver.Chrome(executable_path=chrome_path)
    #script that scrap profile information from linkedin
    #file path where u downloaded chromedriver.exe file 

    driver.set_window_size(1024, 600)
    driver.maximize_window()
    driver.get("https://www.google.com/")
    searchBox = driver.find_element_by_name("q")
    searchBox.send_keys("linkedin")
    searchBox.send_keys(Keys.ENTER)
    time.sleep(4)
    search = driver.find_element_by_name("q")
    search.send_keys(Keys.CONTROL + 'a')
    search.send_keys(Keys.DELETE)
    #parse and extract ceo name
    x = 1
    companyName = []
    companyWebpage = []

    #save it in dictionary
    dict = {'company': companyName, 'webpage': companyWebpage}
    with open(fileName, encoding="utf-8") as newfile:
        reader = csv.DictReader(newfile)
        for row in reader:
            url = "not found"
            company = row.get('\ufeffCompany')
            Company = []
            Company.append(company.lower())
            linkedin1 = []
            linkedin1.append("linkedin")
            crunchbase = []
            crunchbase.append("crunchbase") 
            angellist = []
            angellist.append("angellist")   
            wikipedia = []
            wikipedia.append("wikipedia") 
            wiktionary = []
            wiktionary.append("wiktionary") 
            youtube = []
            youtube.append("youtube")     
            amazon = []
            amazon.append("amazon")   
            medium = []
            medium.append("medium") 
            twitter = []
            twitter.append("twitter") 
            yelp =[]
            yelp.append("yelp")
            try:
                search = driver.find_element_by_name("q")
                search.send_keys(Keys.CONTROL + 'a')
                search.send_keys(Keys.DELETE)
    
    
                search.send_keys(company)

                search.send_keys(Keys.ENTER)
                time.sleep(2)

                description_list = driver.find_elements_by_class_name("g")
                #check if company name matches
                for check in description_list:
                        if any(word in check.text.lower() for word in linkedin1):
                            continue
                        if any(word in check.text.lower() for word in crunchbase):
                            continue
                        if any(word in check.text.lower() for word in angellist):
                            continue
                        if any(word in check.text.lower() for word in wikipedia):
                            continue
                        if any(word in check.text.lower() for word in youtube):
                            continue
                        if any(word in check.text.lower() for word in wiktionary):
                            continue
                        if any(word in check.text.lower() for word in amazon):
                            continue
                        if any(word in check.text.lower() for word in medium):
                            continue
                        if any(word in check.text.lower() for word in twitter):
                            continue
                        if any(word in check.text.lower() for word in yelp):
                            continue
                        if any(word in check.text.lower() for word in Company):
                            name = check.find_element_by_class_name("iUh30").text
                            url = name
                            break
            except:
                companyName.append(company)
                companyWebpage.append(url)
                print(url)
                df = pd.DataFrame(dict)
                df.to_csv('C:/Users/ongkc/Desktop/company_url.csv', index = False)
                continue
            companyName.append(company)
            companyWebpage.append(url)
            print(url)
            df = pd.DataFrame(dict)
            df.to_csv('C:/Users/ongkc/Desktop/company_url.csv', index = False)

    popupmsg("Completed!")

#Extract company's CEO name from linkedin
def linkedinCEO(fileName):
    logger = logging.getLogger(__name__)
    driver = webdriver.Chrome(chrome_path, chrome_options=options)
    # driver = webdriver.Chrome(executable_path=chrome_path)
    #script that scrap profile information from linkedin
    #file path where u downloaded chromedriver.exe file 

    driver.get("https://www.linkedin.com/login?trk=guest_homepage-basic_nav-header-signin")
    driver.maximize_window()
    time.sleep(2)

    #Login
    username = driver.find_element_by_id("username")
    password = driver.find_element_by_id("password")
    #input linkedin account password
    username.send_keys("")
    password.send_keys("")

    driver.find_element_by_xpath('//button[@class="btn__primary--large from__button--floating"]').click()
    #read csv file
    x = 1
    companyName = []
    companyCEO = []
    dict = {'company': companyName, 'CEO': companyCEO}
    with open(fileName, encoding='utf-8') as newfile:
        reader = csv.DictReader(newfile)
        for row in reader:
            
            try:
                x += 1
                company = row.get('\ufeffCompany')
                position = ['ceo', 'chief executive officer', 'founder']
                Company = []
                Company.append(company.lower())
                search = driver.find_element_by_tag_name("input")
                search.send_keys(Keys.CONTROL + 'a')
                search.send_keys(Keys.DELETE)
                search.send_keys(company +' ceo')
                search.send_keys(Keys.ENTER)
                time.sleep(3)
                driver.execute_script("window.scrollTo(0, 2160);")

                description_list = driver.find_elements_by_xpath('//p[@class="subline-level-1 t-14 t-black t-normal search-result__truncate"]')
                name = "not found"
                profiles = driver.find_elements_by_css_selector('.search-result.search-result__occluded-item.ember-view')
                if(len(profiles) == 0): 
                    print(name)   
                    companyName.append(company)
                    companyCEO.append(name)
                    df = pd.DataFrame(dict)
                    df.to_csv('C:/Users/ongkc/Desktop/company_ceo.csv', index = False)
                    continue
                for profile in profiles:

                    name_tag = profile.find_elements_by_css_selector('.name.actor-name')
                    if(len(name_tag) == 0):  
                        continue

                    if any(word in profile.text.lower() for word in Company):
                        if any(word in profile.text.lower() for word in position):
                            name = profile.find_element_by_css_selector('.name.actor-name').text
                            break
            except:
                print(name)
                companyName.append(company)
                companyCEO.append(name)
                df = pd.DataFrame(dict)
                df.to_csv('C:/Users/ongkc/Desktop/company_ceo.csv', index = False)
                continue
            print(name)
            companyName.append(company)
            companyCEO.append(name)
            df = pd.DataFrame(dict)
            df.to_csv('C:/Users/ongkc/Desktop/company_ceo.csv', index = False)
            
    popupmsg("Completed!")
    
#run the script
def OpenCEO():
    name = askopenfilename(initialdir="C:/Users/Batman/Documents/Programming/tkinter/",
                           filetypes =(("csv file", "*.csv"),("All Files","*.*")),
                           title = "Choose a file."
                           )
    linkedinCEO(name)

def OpenDescription():
    name = askopenfilename(initialdir="C:/Users/Batman/Documents/Programming/tkinter/",
                           filetypes =(("csv file", "*.csv"),("All Files","*.*")),
                           title = "Choose a file."
                           )
    description(name)

def OpenWebsite():
    name = askopenfilename(initialdir="C:/Users/Batman/Documents/Programming/tkinter/",
                           filetypes =(("csv file", "*.csv"),("All Files","*.*")),
                           title = "Choose a file."
                           )
    linkedinWebsite(name)

#application window
root = tk.Tk()
canvas1 = tk.Canvas(root, width = 300, height = 300) 
canvas1.pack()

button1 = tk.Button (root, text='CEO', command=OpenCEO)      
button2 = tk.Button (root, text='Description', command=OpenDescription)      
button3 = tk.Button (root, text='Website', command=OpenWebsite)      

button4 = tk.Button (root, text='Exit Application', command=root.destroy) 

canvas1.create_window(150, 50, window=button1) 
canvas1.create_window(150, 100, window=button2) 
canvas1.create_window(150, 150, window=button3) 
canvas1.create_window(150, 200, window=button4) 

x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2

root.geometry("+%d+%d" % (x, y))    
root.mainloop()
