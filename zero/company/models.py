from django.db import models
import string, random
import datetime
from time import mktime

class Company(models.Model):

    SECTOR_CHOICES = (
        ('ts', 'Telecommunications Services'),
        ('in', 'Industrials'),
        ('cd', 'Consumer Discretionary'),
        ('ut', 'Utilities'),
        ('cs', 'Consumer Staples'),
        ('hc', 'Health Care'),
        ('ma', 'Materials'),
        ('fi', 'Financials'),
        ('en', 'Energy'),
        ('it', 'Information Technology'),
    )

    symbol   = models.CharField(primary_key=True, max_length=16)
    name     = models.CharField(max_length=255)
    exchange = models.CharField(max_length=32)
    sector   = models.CharField(max_length=2, choices=SECTOR_CHOICES)
    location = models.CharField(max_length=255)

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.symbol)

    def latest_price(self):
        price = Price.objects.order_by('-date').filter(company=self)[:1].get()
        return price

    def ohlc(self, days):
        prices = self.price_set.order_by('-date').all()[:days]
        results = []
        for i in prices:
            results.append([int(mktime(i.date.timetuple())), i.opened, i.high, i.low, i.closed])
        results.reverse()
        return results

    def google_url(self):
        return 'http://www.google.com/finance?q=%s:%s' % (self.exchange, self.symbol)

    def stats(self, days):
        prices = self.price_set.order_by('-date').all()[:days]
        closes = []
        start = 0
        end = 0
        high = 0
        low = 9999999
        for i in prices:
            if i.high > high:
                high = i.high
            if i.low < low:
                low = i.low
            closes.append(i.closed)
        closes.reverse()
        if low == 9999999:
            low = 0
        return { 'high': high, 'low': low, 'closed': closes, }

    def stats7(self):
        return self.stats(7)

    def stats14(self):
        return self.stats(14)

    def stats30(self):
        return self.stats(30)

    def stats60(self):
        return self.stats(60)

    def stats90(self):
        return self.stats(90)

class Price(models.Model):

    CATEGORY_CHOICES = (
        ('h', 'Hour'),
        ('d', 'Day'),
        ('m', 'Month'),
        ('y', 'Year'),
    )

    company     = models.ForeignKey('Company')
    category    = models.CharField(max_length=1, choices=CATEGORY_CHOICES)
    date        = models.DateTimeField()
    opened      = models.FloatField()
    high        = models.FloatField()
    low         = models.FloatField()
    closed      = models.FloatField()
    adj_closed  = models.FloatField()
    volume      = models.IntegerField()

class Index(models.Model):

    name = models.CharField(max_length=32)

    def __unicode__(self):
        return self.name

class IndexCompany(models.Model):

    company = models.ForeignKey('Company')
    index = models.ForeignKey('Index')

    def __unicode__(self):
        return '%s (%s)' % (self.company.name, self.index.name)

