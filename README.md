# CheapFareFetcher
Finds the cheapest flight fares for given destinations and flexible dates. Sends an email with all the flight deal information.

# Supported functionality
* Multiple destinations
* Flexible dates
* Flexible trip period
* Email notifications

# Supported flight search agencies
* Trip.com

# Usage
1. Download `ChromeDriver` `.exe` file and put it in the root directory of the project
2. Open JSON file `flight.json`
3. Change values by using this example:
```
{
  "Option1":[{
    "CHEAP_FLIGHT_BASE_URL": "https://www.trip.com/flights/london-to-new-york/tickets-lon-nyc/",
    "CHEAP_FLIGHT_FROM": "London (LHR)",
    "CHEAP_FLIGHT_TO": "New York (JFK)",
    "CHEAP_FLIGHT_FROM_AIRPORT": "lhr",
    "CHEAP_FLIGHT_TO_AIRPORT": "jfk",
    "CHEAP_FLIGHT_DATE_FROM": "2021-08-10",
    "CHEAP_FLIGHT_DATE_TO": "2021-08-25",
    "CHEAP_FLIGHT_FLEXIBLE": 1,
    "CHEAP_FLIGHT_MIN_LENGTH": 7,
    "CHEAP_FLIGHT_MAX_LENGTH": 14,
    "CHEAP_FLIGHT_PEOPLE": 1,
    "CHEAP_FLIGHT_PRICE": 1500,
    "MAX_SEARCH_PER_RUN": 0,
    "SECONDS_BETWEEN_SEARCHES": 300
  }]
}
```
4. Start program by using `cmd` command `py start.py` (Windows)

# JSON Documentation
```
CHEAP_FLIGHT_BASE_URL - Direct URL to fetch flight fares from
CHEAP_FLIGHT_FROM - Full name of origin airport
CHEAP_FLIGHT_TO - Full name of destination airport
CHEAP_FLIGHT_FROM_AIRPORT - Code of origin airport
CHEAP_FLIGHT_TO_AIRPORT - Code of destination airport
CHEAP_FLIGHT_DATE_FROM - Start of date range
CHEAP_FLIGHT_DATE_TO - End of date range
CHEAP_FLIGHT_FLEXIBLE - Flight dates flexible? (if yes: 1, otherwise: 0)
CHEAP_FLIGHT_MIN_LENGTH - - Minimum length of trip (days)
CHEAP_FLIGHT_MAX_LENGTH - Maximum length of trip (days)
CHEAP_FLIGHT_PEOPLE - Number of persons
CHEAP_FLIGHT_PRICE - Highest price which is considered cheap. Email notification is only generated if flight fare is lower than this value
MAX_SEARCH_PER_RUN - Number of searches per one program run. (if no limit: 0)
SECONDS_BETWEEN_SEARCHES - Seconds between fetching flight fares
```
