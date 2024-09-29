from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

driver = webdriver.Chrome()
driver.get("https://www.federalreserve.gov/newsevents/pressreleases.htm")
count = 0

dateList = []
titleList = []
timeList = []
mediaList = []  
textList = []

def writeText(text):
    splitted = text.split('\n', 4)

    dateList.append(splitted[0])
    titleList.append(splitted[1])
    timeList.append(splitted[2])
    mediaList.append(splitted[3])
    textList.append(splitted[4])    

while(count <= 120):
    if(count == 120):
        break
    else:
        fomcLink = driver.find_elements(By.PARTIAL_LINK_TEXT, "FOMC statement")
        #include elseif for special cases
        if(fomcLink != None):
            print(len(fomcLink))
            count = count + len(fomcLink)
            print(count)

            for i in range(len(fomcLink)):
                link = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.PARTIAL_LINK_TEXT, "FOMC statement")))[i] 
                print(link.get_attribute('href'))

                driver.execute_script("arguments[0].click()", link)
                link_text = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "article")))
                print(link_text.text)
                writeText(link_text.text)

                driver.back()

            next = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.LINK_TEXT, "Next")))
            driver.execute_script("arguments[0].click()", next)

        else:
            next = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.LINK_TEXT, "Next")))
            next.click()
driver.quit()

df = pd.DataFrame(list(zip(dateList, titleList, timeList, mediaList, textList)), columns = ['Date', 'Title', 'Time', 'Media', 'Text'])
print(df)
df.to_csv('FOMC_Draft.csv', index=False)






