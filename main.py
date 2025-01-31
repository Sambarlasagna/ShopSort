from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

def product(pd_name):
    #Create an empty dictionary to store the data(Platform name, Price and Platform link)
    pd_data = {}
    pd_data['Platform']=[]
    pd_data['Price']=[]
    pd_data['Platform link']=[]
    service = Service(r"Enter your driver path")

    driver = webdriver.Chrome(service=service)
    review_stars = None
    try:
        driver.get("about:blank")
        driver.execute_script(f"window.open('https://www.flipkart.com/search?q={pd_name}')")
        #To open the tabs in a single window
        driver.switch_to.window(driver.window_handles[-1])

        #Find the cost of the product on Flipkart
        try:
            #Getting the cost
            flipcost = driver.find_element(By.CSS_SELECTOR, "[class*='Nx9bqj']").text

        except:
            #If the data is not found the cost is None
            flipcost = None

        #Adding the data to the dictionary
        if flipcost:
            pd_data['Platform'].append('Flipkart')
            pd_data['Price'].append(flipcost)
            pd_data['Platform link'].append(f"https://www.flipkart.com/search?q={pd_name}")

        driver.execute_script(f"window.open('https://www.amazon.in/s?k={pd_name}')")
        driver.switch_to.window(driver.window_handles[-1])
        
        #Finding the cost of the product on Amazon
        try:
            WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "a-price-whole"))
            )
            #Type of currency
            symbol = driver.find_element(By.CLASS_NAME, "a-price-symbol").text

            #The cost
            cost = driver.find_element(By.CLASS_NAME, "a-price-whole").text
            amazoncost = symbol + cost
            
        except:
            #If the data is not found the cost is None
            amazoncost = None
            
        #Adding the data to the dictionary
        if amazoncost:
            pd_data['Platform'].append('Amazon')
            pd_data['Price'].append(amazoncost)
            pd_data['Platform link'].append(f"https://www.amazon.in/s?k={pd_name}")

        driver.execute_script(f"window.open('https://www.reliancedigital.in/search?q={pd_name}')")
        driver.switch_to.window(driver.window_handles[-1])

        #Getting the cost of the product from Reliancedigital
        try:
            #Waiting until the tag where cost is available gets loaded
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//span[@class='TextWeb__Text-sc-1cyx778-0 gimCrs']/span[2]"))
            )
            relcost = '₹' + driver.find_element(By.XPATH, "//span[@class='TextWeb__Text-sc-1cyx778-0 gimCrs']/span[2]").text
            
            #Removing the .00 to make the cost an integer value
            relcost = relcost.replace(".00","")
        except:
            relcost = None

        if relcost:
            pd_data['Platform'].append('Reliance digital')
            pd_data['Price'].append(relcost)
            pd_data['Platform link'].append(f'https://www.reliancedigital.in/search?q={pd_name}')
            
        #Getting data from croma
        driver.execute_script(f"window.open('https://www.croma.com/searchB?q={pd_name}')")
        driver.switch_to.window(driver.window_handles[-1])
        
        try:
            #Waiting for the tag which contains the cost to load 
            WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[@class='amount plp-srp-new-amount' and @data-testid='new-price']")))
            cromacost = driver.find_element(By.XPATH, "//span[@class='amount plp-srp-new-amount' and @data-testid='new-price']").text
        except:
            #If any issue/the cost is not found cromacost is None
            cromacost = None
        
        if cromacost:
            #If the cost is available , append the data to the dictionary
            pd_data['Platform'].append('Croma')
            pd_data['Price'].append(cromacost)
            pd_data['Platform link'].append(f"https://www.croma.com/searchB?q={pd_name}")
            
        #Getting data from poorvika
        driver.execute_script(f"window.open('https://www.poorvika.com/s?q={pd_name}')")
        driver.switch_to.window(driver.window_handles[-1])
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "whitespace-nowrap")))
            #Getting the cost
            poorcost = driver.find_element(By.CLASS_NAME,"whitespace-nowrap ").text
            #Removing spaces from the cost
            poorcost = poorcost.replace(" ","")
        except:
            #If any issue/the cost is not available poorcost is None
            poorcost = None
        
        if poorcost:
            #If the cost is available add the data to the dictionary
            pd_data['Platform'].append('Poorvika')
            pd_data['Price'].append(poorcost)
            pd_data['Platform link'].append(f"https://www.poorvika.com/s?q={pd_name}")

        #Sort prices in ascending order
        #create a prices list which contains the prices
        prices = pd_data['Price'].copy()
        for i in range(len(prices)):
            #Removing the symbols, spaces and commas from the cost
            prices[i] = prices[i].replace('₹', '').replace(',', '').replace(' ', '')
        #Converting the cost to integer form
        prices = [int(i) for i in prices]
        for i in range (len(prices)-1):
            for j in range(i+1,len(prices)):
                if prices[j]<prices[i]:
                    #If there is a lesser price after the price , switch the places in the dictionary
                    prices[j],prices[i]=prices[i],prices[j]
                    pd_data['Platform'][j],pd_data['Platform'][i]=pd_data['Platform'][i],pd_data['Platform'][j]
                    pd_data['Price'][j],pd_data['Price'][i]=pd_data['Price'][i],pd_data['Price'][j]
                    pd_data['Platform link'][j],pd_data['Platform link'][i]=pd_data['Platform link'][i],pd_data['Platform link'][j]
        #Returning the dictionary
        return pd_data
    finally:
        #Close the driver
        driver.quit()   


