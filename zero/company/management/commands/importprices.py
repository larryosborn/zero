from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError
from optparse import make_option
import json
import sys
import datetime
import urllib2
from zero.company.models import *

class Command(BaseCommand):
    args = "<symbol>"
    help = "Fetch historical stock prices for a given symbol."

    option_list = BaseCommand.option_list + (
        make_option('--symbol',     action='store', dest='symbol',  default=None, help='Stock ticker symbol'),
        make_option('--wipe',       action='store', dest='wipe',    default=None, help='Wipe out exiting data'),
        make_option('--days',       action='store', dest='days',    default=None, help='Number of days to go back'),
        make_option('--replace',    action='store', dest='replace', default=None, help='Replace existing data'),
    )

    def handle(self, *args, **options):
        verbosity = int(options['verbosity'])
        symbol = options['symbol']
        wipe = options['wipe']
        days = int(options['days'] or 999999999)
        replace = options['replace']

        if symbol == '__ALL__':
            companies = Company.objects.all()
        else:
            companies = Company.objects.filter(symbol=symbol)

        for company in companies:
            if verbosity >= 2:
                self.stdout.write('Symbol: %s\n' % company.symbol)
            #url = "http://ichart.finance.yahoo.com/table.csv?s=%s&d=2&e=28&f=2014&g=d&a=0&b=2&c=1962&ignore=.csv" % company.symbol
            url = "http://ichart.finance.yahoo.com/table.csv?s=%s&d=2&e=28&f=2014&g=d&a=0&b=2&c=2012&ignore=.csv" % company.symbol
            if verbosity >= 2:
                self.stdout.write('Fetching: %s\n' % url)
            try:
                req = urllib2.Request(url=url)
                f = urllib2.urlopen(req)
            except:
                if verbosity >= 2:
                    self.stdout.write('Failed fetching: %s\n' % url)
                continue
            res = f.read().split('\n')
            res.reverse()
            res.pop()
            res.reverse()
            if verbosity >= 2:
                self.stdout.write('Read lines: %i\n' % len(res))
            if wipe:
                if verbosity >= 2:
                    self.stdout.write('Removing data for %s' % company.symbol)
                prices = Price.objects.filter(company=company)
                prices.delete()
            i = 0
            for line in res:
                line2 = line.strip().split(',')
                if (len(line2) > 1):
                    date = line2[0].strip().split('-')
                    o = {
                        'date':         datetime.date(int(date[0]), int(date[1]), int(date[2])),
                        'opened':       line2[1],
                        'high':         line2[2],
                        'low':          line2[3],
                        'closed':       line2[4],
                        'volume':       line2[5],
                        'adj_closed':   line2[6],
                    }

                    if replace:
                        prices = Price.objects.filter(company=company, date=o['date'])
                        prices.delete()

                    price = Price(
                        company=company,
                        category='d',
                        date=o['date'],
                        opened=o['opened'],
                        high=o['high'],
                        low=o['low'],
                        closed=o['closed'],
                        volume=o['volume'],
                        adj_closed=o['adj_closed'],
                    )
                    price.save()
                i = i + 1
                if days and i > days:
                    break