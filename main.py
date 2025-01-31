from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

def product(pd_name):
    pd_data = {}
    pd_data['Platform']=[]
    pd_data['Price']=[]
    pd_data['Platform link']=[]
    service = Service(r"D:\chromedriver-win64\chromedriver-win64\chromedriver.exe")

    driver = webdriver.Chrome(service=service)
    review_stars = None
    try:
        driver.get("about:blank")
        driver.execute_script(f"window.open('https://www.flipkart.com/search?q={pd_name}')")
        driver.switch_to.window(driver.window_handles[-1])
        try:
            flipcost = driver.find_element(By.CSS_SELECTOR, "[class*='Nx9bqj']").text

        except:
            flipcost = None
        
        if flipcost:
            pd_data['Platform'].append('Flipkart')
            pd_data['Price'].append(flipcost)
            pd_data['Platform link'].append(f"https://www.flipkart.com/search?q={pd_name}")

        driver.execute_script(f"window.open('https://www.amazon.in/s?k={pd_name}')")
        driver.switch_to.window(driver.window_handles[-1])

        try:
            WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "a-price-whole"))
            )
            symbol = driver.find_element(By.CLASS_NAME, "a-price-symbol").text
            cost = driver.find_element(By.CLASS_NAME, "a-price-whole").text
            amazoncost = symbol + cost
        except:
            amazoncost = None
        
        if amazoncost:
            pd_data['Platform'].append('Amazon')
            pd_data['Price'].append(amazoncost)
            pd_data['Platform link'].append(f"https://www.amazon.in/s?k={pd_name}")

        driver.execute_script(f"window.open('https://www.reliancedigital.in/search?q={pd_name}')")
        driver.switch_to.window(driver.window_handles[-1])
        
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//span[@class='TextWeb__Text-sc-1cyx778-0 gimCrs']/span[2]"))
            )
            relcost = '₹' + driver.find_element(By.XPATH, "//span[@class='TextWeb__Text-sc-1cyx778-0 gimCrs']/span[2]").text
            relcost = relcost.replace(".00","")
        except:
            relcost = None

        if relcost:
            pd_data['Platform'].append('Reliance digital')
            pd_data['Price'].append(relcost)
            pd_data['Platform link'].append(f'https://www.reliancedigital.in/search?q={pd_name}')
            

        driver.execute_script(f"window.open('https://www.croma.com/searchB?q={pd_name}')")
        driver.switch_to.window(driver.window_handles[-1])
        
        try:
            WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[@class='amount plp-srp-new-amount' and @data-testid='new-price']")))
            cromacost = driver.find_element(By.XPATH, "//span[@class='amount plp-srp-new-amount' and @data-testid='new-price']").text
        except:
            cromacost = None
        
        if cromacost:
            pd_data['Platform'].append('Croma')
            pd_data['Price'].append(cromacost)
            pd_data['Platform link'].append(f"https://www.croma.com/searchB?q={pd_name}")

        driver.execute_script(f"window.open('https://www.poorvika.com/s?q={pd_name}')")
        driver.switch_to.window(driver.window_handles[-1])
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "whitespace-nowrap")))
            poorcost = driver.find_element(By.CLASS_NAME,"whitespace-nowrap ").text
            poorcost = poorcost.replace(" ","")
        except:
            poorcost = None
        
        if poorcost:
            pd_data['Platform'].append('Poorvika')
            pd_data['Price'].append(poorcost)
            pd_data['Platform link'].append(f"https://www.poorvika.com/s?q={pd_name}")

        #Sort prices in ascending order
        prices = pd_data['Price'].copy()
        for i in range(len(prices)):
            prices[i] = prices[i].replace('₹', '').replace(',', '').replace(' ', '')
        prices = [int(i) for i in prices]
        for i in range (len(prices)-1):
            for j in range(i+1,len(prices)):
                if prices[j]<prices[i]:
                    prices[j],prices[i]=prices[i],prices[j]
                    pd_data['Platform'][j],pd_data['Platform'][i]=pd_data['Platform'][i],pd_data['Platform'][j]
                    pd_data['Price'][j],pd_data['Price'][i]=pd_data['Price'][i],pd_data['Price'][j]
                    pd_data['Platform link'][j],pd_data['Platform link'][i]=pd_data['Platform link'][i],pd_data['Platform link'][j]
        return pd_data
    finally:
        driver.quit()   


