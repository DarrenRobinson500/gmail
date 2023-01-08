from django.shortcuts import render, redirect
from .models import *
from .gmail import *
from collections import Counter

def home(request, start=1, null_only=False):
    start = int(start)
    if null_only == "True":
        senders = Sender.objects.filter(type__isnull=True)
    else:
        senders = Sender.objects.all()
    senders = sorted(senders, key=lambda t: -t.count())
    total_emails = len(Message.objects.all())
    range = f"{start} - {start+9}"
    context = {'senders': senders[start-1:start+9], 'total_emails': total_emails, 'range': range,
               'start': start, 'start_next': start + 10, 'start_prev': start - 10, 'null_only': null_only}
    return render(request, 'home.html', context)

def show_messages(request, sender_id):
    sender = Sender.objects.get(id=sender_id)
    emails = Message.objects.filter(sender=sender)
    # senders = sorted(senders, key=lambda t: -t.count())
    context = {'emails': emails[0:100]}
    return render(request, 'messages.html', context)

def show_messages_year(request, year):
    year = int(year)
    emails = []
    all_emails = Message.objects.all()
    for email in all_emails:
        # print(email.year(), year, type(email.year()), type(year), email.year() == year)
        if email.year() == year:
            emails.append(email)
    print(emails)
    context = {'emails': emails[0:100]}
    return render(request, 'messages.html', context)

def show_years(request):
    years = []
    years_data = []
    messages = Message.objects.all()
    for message in messages:
        years.append(message.year())
    counter = Counter(years)
    for year in counter:
        years_data.append((year, counter[year]))
    years_data = sorted(years_data, key=lambda tup: -tup[0])
    context = {'years': years_data, 'total': len(messages)}
    return render(request, 'years.html', context)




def read_messages(request):
    set_periods(2014, 2024)
    for x in periods:
        messages = search_messages(service, x)
        print("Read messages - no of messages:", len(messages), x)
        count = 0
        for message in messages:
            count += 1
            message_id = message['id']
            existing_message = Message.objects.filter(id=message_id)
            # print(len(existing_message))
            if len(existing_message) == 0:
                print(count, "Loading message")
                txt = service.users().messages().get(userId='me', id=message_id).execute()
                payload = txt['payload']
                headers = payload['headers']
                for header in headers:
                    # print(header['name'])
                    if header['name'] == 'From': sender = header['value']
                    if header['name'] == 'Date': date = header['value']
                    if header['name'] == 'Subject': subject = header['value']
                sender_obj = Sender.objects.filter(name=sender).first()
                if not sender_obj:
                    sender_obj = Sender(name=sender).save()
                Message(id=message['id'], sender=sender_obj, date_string=date, subject=subject).save()
            else:
                print(count, "Message already exists")

    return redirect("home")

def delete_messages(request):
    senders = Sender.objects.all()
    for sender in senders:
        if sender.deletion_ready():
            before = sender.deletion_date().strftime("%y-%m-%d")
            string = f"from: {sender} before: {before}"
            print("Delete messages:", sender, string)
            messages = search_messages(service, string)
            if len(messages) > 0: print()
            print("Search:", string, len(messages))
            trash_messages(messages)
    return redirect("home")


def add_type(request, id, type, start, null_only):
    sender = Sender.objects.get(id=id)
    sender.type = type
    sender.save()
    return redirect(f"/home/{start}/{null_only}")