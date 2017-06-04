"""
loads "http://freerice.com", logs in, selects the math questions and starts
solving those.for every correct answer the website donates 10 grains of rice.
The rice is financed by the ads on the site.

make sure to let the browser start without doing anything else. after that
you can minimize it and the program will run in the background

requires your computer to be able to run python (with the 3-party selenium
module) and a browser with a driver. e.g. geckodriver
(https://github.com/mozilla/geckodriver/releases/tag/v0.16.1) for Firefox
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located as find
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException as NSEException
from selenium.common.exceptions import StaleElementReferenceException as SERException
from selenium.common.exceptions import WebDriverException as WDException



donated = 0
browser = None
wait = None
donated = 0
accName = "" #make your own profile 
accPass = "" #and password



def run():
    """
    the mian method, programm starts here
    """
    global donated
    startBrowser()
    login()
    selectQuestions()
    try:
        startSolving()
    except KeyboardInterrupt or WDException:
        print('donated '+str(donated*10)+ ' grains')
        print("finished")



def startBrowser():
    """
    starts the browser. if you do not use firefox you need to change this part
    """
    global browser, wait
    print('starting browser...')
    firefox_capabilities = DesiredCapabilities.FIREFOX
    firefox_capabilities['marionette'] = True
    geckoPath = r'C:\path\to\driver.exe' 
    browser = webdriver.Firefox(capabilities=firefox_capabilities, executable_path=geckoPath)
    wait = WebDriverWait(browser, 10)
    print('browser started')
    browser.get("http://freerice.com/user/login")
    print('freerice open')



def login():
    """
    logs the bot in with the defined username and password. not neccessary.
    """
    global wait
    elemKey = "input[id=\"edit-name_watermark\"][class=\"watermarkPluginCustomClass\"][style=\"overflow: visible; display: inline;\"][type=\"text\"]"
    elem = wait.until(find((By.CSS_SELECTOR, elemKey)))
    elem.send_keys(accName)

    elemKey = "input[name=\"pass\"][id=\"edit-pass\"][maxlength=\"128\"][size=\"60\"][class=\"form-text required\"][type=\"password\"]"
    elem = wait.until(find((By.CSS_SELECTOR, elemKey)))
    elem.send_keys(accPass)

    elem.submit()
    


def selectQuestions():
    """
    sends the browser to the math questions
    """
    global browser, wait
    browser.get("http://freerice.com/category")
    elemKey = "Multiplication Table"
    elem = wait.until(find((By.LINK_TEXT, elemKey)))
    elem.click()


def startSolving():
    """
    the important part of the program. runs as long as no exception
    (keyboardInterrupt) is thrown. gets the two numbers that make up
    the question, multiplies them and submitts the sulution by clicking
    the right answer.
    """
    global browser, wait, donated
    prevSol = -1
    currSol = -1
    counter = 0
    """ the counter varibale:
    prevents a lock when a special question combination comes.
    EX: 9*4 = 36 then 6*6 = 36. both solutions are the same, the first part
    of the if block is True, the programm would be stuck in a deadlock.
    this counter prevents that. it allows the program to only calculate
    the solution 30 times before trying to submitting it again (this time
    for the new question
    """ 
    donated = 0
    """ the donated variable
    counts how many times a solution was submitted, and therefore how much
    rice the program "bought"
    """
    elemKey = "//a[@class='question-link']"
    while True:
        if currSol == prevSol and counter < 50:
            counter += 1
            try:
                text = wait.until(find((By.XPATH, elemKey))).text.split(' ')
                currSol = int(text[0])*int(text[2])
            except SERException:
                pass
        else:
            counter = 0
            try:
                browser.elem = browser.find_element_by_link_text(str(currSol)).click()
                prevSol = currSol
                donated+=1
                if donated % 100 == 0:
                    print('donated '+str(donated*10)+ ' grains')
            except NSEException:
                pass



run()






