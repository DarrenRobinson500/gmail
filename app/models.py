from django.db import models
from datetime import datetime, timedelta

class Sender(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    type = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name

    def count(self):
        return len(Message.objects.filter(sender=self))

    def oldest_email(self):
        messages = Message.objects.filter(sender=self)
        if len(messages) == 0: return None
        oldest = datetime.today().date()
        for message in messages:
            if message.date() < oldest: oldest = message.date()
        return oldest

    def deletion_date(self):
        if self.type == "Company":
            return datetime.today().date() - timedelta(days=365)
        if self.type == "Person":
            return datetime.today().date() - timedelta(days=365 * 3)
        if self.type == "Own":
            return datetime.today().date() - timedelta(days=365 * 7)
        else:
            return datetime.today().date() - timedelta(days=3650)

    def deletion_ready(self):
        a = self.oldest_email()
        b = self.deletion_date()
        if a and b:
            return a < b
        return False

class Message(models.Model):
    header = models.CharField(max_length=50, null=True, blank=True)
    sender = models.ForeignKey(Sender, blank=True, null=True, on_delete=models.SET_NULL)
    id = models.CharField(max_length=50, primary_key=True)
    subject = models.CharField(max_length=250, null=True, blank=True)
    date_string = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        if self.subject: return self.subject
        else: return "Not found"

    def date(self):
        result = self.date_string
        if result[0].isdigit():
            result = result[0:11]
        else:
            result = result[5:16]
        if result[1] == " ": result = '0' + result[0:10]
        result = datetime.strptime(result, '%d %b %Y').date()
        return result

    def year(self):
        return self.date().year

