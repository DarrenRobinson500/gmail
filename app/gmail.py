from googleapiclient.discovery import build
import pickle
from collections import Counter
from datetime import datetime, timedelta
from .models import *

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

senders = []


creds = pickle.load(open('token.pickle', 'rb'))
service = build('gmail', 'v1', credentials=creds)

periods = []
def set_periods(year_start, year_end, period=None):
    if period == "quarterly":
        for x in range(year_start, year_end + 1):
            periods.append(f"after: {x}/01/01 before: {x}/03/31")
            periods.append(f"after: {x}/04/01 before: {x}/06/30")
            periods.append(f"after: {x}/07/01 before: {x}/09/30")
            periods.append(f"after: {x}/10/01 before: {x}/12/31")
    else:
        for x in range(year_start, year_end + 1):
            # periods.append(f"after: {x}/01/01 before: {x}/3/31")
            periods.append(f"after: {x}/01/01 before: {x}/12/31")

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
    return messages

def trash_messages(messages):
    for message in messages:
        message_id = message['id']
        # print_message(message)
        try:
            txt = service.users().messages().get(userId='me', id=message['id']).execute()
            payload = txt['payload']
            headers = payload['headers']
            for header in headers:
                if header['name'] == 'From': sender = header['value']
                if header['name'] == 'Date': date = header['value']
            print(f"Trashing: From: {sender}. Date: {date}")
            service.users().messages().trash(userId='me', id=message_id).execute()
            message_to_delete = Message.objects.filter(id=message_id)
            message_to_delete.delete()
        except Exception as error:
            print('An error occurred while trashing email: %s' % error)

def print_messages(messages):
    for message in messages:
        print_message(message)

def print_message(message):
    txt = service.users().messages().get(userId='me', id=message['id']).execute()
    payload = txt['payload']
    headers = payload['headers']
    for header in headers:
        # print(header)
        if header['name'] == 'From': sender = header['value']
        if header['name'] == 'Date': date = header['value']
    # size = message.getRawContent().length
    print(f"From: {sender}. Date: {date}")

def get_senders_logic(messages):
    print()
    print("Getting senders")
    global senders
    count = 1
    count_exclusions = 0
    for msg in messages:
        if count % 10 == 0:
            try:
                print(count, date.strftime("%y-%m-%d")) # the date from gmail is a string not a date, so this never works.
            except:
                print(count, date)
        if count % 100 == 0: print(Counter(senders).most_common(20))
        txt = service.users().messages().get(userId='me', id=msg['id']).execute()
        payload = txt['payload']
        headers = payload['headers']
        for header in headers:
            if header['name'] == 'From': sender = header['value']
            if header['name'] == 'Date': date = header['value']
        senders.append(sender)
        count += 1
    print("Exclusions:", count_exclusions)
    return senders

def get_headings(msg):
    global senders
    count = 1
    count_exclusions = 0
    txt = service.users().messages().get(userId='me', id=msg['id']).execute()
    payload = txt['payload']
    headers = payload['headers']
    for header in headers:
        print(header['name'])

# result = service.users().messages().list(maxResults=10, userId='me').execute()
# messages = result.get('messages')

# creds = pickle.load(open('token.pickle', 'rb'))
# service = build('gmail', 'v1', credentials=creds)


