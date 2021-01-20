import random, csv
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/88.0.4324.96 Chrome/88.0.4324.96 Safari/537.36")
driver = webdriver.Chrome('./chromedriver', options=opts) # Using the object driver, I'll do the web scraping

# Seed URL:
driver.get("https://www.flightstats.com/v2/flight-tracker/departures/MEX/")

with open("departures.csv", 'w') as file_obj:
    csv_writer = csv.writer(file_obj)
    
    cols = ["Company", "Flight", "From", "To", "Status", "Scheduled_Departure_Hour_CST", "Real_Departure_Hour_CST", "Flight_Departure_Times"]
    csv_writer.writerow([col_name for col_name in cols])

    for day in ['19-1-2021','20-1-2021']:
        day_button = driver.find_element_by_xpath(f"//select[@name='date']/option[@value='{day}']")
        day_button.click()
        sleep(random.uniform(1,1.5))

        for time in ['0','6','12','18']:
            time_button = driver.find_element_by_xpath(f"//select[@name='time']/option[@value='{time}']")
            time_button.click()
            sleep(random.uniform(1,1.5))

            refresh_button = driver.find_element_by_xpath("//span[text()='Refine Search']")
            refresh_button.click()
            sleep(random.uniform(1,1.5))
            
            pagination_numbers = [1,]
            while True:

                flights_links = driver.find_elements(By.XPATH, "//a[@class='table__A-s1x7nv9w-2 flrJsE']")
                flights_per_page = []
                for a_link in flights_links:
                    flights_per_page.append(a_link.get_attribute('href'))

                for link in flights_per_page:
                    try:
                        # Obtaining the data for every flight:
                        driver.get(link) # I get inside the details of the flight.
                        sleep(random.uniform(0.5,1.0))
                        Company = driver.find_element(By.XPATH, "//div[contains(@class, 'ticket__FlightNumberContainer')]/div[contains(@class, 'text-helper__TextHelper')][last()]").text
                        Flight = driver.find_element(By.XPATH, "//div[contains(@class, 'ticket__FlightNumberContainer')]/div[contains(@class, 'text-helper__TextHelper')][1]").text
                        From = driver.find_element(By.XPATH, "//div[contains(@class, 'route-with-plane__Route-s154xj1h-1')][1]//div[contains(@class, 'text-helper__TextHelper')][last()]").text
                        To = driver.find_element(By.XPATH, "//div[contains(@class, 'route-with-plane__Route-s154xj1h-1')][last()]//div[contains(@class, 'text-helper__TextHelper')][last()]").text
                        Status = driver.find_element(By.XPATH, "//div[contains(@class,'ticket__StatusContainer')]/div[1]").text
                        Scheduled_Departure_Hour = driver.find_element(By.XPATH, "//div[contains(@class, 'ticket__TicketContent')]/div[1]/div[contains(@class, 'ticket__TimeGroupContainer')]/div[1]/div[last()]").text
                        Real_Departure_Hour = driver.find_element(By.XPATH, "//div[contains(@class, 'ticket__TicketContent')]/div[1]/div[contains(@class, 'ticket__TimeGroupContainer')]/div[2]/div[last()]").text
                        Flight_Departure_Times = driver.find_element(By.XPATH, "//div[contains(@class, 'ticket__TicketContent')]/div[1]/div[contains(@class, 'ticket__InfoSection')][last()]/div[last()]").text
                        driver.back() # I return to the main page.
                        
                        # Storing the data inside an "csv" file:
                        flight_data = [Company, Flight, From, To, Status, Scheduled_Departure_Hour, Real_Departure_Hour, Flight_Departure_Times]
                        csv_writer.writerow([data.replace('CST','') if data != '--' else "Unknown" for data in flight_data])
                        
                        sleep(random.uniform(0.5,1.0))
                        
                    except Exception as error:
                        print(error)
                        driver.back() # In case an error appears, I return to the main page to continue doing web scraping.

                pag = driver.find_element(By.XPATH, "//div[contains(@class,'table__CodeshareAndPagination')]/div[last()]/div/div/div[last()-2]").text
                # Just in case we have more than 3 pages per period of time:
                if pag:
                    pagination_numbers.append(int(pag))
                else:
                    pag = driver.find_element(By.XPATH, "//div[contains(@class,'table__CodeshareAndPagination')]/div[last()]/div/div/div[5]").text
                    pagination_numbers.append(int(pag))
                
                if pagination_numbers[0] < pagination_numbers[1]:
                    pags_button = driver.find_element_by_xpath("//div[contains(@class,'table__CodeshareAndPagination')]/div[last()]/div/div/div[last()-1]")
                    pags_button.click()
                    pagination_numbers.pop(0)
                    sleep(random.uniform(1,1.5))
                else:
                    break
                
        print(f"The whole data from the day: {day} has been scraped!")