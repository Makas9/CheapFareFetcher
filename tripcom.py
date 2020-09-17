from __future__ import print_function
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from random import randint
import time

def main(identifier, CHEAP_FLIGHT_BASE_URL, CHEAP_FLIGHT_FROM, CHEAP_FLIGHT_TO, CHEAP_FLIGHT_FROM_AIRPORT, CHEAP_FLIGHT_TO_AIRPORT, CHEAP_FLIGHT_DATE_FROM, CHEAP_FLIGHT_DATE_TO, CHEAP_FLIGHT_FLEXIBLE, CHEAP_FLIGHT_MIN_LENGTH, CHEAP_FLIGHT_MAX_LENGTH, CHEAP_FLIGHT_PEOPLE, CHEAP_FLIGHT_PRICE, MAX_SEARCH_PER_RUN, SECONDS_BETWEEN_SEARCHES):
    if CHEAP_FLIGHT_FLEXIBLE == 1:
        dates = generateRandomDate(CHEAP_FLIGHT_DATE_FROM, CHEAP_FLIGHT_DATE_TO, CHEAP_FLIGHT_MIN_LENGTH, CHEAP_FLIGHT_MAX_LENGTH)
    else:
        dates = CHEAP_FLIGHT_DATE_FROM, CHEAP_FLIGHT_DATE_TO
    airport = getAirportCodes(CHEAP_FLIGHT_BASE_URL)
    CHEAP_FLIGHT_URL = "{0}?curr=EUR&flighttype=d&dcity={1}&acity={2}&startdate={3}&returndate={4}&class=ys&quantity={5}".format(
        CHEAP_FLIGHT_BASE_URL, "{0},{1}".format(airport[0], CHEAP_FLIGHT_FROM_AIRPORT), "{0},{1}".format(airport[1], CHEAP_FLIGHT_TO_AIRPORT), dates[0],
        dates[1], CHEAP_FLIGHT_PEOPLE)
    return getCheapFares(identifier, CHEAP_FLIGHT_URL, dates[0], dates[1], CHEAP_FLIGHT_FROM_AIRPORT, CHEAP_FLIGHT_TO_AIRPORT, CHEAP_FLIGHT_PRICE)

def getAirportCodes(CHEAP_FLIGHT_BASE_URL):
    CHEAP_FLIGHT_BASE_URL = CHEAP_FLIGHT_BASE_URL[:-1]
    destinationAirportIndex = CHEAP_FLIGHT_BASE_URL.rfind('-')+1
    destinationAirport = CHEAP_FLIGHT_BASE_URL[destinationAirportIndex:]
    CHEAP_FLIGHT_BASE_URL = CHEAP_FLIGHT_BASE_URL[:-(len(CHEAP_FLIGHT_BASE_URL)-destinationAirportIndex+1)]
    originAirportIndex = CHEAP_FLIGHT_BASE_URL.rfind('-')+1
    originAirport = CHEAP_FLIGHT_BASE_URL[originAirportIndex:]
    return originAirport, destinationAirport
	
def generateRandomDate(CHEAP_FLIGHT_DATE_FROM, CHEAP_FLIGHT_DATE_TO, CHEAP_FLIGHT_MIN_LENGTH, CHEAP_FLIGHT_MAX_LENGTH):
    date = datetime.strptime(CHEAP_FLIGHT_DATE_FROM, '%Y-%m-%d').date()
    date2 = datetime.strptime(CHEAP_FLIGHT_DATE_TO, '%Y-%m-%d').date()
    flightDateDifference = abs((date2 - date).days);
    generatedRandomDay = randint(0, (flightDateDifference-CHEAP_FLIGHT_MAX_LENGTH))
    generateMinNumber = CHEAP_FLIGHT_MIN_LENGTH
    generateMaxNumber = CHEAP_FLIGHT_MAX_LENGTH
    newGeneratedDuration = randint(generateMinNumber, generateMaxNumber)
    newDateFrom = date + timedelta(days=generatedRandomDay)
    newDateTo = newDateFrom + timedelta(days=newGeneratedDuration)
    return newDateFrom, newDateTo


def getCheapFares(identifier, URL, flightFromDate, flightToDate, CHEAP_FLIGHT_FROM_AIRPORT, CHEAP_FLIGHT_TO_AIRPORT, CHEAP_FLIGHT_PRICE):
    print("[{0}] Starting the browser ({1} <-> {2} | {3} - {4})...".format(identifier, CHEAP_FLIGHT_FROM_AIRPORT.upper(), CHEAP_FLIGHT_TO_AIRPORT.upper(), flightFromDate, flightToDate))
    options = Options()
    options.add_argument('--headless')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("user-agent=Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.6) Gecko/2009011913 Firefox/3.0.6")
    browser = webdriver.Chrome('./chromedriver', options=options)
    browser.get(URL)
    print("[{0}] Waiting 30 seconds for the page to load...".format(identifier))
    time.sleep(30)
    print("[{0}] Loaded, searching for flights!".format(identifier))
    prices = [price.text for price in wait(browser, 150).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "o-price-flight__num")))]
    html = [abc.get_attribute('innerHTML') for abc in wait(browser, 150).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "flight-info")))]
    for i, value in enumerate(prices):
        if ',' in value:
            prices[i] = prices[i].replace(',', '')

    prices = list(map(int, prices))
    foundCheapFares = []
    for i, data in enumerate(html):
        foundCheapFares.append([])
        parsed_html = BeautifulSoup(data, "html.parser")
        airline = parsed_html.find('div', attrs={'class': 'flight-info-airline__name'}).text
        airline = airline.replace('\n', '')
        airline = airline.replace(' ', '')
        duration = parsed_html.find('div', attrs={'class': 'duration'}).text
        duration = duration.replace('\n', '')
        duration = duration.replace(' ', '')
        foundCheapFares[i].append(airline)
        foundCheapFares[i].append(duration)
        foundCheapFares[i].append(prices[i])

    foundCheapFares = sorted(foundCheapFares, key=lambda x: x[2])
    allFlightsNumber = 0
    cheapFlightsNumber = 0
    cheapestFareFound = 99999
    foundCheapestFares = []
    n = 0;

    for data in foundCheapFares:
        allFlightsNumber += 1
        if data[2] < CHEAP_FLIGHT_PRICE:
            cheapFlightsNumber += 1
            foundCheapestFares.append([])
            foundCheapestFares[n].append(CHEAP_FLIGHT_FROM_AIRPORT.upper())
            foundCheapestFares[n].append(CHEAP_FLIGHT_TO_AIRPORT.upper())
            foundCheapestFares[n].append(flightFromDate)
            foundCheapestFares[n].append(flightToDate)
            foundCheapestFares[n].append(abs((flightFromDate - flightToDate).days))
            foundCheapestFares[n].append(data[2])
            foundCheapestFares[n].append(data[0])
            foundCheapestFares[n].append(data[1])
            foundCheapestFares[n].append(URL)
            n += 1
        if data[2] < cheapestFareFound:
            cheapestFareFound = data[2]

    return(foundCheapestFares, cheapFlightsNumber, allFlightsNumber, cheapestFareFound)