def create_database():
    own_database = [
        "Darren.Robinson@BTFinancialgroup.com", "darren.robinson@clearview.com", "Darren.J.Robinson@nab.com.au", "Darren.J.Robinson@mlcinsurance.com.au"
        ]

    people_database = [
        "hidee5@yahoo.com", "ronandbettyrobinson@gmail.com", "brett.harpur@allianz.com.au", "jmcsmitchell@primus.com.au",
        "paul.butler5@defence.gov.au", "brendonandmichelle", "tonipoulter@bigpond.com", "jmcsmitchell@bigpond.com", "lgardner@bigpond.net.au",
        "traceywalker", "allison_tetley@hotmail.com", "cronulla-h.school", "cronulla-p.school", "islta", "3pr", "vanguard",
        "Veronica C Lee <Veronica.S.Lee@nab.com.au", "topteacher", "tpg", "jmcsmitchell@bigpond.com.au", "principalmortgages",
        "wooloowarebay", "bobandjen@iprimus.com.au", "Jennifer.H.Lang@nab.com.au", "Jeff.Poulter@kcc.com", "liz_mattiuzzo@hotmail.com",
        "toni.jeff.poulter", "Amanda.ROBINSON15", "saintpatricks", "michelle.tetley", "superalexrobinson", "fncollective", "masterton",
        "michelle.tetley", "bobandjen29", "mrhayes", "ato.gov", "det.nsw.edu", "zhan_w975@hotmail.com"
        ]

    company_database = [
        "mcafee", "no1personaltraining", "romsite", "btfinancialgroup", "directpoolsupplies.com.au", "aussiekidssoftware.com.au", "teacherscreditunion",
        "sun2seauvprotection", "instinctandreason", "CustomerPreferencesSurvey", "scoopon", "rasnsw", "hairallure1@bigpond.com", "jumponit", "gwsgiants",
        "tellme", "mapmyfitness", "stgeorge", "postie", "gwsgiants", "sharemylesson", "shopadocket", "greaterunion", "myfitnesspal", "hairallure1",
        "outrigger", "losethebackpain", "outrigger", "lusthaveit", "no-reply", "dimmi", "furnitureonline", "ingdirect", "kresta", "punchbowl", "flyscoot",
        "tcsevents", "costumedirect", "bronto", "hidow", "theatreclub", "ifly", "eastershow", "mirvac", "universalorlando", "thefork", "arbonnemail",
        "bitdefender", "secure-booker", "twinkl", "theatreclub", "bellabox", "aremedia", "salonstyle", "noreply", "buildinglink", "luxuryescapes",
        "climbfit", "ultraviolette", "nine", "cloudninehair", "cindrakamphoff", "shangri-la", "uprotein", "sunsetcinema", "propertytree",
        "knncomputers", "cottonon", "stayz", "happyhealthyyou", "bedandhomebarn", "caremonkey", "livelifegetactive", "byronbaygifts", "auspost",
        "victoriastation", "microsoft", "scouts", "sunsetcinema", "easyflowers", "newsdigitalmedia", "bemyguest", "iselect", "kipmcgrath",
        "advancewhitening", "footballnsw", "acmn", "houseofbamboo", "signlite", "cbhs", "zhenhair", "kmeasypay", "smartkidsonly", "thw",
        "greenhillsbeachcommunity", "familyvacationcritic", "grouponmail", "salonstyle", "jobnotification", "luxuryescapes", "cloudninehair",
        "bedandhomebarn", "byronbaygifts", "ultraviolette", "aremedia", "bellabox", "thewinery", "cronullasurfingacademy", "microsoft",
        "michaelcassel", "isubscribe", "cronullaseagullsfc", "cosmeticsnow", "codewithmosh", "sales", "hoyts", "arjancodes", "abettalocksmiths",
        "wantedshoes", "savills", "back4app", "shoesuperstore", "audisutherland", "propertytree", "waterbrook", "upwork", "5minutedeals",
        "trello", "sunsetcinema", "fusionretailbrands", "biomechanicshealthcare", "MarginLoanStatements", "sfemail", "flexischools",
        "bramleyvet", "frasersproperty", "eastershow", "bigideas", "secretfoodies", "instagram", "topteacher", "iwannap", "aplfootball",
        "altituderewards", "mysciaticaexercises", "optus", "nrma", "observatory", "experiencethis", "pandora", "bigfishgames", "proactiv",
        "khanacademy", "smile", "ourdeal", "live", "deals", "info", "hellofresh", "notification", "mavetju", "disney", "boardridersclub",
        "mtatravel", "parkview", "promotion", "GearedInvestments", "recreation", "David.Meyer", "catherinepark", "unleashedtravel",
        "sunselect", "s.newcombe", "sleepinggiant", "colliers", "arkfinishingtouches", "harrington", "telstra", "yhc", "lendlease",
        "americanvogue", "newlivinglandscapes", "bpx", "foxtix", "australand", "shopperdoo", "worldvision", "suttons", "localpools",
        "computershare", "ctaust", "xamarin", "magshop", "support", "iskme", "klika", "neatportal", "cirquedusoleil", "sony", "scribd",
        "ctshirts", "tennis", "enquiries", "bunnings", "allfreekidscrafts", "dell", "inkstation", "middlerock", "totaltilecare", "nutrimetics",
        "twitter", "tiles", "nsw.gov", "tmmsg", "aapt", "ajgrantgroup", "fareharbor", "cruises", "aae", "systweak", "creatures", "elance",
        "clarendon"
    ]

    database = []

    for x in own_database: database.append((x, 7 * 12))
    for x in people_database: database.append((x, 3 * 12))
    for x in company_database: database.append((x, 1 * 12))
    return database

def delete_messages_in_database(database):
    for sender, months in database:
        before = datetime.now() + timedelta(days=-30 * months)
        before = before.strftime("%y-%m-%d")
        string = f"from: {sender} before: {before}"
        messages = search_messages(service, string)
        if len(messages) > 0: print()
        print("Search:", string, len(messages))
        trash_messages(messages)

def delete_old_messages():
    before = datetime.now() + timedelta(days=-365 * 10)
    before = before.strftime("%y-%m-%d")
    string = f"before: {before}"
    print("String:", string)
    messages = search_messages(service, string)
    # print_messages(messages)
    print(len(messages))
    trash_messages(messages)


def get_messages():
    all_messages = []
    print()
    print("Get all messages")
    for x in periods:
        messages = search_messages(service, x)
        all_messages = all_messages + messages
        print(x, len(messages), len(all_messages))
    return all_messages

def print_unidentified_senders(senders, database):
    unidentified = []
    for sender in senders:
        found = False
        for sender_db, months in database:
            if sender_db in sender:
                found = True
        for sender_db in unidentified:
            if sender_db in sender:
                found = True

        if not found:
            unidentified.append(sender)
            print("Not found:", sender)
    print("Number of unidentified senders:", len(unidentified))
    return unidentified

def print_large_messages():
    print()
    print("Large messages")
    messages = search_messages(service, f"larger:1M")
    print(len(messages))
    print_messages(messages)

def main_loop():
    database = create_database()
    set_periods(2014, 2023)
    get_messages()
    delete_old_messages()
    delete_messages_in_database(database)
    print_large_messages()
    all_messages = get_messages()
    senders = get_senders_logic(all_messages)
    print(Counter(senders))
    print_unidentified_senders(senders, database)


# main_loop()