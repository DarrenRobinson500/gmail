# import the required libraries
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path
import base64
import email
from bs4 import BeautifulSoup
from collections import Counter



# Define the SCOPES. If modifying it, delete the token.pickle file.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

exclusion_list = [
    "darrenandamanda.robinson@gmail.com", "propertytree@propertytree.com", "hotmail", "bigpond", "gmail",
    "notify@buildinglink.com", "paynepacific", "eventbrite"]


def getEmails():
    # Variable creds will store the user access token.
    # If no valid token found, we will create one.
    creds = None

    # The file token.pickle contains the user access token.
    # Check if it exists
    if os.path.exists('token.pickle'):
        # Read the token from the file and store it in the variable creds
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If credentials are not available or are invalid, ask the user to log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the access token in token.pickle file for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # Connect to the Gmail API
    service = build('gmail', 'v1', credentials=creds)

    # request a list of all the messages
    result = service.users().messages().list(maxResults=1000, userId='me').execute()

    # We can also pass maxResults to get any number of emails. Like this:
    # result = service.users().messages().list(maxResults=200, userId='me').execute()
    messages = result.get('messages')
    print("Messages extracted")

    # messages is a list of dictionaries where each dictionary contains a message id.

    # iterate through all the messages
    senders = []
    print(len(messages))
    count = 0
    for msg in messages:
        if count % 10 == 0: print(count)
        if count % 100 == 0: print(Counter(senders))

        txt = service.users().messages().get(userId='me', id=msg['id']).execute()
        payload = txt['payload']
        headers = payload['headers']
        for header in headers:
            # print(header['name'])
            if header['name'] == 'Subject': subject = header['value']
            if header['name'] == 'From': sender = header['value']
        # print(f"Subject: {subject}. From: {sender}")
        excluded = False
        for x in exclusion_list:
            if x in sender: excluded = True
        if not excluded:
            senders.append(sender)
        count += 1

    # for sender in senders:
    #     print(sender)

    counter = Counter(senders)
    print(counter)

    # for msg in messages[0:0]:
    #     # Get the message from its id
    #     txt = service.users().messages().get(userId='me', id=msg['id']).execute()
    #
    #     # Use try-except to avoid any Errors
    #     try:
    #         # Get value of 'payload' from dictionary 'txt'
    #         payload = txt['payload']
    #         headers = payload['headers']
    #
    #         # Look for Subject and Sender Email in the headers
    #         for d in headers:
    #             if d['name'] == 'Subject':
    #                 subject = d['value']
    #             if d['name'] == 'From':
    #                 sender = d['value']
    #
    #         # The Body of the message is in Encrypted format. So, we have to decode it.
    #         # Get the data and decode it with base 64 decoder.
    #         parts = payload.get('parts')[0]
    #         data = parts['body']['data']
    #         data = data.replace("-", "+").replace("_", "/")
    #         decoded_data = base64.b64decode(data)
    #
    #         # Now, the data obtained is in lxml. So, we will parse
    #         # it with BeautifulSoup library
    #         soup = BeautifulSoup(decoded_data, "lxml")
    #         body = soup.body()
    #
    #         # Printing the subject, sender's email and message
    #         print("Subject: ", subject)
    #         print("From: ", sender)
    #         print("Message: ", body)
    #         print('\n')
    #     except:
    #         pass


def search_messages(service, query):
    result = service.users().messages().list(userId='me',q=query).execute()
    messages = [ ]
    if 'messages' in result:
        messages.extend(result['messages'])
    while 'nextPageToken' in result:
        page_token = result['nextPageToken']
        result = service.users().messages().list(userId='me',q=query, pageToken=page_token).execute()
        if 'messages' in result:
            messages.extend(result['messages'])
    print("Search messages")
    # for message in messages:
    #     print(message)
    return messages

def delete_messages(service, query):
    messages_to_delete = search_messages(service, query)
    # it's possible to delete a single message with the delete API, like this:
    # service.users().messages().delete(userId='me', id=msg['id'])
    # but it's also possible to delete all the selected messages with one query, batchDelete
    return service.users().messages().batchDelete(
      userId='me',
      body={
          'ids': [ msg['id'] for msg in messages_to_delete]
      }
    ).execute()

def print_messages(messages):
    for message in messages:
        txt = service.users().messages().get(userId='me', id=message['id']).execute()
        payload = txt['payload']
        headers = payload['headers']
        for header in headers:
            # print(header)
            if header['name'] == 'From': sender = header['value']
            if header['name'] == 'Date': date = header['value']
        print(f"From: {sender}. Date: {date}")

def print_message(message):
    txt = service.users().messages().get(userId='me', id=message['id']).execute()
    payload = txt['payload']
    headers = payload['headers']
    for header in headers:
        # print(header)
        if header['name'] == 'From': sender = header['value']
        if header['name'] == 'Date': date = header['value']
    print(f"From: {sender}. Date: {date}")




# delete_messages(service, "jetstar")
#

# periods = []
#
# for x in range(2009,2012):
#     periods.append(f"after: {x}/01/01 before: {x}/03/31")
#     periods.append(f"after: {x}/01/04 before: {x}/06/30")
#     periods.append(f"after: {x}/01/07 before: {x}/09/30")
#     periods.append(f"after: {x}/01/10 before: {x}/12/31")
#
# for x in periods:
#     messages = search_messages(service, x)
#     print(x, len(messages))
# print(messages)

# count = 1
# for msg in messages:
#     txt = service.users().messages().get(userId='me', id=msg['id']).execute()
#     payload = txt['payload']
#     headers = payload['headers']
#     for header in headers:
#         # print(header['name'])
#         if header['name'] == 'Subject': subject = header['value']
#         if header['name'] == 'From': sender = header['value']
#     print(f"{count}: Subject: {subject}. From: {sender}")
#     count += 1

# getEmails()
