from os import path
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from email.mime.text import MIMEText
import base64
from apiclient import errors
from datetime import datetime, timedelta
from random import randint
import time
import json
from pprint import pprint
import tripcom as tripcomscrapper

SCOPES = 'https://www.googleapis.com/auth/gmail.send'

config = None

def main():
    global config
    with open('config.json') as data:
        config = json.load(data)

    if not path.exists("token.json"):
        with open("token.json", "w") as data:
            data.write("{}")

    service = None
    try:
        store = file.Storage('token.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
            creds = tools.run_flow(flow, store)
        service = build('gmail', 'v1', http=creds.authorize(Http()))
    except Exception as error:
        service = None
        print('[EMAIL] An error occurred: %s' % error)
        print('[EMAIL] Email service is not connected!')

    parsedJsonFile = parseJsonFile()
    for i, x in enumerate(parsedJsonFile):
        for data in parsedJsonFile[x]:
            startFareFinder(service, x, data)


def startFareFinder(service, identifier, data):
    MAX_SEARCH_PER_RUN = data["MAX_SEARCH_PER_RUN"];
    if MAX_SEARCH_PER_RUN == 0:
        MAX_SEARCH_PER_RUN = 1;
        inf = True;
        print("[{0}] Search will run without limits!".format(identifier));
    while MAX_SEARCH_PER_RUN > 0:
        cheapFareData = tripcomscrapper.main(identifier, data["CHEAP_FLIGHT_BASE_URL"], data["CHEAP_FLIGHT_FROM"],
                                             data["CHEAP_FLIGHT_TO"], data["CHEAP_FLIGHT_FROM_AIRPORT"],
                                             data["CHEAP_FLIGHT_TO_AIRPORT"], data["CHEAP_FLIGHT_DATE_FROM"],
                                             data["CHEAP_FLIGHT_DATE_TO"], data["CHEAP_FLIGHT_FLEXIBLE"],
                                             data["CHEAP_FLIGHT_MIN_LENGTH"], data["CHEAP_FLIGHT_MAX_LENGTH"],
                                             data["CHEAP_FLIGHT_PEOPLE"], data["CHEAP_FLIGHT_PRICE"],
                                             data["MAX_SEARCH_PER_RUN"], data["SECONDS_BETWEEN_SEARCHES"])
        if cheapFareData[0]:
            generatedMessage = generateMessage(service, identifier, cheapFareData[0], cheapFareData[3])
        print("[{0}] {1} cheap flights were found out of {2} total flights (cheapest: {3} EUR)!".format(identifier, cheapFareData[1], cheapFareData[2], cheapFareData[3]))
        if not inf:
            MAX_SEARCH_PER_RUN -= 1
        print("[{0}] Going to sleep for {1} seconds...".format(identifier, data["SECONDS_BETWEEN_SEARCHES"]))
        print("----------")
        time.sleep(data["SECONDS_BETWEEN_SEARCHES"])
    print("[{0}] Stopping bot, all searches completed!".format(identifier))
    return();


def parseJsonFile():
	with open('flight.json') as f:
		parsedJson = json.load(f);
	for i, x in enumerate(parsedJson):
		for data in parsedJson[x]:
			for key in data:
				if not data[key] and data[key] is not 0:
					print("NULL value detected -> ", key);
					exit();
	return parsedJson;


def generateMessage(service, identifier, object, cheapest):
    print("[{0}] Cheap Fare found, sending email...".format(identifier))
    subject = "[{0} EUR] {1} <-> {2} | {3} - {4} ({5} days)\n".format(cheapest, object[0][0], object[0][1], object[0][2], object[0][3], object[0][4])
    message_text = ""
    if service is not None and config is not None:
        message_text = "Hello!\n\nWe have just found these cheap flights:\n\n"
    for data in object:
        message_text += "{0} | {1} <-> {2} | {3} - {4} ({5} days) | {6} | {7} EUR | Fast booking here: {8}\n".format(data[6], data[0], data[1], data[2], data[3], data[4], data[7], data[5], data[8])
    if service is None or config is None:
        print(message_text)
    else:
        message = create_message(config["emailFrom"], config["emailTo"], subject, message_text)
        send_message(service, message)


def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    b64_bytes = base64.urlsafe_b64encode(message.as_bytes())
    b64_string = b64_bytes.decode()
    return {'raw': b64_string}


def send_message(service, message):
    try:
        message = (service.users().messages().send(userId='me', body=message).execute())
        print('Successfully sent the email!')
        return (message)
    except errors.HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
  main()